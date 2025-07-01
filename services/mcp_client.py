from fastapi import HTTPException
import logging
from typing import Optional, List, Dict, Any, Tuple
from aiohttp import ClientSession
from contextlib import AsyncExitStack
from google import genai
from google.genai import types
import vertexai
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import os
from google.cloud import storage
from dotenv import load_dotenv
from services.authentication import authenticate_tool
from schemas.authentication import GetApiKey
from utils.dsh_apis import get_api_details, get_user_subscription_details
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from utils.utils import auditing_logs
from schemas.servers import ToolCallResponse
from schemas.servers import Source
# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


BASE_URL = os.environ.get("BASE_URL")


class MCPClient:
    def __init__(self):
        logger.info("Initializing MCPClient")
        self.sessions: Optional[List[Tuple[ClientSession, str]]] = []
        self.exit_stack = AsyncExitStack()
        self.client = genai.Client(vertexai=True, project="apimanager-12", location="us-central1")
        self.bucket_name = os.environ.get("SERVER_BUCKET_NAME")

        # MongoDB setup
        self.mongo_client = AsyncIOMotorClient(os.getenv("MONGO_DB_URI"))
        self.db = self.mongo_client.get_database("mcp_dac_assistant")
        self.sessions_collection = self.db.get_collection("user_sessions")
        self.default_servers = []
        self.available_tools = []
        self.tool_to_session = {}

    async def _get_recent_messages(self, session_id: str) -> List[Dict[str, str]]:
        logger.debug(f"Fetching recent messages for session: {session_id}")
        session = await self.sessions_collection.find_one({"session_id": session_id})
        if session and "messages" in session:
            return session["messages"][-6:]
        return []

    async def _save_message(self, session_id: str, role: str, content: str):
        await self.sessions_collection.update_one(
            {"session_id": session_id},
            {
                "$push": {"messages": {"role": role, "content": content, "timestamp": datetime.now()}},
                "$setOnInsert": {"session_id": session_id}
            },
            upsert=True
        )

    async def add_tools(self, session,server_meta):
        logger.info(f"Adding tools from server: {server_meta.serverInfo.name}")
        try:
            response = await session.list_tools()
            for tool in response.tools:
                self.tool_to_session[tool.name] = (session, server_meta.serverInfo.name)
                self.available_tools.append(
                    types.Tool(
                        function_declarations=[{
                            "name": tool.name,
                            "description": tool.description,
                            "parameters": {
                                k: v for k, v in tool.inputSchema.items()
                                if k not in ["additionalProperties", "$schema"]
                            },
                        }]
                    )
                )
        except Exception as e:
            logger.error(f"Error adding tools from server {server_meta.serverInfo.name}: {e}")
            raise ValueError(f"Error adding tools")

    async def connect_to_servers_from_directory(self, bucket_name: str, prefix: str = ""):
        logger.info(f"Connecting to servers from bucket: {bucket_name}, prefix: {prefix}")
        try:
            self.sessions = []
            storage_client = storage.Client()
            bucket = storage_client.bucket(bucket_name)
            blobs = bucket.list_blobs(prefix=prefix)

            script_files = [
                f"gs://{bucket_name}/{blob.name}"
                for blob in blobs
                if blob.name.endswith(".py") or blob.name.endswith(".js")
            ]

            for server_script_path in script_files:
                await self.connect_to_server(server_script_path)
            await self.connect_default_servers()

        except Exception as e:
            logger.error(f"Failed to connect to servers: {e}")
            raise RuntimeError(f"Failed to connect to servers: {e}")

    async def connect_to_server(self, server_script_path: str):
        logger.info(f"Connecting to server from script: {server_script_path}")
        is_python = server_script_path.endswith(".py")
        is_js = server_script_path.endswith(".js")
        if not (is_python or is_js):
            raise ValueError("Server script must be a .py or .js file")

        try:
            if server_script_path.startswith("gs://"):
                storage_client = storage.Client()
                bucket_name, blob_name = server_script_path[5:].split("/", 1)
                bucket = storage_client.bucket(bucket_name)
                blob = bucket.blob(blob_name)
                file_content = blob.download_as_text()

                local_path = os.path.join("/tmp", os.path.basename(blob_name))
                with open(local_path, "w") as temp_file:
                    temp_file.write(file_content)
                server_script_path = local_path

            load_dotenv()
            command = "python" if is_python else "node"
            server_params = StdioServerParameters(command=command, args=[server_script_path], env=os.environ.copy())

            stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
            self.stdio, self.write = stdio_transport

            session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))
            server_meta = await session.initialize()
            self.sessions.append((session, server_meta.serverInfo.name))
            await self.add_tools(session, server_meta)


            logger.info(f"Server added from {server_script_path}")
            return (True, "")
        except Exception as e:
            logger.error(f"Error connecting to server {server_script_path}: {e}")
            return (False, str(e))

    async def connect_default_servers(self):
        logger.info("Connecting to default servers")
        try:
            load_dotenv()
            # command = "mcp-server-chart"
            # args = ["--transport", "stdio"]

            command = "node"
            args = ["node_modules/@gongrzhe/quickchart-mcp-server/build/index.js"]

            self.default_servers.append("quickchart-server")
            server_params = StdioServerParameters(command=command, args=args, env=os.environ.copy())

            stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
            self.stdio, self.write = stdio_transport

            session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))
            server_meta = await session.initialize()
            self.sessions.append((session, server_meta.serverInfo.name))
            await self.add_tools(session, server_meta)

            logger.info("Default server 'quickchart-server' has been added")
            return (True, "")
        except Exception as e:
            logger.error(f"Error connecting to server mcp-server-chart: {e}")
            return (False, str(e))

    async def delete_server(self, server_name: str):
        logger.info(f"Deleting server: {server_name}")
        try:
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(server_name)
            blob.delete()
            return True
        except Exception as e:
            logger.error(f"Error deleting server: {e}")
            return False

    async def make_llm_call(self, messages, use_tools=False):
        logger.info("Making LLM call")
        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    temperature=0.4,
                    tools=self.available_tools,
                    system_instruction=[
                        types.Part.from_text(text="""
You are a **reasoning-focused AI agent** designed to autonomously process user queries with minimal clarification. For every task, apply deep reasoning and structured thinking as follows:

---

### 🧠 Self-Directed Reasoning

* Thoroughly **analyze the user’s request** without needing clarification.
* Make **intelligent assumptions** where appropriate to reduce dependency on user input.
* Use **step-by-step logical reasoning** to construct a complete and accurate response.
* If a tool is required, **use it effectively**. Otherwise, rely on inbuilt reasoning and capabilities to complete the task.**.
* Return the function call required, Don't run the tool by yourself

---

### 📝 Professional Output Formatting

* Format all responses in **clear, polished Markdown**.

* Always structure content with:

  * **Headings** and **subheadings** for clarity
  * **Bullet points** for lists
  * **Tables** for structured data
  * **Code blocks** for code, logs, or technical outputs

* When generating visual content or charts:

  * Use embedded Markdown images:
  ![Chart](image_url)

    Example:
    ```markdown
    ![Chart](https://example.com/chart.png)
    ```
  * **Do not** show raw image URLs unless explicitly requested.

---

### 📊 Data Handling and Presentation

* Default to **tables, charts, or structured summaries** for data.
* Use visual organization to enhance **readability and professional presentation**.

---

### 🔐 API Keys and Tools

* **Never ask the user for API keys.**
* Assume all required credentials are **pre-configured** and available to tools.
""")
                    ]
                )
            )
            return response
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            raise RuntimeError(f"LLM call failed: {e}")

    # async def autenticate_tool(self, email: str, versioned_content_id: str) -> str:
    #     logger.debug(f"Authenticating tool for email: {email}")
    #     user_credentials = GetApiKey(email_id=email, versioned_content_id=versioned_content_id)
    #     api_key = authenticate_tool(user_credentials)
    #     return api_key

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any], user_id: str, sources:list = []) -> ToolCallResponse:
                logger.info(f"Calling tool: {tool_name} with user ID: {user_id}")
                action = None
                versioned_content_id = None
                digital_content_id =  None
                source = Source()

                if not self.sessions:
                    raise ValueError("No server sessions available. Please connect to a server first.")

                try:
                    session = self.tool_to_session.get(tool_name)
                    if session[1] not in self.default_servers:
                        versioned_content_id, digital_content_id = session[1].split("_")
                        api_details = get_api_details(
                            versioned_content_id=versioned_content_id,
                            digital_content_id=digital_content_id
                        )
                        if api_details.auth_flag:
                            subscription_key = get_user_subscription_details(
                                versioned_content_id=versioned_content_id,
                                user_id=user_id
                            )
                            if subscription_key is None:
                                return ToolCallResponse(
                                    response=f"The user needs to subscribe to the API {api_details.api_name}.",
                                    action="subscription",
                                    versioned_content_id=versioned_content_id,
                                    digital_content_id=digital_content_id
                                )
                            arguments["API_KEY"] = subscription_key
                            auditing_logs(
                                versioned_content_id=api_details.versioned_content_id,
                                user_id=user_id,
                                tool_name=tool_name,
                                tool_args=arguments.copy(),
                                api_name=api_details.api_name
                            )

                            source.source_name = api_details.api_name
                            source.content_type = api_details.content_type
                            source.source_url = f"{BASE_URL}/home/discover-apis/details?digitalContentId={digital_content_id}&versionedContentId={versioned_content_id}"

                    result = await session[0].call_tool(tool_name, arguments=arguments)
                    if session[1] not in self.default_servers:
                        source.data = str(result.content[0].text)
                        sources.append(source)

                    return ToolCallResponse(
                        response=str(result.content[0].text),
                        action=action,
                        versioned_content_id=versioned_content_id,
                        digital_content_id=digital_content_id
                    )

                except Exception as e:
                    logger.error(f"Error calling tool {tool_name}: {e}")
                    raise ValueError(f"Error calling tool {tool_name}: {e}")
        # raise ValueError(f"Tool {tool_name} not found in any connected server.")

    async def process_query(self, query: str, session_id: str, email: str = None, consent: bool = None):
        logger.info(f"Processing query for session: {session_id}")
        final_text_parts = []
        used_tools = None
        action = None
        versioned_content_id = None
        digital_content_id = None
        sources = []

        messages = await self._get_recent_messages(session_id)
        messages = [
            types.Content(
                role=message["role"],
                parts=[types.Part.from_text(text=message["content"])]
            ) for message in messages
        ]
        messages.append(
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=f'"{query}"')]
            )
        )

        await self._save_message(session_id, "user", query)

        try:
            llm_response = await self.make_llm_call(messages=messages, use_tools=True)

            while llm_response and llm_response.candidates[0].content.parts:
                candidate = llm_response.candidates[0].content.parts

                if len(candidate) == 1 and getattr(candidate[0], "function_call", None) is None:
                    logger.debug("Final response without tool usage.")
                    final_text_parts.append(candidate[0].text)
                    await self._save_message(session_id, "model", candidate[0].text)
                    return {
                        "message": "\n".join(final_text_parts),
                        "action": action,
                        "versioned_content_id": versioned_content_id,
                        "digital_content_id": digital_content_id,
                        "tool_call": used_tools,
                        "sources": sources
                    }

                # if getattr(llm_response, "text", None):
                #     final_text_parts.append(llm_response.text)
                #     await self._save_message(session_id, "model", llm_response.text)

                for part in candidate:
                    if getattr(part, "text", None):
                        final_text_parts.append(part.text)
                        await self._save_message(session_id, "model", part.text)

                    function_call = getattr(part, "function_call", None)
                    if function_call:
                        if not consent:
                            prompt = (
                                f"Please provide your consent to use your API keys to use tool {function_call.name} and try again'"
                            )
                            logger.warning(prompt)
                            return {"message": prompt,
                                    "tool_call": used_tools,
                                    "action": "consent",
                                    "versioned_content_id": versioned_content_id,
                                    "digital_content_id": digital_content_id,
                                    "sources": sources}

                        used_tools = {
                            "name": function_call.name,
                            "parameters": function_call.args or {}
                        }

                        messages.append(
                            types.Content(
                                parts=[
                                    types.Part.from_function_call(
                                        name=function_call.name,
                                        args=function_call.args
                                    )
                                ]
                            )
                        )

                        final_text_parts.append(
                            f"#### Calling tool '{function_call.name}\n"
                            f"<details open>\n"
                            f"<summary><strong>Tool arguments</strong></summary>\n"
                            f"\n```\n{function_call.args}\n```\n"
                            f"</details>\n"
                        )
                        logger.info(f"Calling tool: {function_call.name}")
                        tool_result = await self.call_tool(function_call.name, function_call.args, email, sources)
                        versioned_content_id = tool_result.versioned_content_id
                        digital_content_id = tool_result.digital_content_id
                        action = tool_result.action
                        logger.debug(f"Tool result: {tool_result.response}")
                        if tool_result.response:
                            messages.append(
                                types.Content(
                                    parts=[
                                        types.Part.from_function_response(
                                            name=function_call.name,
                                            response={"tool_response": tool_result.response},
                                        )
                                    ]
                                )
                            )
                llm_response = await self.make_llm_call(messages=messages, use_tools=True)

        except Exception as e:
            logger.error(f"Query processing failed: {e}")
            return {"message": f"Query processing failed: {e}", "tool_call": used_tools}

        return {
            "message": "\n".join(final_text_parts),
            "tool_call": used_tools,
            "action": action,
            "versioned_content_id": versioned_content_id,
            "digital_content_id": digital_content_id,
            "sources": sources
        }

    async def cleanup(self):
        logger.info("Cleaning up resources")
        try:
            await self.exit_stack.aclose()
        except Exception as e:
            logger.error(f"Cleanup error: {e}")

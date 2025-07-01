from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Set, Any
from aiohttp import ClientSession
from contextlib import AsyncExitStack
from google import genai
from google.genai import types
import vertexai
from mcp import ClientSession, StdioServerParameters
from fastapi.responses import JSONResponse
import asyncio
from vertexai.generative_models import GenerativeModel, Tool, FunctionDeclaration, Content
from mcp.client.stdio import stdio_client
import os
from fastapi.middleware.cors import CORSMiddleware

class MCPClient:
    def __init__(self):
        self.sessions: Optional[List[ClientSession]] = []
        self.exit_stack = AsyncExitStack()
        self.client = genai.Client(vertexai=True, project="apimanager-12", location="us-central1")

    async def connect_to_servers_from_directory(self, server_directory: str):
        script_files = [
            os.path.join(server_directory, f)
            for f in os.listdir(server_directory)
            if f.endswith(".py") or f.endswith(".js")
        ]
        if not script_files:
            raise ValueError("No .py or .js files found in directory.")

        for server_script_path in script_files:
            await self.connect_to_server(server_script_path)

        for idx, loc in enumerate(self.sessions):
            response = await loc.list_tools()
            loc_tools = response.tools
            print(
                f"\nConnected to {script_files[idx]} server with tools:",
                [tool.name for tool in loc_tools],
            )

    async def connect_to_server(self, server_script_path: str):
        is_python = server_script_path.endswith(".py")
        is_js = server_script_path.endswith(".js")
        if not (is_python or is_js):
            raise ValueError("Server script must be a .py or .js file")

        command = "python" if is_python else "node"
        from dotenv import load_dotenv
        load_dotenv()
        server_params = StdioServerParameters(command=command, args=[server_script_path],env=os.environ.copy())

        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport

        loc_session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))
        self.sessions.append(loc_session)

        await self.sessions[-1].initialize()

    async def process_query(self, query: str):
        # if not self.session:
        #     raise ValueError("Not connected to any server. Call /connect first.")

        final_text_parts = []
        tools = []
        messages = [f"""role": "user", "content": {query}"""]
        used_tools = None
        for session in self.sessions:
            response = await session.list_tools()
            # available_tools.extend([tool for tool in response.tools
            # ])
            tools.extend(
                types.Tool(
                    function_declarations=[
                        {
                            "name": tool.name,
                            "description": tool.description,
                            "parameters": {
                                k: v for k, v in tool.inputSchema.items()
                                if k not in ["additionalProperties", "$schema"]
                            },
                        }
                    ]
                )
                for tool in response.tools
        )

        response = self.client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=query,
            config=types.GenerateContentConfig(
                temperature=0.4,
                tools=tools,
                system_instruction=[
                    types.Part.from_text(text="""answer as per user queries with the tools available to you""")]
            ),

        )

        if response.candidates[0].content.parts[0].function_call:
            function_call = response.candidates[0].content.parts[0].function_call
            # print(function_call.args)

            try:
                used_tools = {"name": function_call.name, "parameters":{function_call.args}}
            except Exception as e:
                used_tools = None
            for session in self.sessions:
                response = await session.list_tools()
                if function_call.name in [tool.name for tool in response.tools]:
                    result = await session.call_tool(
                        function_call.name, arguments=dict(function_call.args) if function_call.args else None
                    )
                    # print(result)
                    try:
                        tool_response = result.content[0].text
                        messages.append(f"""role": "assistant", "content": {tool_response}""")
                        final_text_parts.append(f"Calling tool {function_call.name} with args {function_call.args}")
                    except Exception:
                        final_text_parts.append("Error parsing tool response")


        else:
            if response.text:
                messages.append(f"""role": "assistant", "content": {response.text}""")
                final_text_parts.append(response.text)

        # response = self.client.models.generate_content(
        #     model="gemini-2.0-flash-001",
        #     contents=final_text_parts,
        #     config=types.GenerateContentConfig(
        #         temperature=0.3,
        #     ),
        # )

        final_response = self.client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents="\n".join(messages),
            config=types.GenerateContentConfig(
                temperature=0.4,
                system_instruction=[
                    types.Part.from_text(text="""answer as per user queries with the content available to you""")]
            )
            )
        final_text_parts.append(final_response.text)
        return {"message":"\n".join(final_text_parts),
                                    "tool_call": used_tools}

        # return "\n".join(final_text)

    async def cleanup(self):
        await self.exit_stack.aclose()


# -------------------------------
# FASTAPI App
# -------------------------------
app = FastAPI()
mcp_client = MCPClient()

origins = [
    "http://localhost:4200",  # Allow requests from this origin
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


class QueryInput(BaseModel):
    message: str


@app.on_event("startup")
async def startup_event():
    await mcp_client.connect_to_servers_from_directory("./generated_servers")  # <-- CHANGE path here


@app.on_event("shutdown")
async def shutdown_event():
    await mcp_client.cleanup()


@app.post("/query")
async def handle_query(input: QueryInput):
    # try:
    result = await mcp_client.process_query(input.message)
    return (result)
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("client_api:api", host="0.0.0.0", port=5005, reload=True)

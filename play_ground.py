# from fastapi import HTTPException
# from typing import Optional, List, Dict, Any
# from contextlib import AsyncExitStack
# from google import genai
# from google.genai import types
# import vertexai
# from mcp import ClientSession, StdioServerParameters
# from vertexai.generative_models import GenerativeModel, Tool, FunctionDeclaration, Content
# from mcp.client.stdio import stdio_client
# import os
# from google.cloud import storage
# from dotenv import load_dotenv
#
#
# async def initialize_server():
#     load_dotenv()
#     command = "python"
#     server_script_path = "generated_servers/ai-apis_server.py"
#     server_params = StdioServerParameters(command=command, args=[server_script_path], env=os.environ.copy())
#
#     exit_stack = AsyncExitStack()
#     stdio_transport = await exit_stack.enter_async_context(stdio_client(server_params))
#     stdio, write = stdio_transport
#
#     client_session = ClientSession(stdio, write)
#     session = await exit_stack.enter_async_context(client_session)
#     result = await session.initialize()
#     response = await session.list_tools()
#
#
#     # print(type(session))
#     print(result.serverInfo.name)
#     # tool = response.tools[0]
#
#     # for attr in dir(tool):
#     #     print(f"{attr}: {getattr(tool, attr, 'Attribute not accessible')}")
#
#     print(session.server_url)
#
#     # for attr in dir(session):
#     #
#     #     print(f"{attr}: {getattr(session, attr, 'Attribute not accessible')}")
#
#     # for attr in dir(session.read_resource):
#     #
#     #     print(f"{attr}: {getattr(session.read_resource, attr, 'Attribute not accessible')}")
#
#     return session
#
# async def __main__():
#     print("Initializing server...")
#     await initialize_server()
#
# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(__main__())

from google import genai
from google.genai import types
client = genai.Client(vertexai=True, project="apimanager-12", location="us-central1")
def make_llm_call(messages):
    # contents = [
    #     types.Content(
    #         role=message["role"],
    #         parts=[types.Part.from_text(text=message["content"])]
    #
    #     ) for message in messages
    # ]
    contents = messages

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=contents,
            config=types.GenerateContentConfig(
                temperature=0.4,
                system_instruction=[
                    types.Part.from_text(text="""
You are a **reasoning-focused AI agent**. For every user query, follow these principles:

---

#### 🧠 Reasoning & Structure

* Carefully **analyze the user’s intent**.
* Organize responses using **logical, step-by-step reasoning**.
* If a tool is required, **use it effectively**. If not, complete the task using **inbuilt capabilities**.

---

#### 📝 Output Formatting

* Always use **clear and well-structured Markdown formatting**.
* Include the following where appropriate:

* **Bullet points** for lists
* **Tables** for structured data
* **Code blocks** for code, logs, or technical content
* Ensure all output is **visually readable and professional**.

---

#### 📊 Data Presentation

* Present **data in tables** or other clear formats — even if tools are not used.
* Use **headings** and **subheadings** to enhance readability.

---

#### 🔐 User Consent

* If any action **requires the user's consent** (e.g. using or storing personal data), clearly explain:

* **Why consent is needed**
* **What will happen**
* Explicitly **request consent** before proceeding.

---

#### 🔑 API Keys

* **Do not ask the user for API keys**.
* Assume that **API keys are automatically provided** to the tools.
""")
                ]
            )
        )
        return response
    except Exception as e:
        raise RuntimeError(f"LLM call failed: {e}")
query = "get all tools"
messages = []
messages.append(types.Content(
                role="user",
                parts=[types.Part.from_text(text=query)]

            ))

messages.append(types.Content(
    parts=[
        types.Part.from_function_call(
            name="get_weather",
            args={"city":"bengaluru"}
        )
    ]
))

messages.append(types.Content(
    parts=[
        types.Part.from_function_call(
            name="get_weather",
            args={"city":"bengaluru"}
        )
    ]
))

messages.append(types.Content(parts=[types.Part.from_function_response(
                        name="get_weather",
                        response={"message":"26°C, clear sky, humidity 60% with no rain expected in the next 24 hours."},
                    )]))
print(messages)


print(make_llm_call(messages=messages).text)
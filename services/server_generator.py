import streamlit as st
import yaml
import json
import os
import base64
import requests
import time
import logging
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.cloud import storage
from schemas.servers import ServerCreate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()
PROJECT = os.environ.get("PROJECT_ID")
SERVER_BUCKET_NAME = os.environ.get("SERVER_BUCKET_NAME")


async def load_api_contract(file_content, file_extension):
    logger.info(f"Loading API contract with extension: {file_extension}")
    if file_extension in [".yaml", ".yml"]:
        return yaml.safe_load(file_content)
    elif file_extension == ".json":
        return json.loads(file_content)
    else:
        raise ValueError("Only .yaml, .yml, and .json files are supported.")


# async def build_gemini_prompt(api_contract,versioned_content_id=None):
#     prompt = f"""You are an expert Python developer specializing in writing servers that act as wrappers for external APIs, specifically using the `mcp` library.
#
# **Objective:**
#
# Create a complete Python `mcp` server using `from mcp.server.fastmcp import FastMCP` that implements the following provided API contract by wrapping calls to the external API described in the contract.
# The code should bw within 700 lines
# **Server Details:**
#
# *   **Initialization:** Initialize the server using `mcp = FastMCP("server_name")`.
# *   **Dependencies:** Assume `mcp`, `aiohttp`, and `os` are available.
#
# **Implementation Requirements (for each endpoint in the provided contract):**
#
# 1.  **Function Definition:** Create one `async def` function for each endpoint.
# 2.  **Decorator:** Decorate each function with `@mcp.tool()`.
# 3.  **Function Name & Parameters:**
#     *   Derive the function name intuitively from the endpoint path/operation ID.
#     *   Define function arguments (`params`) based directly on the endpoint's request schema (path parameters, query parameters, request body). Use appropriate Python type hints.
#     *   The function signature must be `async def function_name(...) -> str:`.
# 4.  **Docstring:**
#     *   Include a PEP 257 compliant docstring.
#     *   The first line should be a concise description of the tool's purpose (derived from the endpoint summary/description).
#     *   Must Include an "Args:" section listing each parameter, its type hint, and a brief description (derived from the parameter description in the contract).
# 5.  **API Key Handling:**
#     *   Read the external API key from the environment variable named (generate key name) using `os.environ.get()`.
#     *   Include this key in the HTTP request headers when calling the external API (assume a common header like `Authorization: Bearer <key>` or `X-API-Key: <key>`; choose one that seems appropriate or is implied by the contract, if not specified the api doesn't need authentication.
# 6.  **External API Call:**
#     *   Use the `aiohttp` library to make asynchronous HTTP requests to the external API endpoint defined in the contract.
#     *   Construct the full request URL and body/query parameters from the function arguments.
# 7.  **Error Handling:**
#     *   Gracefully handle potential issues during the API call, such as network errors or non-successful HTTP status codes (e.g., 4xx, 5xx).
#     *   If an error occurs, return a clear, informative error message *as a string*.
# 8.  **Result Formatting:**
#     *   Upon a successful API response (e.g., 200 status code), parse the response data (assuming JSON).
#     *   Format the relevant information from the successful response into a human-readable plain text string. This string will be the function's return value.
# 9.  **No Helper Functions:** Do not create separate helper functions like `make_request`; the `aiohttp` call and logic should be within the `@mcp.tool()` function itself.
#
# **Overall Structure:**
#
# *   Include necessary imports (`os`, `aiohttp`, `FastMCP`).
# *   Define all `@mcp.tool()` functions.
# *   End the script with the standard entry point:
#
# ```python
# if __name__ == "__main__":
#     mcp.run(transport="stdio")
#
# optimize the code to fit in 8192 token limit
#
#     api contract = {api_contract}
#         """
#
#     return prompt

async def build_gemini_prompt(api_contract, versioned_content_id, digital_content_id):
    logger.info("Building Gemini prompt for server generation")
    prompt = f"""
**You are an expert Python developer specializing in creating server wrappers for external APIs using the `mcp` framework.**

---

### ✅ Objective

Write a complete Python server using `from mcp.server.fastmcp import FastMCP` to wrap all endpoints from the provided OpenAPI contract (`{api_contract}`), exposing each as a tool.

---

### ✅ Server Initialization

```python
mcp = FastMCP("{versioned_content_id}_{digital_content_id}")
```

---

### ✅ Constraints

* **Code must fit within 700 lines and under 8192 tokens.**
* Only use these libraries: `os`, `aiohttp`, `pydantic`, and `mcp`.
* No helper functions. All logic must live inside the `@mcp.tool()` functions.

---

### ✅ Endpoint Tool Generation Rules

#### 1. Function Declaration

* Define **one async function per endpoint**.
* Use the decorator: `@mcp.tool()`
* Signature: `async def function_name(...) -> str:`
* Name the function based on the `operationId` or the endpoint path meaningfully.

#### 2. Parameter Flattening & Input Schema

* **Do not use Pydantic models in function parameters.**
* **Flatten** all fields from request bodies, query params, and path params into **individual parameters** with proper type hints.
* Reconstruct Pydantic models **inside** the function if needed.

#### 3. Pydantic Usage (Internal Only)

* Use `pydantic.BaseModel` only **within** tool functions.
* Always set `class Config: extra = "forbid"` to prevent `additionalProperties`.
* Do not use `$ref`, `$defs`, nested models, or `: dict` types.

#### 4. Docstrings (PEP 257-Compliant)

* Start with a one-line summary of the tool’s purpose.
* Include an `Args:` section with:

  * Each parameter
  * Type hint
  * Brief description (from OpenAPI if available)

---

### ✅ API Authentication

* If authentication is required:

  * Add a parameter: `API_KEY: Optional[str] = None`
  * Retrieve default from: `os.environ.get("EXTERNAL_API_KEY")`
  * Use either `Authorization: Bearer <API_KEY>` or `X-API-Key: <API_KEY>` based on the OpenAPI spec or your best judgment.

---

### ✅ API Call Implementation

* Use `aiohttp` to perform **asynchronous** requests to the external API.
* Set query parameters, path variables, headers, and JSON body from flattened arguments.
* Handle response:

  * On error: return a string like `"Error: <description>"`
  * On success: return the json object of the api response.

---

### ✅ Final Code Structure

1. **Imports**:

   ```python
   import os
   import aiohttp
   from pydantic import BaseModel
   from mcp.server.fastmcp import FastMCP
   ```

2. **Optional** internal-only Pydantic models

3. **One `@mcp.tool()` function per endpoint**, each with:

   * Flattened parameters
   * Reconstructed models (if needed)
   * Inline HTTP call
   * Docstring and error handling
   * The tool output should be a string representation of the API response

4. **Entry Point**:

   ```python
   if __name__ == "__main__":
       mcp.run(transport="stdio")
   ```

---

### 🚫 Do Not Use

* `: dict` as a parameter type
* `additionalProperties`
* `$ref`, `$defs`, or nested Pydantic models
* Helper functions
* Unused libraries

---

### 📎 OpenAPI Contract

```
{api_contract}
```
    """

    return prompt



async def generate_code_with_gemini(prompt):
    logger.info("Generating code with Gemini model")
    try:
        client = genai.Client(
            vertexai=True,
            project=PROJECT,
            location="us-central1",
        )

        model = "gemini-2.0-flash-001"
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=prompt),
                ]
            ),
        ]
        generate_content_config = types.GenerateContentConfig(
            temperature=0.2,
            top_p=0.95,
            max_output_tokens=8192,
            response_modalities=["TEXT"],
            safety_settings=[types.SafetySetting(
                category="HARM_CATEGORY_HATE_SPEECH",
                threshold="OFF"
            ), types.SafetySetting(
                category="HARM_CATEGORY_DANGEROUS_CONTENT",
                threshold="OFF"
            ), types.SafetySetting(
                category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                threshold="OFF"
            ), types.SafetySetting(
                category="HARM_CATEGORY_HARASSMENT",
                threshold="OFF"
            )],
        )

        response = client.models.generate_content(
            model=model,
            contents=contents,
            config=generate_content_config,
        )
        logger.info("Code generation completed successfully")

        return response.text.strip()
    except Exception as e:
        logger.error(f"Gemini code generation failed: {e}")
        raise

async def generate_mcp_server_from_upload(uploaded_file):
    logger.info(f"Generating MCP server from uploaded file: {uploaded_file.file_name}")
    try:
        filename = uploaded_file.file_name
        versioned_content_id = uploaded_file.versionedContentId
        digital_content_id = uploaded_file.digitalContentId
        output_filename = filename.split(".")[0]
        output_filename = f"{output_filename}_server.py"

        # Step 1: Load contract
        content = uploaded_file.file_content
        file_extension = "." + filename.split(".")[-1]
        # api_contract = await load_api_contract(content, file_extension)

        # Step 2: Build prompt
        prompt = await build_gemini_prompt(content, versioned_content_id=versioned_content_id, digital_content_id=digital_content_id)

        # Step 3: Generate MCP server code
        generated_code = await generate_code_with_gemini(prompt)

        generated_code = generated_code.replace("```python", "").replace("```", "")

        # Step 4: Save the generated code to GCP
        logger.info(f"Uploading generated code to GCS as: {output_filename}")
        client = storage.Client()
        bucket_name = SERVER_BUCKET_NAME  # Replace with your GCP bucket name
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(output_filename)
        if blob is None:
            raise ValueError("Blob object is None. Ensure it is properly initialized.")

        # Proceed with the upload

        blob.upload_from_string(generated_code, content_type="text/plain")
        gcs_path = f"gs://{bucket_name}/{output_filename}"

        logger.info(f"Upload successful: {gcs_path}")
        return gcs_path
    except Exception as e:
        logger.error(f"Failed to generate server from upload: {e}")
        raise



import asyncio
import json
import os
from typing import Dict, Any
import aiohttp
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
load_dotenv()

mcp = FastMCP("ai_tools")
BASE_URL = "https://kong-admin-api-preprod.dsh.digitalapicraft.com"


async def make_request(method: str, url: str, headers: Dict[str, str], data: Dict[str, Any] = None) -> Any:
    """Makes an asynchronous HTTP request using aiohttp.

    Args:
        method: HTTP method (e.g., "POST", "GET", "DELETE").
        url: The URL to request.
        headers: HTTP headers.
        data: Request body (for POST, PUT, etc.).

    Returns:
        The JSON response, or None if an error occurred.
    """
    async with aiohttp.ClientSession() as session:
        try:
            async with session.request(method, url, headers=headers, json=data) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return f"Error: {response.status} - {await response.text()}"
        except aiohttp.ClientError as e:
            return f"Request failed: {e}"


@mcp.tool()
async def retrieveUserSearchesByLoggedInUser(user_id: str) -> str:
    """Retrieves user searches by logged-in user.

    Args:
        user_id: The ID of the logged-in user.
    """
    url = f"{BASE_URL}/api/v1/search/user/searches/history"
    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": os.environ.get("AI_TOOLS_KEY", "")
    }
    data = {"user_id": user_id}
    response = await make_request("POST", url, headers, data)
    return json.dumps(response, indent=2)


@mcp.tool()
async def search(query: str, limit: int = 10) -> str:
    """Performs a search.

    Args:
        query: The search query.
        limit: The maximum number of results to return.
    """
    url = f"{BASE_URL}/api/v1/search/ai"
    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": os.environ.get("AI_TOOLS_KEY", "")
    }
    data = {"query": query, "limit": limit}
    response = await make_request("POST", url, headers, data)
    return json.dumps(response, indent=2)


@mcp.tool()
async def retrieveSdkSourceForLanguage(language: str, sdk_name: str) -> str:
    """Retrieves SDK source code for a given language.

    Args:
        language: The programming language (e.g., "python", "java").
        sdk_name: The name of the SDK.
    """
    url = f"{BASE_URL}/api/v1/ai/sdk/retrieve"
    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": os.environ.get("AI_TOOLS_KEY", "")
    }
    data = {"language": language, "sdk_name": sdk_name}
    response = await make_request("POST", url, headers, data)
    return json.dumps(response, indent=2)


@mcp.tool()
async def retrieveAutoDocumentation(api_endpoint: str) -> str:
    """Retrieves auto-generated documentation for an API endpoint.

    Args:
        api_endpoint: The API endpoint to document.
    """
    url = f"{BASE_URL}/api/v1/ai/documentation"
    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": os.environ.get("AI_TOOLS_KEY", "")
    }
    data = {"api_endpoint": api_endpoint}
    response = await make_request("POST", url, headers, data)
    return json.dumps(response, indent=2)


@mcp.tool()
async def getApiAffinity(api_endpoint: str, user_id: str) -> str:
    """Retrieves API affinity for a given endpoint and user.

    Args:
        api_endpoint: The API endpoint.
        user_id: The ID of the user.
    """
    url = f"{BASE_URL}/api/v1/ai/affinity"
    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": os.environ.get("AI_TOOLS_KEY", "")
    }
    data = {"api_endpoint": api_endpoint, "user_id": user_id}
    response = await make_request("POST", url, headers, data)
    return json.dumps(response, indent=2)


@mcp.tool()
async def refreshCacheAndGetApiAffinity(api_endpoint: str, user_id: str) -> str:
    """Refreshes the cache and retrieves API affinity.

    Args:
        api_endpoint: The API endpoint.
        user_id: The ID of the user.
    """
    url = f"{BASE_URL}/api/v1/ai/affinity/refresh"
    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": os.environ.get("AI_TOOLS_KEY", "")
    }
    data = {"api_endpoint": api_endpoint, "user_id": user_id}
    response = await make_request("POST", url, headers, data)
    return json.dumps(response, indent=2)


@mcp.tool()
async def retrieveAllGlobalSearches() -> str:
    """Retrieves all global searches."""
    url = f"{BASE_URL}/api/v1/search/global/searches/history"
    headers = {
        "X-API-KEY": os.environ.get("AI_TOOLS_KEY", "")
    }
    response = await make_request("GET", url, headers)
    return json.dumps(response, indent=2)


@mcp.tool()
async def invalidateEntireApiAffinityCache() -> str:
    """Invalidates the entire API affinity cache."""
    url = f"{BASE_URL}/api/v1/ai/affinity/invalidate"
    headers = {
        "X-API-KEY": os.environ.get("AI_TOOLS_KEY", "")
    }
    response = await make_request("DELETE", url, headers)
    return json.dumps(response, indent=2)

if __name__ == "__main__":
    mcp.run(transport="stdio")

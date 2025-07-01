
import asyncio
import os
import aiohttp
import json
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
load_dotenv()
mcp = FastMCP("digital_api")
BASE_URL = "https://kong-admin-api-preprod.dsh.digitalapicraft.com"

@mcp.tool()
async def updateDigitalProduct(data: str) -> str:
    """Updates a digital product.

    Args:
        data: JSON string containing the digital product data.
    """
    url = f"{BASE_URL}/api/v1/digital-products"
    headers = {"Content-Type": "application/json", "x-api-key": os.environ.get("DIGITAL_API_KEY")}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.put(url, headers=headers, data=data) as response:
                response.raise_for_status()
                return await response.text()
    except aiohttp.ClientError as e:
        return f"Error: {e}"

@mcp.tool()
async def createDigitalProduct(data: str) -> str:
    """Creates a digital product.

    Args:
        data: JSON string containing the digital product data.
    """
    url = f"{BASE_URL}/api/v1/digital-products"
    headers = {"Content-Type": "application/json", "x-api-key": os.environ.get("DIGITAL_API_KEY")}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=data) as response:
                response.raise_for_status()
                return await response.text()
    except aiohttp.ClientError as e:
        return f"Error: {e}"

@mcp.tool()
async def deleteVersionedContentDocumentation(data: str) -> str:
    """Deletes versioned content documentation.

    Args:
        data: JSON string containing the data for deletion.
    """
    url = f"{BASE_URL}/api/v1/digital-content/documentation/delete"
    headers = {"Content-Type": "application/json", "x-api-key": os.environ.get("DIGITAL_API_KEY")}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.put(url, headers=headers, data=data) as response:
                response.raise_for_status()
                return await response.text()
    except aiohttp.ClientError as e:
        return f"Error: {e}"

@mcp.tool()
async def updateApi(data: str) -> str:
    """Updates an API.

    Args:
        data: JSON string containing the API data.
    """
    url = f"{BASE_URL}/api/v1/digital-content/apis"
    headers = {"Content-Type": "application/json", "x-api-key": os.environ.get("DIGITAL_API_KEY")}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.put(url, headers=headers, data=data) as response:
                response.raise_for_status()
                return await response.text()
    except aiohttp.ClientError as e:
        return f"Error: {e}"

@mcp.tool()
async def getContentRatingForUser(content_id: str, user_id: str) -> str:
    """Gets the content rating for a user.

    Args:
        content_id: The ID of the content.
        user_id: The ID of the user.
    """
    url = f"{BASE_URL}/api/v1/ratings?contentId={content_id}&userId={user_id}"
    headers = {"x-api-key": os.environ.get("DIGITAL_API_KEY")}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                return await response.text()
    except aiohttp.ClientError as e:
        return f"Error: {e}"

@mcp.tool()
async def rateApi(data: str) -> str:
    """Rates an API.

    Args:
        data: JSON string containing the rating data.
    """
    url = f"{BASE_URL}/api/v1/ratings"
    headers = {"Content-Type": "application/json", "x-api-key": os.environ.get("DIGITAL_API_KEY")}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=data) as response:
                response.raise_for_status()
                return await response.text()
    except aiohttp.ClientError as e:
        return f"Error: {e}"

@mcp.tool()
async def deleteDigitalProduct(data: str) -> str:
    """Deletes a digital product.

    Args:
        data: JSON string containing the data for deletion.
    """
    url = f"{BASE_URL}/api/v1/digital-products/delete"
    headers = {"Content-Type": "application/json", "x-api-key": os.environ.get("DIGITAL_API_KEY")}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=data) as response:
                response.raise_for_status()
                return await response.text()
    except aiohttp.ClientError as e:
        return f"Error: {e}"

@mcp.tool()
async def updatePublishedApi(data: str) -> str:
    """Updates a published API.

    Args:
        data: JSON string containing the API data.
    """
    url = f"{BASE_URL}/api/v1/digital-content/virtual-gateway/update-published-api"
    headers = {"Content-Type": "application/json", "x-api-key": os.environ.get("DIGITAL_API_KEY")}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=data) as response:
                response.raise_for_status()
                return await response.text()
    except aiohttp.ClientError as e:
        return f"Error: {e}"

@mcp.tool()
async def publishApi(data: str) -> str:
    """Publishes an API.

    Args:
        data: JSON string containing the API data.
    """
    url = f"{BASE_URL}/api/v1/digital-content/virtual-gateway/publish-api"
    headers = {"Content-Type": "application/json", "x-api-key": os.environ.get("DIGITAL_API_KEY")}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=data) as response:
                response.raise_for_status()
                return await response.text()
    except aiohttp.ClientError as e:
        return f"Error: {e}"

@mcp.tool()
async def deleteVersionedContent(data: str) -> str:
    """Deletes versioned content.

    Args:
        data: JSON string containing the data for deletion.
    """
    url = f"{BASE_URL}/api/v1/digital-content/versioned/delete"
    headers = {"Content-Type": "application/json", "x-api-key": os.environ.get("DIGITAL_API_KEY")}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=data) as response:
                response.raise_for_status()
                return await response.text()
    except aiohttp.ClientError as e:
        return f"Error: {e}"

@mcp.tool()
async def getDigitalContentPage(data: str) -> str:
    """Gets a digital content page.

    Args:
        data: JSON string containing the request data.
    """
    url = f"{BASE_URL}/api/v1/digital-content/page"
    headers = {"Content-Type": "application/json", "x-api-key": os.environ.get("DIGITAL_API_KEY")}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=data) as response:
                response.raise_for_status()
                return await response.text()
    except aiohttp.ClientError as e:
        return f"Error: {e}"

@mcp.tool()
async def getDigitalContentsPageForWrappedVersionedContents(data: str) -> str:
    """Gets a digital contents page for wrapped versioned contents.

    Args:
        data: JSON string containing the request data.
    """
    url = f"{BASE_URL}/api/v1/digital-content/page/wrapped-versioned-contents"
    headers = {"Content-Type": "application/json", "x-api-key": os.environ.get("DIGITAL_API_KEY")}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=data) as response:
                response.raise_for_status()
                return await response.text()
    except aiohttp.ClientError as e:
        return f"Error: {e}"

@mcp.tool()
async def getGcsFile(file_path: str) -> str:
    """Gets a GCS file.

    Args:
        file_path: The path to the file in GCS.
    """
    url = f"{BASE_URL}/api/v1/digital-content/documentation?filePath={file_path}"
    headers = {"x-api-key": os.environ.get("DIGITAL_API_KEY")}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                return await response.text()
    except aiohttp.ClientError as e:
        return f"Error: {e}"

@mcp.tool()
async def uploadAiGeneratedDocumentation_1(data: str) -> str:
    """Uploads AI-generated documentation.

    Args:
        data: JSON string containing the documentation data.
    """
    url = f"{BASE_URL}/api/v1/digital-content/documentation"
    headers = {"Content-Type": "application/json", "x-api-key": os.environ.get("DIGITAL_API_KEY")}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=data) as response:
                response.raise_for_status()
                return await response.text()
    except aiohttp.ClientError as e:
        return f"Error: {e}"

@mcp.tool()
async def validateZipStructure(data: str) -> str:
    """Validates the structure of a ZIP file.

    Args:
        data: JSON string containing the ZIP file data.
    """
    url = f"{BASE_URL}/api/v1/digital-content/documentation/validate"
    headers = {"Content-Type": "application/json", "x-api-key": os.environ.get("DIGITAL_API_KEY")}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=data) as response:
                response.raise_for_status()
                return await response.text()
    except aiohttp.ClientError as e:
        return f"Error: {e}"

@mcp.tool()
async def revokeCredentialsForDigitalProducts(data: str) -> str:
    """Revokes credentials for digital products.

    Args:
        data: JSON string containing the data for revocation.
    """
    url = f"{BASE_URL}/api/v1/digital-content/digital-products/revoke-credentials"
    headers = {"Content-Type": "application/json", "x-api-key": os.environ.get("DIGITAL_API_KEY")}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=data) as response:
                response.raise_for_status()
                return await response.text()
    except aiohttp.ClientError as e:
        return f"Error: {e}"

@mcp.tool()
async def generateCredentialsForDigitalProducts(data: str) -> str:
    """Generates credentials for digital products.

    Args:
        data: JSON string containing the data for generation.
    """
    url = f"{BASE_URL}/api/v1/digital-content/digital-products/generate-credentials"
    headers = {"Content-Type": "application/json", "x-api-key": os.environ.get("DIGITAL_API_KEY")}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=data) as response:
                response.raise_for_status()
                return await response.text()
    except aiohttp.ClientError as e:
        return f"Error: {e}"

@mcp.tool()
async def fetchCredentialsForDigitalProducts(data: str) -> str:
    """Fetches credentials for digital products.

    Args:
        data: JSON string containing the data for fetching.
    """
    url = f"{BASE_URL}/api/v1/digital-content/digital-products/fetch-credentials"
    headers = {"Content-Type": "application/json", "x-api-key": os.environ.get("DIGITAL_API_KEY")}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=data) as response:
                response.raise_for_status()
                return await response.text()
    except aiohttp.ClientError as e:
        return f"Error: {e}"

@mcp.tool()
async def checkIfDigitalContentByUniqueIndexExist(data: str) -> str:
    """Checks if digital content exists by unique index.

    Args:
        data: JSON string containing the data for checking.
    """
    url = f"{BASE_URL}/api/v1/digital-content/check-duplicate"
    headers = {"Content-Type": "application/json", "x-api-key": os.environ.get("DIGITAL_API_KEY")}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=data) as response:
                response.raise_for_status()
                return await response.text()
    except aiohttp.ClientError as e:
        return f"Error: {e}"

@mcp.tool()
async def revokeCredentials(data: str) -> str:
    """Revokes credentials for APIs.

    Args:
        data: JSON string containing the data for revocation.
    """
    url = f"{BASE_URL}/api/v1/digital-content/apis/revoke-credentials"
    headers = {"Content-Type": "application/json", "x-api-key": os.environ.get("DIGITAL_API_KEY")}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=data) as response:
                response.raise_for_status()
                return await response.text()
    except aiohttp.ClientError as e:
        return f"Error: {e}"

@mcp.tool()
async def getImportedApis(id: str) -> str:
    """Gets imported APIs by ID.

    Args:
        id: The ID of the imported API.
    """
    url = f"{BASE_URL}/api/v1/digital-content/apis/import/{id}"
    headers = {"x-api-key": os.environ.get("DIGITAL_API_KEY")}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                return await response.text()
    except aiohttp.ClientError as e:
        return f"Error: {e}"

@mcp.tool()
async def importApis(id: str, data: str) -> str:
    """Imports APIs by ID.

    Args:
        id: The ID for importing the API.
        data: JSON string containing the API data.
    """
    url = f"{BASE_URL}/api/v1/digital-content/apis/import/{id}"
    headers = {"Content-Type": "application/json", "x-api-key": os.environ.get("DIGITAL_API_KEY")}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=data) as response:
                response.raise_for_status()
                return await response.text()
    except aiohttp.ClientError as e:
        return f"Error: {e}"

@mcp.tool()
async def generateCredentials(data: str) -> str:
    """Generates credentials for APIs.

    Args:
        data: JSON string containing the data for generation.
    """
    url = f"{BASE_URL}/api/v1/digital-content/apis/generate-credentials"
    headers = {"Content-Type": "application/json", "x-api-key": os.environ.get("DIGITAL_API_KEY")}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=data) as response:
                response.raise_for_status()
                return await response.text()
    except aiohttp.ClientError as e:
        return f"Error: {e}"

@mcp.tool()
async def fetchCredentials(data: str) -> str:
    """Fetches credentials for APIs.

    Args:
        data: JSON string containing the data for fetching.
    """
    url = f"{BASE_URL}/api/v1/digital-content/apis/fetch-credentials"
    headers = {"Content-Type": "application/json", "x-api-key": os.environ.get("DIGITAL_API_KEY")}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=data) as response:
                response.raise_for_status()
                return await response.text()
    except aiohttp.ClientError as e:
        return f"Error: {e}"

@mcp.tool()
async def getVersionedContentById(id: str) -> str:
    """Gets versioned content by ID.

    Args:
        id: The ID of the versioned content.
    """
    url = f"{BASE_URL}/api/v1/digital-content?id={id}"
    headers = {"x-api-key": os.environ.get("DIGITAL_API_KEY")}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                return await response.text()
    except aiohttp.ClientError as e:
        return f"Error: {e}"

@mcp.tool()
async def getContentForDetailPage(content_id: str) -> str:
    """Gets content for a detail page.

    Args:
        content_id: The ID of the content.
    """
    url = f"{BASE_URL}/api/v1/digital-content/detail?contentId={content_id}"
    headers = {"x-api-key": os.environ.get("DIGITAL_API_KEY")}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                return await response.text()
    except aiohttp.ClientError as e:
        return f"Error: {e}"

@mcp.tool()
async def getAllImportedApis() -> str:
    """Gets all imported APIs.
    """
    url = f"{BASE_URL}/api/v1/digital-content/apis/import"
    headers = {"x-api-key": os.environ.get("DIGITAL_API_KEY")}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                return await response.text()
    except aiohttp.ClientError as e:
        return f"Error: {e}"

if __name__ == "__main__":
    mcp.run(transport="stdio")

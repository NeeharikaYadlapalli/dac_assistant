
import asyncio
import os
import aiohttp
import json
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
load_dotenv()
import logging

logging.basicConfig(level=logging.DEBUG)

mcp = FastMCP("organisation_settings")
BASE_URL = "https://kong-admin-api-preprod-1019068528267.europe-west4.run.app"
API_KEY = os.environ.get("ORGANISATION_SETTINGS_KEY")

logging.info("setting server API KEY %s", API_KEY)

async def make_request(method, url, headers=None, data=None):
    """
    Makes an asynchronous HTTP request using aiohttp.

    Args:
        method (str): HTTP method (e.g., "GET", "POST", "PUT").
        url (str): The URL to request.
        headers (dict, optional): Request headers. Defaults to None.
        data (dict, optional): Request body data (for POST/PUT). Defaults to None.

    Returns:
        tuple: A tuple containing the status code and the JSON response (if any).
               Returns None if an error occurs.
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, headers=headers, json=data) as response:
                status_code = response.status
                try:
                    response_json = await response.json()
                except aiohttp.ContentTypeError:
                    response_json = await response.text()
                return status_code, response_json
    except Exception as e:
        print(f"Error during request: {e}")
        return None, None

@mcp.tool()
async def getUiCustomisationSettings() -> str:
    """Retrieves UI customisation settings.

    Args:
        None
    """
    url = f"{BASE_URL}/api/v1/org/settings/ui-customisation"
    headers = {"apikey": API_KEY}
    status_code, response_json = await make_request("GET", url, headers=headers)

    if status_code == 200:
        print("Request successful: Retrieved UI customisation settings.")
        print(response_json)
        return json.dumps(response_json, indent=2)
    else:
        print("Request unsuccessful: ", {response_json})
        logging.error("Request unsuccessful: %s", status_code)
        logging.error("Request unsuccessful: %s", response_json)
        return f"Error: {status_code} - {response_json}"

@mcp.tool()
async def updateUiCustomisationSettings(settings: str) -> str:
    """Updates UI customisation settings.

    Args:
        settings: JSON string representing the UI customisation settings to update.
    """
    url = f"{BASE_URL}/api/v1/org/settings/ui-customisation"
    headers = {"apikey": API_KEY}
    try:
        data = json.loads(settings)
    except json.JSONDecodeError:
        return "Error: Invalid JSON format for settings."

    status_code, response_json = await make_request("PUT", url, headers=headers, data=data)

    if status_code == 200:
        return json.dumps(response_json, indent=2)
    else:
        return f"Error: {status_code} - {response_json}"

@mcp.tool()
async def primeDefaultUiCustomisationSettings() -> str:
    """Primes default UI customisation settings.

    Args:
        None
    """
    url = f"{BASE_URL}/api/v1/org/settings/ui-customisation/default"
    headers = {"apikey": API_KEY}
    status_code, response_json = await make_request("PUT", url, headers=headers)

    if status_code == 200:
        return json.dumps(response_json, indent=2)
    else:
        return f"Error: {status_code} - {response_json}"

@mcp.tool()
async def updateActiveUiCustomisationSettings() -> str:
    """Updates active UI customisation settings.

    Args:
        None
    """
    url = f"{BASE_URL}/api/v1/org/settings/ui-customisation/active"
    headers = {"apikey": API_KEY}
    status_code, response_json = await make_request("PUT", url, headers=headers)

    if status_code == 200:
        return json.dumps(response_json, indent=2)
    else:
        return f"Error: {status_code} - {response_json}"

@mcp.tool()
async def findOrganisationSettingByOrganisationId() -> str:
    """Finds organisation settings by organisation ID.

    Args:
        None
    """
    url = f"{BASE_URL}/api/v1/org/settings"
    headers = {"apikey": API_KEY}
    status_code, response_json = await make_request("GET", url, headers=headers)

    if status_code == 200:
        return json.dumps(response_json, indent=2)
    else:
        return f"Error: {status_code} - {response_json}"

@mcp.tool()
async def createOrUpdateOrgSettings(settings: str) -> str:
    """Creates or updates organisation settings.

    Args:
        settings: JSON string representing the organisation settings to create or update.
    """
    url = f"{BASE_URL}/api/v1/org/settings"
    headers = {"apikey": API_KEY}
    try:
        data = json.loads(settings)
    except json.JSONDecodeError:
        return "Error: Invalid JSON format for settings."

    status_code, response_json = await make_request("POST", url, headers=headers, data=data)

    if status_code == 200:
        return json.dumps(response_json, indent=2)
    else:
        return f"Error: {status_code} - {response_json}"

@mcp.tool()
async def sendBasicSupportEmail(email_data: str) -> str:
    """Sends a basic support email.

    Args:
        email_data: JSON string containing the email data (e.g., recipient, subject, body).
    """
    url = f"{BASE_URL}/api/v1/operations/support/basic/support/email"
    headers = {"apikey": API_KEY}
    try:
        data = json.loads(email_data)
    except json.JSONDecodeError:
        return "Error: Invalid JSON format for email_data."

    status_code, response_json = await make_request("POST", url, headers=headers, data=data)

    if status_code == 200:
        return json.dumps(response_json, indent=2)
    else:
        return f"Error: {status_code} - {response_json}"

@mcp.tool()
async def getAllVisibilities() -> str:
    """Retrieves all visibilities.

    Args:
        None
    """
    url = f"{BASE_URL}/api/v1/org/visibilities"
    headers = {"apikey": API_KEY}
    status_code, response_json = await make_request("GET", url, headers=headers)

    if status_code == 200:
        return json.dumps(response_json, indent=2)
    else:
        return f"Error: {status_code} - {response_json}"

@mcp.tool()
async def extractUserCreditsFromOrganisation() -> str:
    """Extracts user credits from an organisation.

    Args:
        None
    """
    url = f"{BASE_URL}/api/v1/org/user-remaining-credits"
    headers = {"apikey": API_KEY}
    status_code, response_json = await make_request("GET", url, headers=headers)

    if status_code == 200:
        return json.dumps(response_json, indent=2)
    else:
        return f"Error: {status_code} - {response_json}"

@mcp.tool()
async def retrievePubliclyEnabledPortals() -> str:
    """Retrieves publicly enabled portals.

    Args:
        None
    """
    url = f"{BASE_URL}/api/v1/org/settings/public-portals"
    headers = {"apikey": API_KEY}
    status_code, response_json = await make_request("GET", url, headers=headers)

    if status_code == 200:
        return json.dumps(response_json, indent=2)
    else:
        return f"Error: {status_code} - {response_json}"

@mcp.tool()
async def getAllRoles() -> str:
    """Retrieves all roles.

    Args:
        None
    """
    url = f"{BASE_URL}/api/v1/org/roles"
    headers = {"apikey": API_KEY}
    status_code, response_json = await make_request("GET", url, headers=headers)

    if status_code == 200:
        return json.dumps(response_json, indent=2)
    else:
        return f"Error: {status_code} - {response_json}"

@mcp.tool()
async def getAllSupportedContentTypes() -> str:
    """Retrieves all supported content types.

    Args:
        None
    """
    url = f"{BASE_URL}/api/v1/org/content-types"
    headers = {"apikey": API_KEY}
    status_code, response_json = await make_request("GET", url, headers=headers)

    if status_code == 200:
        return json.dumps(response_json, indent=2)
    else:
        return f"Error: {status_code} - {response_json}"

@mcp.tool()
async def getAppVersion() -> str:
    """Retrieves the api version.

    Args:
        None
    """
    url = f"{BASE_URL}/api/v1/org/api/version"
    headers = {"apikey": API_KEY}
    status_code, response_json = await make_request("GET", url, headers=headers)

    if status_code == 200:
        return json.dumps(response_json, indent=2)
    else:
        return f"Error: {status_code} - {response_json}"

if __name__ == "__main__":
    mcp.run(transport="stdio")

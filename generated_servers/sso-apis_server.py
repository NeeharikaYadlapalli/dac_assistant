
import asyncio
import json
import os
from typing import Dict, Any

import aiohttp
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
load_dotenv()
mcp = FastMCP("sso_profiles")
BASE_URL = "https://kong-admin-api-preprod.dsh.digitalapicraft.com"
API_KEY = os.environ.get("SSO_PROFILES_KEY")


@mcp.tool()
async def getSsoProfiles() -> str:
    """Retrieves SSO profiles.

    Args:
        None
    """
    headers = {"apikey": API_KEY}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{BASE_URL}/api/v1/sso/profiles", headers=headers) as response:
                response.raise_for_status()
                data = await response.json()

                return json.dumps(data, indent=2)
        except aiohttp.ClientError as e:
            return f"Error: {e}"


@mcp.tool()
async def updateSsoProfile(profile_data: str) -> str:
    """Updates an SSO profile.

    Args:
        profile_data: JSON string containing the profile data to update.
    """
    headers = {"apikey": API_KEY, "Content-Type": "application/json"}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.put(f"{BASE_URL}/api/v1/sso/profiles", headers=headers, data=profile_data) as response:
                response.raise_for_status()
                data = await response.json()
                return json.dumps(data, indent=2)
        except aiohttp.ClientError as e:
            return f"Error: {e}"


@mcp.tool()
async def createSsoProfile(profile_data: str) -> str:
    """Create a new SSO profile

    Args:
        profile_data: JSON string containing the profile data to create.
    """
    headers = {"apikey": API_KEY, "Content-Type": "application/json"}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(f"{BASE_URL}/api/v1/sso/profiles", headers=headers, data=profile_data) as response:
                response.raise_for_status()
                data = await response.json()
                return json.dumps(data, indent=2)
        except aiohttp.ClientError as e:
            return f"Error: {e}"


@mcp.tool()
async def deleteSsoProfile() -> str:
    """Deletes an SSO profile.

    Args:
        None
    """
    headers = {"apikey": API_KEY}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.delete(f"{BASE_URL}/api/v1/sso/profiles", headers=headers) as response:
                response.raise_for_status()
                return "SSO profile deleted successfully."
        except aiohttp.ClientError as e:
            return f"Error: {e}"


@mcp.tool()
async def validateSamlToken(saml_token: str) -> str:
    """Validates a SAML token.

    Args:
        saml_token: The SAML token to validate.
    """
    headers = {"apikey": API_KEY, "Content-Type": "application/json"}
    data = {"token": saml_token}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(f"{BASE_URL}/api/v1/sso/saml/validate", headers=headers, json=data) as response:
                response.raise_for_status()
                data = await response.json()
                return json.dumps(data, indent=2)
        except aiohttp.ClientError as e:
            return f"Error: {e}"


@mcp.tool()
async def validateSamlToken_1(saml_token: str) -> str:
    """Validates a SAML token.

    Args:
        saml_token: The SAML token to validate.
    """
    headers = {"apikey": API_KEY, "Content-Type": "application/json"}
    data = {"token": saml_token}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(f"{BASE_URL}/api/v1/sso/saml-token/validate", headers=headers, json=data) as response:
                response.raise_for_status()
                data = await response.json()
                return json.dumps(data, indent=2)
        except aiohttp.ClientError as e:
            return f"Error: {e}"


@mcp.tool()
async def validateOpenIdToken(openid_token: str) -> str:
    """Validates an OpenID token.

    Args:
        openid_token: The OpenID token to validate.
    """
    headers = {"apikey": API_KEY, "Content-Type": "application/json"}
    data = {"token": openid_token}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(f"{BASE_URL}/api/v1/sso/openid-token/validate", headers=headers, json=data) as response:
                response.raise_for_status()
                data = await response.json()
                return json.dumps(data, indent=2)
        except aiohttp.ClientError as e:
            return f"Error: {e}"


@mcp.tool()
async def getCustomToken() -> str:
    """Retrieves a custom token.

    Args:
        None
    """
    headers = {"apikey": API_KEY}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{BASE_URL}/api/v1/sso/custom-token", headers=headers) as response:
                response.raise_for_status()
                data = await response.json()
                return json.dumps(data, indent=2)
        except aiohttp.ClientError as e:
            return f"Error: {e}"


if __name__ == "__main__":
    mcp.run(transport="stdio")


import asyncio
import os
import aiohttp
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
load_dotenv()
mcp = FastMCP("kong_gateway")
BASE_URL = "https://kong-admin-api-preprod.dsh.digitalapicraft.com"

async def make_request(method, url, headers=None, json=None):
    """
    Makes an asynchronous HTTP request.

    Args:
        method (str): HTTP method (e.g., "GET", "POST", "PUT").
        url (str): The URL to request.
        headers (dict, optional): Request headers. Defaults to None.
        json (dict, optional): JSON payload for the request. Defaults to None.

    Returns:
        tuple: (status_code, response_text)
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, headers=headers, json=json) as response:
                status_code = response.status
                response_text = await response.text()
                return status_code, response_text
    except aiohttp.ClientError as e:
        return 500, f"Error during request: {e}"
    except Exception as e:
        return 500, f"Unexpected error: {e}"


@mcp.tool()
async def getAllGatewayConnectionInstances() -> str:
    """Retrieves all gateway connection instances.

    Args:
        None
    """
    api_key = os.environ.get("KONG_GATEWAY_KEY")
    headers = {"X-Api-Key": api_key}
    status_code, response_text = await make_request("GET", f"{BASE_URL}/api/v1/gateway/connections", headers=headers)
    return f"Status: {status_code}, Response: {response_text}"


@mcp.tool()
async def updateGatewayConnectionInstance(id: str, connection_details: str) -> str:
    """Updates a gateway connection instance.

    Args:
        id: The ID of the gateway connection instance to update.
        connection_details: JSON string containing the updated connection details.
    """
    api_key = os.environ.get("KONG_GATEWAY_KEY")
    headers = {"X-Api-Key": api_key, "Content-Type": "application/json"}
    status_code, response_text = await make_request("PUT", f"{BASE_URL}/api/v1/gateway/connections", headers=headers, json=connection_details)
    return f"Status: {status_code}, Response: {response_text}"


@mcp.tool()
async def createGatewayConnection(connection_details: str) -> str:
    """Creates a new gateway connection.

    Args:
        connection_details: JSON string containing the connection details.
    """
    api_key = os.environ.get("KONG_GATEWAY_KEY")
    headers = {"X-Api-Key": api_key, "Content-Type": "application/json"}
    status_code, response_text = await make_request("POST", f"{BASE_URL}/api/v1/gateway/connections", headers=headers, json=connection_details)
    return f"Status: {status_code}, Response: {response_text}"


@mcp.tool()
async def logHttpRequest(log_data: str) -> str:
    """Logs an HTTP request.

    Args:
        log_data: JSON string containing the log data.
    """
    api_key = os.environ.get("KONG_GATEWAY_KEY")
    headers = {"X-Api-Key": api_key, "Content-Type": "application/json"}
    status_code, response_text = await make_request("POST", f"{BASE_URL}/api/v1/kong/http-log", headers=headers, json=log_data)
    return f"Status: {status_code}, Response: {response_text}"


@mcp.tool()
async def testGatewayConnection(connection_details: str) -> str:
    """Tests a gateway connection.

    Args:
        connection_details: JSON string containing the connection details.
    """
    api_key = os.environ.get("KONG_GATEWAY_KEY")
    headers = {"X-Api-Key": api_key, "Content-Type": "application/json"}
    status_code, response_text = await make_request("POST", f"{BASE_URL}/api/v1/gateway/connections/test", headers=headers, json=connection_details)
    return f"Status: {status_code}, Response: {response_text}"


@mcp.tool()
async def deleteGatewayConnectionInstance(connection_details: str) -> str:
    """Deletes a gateway connection instance.

    Args:
        connection_details: JSON string containing the details of the connection to delete.
    """
    api_key = os.environ.get("KONG_GATEWAY_KEY")
    headers = {"X-Api-Key": api_key, "Content-Type": "application/json"}
    status_code, response_text = await make_request("POST", f"{BASE_URL}/api/v1/gateway/connections/delete", headers=headers, json=connection_details)
    return f"Status: {status_code}, Response: {response_text}"


@mcp.tool()
async def registerWebTrafficInAnalyticsEngine(traffic_data: str) -> str:
    """Registers web traffic in the analytics engine.

    Args:
        traffic_data: JSON string containing the web traffic data.
    """
    api_key = os.environ.get("KONG_GATEWAY_KEY")
    headers = {"X-Api-Key": api_key, "Content-Type": "application/json"}
    status_code, response_text = await make_request("POST", f"{BASE_URL}/api/v1/analytics/web-traffic", headers=headers, json=traffic_data)
    return f"Status: {status_code}, Response: {response_text}"


@mcp.tool()
async def registerUserActivityInAnalyticsEngine(activity_data: str) -> str:
    """Registers user activity in the analytics engine.

    Args:
        activity_data: JSON string containing the user activity data.
    """
    api_key = os.environ.get("KONG_GATEWAY_KEY")
    headers = {"X-Api-Key": api_key, "Content-Type": "application/json"}
    status_code, response_text = await make_request("POST", f"{BASE_URL}/api/v1/analytics/user-activity", headers=headers, json=activity_data)
    return f"Status: {status_code}, Response: {response_text}"


@mcp.tool()
async def exportSubscriptionActivityInAnalyticsEngine(subscription_data: str) -> str:
    """Exports subscription activity to the analytics engine.

    Args:
        subscription_data: JSON string containing the subscription activity data.
    """
    api_key = os.environ.get("KONG_GATEWAY_KEY")
    headers = {"X-Api-Key": api_key, "Content-Type": "application/json"}
    status_code, response_text = await make_request("POST", f"{BASE_URL}/api/v1/analytics/subscription", headers=headers, json=subscription_data)
    return f"Status: {status_code}, Response: {response_text}"


@mcp.tool()
async def getAllRegionsAndCountries() -> str:
    """Retrieves all regions and countries.

    Args:
        None
    """
    api_key = os.environ.get("KONG_GATEWAY_KEY")
    headers = {"X-Api-Key": api_key}
    status_code, response_text = await make_request("GET", f"{BASE_URL}/api/v1/gateway/regions-and-countries", headers=headers)
    return f"Status: {status_code}, Response: {response_text}"


@mcp.tool()
async def getAllGatewayConnectionTypes() -> str:
    """Retrieves all gateway connection types.

    Args:
        None
    """
    api_key = os.environ.get("KONG_GATEWAY_KEY")
    headers = {"X-Api-Key": api_key}
    status_code, response_text = await make_request("GET", f"{BASE_URL}/api/v1/gateway/metadata/connection-types", headers=headers)
    return f"Status: {status_code}, Response: {response_text}"


@mcp.tool()
async def getGatewayConnectionInstance(id: str) -> str:
    """Retrieves a specific gateway connection instance by ID.

    Args:
        id: The ID of the gateway connection instance to retrieve.
    """
    api_key = os.environ.get("KONG_GATEWAY_KEY")
    headers = {"X-Api-Key": api_key}
    status_code, response_text = await make_request("GET", f"{BASE_URL}/api/v1/gateway/connections/{id}", headers=headers)
    return f"Status: {status_code}, Response: {response_text}"


if __name__ == "__main__":
    mcp.run(transport="stdio")

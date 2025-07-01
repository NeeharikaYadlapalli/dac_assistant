
import asyncio
import os
import json
import aiohttp
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
load_dotenv()

mcp = FastMCP("user_management")
BASE_URL = "https://kong-admin-api-preprod.dsh.digitalapicraft.com"

@mcp.tool()
async def updateUserInfo(user_id: str, data: str) -> str:
    """Updates user information.

    Args:
        user_id: The ID of the user to update.
        data: JSON string containing the user data to update.
    """
    url = f"{BASE_URL}/api/v1/users"
    headers = {"Content-Type": "application/json", "x-api-key": os.environ.get("USER_MANAGEMENT_KEY")}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.put(url, headers=headers, data=data) as response:
                response_data = await response.text()
                return f"Update User Info Response: {response.status} - {response_data}"
    except Exception as e:
        return f"Error updating user info: {e}"

@mcp.tool()
async def removeUserFavourite(user_id: str, favourite_id: str) -> str:
    """Removes a user's favourite.

    Args:
        user_id: The ID of the user.
        favourite_id: The ID of the favourite to remove.
    """
    url = f"{BASE_URL}/api/v1/users/favourites/remove"
    headers = {"Content-Type": "application/json", "x-api-key": os.environ.get("USER_MANAGEMENT_KEY")}
    payload = json.dumps({"user_id": user_id, "favourite_id": favourite_id})
    try:
        async with aiohttp.ClientSession() as session:
            async with session.put(url, headers=headers, data=payload) as response:
                response_data = await response.text()
                return f"Remove User Favourite Response: {response.status} - {response_data}"
    except Exception as e:
        return f"Error removing user favourite: {e}"

@mcp.tool()
async def addUserFavourite(user_id: str, favourite_id: str) -> str:
    """Adds a user's favourite.

    Args:
        user_id: The ID of the user.
        favourite_id: The ID of the favourite to add.
    """
    url = f"{BASE_URL}/api/v1/users/favourites/add"
    headers = {"Content-Type": "application/json", "x-api-key": os.environ.get("USER_MANAGEMENT_KEY")}
    payload = json.dumps({"user_id": user_id, "favourite_id": favourite_id})
    try:
        async with aiohttp.ClientSession() as session:
            async with session.put(url, headers=headers, data=payload) as response:
                response_data = await response.text()
                return f"Add User Favourite Response: {response.status} - {response_data}"
    except Exception as e:
        return f"Error adding user favourite: {e}"

@mcp.tool()
async def updateUserWithCompactData(user_id: str, data: str) -> str:
    """Updates a user with compact data.

    Args:
        user_id: The ID of the user to update.
        data: JSON string containing the compact user data.
    """
    url = f"{BASE_URL}/api/v1/users/compact"
    headers = {"Content-Type": "application/json", "x-api-key": os.environ.get("USER_MANAGEMENT_KEY")}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.put(url, headers=headers, data=data) as response:
                response_data = await response.text()
                return f"Update User With Compact Data Response: {response.status} - {response_data}"
    except Exception as e:
        return f"Error updating user with compact data: {e}"

@mcp.tool()
async def onboardUser(data: str) -> str:
    """Onboards a user.

    Args:
        data: JSON string containing the user onboarding data.
    """
    url = f"{BASE_URL}/api/v1/onboarding/users"
    headers = {"Content-Type": "application/json", "x-api-key": os.environ.get("USER_MANAGEMENT_KEY")}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.put(url, headers=headers, data=data) as response:
                response_data = await response.text()
                return f"Onboard User Response: {response.status} - {response_data}"
    except Exception as e:
        return f"Error onboarding user: {e}"

@mcp.tool()
async def userRevokesTermsAndConditionsAcceptance(user_id: str) -> str:
    """Revokes a user's acceptance of terms and conditions.

    Args:
        user_id: The ID of the user.
    """
    url = f"{BASE_URL}/api/v1/onboarding/users/consent/revoke"
    headers = {"Content-Type": "application/json", "x-api-key": os.environ.get("USER_MANAGEMENT_KEY")}
    payload = json.dumps({"user_id": user_id})
    try:
        async with aiohttp.ClientSession() as session:
            async with session.put(url, headers=headers, data=payload) as response:
                response_data = await response.text()
                return f"User Revokes Terms Response: {response.status} - {response_data}"
    except Exception as e:
        return f"Error revoking terms acceptance: {e}"

@mcp.tool()
async def validateToken(token: str) -> str:
    """Validates a token.

    Args:
        token: The token to validate.
    """
    url = f"{BASE_URL}/api/v1/onboarding/tokens"
    headers = {"Content-Type": "application/json", "x-api-key": os.environ.get("USER_MANAGEMENT_KEY")}
    payload = json.dumps({"token": token})
    try:
        async with aiohttp.ClientSession() as session:
            async with session.put(url, headers=headers, data=payload) as response:
                response_data = await response.text()
                return f"Validate Token Response: {response.status} - {response_data}"
    except Exception as e:
        return f"Error validating token: {e}"

@mcp.tool()
async def validateUserToken(token: str, user_id: str) -> str:
    """Validates a user token.

    Args:
        token: The token to validate.
        user_id: The ID of the user.
    """
    url = f"{BASE_URL}/api/v1/onboarding/tokens/users/validate"
    headers = {"Content-Type": "application/json", "x-api-key": os.environ.get("USER_MANAGEMENT_KEY")}
    payload = json.dumps({"token": token, "user_id": user_id})
    try:
        async with aiohttp.ClientSession() as session:
            async with session.put(url, headers=headers, data=payload) as response:
                response_data = await response.text()
                return f"Validate User Token Response: {response.status} - {response_data}"
    except Exception as e:
        return f"Error validating user token: {e}"

@mcp.tool()
async def signupExternalUser(data: str) -> str:
    """Signs up an external user.

    Args:
        data: JSON string containing the user signup data.
    """
    url = f"{BASE_URL}/api/v1/users/signup/external"
    headers = {"Content-Type": "application/json", "x-api-key": os.environ.get("USER_MANAGEMENT_KEY")}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=data) as response:
                response_data = await response.text()
                return f"Signup External User Response: {response.status} - {response_data}"
    except Exception as e:
        return f"Error signing up external user: {e}"

@mcp.tool()
async def getUsersByGreedySearch(search_term: str) -> str:
    """Gets users by greedy search.

    Args:
        search_term: The search term.
    """
    url = f"{BASE_URL}/api/v1/users/greedySearch"
    headers = {"Content-Type": "application/json", "x-api-key": os.environ.get("USER_MANAGEMENT_KEY")}
    payload = json.dumps({"search_term": search_term})
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=payload) as response:
                response_data = await response.text()
                return f"Get Users By Greedy Search Response: {response.status} - {response_data}"
    except Exception as e:
        return f"Error getting users by greedy search: {e}"

@mcp.tool()
async def getPagedAnaltyicsUsers(page: int, page_size: int) -> str:
    """Gets paged analytics users.

    Args:
        page: The page number.
        page_size: The page size.
    """
    url = f"{BASE_URL}/api/v1/users/analytics/page"
    headers = {"Content-Type": "application/json", "x-api-key": os.environ.get("USER_MANAGEMENT_KEY")}
    payload = json.dumps({"page": page, "page_size": page_size})
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=payload) as response:
                response_data = await response.text()
                return f"Get Paged Analytics Users Response: {response.status} - {response_data}"
    except Exception as e:
        return f"Error getting paged analytics users: {e}"

@mcp.tool()
async def requestAnalyticsUserAction(user_id: str, action: str) -> str:
    """Requests an analytics user action.

    Args:
        user_id: The ID of the user.
        action: The action to request.
    """
    url = f"{BASE_URL}/api/v1/users/analytics/access/action"
    headers = {"Content-Type": "application/json", "x-api-key": os.environ.get("USER_MANAGEMENT_KEY")}
    payload = json.dumps({"user_id": user_id, "action": action})
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=payload) as response:
                response_data = await response.text()
                return f"Request Analytics User Action Response: {response.status} - {response_data}"
    except Exception as e:
        return f"Error requesting analytics user action: {e}"

@mcp.tool()
async def getUserCompactView(user_id: str) -> str:
    """Gets a user's compact view.

    Args:
        user_id: The ID of the user.
    """
    url = f"{BASE_URL}/api/v1/user-compact-view"
    headers = {"Content-Type": "application/json", "x-api-key": os.environ.get("USER_MANAGEMENT_KEY")}
    payload = json.dumps({"user_id": user_id})
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=payload) as response:
                response_data = await response.text()
                return f"Get User Compact View Response: {response.status} - {response_data}"
    except Exception as e:
        return f"Error getting user compact view: {e}"

@mcp.tool()
async def getAllUsersPage(page: int, page_size: int) -> str:
    """Gets all users on a page.

    Args:
        page: The page number.
        page_size: The page size.
    """
    url = f"{BASE_URL}/api/v1/registered-users/page"
    headers = {"Content-Type": "application/json", "x-api-key": os.environ.get("USER_MANAGEMENT_KEY")}
    payload = json.dumps({"page": page, "page_size": page_size})
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=payload) as response:
                response_data = await response.text()
                return f"Get All Users Page Response: {response.status} - {response_data}"
    except Exception as e:
        return f"Error getting all users page: {e}"

@mcp.tool()
async def deleteUser(user_id: str) -> str:
    """Deletes a user.

    Args:
        user_id: The ID of the user to delete.
    """
    url = f"{BASE_URL}/api/v1/registered-users/delete"
    headers = {"Content-Type": "application/json", "x-api-key": os.environ.get("USER_MANAGEMENT_KEY")}
    payload = json.dumps({"user_id": user_id})
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=payload) as response:
                response_data = await response.text()
                return f"Delete User Response: {response.status} - {response_data}"
    except Exception as e:
        return f"Error deleting user: {e}"

@mcp.tool()
async def getStatusOfInvitedUsers(emails: str) -> str:
    """Gets the status of invited users.

    Args:
        emails: JSON string array of email addresses.
    """
    url = f"{BASE_URL}/api/v1/onboarding/users/pending-invitations"
    headers = {"Content-Type": "application/json", "x-api-key": os.environ.get("USER_MANAGEMENT_KEY")}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=emails) as response:
                response_data = await response.text()
                return f"Get Status Of Invited Users Response: {response.status} - {response_data}"
    except Exception as e:
        return f"Error getting status of invited users: {e}"

@mcp.tool()
async def sendUserInvitationRejectionEmailToAdmin(email: str) -> str:
    """Sends a user invitation rejection email to the admin.

    Args:
        email: The email address of the user who rejected the invitation.
    """
    url = f"{BASE_URL}/api/v1/onboarding/users/declines-invitation"
    headers = {"Content-Type": "application/json", "x-api-key": os.environ.get("USER_MANAGEMENT_KEY")}
    payload = json.dumps({"email": email})
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=payload) as response:
                response_data = await response.text()
                return f"Send User Invitation Rejection Email Response: {response.status} - {response_data}"
    except Exception as e:
        return f"Error sending user invitation rejection email: {e}"

@mcp.tool()
async def retrieveAllUsersForAPartnerOrganisation(partner_organisation_id: str, page: int, page_size: int) -> str:
    """Retrieves all users for a partner organisation.

    Args:
        partner_organisation_id: The ID of the partner organisation.
        page: The page number.
        page_size: The page size.
    """
    url = f"{BASE_URL}/api/v1/onboarding/users-by-partner-organisations"
    headers = {"Content-Type": "application/json", "x-api-key": os.environ.get("USER_MANAGEMENT_KEY")}
    payload = json.dumps({"partner_organisation_id": partner_organisation_id, "page": page, "page_size": page_size})
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=payload) as response:
                response_data = await response.text()
                return f"Retrieve All Users For Partner Organisation Response: {response.status} - {response_data}"
    except Exception as e:
        return f"Error retrieving all users for partner organisation: {e}"

@mcp.tool()
async def sendForgotPasswordEmail(email: str) -> str:
    """Sends a forgot password email.

    Args:
        email: The email address to send the forgot password email to.
    """
    url = f"{BASE_URL}/api/v1/onboarding/tokens/users/forgot-password"
    headers = {"Content-Type": "application/json", "x-api-key": os.environ.get("USER_MANAGEMENT_KEY")}
    payload = json.dumps({"email": email})
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=payload) as response:
                response_data = await response.text()
                return f"Send Forgot Password Email Response: {response.status} - {response_data}"
    except Exception as e:
        return f"Error sending forgot password email: {e}"

@mcp.tool()
async def sendUserOnboardingFirstLoginEmail(email: str) -> str:
    """Sends a user onboarding first login email.

    Args:
        email: The email address to send the onboarding email to.
    """
    url = f"{BASE_URL}/api/v1/onboarding/tokens/users/first-login"
    headers = {"Content-Type": "application/json", "x-api-key": os.environ.get("USER_MANAGEMENT_KEY")}
    payload = json.dumps({"email": email})
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=payload) as response:
                response_data = await response.text()
                return f"Send User Onboarding First Login Email Response: {response.status} - {response_data}"
    except Exception as e:
        return f"Error sending user onboarding first login email: {e}"

@mcp.tool()
async def sendUserOnboardingFirstLoginBulkEmails(emails: str) -> str:
    """Sends user onboarding first login emails in bulk.

    Args:
        emails: JSON string array of email addresses.
    """
    url = f"{BASE_URL}/api/v1/onboarding/tokens/users/first-login/bulk"
    headers = {"Content-Type": "application/json", "x-api-key": os.environ.get("USER_MANAGEMENT_KEY")}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=emails) as response:
                response_data = await response.text()
                return f"Send User Onboarding First Login Bulk Emails Response: {response.status} - {response_data}"
    except Exception as e:
        return f"Error sending user onboarding first login bulk emails: {e}"

@mcp.tool()
async def validateExternalSignupToken(token: str) -> str:
    """Validates an external signup token.

    Args:
        token: The token to validate.
    """
    url = f"{BASE_URL}/api/v1/onboarding/tokens/users/external/signup/validate"
    headers = {"Content-Type": "application/json", "x-api-key": os.environ.get("USER_MANAGEMENT_KEY")}
    payload = json.dumps({"token": token})
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=payload) as response:
                response_data = await response.text()
                return f"Validate External Signup Token Response: {response.status} - {response_data}"
    except Exception as e:
        return f"Error validating external signup token: {e}"

@mcp.tool()
async def retrieveAPageOfPartnerOrganisations(page: int, page_size: int) -> str:
    """Retrieves a page of partner organisations.

    Args:
        page: The page number.
        page_size: The page size.
    """
    url = f"{BASE_URL}/api/v1/onboarding/partner-organisations"
    headers = {"Content-Type": "application/json", "x-api-key": os.environ.get("USER_MANAGEMENT_KEY")}
    payload = json.dumps({"page": page, "page_size": page_size})
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=payload) as response:
                response_data = await response.text()
                return f"Retrieve A Page Of Partner Organisations Response: {response.status} - {response_data}"
    except Exception as e:
        return f"Error retrieving a page of partner organisations: {e}"

@mcp.tool()
async def retrievePartnerOrganisationByName(name: str) -> str:
    """Retrieves a partner organisation by name.

    Args:
        name: The name of the partner organisation.
    """
    url = f"{BASE_URL}/api/v1/onboarding/partner-organisation/name"
    headers = {"Content-Type": "application/json", "x-api-key": os.environ.get("USER_MANAGEMENT_KEY")}
    payload = json.dumps({"name": name})
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=payload) as response:
                response_data = await response.text()
                return f"Retrieve Partner Organisation By Name Response: {response.status} - {response_data}"
    except Exception as e:
        return f"Error retrieving partner organisation by name: {e}"

@mcp.tool()
async def retrievePartnerOrganisationByCompanyRegisteredId(company_registered_id: str) -> str:
    """Retrieves a partner organisation by company registered ID.

    Args:
        company_registered_id: The company registered ID.
    """
    url = f"{BASE_URL}/api/v1/onboarding/partner-organisation/company-registered-id"
    headers = {"Content-Type": "application/json", "x-api-key": os.environ.get("USER_MANAGEMENT_KEY")}
    payload = json.dumps({"company_registered_id": company_registered_id})
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=payload) as response:
                response_data = await response.text()
                return f"Retrieve Partner Organisation By Company Registered Id Response: {response.status} - {response_data}"
    except Exception as e:
        return f"Error retrieving partner organisation by company registered id: {e}"

@mcp.tool()
async def deleteUserInvitation(email: str) -> str:
    """Deletes a user invitation.

    Args:
        email: The email address of the user invitation to delete.
    """
    url = f"{BASE_URL}/api/v1/onboarding/invitations"
    headers = {"Content-Type": "application/json", "x-api-key": os.environ.get("USER_MANAGEMENT_KEY")}
    payload = json.dumps({"email": email})
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=payload) as response:
                response_data = await response.text()
                return f"Delete User Invitation Response: {response.status} - {response_data}"
    except Exception as e:
        return f"Error deleting user invitation: {e}"

@mcp.tool()
async def getUserCompactModelForAllRegisteredUsers() -> str:
    """Gets the compact user model for all registered users."""
    url = f"{BASE_URL}/api/v1/registered-users"
    headers = {"Content-Type": "application/json", "x-api-key": os.environ.get("USER_MANAGEMENT_KEY")}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response_data = await response.text()
                return f"Get User Compact Model For All Registered Users Response: {response.status} - {response_data}"
    except Exception as e:
        return f"Error getting user compact model for all registered users: {e}"

@mcp.tool()
async def deleteTokenById(id: str) -> str:
    """Deletes a token by ID.

    Args:
        id: The ID of the token to delete.
    """
    url = f"{BASE_URL}/api/v1/onboarding/users/tokens/{id}"
    headers = {"Content-Type": "application/json", "x-api-key": os.environ.get("USER_MANAGEMENT_KEY")}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.delete(url, headers=headers) as response:
                response_data = await response.text()
                return f"Delete Token By Id Response: {response.status} - {response_data}"
    except Exception as e:
        return f"Error deleting token by id: {e}"

if __name__ == "__main__":
    mcp.run(transport="stdio")

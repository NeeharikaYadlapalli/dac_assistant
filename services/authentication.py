import os

from dotenv import load_dotenv

load_dotenv()
from schemas.authentication import GetApiKey
import requests
def authenticate_tool(user_credentials: GetApiKey):
    """
    Authenticates a user by fetching an API key using their credentials.

    Args:
        user_credentials (GetApiKey): An object containing the user's email ID and versioned content ID.

    Returns:
        str: The API key associated with the user's credentials, or None if not found.

    Environment Variables:
        FETCH_CRED_API_KEY: The API key used to authenticate the request to the external service.

    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
        KeyError: If the expected keys are not found in the response JSON.

    """


    FETCH_CRED_API_KEY = os.environ.get("FETCH_CRED_API_KEY")
    url = "https://kong-admin-api-preprod.dsh.digitalapicraft.com/api/v1/digital-content/apis/fetch-credentials"
    headers = {
        "accept": "application/json, text/plain, */*",
        "apikey": FETCH_CRED_API_KEY,
        "content-type": "application/json"
    }
    data = {
        "emailId": user_credentials.email_id,
        "apiVersionedContentId": user_credentials.versioned_content_id
    }
    response = requests.post(url, headers=headers, json=data)
    response_json = response.json()
    print(response_json)
    if response_json.get('data') is None:
        return None
    api_key = response_json.get('data', {}).get('productCredentials', [])[0].get('clientId', None)
    return api_key

# # Sample user credentials
# user_credentials = GetApiKey(
#     email_id="mansoor.b@digitalapicraft.com",
#     versioned_content_id="680a4532760a4702bcdcdea7"
# )
#
# # Call the authenticate function
# api_key = authenticate(user_credentials)
#
# # Print the result
# print("API Key:", api_key)
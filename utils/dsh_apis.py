import os
import requests
from dotenv import load_dotenv
from schemas.dsh import ApiDetails
load_dotenv()

ADMIN_API_URL = os.environ.get("ADMIN_API_URL")
def get_api_details(versioned_content_id: str, digital_content_id: str):
    """"""

    url = f"{ADMIN_API_URL}/api/v1/digital-content/detail?digitalContentId={digital_content_id}&versionedContentId={versioned_content_id}"
    apikey =os.environ.get("DIGITAL_CONTENT_API_KEY")
    headers = {"Content-Type": "application/json", "apikey": apikey}

    api_response = requests.get(url, headers=headers)
    digital_content_details = api_response.json()

    if digital_content_details.get('data') is None:
        api_name = None
        content_type = None
    else:
        api_name = digital_content_details.get("data", {}).get("digitalContentModel", {}).get("name", None)
        content_type = digital_content_details.get("data", {}).get("digitalContentModel", {}).get("contentType", None)
    auth_flag = True
    api_details = ApiDetails(
        digital_content_id=digital_content_id,
        versioned_content_id=versioned_content_id,
        auth_flag=auth_flag,
        api_name=api_name,
        content_type=content_type
    )

    return api_details
# ApiDetails()

def get_user_subscription_details(user_id: str, versioned_content_id: str):
    """"""
    FETCH_CRED_API_KEY = os.environ.get("DIGITAL_CONTENT_API_KEY")
    url = f"{ADMIN_API_URL}/api/v1/digital-content/apis/fetch-credentials"
    headers = {
        "accept": "application/json, text/plain, */*",
        "apikey": FETCH_CRED_API_KEY,
        "content-type": "application/json"
    }
    data = {
        "emailId": user_id,
        "apiVersionedContentId": versioned_content_id
    }
    response = requests.post(url, headers=headers, json=data)
    response_json = response.json()
    # print(response_json)
    if response_json.get('data') is None:
        return None
    api_key = response_json.get('data', {}).get('productCredentials', [])[0].get('clientId', None)
    return api_key


# get_api_details(digital_content_id="67ee58c548930c2ef15bedb8", versioned_content_id="67ee58c548930c2ef15bedb9")
# api_key = get_user_subscription_details(user_id="mansoor.b@digitalapicraft.com", versioned_content_id="67ee58c548930c2ef15bedb9")
# print(api_key)
#
# get_api_details(digital_content_id="681dcc59df8c3b27225caf4c", versioned_content_id="681dcc58df8c3b27225caf4b")
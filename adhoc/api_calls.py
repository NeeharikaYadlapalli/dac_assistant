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

print(get_api_details(versioned_content_id="685a61f6b88d137b3e6bea94", digital_content_id="685a61f4b88d137b3e6bea93"))

import requests

# Define the API endpoint
url = "http://127.0.0.1:8000/query"
cloudrun_url = "https://dac-mcp-client-preprod-1019068528267.europe-west4.run.app/query"
dev_cloudrun_url ="https://dac-mcp-client-dev-preprod-1019068528267.europe-west4.run.app/query"
# Define headers (e.g., for authentication)
headers = {
    "Content-Type": "application/json",
"email":"mansoor.b@digitalapicraft.com",
"session_id":"ejfdwfdwfwqrfefvekhndevce894fd8gfbrhj4cb",
}


payload = {"message": input("Type your question here: "), "consent": True}

# # Send a GET request
try:
    response = requests.post(dev_cloudrun_url, headers=headers, json=payload)
    response.raise_for_status()  # Raise an exception for HTTP errors
    data = response.json()  # Parse the JSON response
    print("Response Data:", data)
except requests.exceptions.RequestException as e:
    print(f"API request failed: {e}")

# with requests.post(url, headers=headers, json=payload, stream=True) as response:
#     response.raise_for_status()  # Raise an exception for HTTP errors
#     for chunk in response.iter_content(chunk_size=8192):
#         if chunk:  # Filter out keep-alive chunks
#             print(chunk.decode('utf-8'))

#
# import requests
# from dotenv import load_dotenv
# load_dotenv()
# # Define the API endpoint
# url = "http://127.0.0.1:8000/query"
#
# import os
# BASE_URL = "https://kong-admin-api-preprod.dsh.digitalapicraft.com"
#
# API_KEY = os.environ.get("SSO_PROFILES_KEY")
# # API_KEY = "B4253A7A-E78C-4923-A0A3-3E10B9847724"
#
# print(API_KEY)
#
# # Define headers (e.g., for authentication)
# headers = {"apikey": API_KEY}
#
# # Send a GET request
# try:
#     response = requests.get(f"{BASE_URL}/api/v1/sso/profiles", headers=headers)
#     response.raise_for_status()  # Raise an exception for HTTP errors
#     data = response.json()  # Parse the JSON response
#     print("Response Data:", data)
# except requests.exceptions.RequestException as e:
#     print(f"API request failed: {e}")
#

#
#     async with aiohttp.ClientSession() as session:
#         try:
#             async with session.get(f"{BASE_URL}/api/v1/sso/profiles", headers=headers) as response:
#                 response.raise_for_status()
#                 data = await response.json()
#
#                 return json.dumps(data, indent=2)
#         except aiohttp.ClientError as e:
#             return f"Error: {e}"
#
#
#
# create an api call

#            --vpc-connector=projects/apimanager-12/locations/europe-west4/connectors/apimanager-vpc-connector
#            --vpc-egress=all-traffic


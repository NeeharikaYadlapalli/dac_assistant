import requests

url = "http://127.0.0.1:8000/delete_server"
cloudrun_url = "https://dac-mcp-client-preprod-1019068528267.europe-west4.run.app/delete_server"
# Define headers (e.g., for authentication)
headers = {
    "Content-Type": "application/json"
}
payload = {"server_name":"Finance Asset Physical_server.py"}

# Send a GET request
try:
    response = requests.delete(cloudrun_url, headers=headers, json=payload)
    response.raise_for_status()  # Raise an exception for HTTP errors
    data = response.json()  # Parse the JSON response
    print("Response Data:", data)
except requests.exceptions.RequestException as e:
    print(f"API request failed: {e}")


# import requests
#
# url = "http://127.0.0.1:8000/list_servers"
# # cloudrun_url = "https://dac-mcp-client-preprod-1019068528267.europe-west4.run.app/query"
# # Define headers (e.g., for authentication)
# headers = {
#     "Content-Type": "application/json"
# }
# payload = {}
#
# # Send a GET request
# try:
#     response = requests.get(url, headers=headers, json=payload)
#     response.raise_for_status()  # Raise an exception for HTTP errors
#     data = response.json()  # Parse the JSON response
#     print("Response Data:", data)
# except requests.exceptions.RequestException as e:
#     print(f"API request failed: {e}")
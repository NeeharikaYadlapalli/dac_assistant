# Project Overview

This project is a Python-based asynchronous API server that provides various tools and functionalities for managing AI tools, organisation settings, and related operations. It uses the `FastMCP` framework for defining tools and `aiohttp` for making asynchronous HTTP requests.

## Project Structure

The project consists of the following key files:

### 1. `services/mcp_client.py`
This file contains the logic for interacting with an LLM (Language Model) and managing tool calls. It includes error handling, cleanup operations, and the orchestration of LLM calls.

#### Functions:
- **`make_llm_call`**: Makes a call to the LLM with the provided messages and tools.
- **`cleanup`**: Cleans up asynchronous resources and closes active sessions.

---

### 2. `generated_servers/ai-apis_server.py`
This file defines tools for interacting with AI-related APIs. It includes functions for retrieving user searches, performing searches, retrieving SDK source code, generating documentation, and managing API affinity.

#### Functions:
- **`make_request`**: A utility function for making asynchronous HTTP requests.
- **`retrieveUserSearchesByLoggedInUser`**: Retrieves search history for a specific user.
- **`search`**: Performs a search query with a specified limit.
- **`retrieveSdkSourceForLanguage`**: Retrieves SDK source code for a given language and SDK name.
- **`retrieveAutoDocumentation`**: Retrieves auto-generated documentation for an API endpoint.
- **`getApiAffinity`**: Retrieves API affinity for a given endpoint and user.
- **`refreshCacheAndGetApiAffinity`**: Refreshes the cache and retrieves API affinity.
- **`retrieveAllGlobalSearches`**: Retrieves all global searches.
- **`invalidateEntireApiAffinityCache`**: Invalidates the entire API affinity cache.

---

### 3. `generated_servers/settings-apis_server.py`
This file defines tools for managing organisation settings, such as UI customisation, roles, and content types. It also includes functions for sending support emails and retrieving API versions.

#### Functions:
- **`make_request`**: A utility function for making asynchronous HTTP requests.
- **`getUiCustomisationSettings`**: Retrieves UI customisation settings.
- **`updateUiCustomisationSettings`**: Updates UI customisation settings.
- **`primeDefaultUiCustomisationSettings`**: Primes default UI customisation settings.
- **`updateActiveUiCustomisationSettings`**: Updates active UI customisation settings.
- **`findOrganisationSettingByOrganisationId`**: Finds organisation settings by organisation ID.
- **`createOrUpdateOrgSettings`**: Creates or updates organisation settings.
- **`sendBasicSupportEmail`**: Sends a basic support email.
- **`getAllVisibilities`**: Retrieves all visibilities.
- **`extractUserCreditsFromOrganisation`**: Extracts user credits from an organisation.
- **`retrievePubliclyEnabledPortals`**: Retrieves publicly enabled portals.
- **`getAllRoles`**: Retrieves all roles.
- **`getAllSupportedContentTypes`**: Retrieves all supported content types.
- **`getAppVersion`**: Retrieves the API version.

---

## Key Technologies Used

- **Python**: The primary programming language.
- **aiohttp**: For making asynchronous HTTP requests.
- **FastMCP**: A framework for defining and running tools.
- **dotenv**: For managing environment variables.
- **Logging**: For debugging and monitoring.

## How to Run

1. Install the required dependencies using `pip install -r requirements.txt`.
2. Set up the environment variables in a `.env` file.
3. Run the servers using the following commands:
   - For AI APIs: `python generated_servers/ai-apis_server.py`
   - For Organisation Settings: `python generated_servers/settings-apis_server.py`

## Environment Variables

- `AI_TOOLS_KEY`: API key for AI tools.
- `ORGANISATION_SETTINGS_KEY`: API key for organisation settings.

## Notes

- Ensure that the `BASE_URL` values in the files point to the correct API endpoints.
- The project uses asynchronous programming, so all functions are `async` and should be awaited when called.
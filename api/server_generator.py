# from fastapi import APIRouter, HTTPException, UploadFile, File
# from fastapi.responses import JSONResponse
# from schemas.servers import ServerCreate
# from services.server_generator import generate_mcp_server_from_upload
# from api.mcp_client import startup_event
#
# router = APIRouter()
#
# @router.post("/generate_server")
# async def create(file: ServerCreate):
#     """
#     Endpoint to generate an MCP server from the uploaded file.
#
#     Args:
#         file (ServerCreate): The file containing the server configuration.
#
#     Returns:
#         JSONResponse: Response with the server creation status and data.
#     """
#     # try:
#     # Ensure the server generation function is asynchronous
#     data = await generate_mcp_server_from_upload(file)
#     response = {
#         "data": data,
#         "message": "Server has been created successfully"
#     }
#
#     # Call the startup event if necessary
#     # except Exception as e:
#     #     # Handle exceptions and return a 500 error response
#     #     return JSONResponse(
#     #         status_code=500,
#     #         content={"status": "error", "message": str(e)}
#     #     )
#     # Return a success response
#     return JSONResponse(content=response, status_code=201)
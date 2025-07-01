import os

from dotenv import load_dotenv
from fastapi import FastAPI
from api import server_generator
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import server_generator,mcp_client,server_management
from services.mcp_client import MCPClient
import os
# from api.mcp_client import startup_event
from pydantic import BaseModel
load_dotenv()
BUCKET_NAME = os.environ.get("SERVER_BUCKET_NAME")


app = FastAPI()
#
# app.include_router(server_generator.router, prefix="/servers", tags=["Servers"])
class ServerName(BaseModel):
    server_name: str


# CORS setup
origins = ["http://localhost:4200", "*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
# app.include_router(server_generator.router, prefix="/servers")
app.include_router(mcp_client.router, tags=["MCP"])
app.include_router(server_management.router, tags=["Server Management"])




# @app.on_event("startup")
# async def startup_event_wrapper():
#     await startup_event(app)

BUCKET_NAME = os.environ.get("SERVER_BUCKET_NAME")
@app.on_event("startup")
async def startup_event():
    app.state.mcp_client = MCPClient()
    await app.state.mcp_client.connect_to_servers_from_directory(bucket_name=BUCKET_NAME)


@app.on_event("shutdown")
async def shutdown_event():
    await app.state.mcp_client.cleanup()


from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from schemas.servers import ServerCreate
from services.server_generator import generate_mcp_server_from_upload
# from api.mcp_client import startup_event

router = APIRouter()


@app.post("/generate_server")
async def create(file: ServerCreate):
    """
    Endpoint to generate an MCP server from the uploaded file.

    Args:
        file (ServerCreate): The file containing the server configuration.

    Returns:
        JSONResponse: Response with the server creation status and data.
    """
    # try:
    # Ensure the server generation function is asynchronous
    data = await generate_mcp_server_from_upload(file)
    response = {
        "data": data,
        "message": "Server has been created successfully"
    }
    # startup_event()
    created, error = await app.state.mcp_client.connect_to_server(server_script_path=data)

    if created:
        response["status"] = "success"



    # Call the startup event if necessary
    # except Exception as e:
    #     # Handle exceptions and return a 500 error response
    #     return JSONResponse(
    #         status_code=500,
    #         content={"status": "error", "message": str(e)}
    #     )
    # Return a success response
        return JSONResponse(content=response, status_code=201)
    else:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": error}
        )

@app.delete("/delete_server")
async def delete_server(server:ServerName):
    """Deletes a server"""
    # try:
    result = await app.state.mcp_client.delete_server(server.server_name)
    await app.state.mcp_client.connect_to_servers_from_directory(bucket_name=BUCKET_NAME)
    return {"data": None, "message": "Server deleted successfully"}
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:api", host="0.0.0.0", port=5005, reload=True)

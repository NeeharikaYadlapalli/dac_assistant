from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from services.server_management import list_gcs_modules
import os

router = APIRouter()

# class ListServers(BaseModel):
#     message: str

@router.get("/list_servers")
async def list_servers():
    """Lists all servers"""
    # try:
    servers = list_gcs_modules()
    return {"data":{"servers":servers},"message":"List of servers"}
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))







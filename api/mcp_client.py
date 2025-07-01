from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from services.mcp_client import MCPClient
import os

router = APIRouter()

class QueryInput(BaseModel):
    message: str
    consent:bool | None = None

@router.post("/query")
async def handle_query(input: QueryInput, request: Request):

    mcp_client = request.app.state.mcp_client
    headers = request.headers
    email = headers.get("email", None)
    session_id = headers.get("session_id", None)
    consent = input.consent

    result = await mcp_client.process_query(input.message, email=email, consent=consent, session_id=session_id)
    return result
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))




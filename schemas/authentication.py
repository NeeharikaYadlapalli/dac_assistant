from pydantic import BaseModel
from fastapi import UploadFile

class GetApiKey(BaseModel):
    email_id: str
    versioned_content_id: str
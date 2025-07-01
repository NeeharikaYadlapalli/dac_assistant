from pydantic import BaseModel
from fastapi import UploadFile

class ServerCreate(BaseModel):
    file_content: str
    file_name: str
    versionedContentId: str | None = None
    digitalContentId: str | None = None

class ToolCallResponse(BaseModel):
    response: str
    action: str | None = None
    versioned_content_id: str | None = None
    digital_content_id: str | None = None

class Source(BaseModel):
    source_url: str | None = None
    source_name: str | None = None
    data: str | None = None
    content_type: str | None = None

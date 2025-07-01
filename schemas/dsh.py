


from pydantic import BaseModel
from fastapi import UploadFile

class ApiDetails(BaseModel):
    digital_content_id: str
    versioned_content_id: str
    auth_flag: bool | None = None
    api_name: str | None = None
    content_type:str | None = None

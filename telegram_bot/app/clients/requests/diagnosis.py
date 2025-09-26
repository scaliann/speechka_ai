from typing import List

from pydantic import BaseModel


class DiagnosisRequest(BaseModel):
    mongo_object_ids: List[str]
    chat_id: int
    user_id: int

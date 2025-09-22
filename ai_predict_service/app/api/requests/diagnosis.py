from typing import List

from pydantic import BaseModel


class DiagnosisRequest(BaseModel):
    mongo_ids: List[str]
    chat_id: int

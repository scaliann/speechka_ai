from typing import List

from pydantic import BaseModel


class DiagnosisSchema(BaseModel):
    user_id: int | None = None
    chat_id: int
    mongo_object_ids: List[str]

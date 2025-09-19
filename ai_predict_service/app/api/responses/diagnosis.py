from typing import List, Dict

from pydantic import BaseModel


class DiagnosisResponse(BaseModel):
    diagnosis: str
    results: Dict[int, str]

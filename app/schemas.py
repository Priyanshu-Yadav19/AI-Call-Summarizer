from pydantic import BaseModel
from typing import Dict


class ProcessResponse(BaseModel):
    transcript: str
    summary: str
    draft: str
    latency: Dict[str, float]
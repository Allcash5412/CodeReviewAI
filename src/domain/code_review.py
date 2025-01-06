from typing import List

from pydantic import BaseModel


class CodeReview(BaseModel):
    founded_files: List[str]
    result: str

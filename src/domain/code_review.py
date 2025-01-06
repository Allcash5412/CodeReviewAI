from pydantic import BaseModel


class CodeReview(BaseModel):
    founded_files: str
    result: str

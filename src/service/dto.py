from pydantic import BaseModel


class FetchedFile(BaseModel):
    path: str
    content: str

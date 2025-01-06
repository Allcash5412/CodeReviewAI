from enum import Enum

from pydantic import BaseModel, Field


class CandidateLevel(Enum):
    junior = 'junior'
    middle = 'middle'
    senior = 'senior'

class ReviewRequest(BaseModel):
    assigment_description: str
    github_url: str = Field(pattern=r'^https:\/\/github\.com\/([\w-]+)\/([\w.-]+)(?:\.git)?$')
    candidate_level: CandidateLevel

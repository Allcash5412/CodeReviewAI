import logging
from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel, ConfigDict

from src.config import settings
from src.infrastructure.external_api.github_api import GitHubAPI
from src.api.routes.dto import ReviewRequest

logger = logging.getLogger('app')


def create_github_api() -> GitHubAPI:
    return GitHubAPI(settings.external_api.github_api_token)

GitHubApiDep = Annotated[GitHubAPI, Depends(create_github_api)]

class CreateReviewRequestDependency(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, extra='forbid')
    review_request: ReviewRequest
    github_api: GitHubApiDep

CreateReviewRequestDep = Annotated[CreateReviewRequestDependency, Depends()]

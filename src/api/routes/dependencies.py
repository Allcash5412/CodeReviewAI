import logging
from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel, ConfigDict

from src.infrastructure.external_api.ai_chat_api import AIChatAPI
from src.infrastructure.external_api.github_api import GitHubAPI

from src.api.routes.dto import ReviewRequest

from src.config import settings

logger = logging.getLogger('app')


def create_github_api() -> GitHubAPI:
    return GitHubAPI(settings.external_api.github_api_token)

GitHubAPIDep = Annotated[GitHubAPI, Depends(create_github_api)]

def create_ai_chat_api() -> AIChatAPI:
    return AIChatAPI(settings.external_api.ai_chat_api_url)

AIChatAPIDep = Annotated[AIChatAPI, Depends(create_ai_chat_api)]

class CreateReviewRequestDependency(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, extra='forbid')
    review_request: ReviewRequest
    github_api: GitHubAPIDep
    ai_chat_api: AIChatAPIDep

CreateReviewRequestDep = Annotated[CreateReviewRequestDependency, Depends()]

import logging

from fastapi import APIRouter

from src.domain.code_review import CodeReview
from src.service.create_code_review import CreateCodeReviewCommand
from src.api.routes.dependencies import CreateReviewRequestDep

review = APIRouter(prefix='/review')
logger = logging.getLogger('app')


@review.post('', response_model=CodeReview)
async def create_code_review(create_review_request_dep: CreateReviewRequestDep):
    logger.debug('def review')
    logger.debug(f'{create_review_request_dep=}')

    code_review: CodeReview = await CreateCodeReviewCommand(create_review_request_dep).execute()

    return code_review
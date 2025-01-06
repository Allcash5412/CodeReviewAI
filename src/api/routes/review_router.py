import logging

from fastapi import APIRouter


from src.domain.code_review import CodeReview
from src.service.create_code_review import CreateCodeReviewService
from src.api.routes.dependencies import CreateReviewRequestDep

review = APIRouter(prefix='/review')
logger = logging.getLogger('app')


@review.post('')
async def create_code_review(create_review_request_dep: CreateReviewRequestDep):
    logger.debug('def review')
    logger.debug(f'{create_review_request_dep =}')

    create_code_review: CreateCodeReviewService = CreateCodeReviewService(create_review_request_dep)
    code_review: CodeReview = await create_code_review.create_code_review()

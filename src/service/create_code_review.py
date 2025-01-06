import logging
import re

from fastapi import HTTPException
from typing import Tuple, Union, List

from src.service.dto import FetchedFile
from src.service.interface import ICreateCodeReviewDep, IGithubAPI, IReviewRequest, IAIChatAPI
from src.exceptions import get_exception_400_bad_request_with_detail
from src.domain.code_review import CodeReview


logger = logging.getLogger('app')

class CreateCodeReviewCommand:

    def __init__(self, create_code_review_dep: ICreateCodeReviewDep):
        self.github_api: IGithubAPI = create_code_review_dep.github_api
        self.ai_chat_api: IAIChatAPI = create_code_review_dep.ai_chat_api
        self.review_request: IReviewRequest = create_code_review_dep.review_request

    async def execute(self) -> CodeReview:
        """
            Method to getting code reviews from github repository files and analyzing AIs
            :return: CodeReview, code review with the result of the reviewed
            files and the result of the analysis.
        """
        logger.debug(f'def create_code_review')

        repository_owner, repository_name = self._extract_owner_and_repository_names()
        fetched_files: List[FetchedFile] = await self.github_api.get_repo_files(repository_owner, repository_name)

        result: str = await self.ai_chat_api.send_to_ai_chat(fetched_files, self.review_request.candidate_level)

        logger.debug(f'{result=}')

        code_review = CodeReview(founded_files=', '.join([file.path for file in fetched_files]),
                                 result=result)

        return code_review

    def _extract_owner_and_repository_names(self) -> Union[Tuple[str, str] | HTTPException]:
        """
            Method to extract owner and repository name from github url.
            :return: Return tuple of owner and repository name or HTTPException 400.
        """
        pattern = r'^https:\/\/github\.com\/([\w-]+)\/([\w.-]+)(?:\.git)?$'
        match = re.match(pattern, self.review_request.github_url)

        if match:
            match_group_first: str = match.group(1)
            match_group_second: str = match.group(2)

            if match_group_second.endswith('.git'):
                match_group_second = match_group_second[:-len('.git')]

            return match_group_first, match_group_second

        raise get_exception_400_bad_request_with_detail('Invalid GitHub URL')

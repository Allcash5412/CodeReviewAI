import re

from fastapi import HTTPException
from pprint import pprint
from typing import Tuple, Union, List

from service.dto import FetchedFile
from service.interface import IGithubAPI, IReviewRequest
from src.exceptions import get_exception_400_bad_request_with_detail
from src.domain.code_review import CodeReview
from src.service.interface import ICreateCodeReviewDep


class CreateCodeReviewService:
    def __init__(self, create_code_review_dep: ICreateCodeReviewDep):
        self.github_api: IGithubAPI = create_code_review_dep.github_api
        self.review_request: IReviewRequest = create_code_review_dep.review_request

    async def create_code_review(self) -> CodeReview:
        """
            Method to getting code reviews from github repository files and analyzing AIs
            :return: CodeReview, code review with the result of the reviewed
            files and the result of the analysis.
        """
        repository_owner, repository_name = self._extract_owner_and_repository_names()
        fetched_files: List[FetchedFile] = await self.github_api.get_repo_files(repository_owner, repository_name)

        for item in fetched_files:
            pprint(item)



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

from typing import Protocol, List, Dict
from fastapi import HTTPException

from httpx import AsyncClient

from src.service.dto import FetchedFile
from src.api.routes.dto import CandidateLevel


class IGithubAPI(Protocol):

    async def _fetch_file(self, client: AsyncClient, url: str) -> Dict:
        pass

    async def _create_fetched_file(self, client: AsyncClient, file: Dict) -> FetchedFile | HTTPException:
        pass

    async def get_repo_files(self, owner: str, repo: str) -> List[FetchedFile]:
        """
            Method to get all files from the repository including files in directories
            :param owner: str, Repository owner
            :param repo: str, Repository name
            :return: List[FetchedFile], A list of FetchedFile's each has the full path and contents of that file
        """
        pass

class IReviewRequest(Protocol):

    @property
    def assigment_description(self) -> str:
        pass

    @property
    def github_url(self) -> str:
        pass

    @property
    def candidate_level(self) -> CandidateLevel:
        pass

class ICreateCodeReviewDep(Protocol):

    @property
    def review_request(self) -> IReviewRequest:
        pass

    @property
    def github_api(self) -> IGithubAPI:
        pass

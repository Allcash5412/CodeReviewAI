import asyncio
import logging

from fastapi import HTTPException
from typing import Dict, List

from httpx import AsyncClient, HTTPStatusError

from src.exceptions import get_exception_404_not_found_with_detail
from src.service.dto import FetchedFile



logger = logging.getLogger('app')

class GitHubAPI:
    def __init__(self, token: str):
        self.token = token
        self.base_url = 'https://api.github.com'
        self.headers = {
            'Accept': 'application/vnd.github.v3+json',
            'Authorization': f'token {self.token}'
        }

    async def get_repo_files(self, owner: str, repo: str) -> List[FetchedFile]:
        """
            Method to get all files from the repository including files in directories
            :param owner: str, Repository owner
            :param repo: str, Repository name
            :return: List[FetchedFile], A list of FetchedFile's each has the full path and contents of that file
        """
        url = f'{self.base_url}/repos/{owner}/{repo}/contents'

        async with AsyncClient() as client:
            tasks = []

            async def fetch_files(api_url: str) -> None:
                """
                    The method that passes through the initial list of files, that is,
                    which were obtained by the first request further if the file is a file,
                    then it is added to the 'tasks' for the request to obtain a file if it is
                    a directory, then the function is recursively called and the algorithm
                    is repeated again until all files are retrieved further when
                    all files are obtained they are run once and the result is returned as a list of FetchedFile.
                    :param api_url: str, Repository owner
                    :return: List[FetchedFile], A list of FetchedFile's each has the full path and contents of that file
                """

                files: Dict = await self._fetch_file(client, api_url)

                for file_credentials in files:
                    if file_credentials['type'] == 'file':
                        logger.debug(f'if file_credentials["type"] == "file"')
                        logger.debug(f'{file_credentials=}')

                        tasks.append(
                            asyncio.create_task(self._create_fetched_file(client, file_credentials))
                        )

                    elif file_credentials['type'] == 'dir':
                        logger.debug(f'if file_credentials["type"] == "dir"')
                        logger.debug(f'{file_credentials['url']=}')

                        await fetch_files(file_credentials['url'])
            try:
                await fetch_files(url)
            except HTTPStatusError as e:
                raise get_exception_404_not_found_with_detail(str(e))

            fetched_files: List[FetchedFile] = await asyncio.gather(*tasks)

            logger.debug(f'Count files: {len(fetched_files)}')

            return fetched_files

    async def _fetch_file(self, client: AsyncClient, url: str) -> Dict:
        """
            Method to fetch one file
            :param client: AsyncClient, async client for async requests
            :param url: url, file url
            :return: Dict, response in json format
        """
        response = await client.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    async def _create_fetched_file(self, client: AsyncClient, file: Dict) -> FetchedFile | HTTPException:
        """
            Method to create fetched file from file
            :param client: AsyncClient,
            :param file: Dict
            :return: FetchedFile | HTTPException, fetched file or exception
        """
        try:
            item_url: str = file['download_url']
            item_path: str = file['path']

            response = await client.get(item_url, headers=self.headers)
            response.raise_for_status()

            fetched_file = FetchedFile(path=item_path, content=response.text)
            return fetched_file

        except KeyError:
            raise get_exception_404_not_found_with_detail(f'File {file["name"]} not found')

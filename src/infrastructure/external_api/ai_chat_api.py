import asyncio
import logging

from typing import Dict, List
from httpx import AsyncClient, HTTPStatusError


from src.exceptions import get_exception_400_bad_request_with_detail
from src.api.routes.dto import CandidateLevel
from src.service.dto import FetchedFile



logger = logging.getLogger('app')

class AIChatAPI:
    """
        AI Chat API - this is gpt4free
    """
    def __init__(self, ai_chat_url: str):
        self.ai_chat_url = ai_chat_url

    async def send_to_ai_chat(self, fetched_files: List[FetchedFile], level: CandidateLevel) -> str:
        tasks = []
        async with AsyncClient(timeout=30.0) as client:
            await self.send_prompt_configuration(client, level)
            tasks.extend([asyncio.create_task(self.send_file(file, client)) for file in fetched_files])


            file_responses = await asyncio.gather(*tasks)

        combined_response = "\n\n".join(file_responses)
        return combined_response

    async def send_prompt_configuration(self, client: AsyncClient, level: CandidateLevel):
        initial_payload = self._get_initial_payload(level)

        try:
            initial_response = await client.post(self.ai_chat_url,
                                                 json=initial_payload)
            initial_response.raise_for_status()
        except HTTPStatusError as e:
            raise get_exception_400_bad_request_with_detail(f"Failed to send initial prompt: {e.response.text}") from e

    async def send_file(self, file: FetchedFile, client) -> str:
        payload = {
            'model': 'gpt-4o',
            'temperature': 0.9,
            'messages': [
                {'role': 'user', 'content': file.content}
            ]
        }

        response = await client.post(self.ai_chat_url, json=payload)
        response.raise_for_status()
        response_json = response.json()
        logger.debug(f'response_json = {response_json}')

        return response.text

    def _get_initial_payload(self, level: CandidateLevel) -> Dict:
        initial_payload = {
            'model': 'gpt-4o',
            'temperature': 0.9,
            'messages': [
                {'role': 'system','content': self._get_prompt_for_candidate_level(level)},
                {'role': 'system', 'content': self._get_review_format_prompt()}
            ]
        }
        return initial_payload

    def _get_prompt_for_candidate_level(self, level: CandidateLevel) -> str:
        return f'This is a code review for a {level.value} level developer.'

    def _get_review_format_prompt(self) -> str:
        return """
                    Please format the review result in the following way:
                    Each of the Review items is allocated to a separate item with a blank line after it
                    Review:
                    - Downsides/Comments: Provide feedback with downsides or things to improve.
                    - Rating: Give a rating based on the level (Junior, Middle, Senior).
                    - Conclusion: A short conclusion summarizing the overall review.
    
                    Example:
                    Review:
    
                    [Downsides]: ....
    
                    [Comments]: ....
    
                    Rating: n/5 n - is any number by which you have evaluated the code, (for n level) - is level what i am handing over
    
                    [Conclusion]:
    
                    Make sure the review is detailed and follows this structure.
                """

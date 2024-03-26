import openai
import os

from app.config import app_config


class OpenAIClient:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("API key is not set")
        self.client = openai.Client(api_key=api_key)


openai_client = OpenAIClient(app_config.openai_api_key)

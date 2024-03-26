import openai
import os

from app.config import app_config

api_key = app_config.openai_api_key

if not api_key:
    raise ValueError("API key is not set")


openai_client = openai.Client(api_key=api_key)

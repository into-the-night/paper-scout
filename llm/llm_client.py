import openai
from typing import List
from setup.config import Config
import os
import logging

logging.getLogger("openai").setLevel(logging.ERROR)
logging.getLogger("httpx").setLevel(logging.ERROR)

class LLM:
    def __init__(self):
        # Use OpenRouter endpoint and API key
        self.api_base = "https://openrouter.ai/api/v1"
        self.api_key = Config.OPENROUTER_API_KEY
        self.model = Config.MODEL_NAME

    def generate_response(self, messages: List, tools: List = [], stream: bool = False):
        """Generate response using OpenAI/OpenRouter"""
        client = openai.OpenAI(
            api_key=self.api_key,
            base_url=self.api_base
        )
        response = client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=tools if tools else None,
            stream=stream
        )
        return response
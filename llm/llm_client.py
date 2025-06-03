import litellm
from typing import List
from setup.config import Config

class LLM:
    def __init__(self):
        self.model = "gemini/gemini-2.5-flash-preview-04-17"

    def generate_response(self, messages: List, tools: List = [], stream: bool = False):
        """Generate response using LiteLLM"""
        response = litellm.completion(
            model=self.model,
            messages=messages,
            stream=stream,
            tools=tools
        )

        return response
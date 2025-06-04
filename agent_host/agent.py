import os
import time
import json
from pathlib import Path
from setup.logging_config import setup_logger
from .mcp_client import MCPClient
from llm.llm_client import LLM

logger = setup_logger(__name__)

class Agent:
    def __init__(self):
        print("Initializing agent...")

        self.mcp_client = MCPClient()
        self.llm = LLM()
        print("Agent initialized...")

    async def start_servers(self):
        print("MCP servers running...")
    
    async def process_query(self, query: str):
        """Process a query using LLM and MCP servers"""
        await self.mcp_client.connect_to_server()


        messages = [
            {
                "role": "user",
                "content": query
            }
        ]
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "pdf_search",
                    "description": "Search arXiv for scientific papers with a query",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string"},
                            "max_results": {"type": "number"}
                        },
                        "required": ["query", "max_results"],
                        "additionalProperties": False
                    },
                    "strict": True
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "pdf_summarize",
                    "description": "Summarize a PDF given the PDF URL",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "pdf_url": {"type": "string"}
                        },
                        "required": ["pdf_url"],
                        "additionalProperties": False
                    },
                    "strict": True
                }
            }
        ]
        
        logger.info("Processing query...")
        # Initial LLM API call
        response = self.llm.generate_response(
            messages=messages,
            tools=tools
        )
        logger.info(f"Returning LLM response {response}")

        if tool_calls := response.choices[0].message.tool_calls:
            for tool_call in tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)
                result = await self.mcp_client.invoke_tool(tool_name, tool_args)
                return result

        return response.choices[0].message.content

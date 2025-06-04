import os
import time
import json
from pathlib import Path
from setup.logging_config import setup_logger
from setup.stream_to_cli import stream_to_cli
from .mcp_client import MCPClient
from llm.llm_client import LLM

logger = setup_logger(__name__)

class Agent:
    def __init__(self):
        # logger.debug("Initializing agent...")
        self.mcp_client = MCPClient()
        self.llm = LLM()
        # logger.debug("Agent initialized...")

    async def start_servers(self):
        self.search_client, self.summarize_client = await self.mcp_client.connect_to_servers()
        # logger.debug("MCP servers running...")
    
    async def process_query(self, query: str):
        """Process a query using LLM and MCP servers"""

        messages = [
            {
                "role": "system",
                "content": "You are expect at answer and routing requests to the MCP tools. Note: YOU MUST stick to the tool schema! It must be a proper JSON as specificied."
            },
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
        
        stream_to_cli("Processing query...")
        # logger.debug("Processing query...")
        # Initial LLM API call
        response = self.llm.generate_response(
            messages=messages,
            tools=tools
        )
        # logger.debug(f"LLM Response: {response}")
        if tool_calls := response.choices[0].message.tool_calls:
            for tool_call in tool_calls:
                tool_name = tool_call.function.name
                # logger.debug(f"tool_name: {tool_name}")
                tool_args = json.loads(tool_call.function.arguments)
                # logger.debug(f"tool_name: {tool_args}")
                if tool_name == "pdf_search":
                    result = await self.mcp_client.invoke_tool(self.search_client, tool_name, tool_args)
                elif tool_name == "pdf_summarize":
                    result = await self.mcp_client.invoke_tool(self.summarize_client, tool_name, tool_args)
                return result

        return response.choices[0].message.content

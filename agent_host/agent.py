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

        base_dir = Path(__file__).resolve().parent.parent  # Go up one level from agent_host
        search_server_path = base_dir / "mcp_servers" / "pdf_search" / "server.py"
        self.search_mcp = MCPClient(str(search_server_path))
        summary_server_path = base_dir / "mcp_servers" / "pdf_summarize" / "server.py"
        self.summary_mcp = MCPClient(str(summary_server_path))
        self.llm = LLM()

        print("Agent initialized...")

    async def start_servers(self):
        await self.search_mcp.connect_to_server()
        await self.summary_mcp.connect_to_server()

        print("MCP servers running")
    
    async def process_query(self, query: str):
        """Process a query using LLM and MCP servers"""

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

        for tool_call in response.choices[0].message.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            if name == "pdf_search":
                result = await self.search_mcp.invoke_tool(tool_args=args)
            elif name == "pdf_summarize":
                result = await self.summary_mcp.invoke_tool(tool_args=args)
            return result
        
        return response.choices[0].message.content

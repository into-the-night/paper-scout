import asyncio
from typing import Optional, Dict
from llm.llm_client import LLM
from setup.logging_config import setup_logger
from setup.stream_to_cli import stream_to_cli
from dotenv import load_dotenv
from fastmcp import Client

import logging
logging.getLogger("httpcore").setLevel(logging.ERROR)
logging.getLogger("httpx").setLevel(logging.ERROR)

load_dotenv()  # load environment variables from .env
file_logger = setup_logger(__name__)

from fastmcp.client.logging import LogMessage

async def log_handler(message: LogMessage):
    level = message.level.upper()
    logger = message.logger or 'default'
    data = message.data
    file_logger.info(f"[Server Log - {level}] {logger}: {data}")


class MCPClient:
    def __init__(self):
        self.llm = LLM()

    async def connect_to_servers(self):
        """Connect to the pdf-search MCP server

        Args:
            server_script_path: Path to the server script
        """
        search_config = {
            "mcpServers": {
                "pdf_search": {
                    "command": "python",
                    "args": ["./mcp_servers/pdf_search/server.py"],
                }
            }
        }
        summarize_config = {
            "mcpServers": {
                "pdf_summarize": {
                    "command": "python",
                    "args": ["./mcp_servers/pdf_summarize/server.py"],
                }
            }
        }
        search_client = Client(search_config, log_handler=log_handler)
        summarize_client = Client(summarize_config, log_handler=log_handler)
        return search_client, summarize_client

    async def list_tools(self, client: Client):
        async with client:
            tools = await client.list_tools()
            return tools
    
    async def invoke_tool(self, client: Client, tool_name: str, tool_args: Dict[str, str]) -> Dict[str, str]:
        """Process a query using available tools"""
        async with client:
            try:
                # Execute tool call
                # file_logger.debug(f"\nClient connected: {client.is_connected()}")
                # file_logger.debug(f"[Calling tool {tool_name} with args {tool_args}]")
                stream_to_cli(f"[Calling tool {tool_name} with args {tool_args}]")
                result = await client.call_tool(tool_name, tool_args)
                return result[0].text
            except Exception as e:
                stream_to_cli(f"[ERROR] Error invoking tools: {e}")
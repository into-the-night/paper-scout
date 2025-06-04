import asyncio
from typing import Optional, Dict
from llm.llm_client import LLM
from setup.logging_config import setup_logger
from dotenv import load_dotenv
from fastmcp import Client

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

    async def connect_to_server(self):
        """Connect to the pdf-search MCP server

        Args:
            server_script_path: Path to the server script
        """
        config = {
            "mcpServers": {
                "pdf_search": {
                    "command": "python",
                    "args": ["./mcp_servers/pdf_search/server.py"],
                },
                "pdf_summarize": {
                    "command": "python",
                    "args": ["./mcp_servers/pdf_summarize/server.py"],
                }
            }
        }
        client = Client(config, log_handler=log_handler)
        self.client = client
        # file_logger.info(f"\nClient connected: {client.is_connected()}")
        # return client
    
    async def list_tools(self):
        async with self.client:
            tools = await self.client.list_tools()
            return tools
    
    async def invoke_tool(self, tool_name: str, tool_args: Dict[str, str]) -> Dict[str, str]:
        """Process a query using available tools"""
        async with self.client:
            try:
                file_logger.info(f"\nClient connected: {self.client.is_connected()}")
                # Execute tool call
                file_logger.info(f"[Calling tool {tool_name} with args {tool_args}]")
                result = await self.client.call_tool(tool_name, tool_args)
                file_logger.info(f"Tool Result: {result.text}")
                return result.text
            except Exception as e:
                file_logger.error(f"Error invoking tools: {e}")
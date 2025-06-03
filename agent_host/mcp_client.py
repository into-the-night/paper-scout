import asyncio
from typing import Optional, Dict
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from llm.llm_client import LLM
from setup.logging_config import setup_logger
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env
logger = setup_logger(__name__)


class MCPClient:
    def __init__(self, server_script_path: str):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.server_script_path = server_script_path
        self.llm = LLM()

    async def connect_to_server(self):
        """Connect to the pdf-search MCP server

        Args:
            server_script_path: Path to the server script
        """
        command = "python"
        server_params = StdioServerParameters(
            command=command,
            args=[self.server_script_path],
            env=None
        )

        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        await self.session.initialize()

        # List available tools
        response = await self.session.list_tools()
        tools = response.tools
        logger.info(f"\nConnected to server with tools:{[tool.name for tool in tools]}")

    
    async def invoke_tool(self, tool_args: Dict[str, str]) -> Dict[str, str]:
        """Process a query using available tools"""

        tool_names = await self.session.list_tools()
        tool_name = tool_names.tools[0].name

        # Execute tool call
        logger.info(f"[Calling tool {tool_name} with args {tool_args}]")
        result = await self.session.call_tool(tool_names.tools[0].name, tool_args)
        logger.info(f"Tool Result: {result}")

        return result.content

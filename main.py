import time
import json
import asyncio
from datetime import datetime
from setup.logging_config import setup_logger
from setup.stream_to_cli import stream_to_cli
from agent_host.agent import Agent

logger = setup_logger(__name__)

async def run_cli():
    print("📚 Scientific-Paper Scout CLI — type 'exit' to quit")

    agent = Agent()
    await agent.start_servers()

    while True:
        user_input = str(input("\nYou: "))
        if user_input.lower() == "exit":
            break

        try:
            start = time.time()
            result = await agent.process_query(user_input)

            latency = time.time() - start
            # logger.debug(f"[SUCCESS] Returning LLM response (took {latency}ms): {result}")
            stream_to_cli(f"[SUCCESS] Returning LLM response (took {latency}ms):")
            stream_to_cli(result)
        except Exception as e:
            latency = time.time() - start
            stream_to_cli(f"[ERROR] LLM response failed (took {latency}ms) with error {e}")

if __name__ == "__main__":
    asyncio.run(run_cli())

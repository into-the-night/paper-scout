import time
import json
import asyncio
from datetime import datetime
from setup.logging_config import setup_logger
from agent_host.agent import Agent

logger = setup_logger(__name__)

def log_tool_call(tool_name, args, latency, status):
    log = {
        "tool": tool_name,
        "args": args,
        "timestamp": datetime.utcnow().isoformat(),
        "duration": f"{latency:.2f}s",
        "status": status
    }
    print(f"[TOOL CALL] {json.dumps(log, indent=2)}")

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
            print(f"[SUCCESS] Returning LLM response (took {latency}ms):")

            # for chunk in result:
            #     if chunk.choices[0].delta.content is not None:
            #         print(chunk.choices[0].delta.content, end="")
            print(result)
        except Exception as e:
            latency = time.time() - start
            print(f"[ERROR] LLM response failed (took {latency}ms) with error {e}")

if __name__ == "__main__":
    asyncio.run(run_cli())

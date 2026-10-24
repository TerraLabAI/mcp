# /// script
# requires-python = ">=3.10"
# dependencies = ["langchain-mcp-adapters>=0.3", "langchain>=1.0", "langchain-openai"]
# ///
"""A LangChain / LangGraph agent with TerraLab tools via langchain-mcp-adapters.

    export OPENAI_API_KEY=sk-...        # or swap the model for any LangChain chat model
    uv run agent.py "Contour lines every 10 m around Annecy old town"

Without OPENAI_API_KEY it loads the tools and calls one directly (no model call).
"""
import asyncio
import os
import sys

from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

# Your TerraLab API key, sent when TERRALAB_API_KEY is set.
KEY = os.environ.get("TERRALAB_API_KEY")
client = MultiServerMCPClient(
    {
        "terralab": {
            "url": "https://mcp.terra-lab.ai/mcp",
            "transport": "streamable_http",
            "headers": {"Authorization": f"Bearer {KEY}"} if KEY else {},
        }
    }
)


async def main(prompt: str) -> None:
    tools = await client.get_tools()
    print("TerraLab tools:", ", ".join(t.name for t in tools))

    if not os.environ.get("OPENAI_API_KEY"):
        convert = next(t for t in tools if t.name == "convert_coordinates")
        print(await convert.ainvoke({"text": "48.8584, 2.2945", "target_epsg": "EPSG:2154"}))
        print("Set OPENAI_API_KEY to run the agent.")
        return

    agent = create_agent("openai:" + os.environ.get("OPENAI_MODEL", "gpt-5.5"), tools)
    result = await agent.ainvoke({"messages": [{"role": "user", "content": prompt}]})
    print(result["messages"][-1].content)


asyncio.run(main(" ".join(sys.argv[1:]) or "What is the elevation of the Eiffel Tower?"))

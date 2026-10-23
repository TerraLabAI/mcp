# /// script
# requires-python = ">=3.10"
# dependencies = ["openai-agents>=0.24"]
# ///
"""An OpenAI Agents SDK agent with TerraLab as its geospatial toolset.

    export OPENAI_API_KEY=sk-...
    uv run agent.py "Give me the roads of Nairobi CBD as GeoJSON"

Without OPENAI_API_KEY it only connects and lists the tools (no model call).
"""
import asyncio
import os
import sys

from agents import Agent, Runner
from agents.mcp import MCPServerStreamableHttp

URL = "https://mcp.terra-lab.ai/mcp"


async def main(prompt: str) -> None:
    async with MCPServerStreamableHttp(
        name="terralab",
        params={"url": URL, "timeout": 120},
        client_session_timeout_seconds=300,
        cache_tools_list=True,
    ) as terralab:
        tools = await terralab.list_tools()
        print("TerraLab tools:", ", ".join(t.name for t in tools))
        if not os.environ.get("OPENAI_API_KEY"):
            print("Set OPENAI_API_KEY to run the agent.")
            return

        agent = Agent(
            name="GIS assistant",
            instructions=(
                "You get map data for places with the TerraLab tools. "
                "Always give the download links and the sources and licences."
            ),
            mcp_servers=[terralab],
            model=os.environ.get("OPENAI_MODEL", "gpt-5.5"),
        )
        result = await Runner.run(agent, prompt)
        print(result.final_output)


asyncio.run(main(" ".join(sys.argv[1:]) or "What is the elevation of the Eiffel Tower?"))

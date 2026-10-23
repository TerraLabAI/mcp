# /// script
# requires-python = ">=3.10"
# dependencies = ["google-adk[mcp]>=2.12"]
# ///
"""A Google ADK agent with TerraLab as an MCP toolset.

    export GOOGLE_API_KEY=...           # Gemini API key
    uv run agent.py "Which cadastral parcel is at 12 rue de la Paix, Annecy?"

Without GOOGLE_API_KEY it only connects and lists the tools (no model call).
"""
import asyncio
import os
import sys

from google.adk.agents import LlmAgent
from google.adk.runners import InMemoryRunner
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams
from google.genai import types

terralab = McpToolset(
    connection_params=StreamableHTTPConnectionParams(
        url="https://mcp.terra-lab.ai/mcp", timeout=120, sse_read_timeout=300
    )
)

root_agent = LlmAgent(
    model="gemini-flash-latest",
    name="gis_assistant",
    instruction="Get map data with the TerraLab tools. Give download links, sources and licences.",
    tools=[terralab],
)


async def main(prompt: str) -> None:
    tools = await terralab.get_tools()
    print("TerraLab tools:", ", ".join(t.name for t in tools))
    if not os.environ.get("GOOGLE_API_KEY"):
        print("Set GOOGLE_API_KEY to run the agent.")
        await terralab.close()
        return

    runner = InMemoryRunner(agent=root_agent, app_name="terralab-demo")
    session = await runner.session_service.create_session(app_name="terralab-demo", user_id="me")
    message = types.Content(role="user", parts=[types.Part(text=prompt)])
    async for event in runner.run_async(user_id="me", session_id=session.id, new_message=message):
        if event.is_final_response() and event.content:
            print("".join(p.text or "" for p in event.content.parts))
    await terralab.close()


if __name__ == "__main__":
    asyncio.run(main(" ".join(sys.argv[1:]) or "What is the elevation of the Eiffel Tower?"))

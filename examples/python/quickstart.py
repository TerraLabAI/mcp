# /// script
# requires-python = ">=3.10"
# dependencies = ["mcp>=2.3,<3"]
# ///
"""List the TerraLab tools and run one.

    export TERRALAB_API_KEY=tlk_...   # your TerraLab API key
    uv run quickstart.py
"""
import asyncio
import os

from mcp import Client
from mcp.client.streamable_http import create_mcp_http_client, streamable_http_client

URL = "https://mcp.terra-lab.ai/mcp"


def server():
    """The TerraLab server, with your API key when TERRALAB_API_KEY is set."""
    key = os.environ.get("TERRALAB_API_KEY")
    if not key:
        return URL
    headers = {"Authorization": f"Bearer {key}"}
    return streamable_http_client(URL, http_client=create_mcp_http_client(headers=headers))


async def main() -> None:
    async with Client(server()) as client:
        tools = await client.list_tools()
        print("Tools:", ", ".join(t.name for t in tools.tools))

        result = await client.call_tool(
            "convert_coordinates",
            {"text": "48.8584, 2.2945 Eiffel Tower", "target_epsg": "EPSG:2154"},
        )
        print(result.content[0].text)


asyncio.run(main())

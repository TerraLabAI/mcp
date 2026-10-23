# /// script
# requires-python = ">=3.10"
# dependencies = ["mcp>=2.3,<3"]
# ///
"""List the TerraLab tools and run one. No key, no account.

    uv run quickstart.py
"""
import asyncio

from mcp import Client

URL = "https://mcp.terra-lab.ai/mcp"


async def main() -> None:
    async with Client(URL) as client:
        tools = await client.list_tools()
        print("Tools:", ", ".join(t.name for t in tools.tools))

        result = await client.call_tool(
            "convert_coordinates",
            {"text": "48.8584, 2.2945 Eiffel Tower", "target_epsg": "EPSG:2154"},
        )
        print(result.content[0].text)


asyncio.run(main())

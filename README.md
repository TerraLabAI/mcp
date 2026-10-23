# TerraLab

GIS data for any place, for your AI agent. One hosted MCP server, no API key, no account:

```
https://mcp.terra-lab.ai/mcp
```

Ask for a place, get real GIS files back: buildings, roads, addresses, land use, water,
transit, protected areas, elevation, contour lines, as GeoJSON, Shapefile, KML, CSV, GeoPackage
or GeoTIFF, each with its sources and licence. Works anywhere in the world.
Made by [TerraLab](https://terra-lab.ai), which builds AI tools for QGIS.

## Start in 30 seconds

```bash
claude mcp add --transport http terralab https://mcp.terra-lab.ai/mcp
```

Then ask Claude Code: *"Get the buildings and roads within 500 m of Porto-Vecchio, Corsica, as GeoJSON."*
Other clients and frameworks are below; it is the same URL everywhere.

## Tools

| Tool | What it returns |
| --- | --- |
| `find_places` | Coordinates for an address or place, an address for coordinates, or up to 100 addresses on a map |
| `extract_open_data` | OpenStreetMap and Overture Maps layers for an area (buildings, roads, addresses, admin boundaries, land use, POIs, waterways, water, power, railways, transit stops, protected areas) as downloadable files |
| `get_elevation` | Elevation of points, a profile along a route, or for an area: DEM, hillshade and slope GeoTIFFs plus contour lines (Copernicus DEM 30 m) |
| `open_gis_file` | Reads a GeoJSON, KML, KMZ, GPX, zipped Shapefile, CSV or WKT file (upload, URL or text), shows it and converts it |
| `convert_coordinates` | Decimal degrees, DMS, UTM, MGRS, Lambert 93 or any EPSG code, with a recommended local CRS |
| `french_parcel` | French cadastral parcel and local urban plan (PLU) zone at an address or point |

Every result has a short text answer for the model, structured content for code
(`places`, `downloads`, `sources`), and download links that build the file when opened.
All tools are read-only. Tool changes are additive: tools, parameters and output fields are
never removed or renamed without 30 days' notice on [terra-lab.ai/mcp](https://terra-lab.ai/mcp).

## Connect a client

| Client | Setup |
| --- | --- |
| Claude Code | `claude mcp add --transport http terralab https://mcp.terra-lab.ai/mcp` (add `--scope user` for all projects) |
| Cursor | Add to `~/.cursor/mcp.json`: `{"mcpServers": {"terralab": {"url": "https://mcp.terra-lab.ai/mcp"}}}` |
| VS Code (Copilot) | `code --add-mcp '{"name":"terralab","type":"http","url":"https://mcp.terra-lab.ai/mcp"}'`, or **MCP: Add Server**, HTTP, the URL above |
| Windsurf | Add to `mcp_config.json`: `{"mcpServers": {"terralab": {"serverUrl": "https://mcp.terra-lab.ai/mcp"}}}` |
| Gemini CLI | `gemini extensions install https://github.com/TerraLabAI/mcp` |
| Claude.ai, Claude Desktop | Settings, Connectors, add a custom connector with the URL above |
| ChatGPT | Search for TerraLab in the ChatGPT app directory |

In `.vscode/mcp.json` the key is `servers`:
`{"servers": {"terralab": {"type": "http", "url": "https://mcp.terra-lab.ai/mcp"}}}`.
If tools change, run **MCP: Reset Cached Tools** in VS Code.

## Use it from code

Every snippet below talks to the production server. The runnable versions are in
[`examples/`](examples/), with the date each one was last run.

**Python, official MCP SDK** (`pip install "mcp>=2.3"`)

```python
import asyncio
from mcp import Client

async def main():
    async with Client("https://mcp.terra-lab.ai/mcp") as client:
        result = await client.call_tool(
            "extract_open_data",
            {"theme": "buildings", "area": {"place": "Kreuzberg, Berlin", "radius_m": 300}},
        )
        print(result.content[0].text)
        for d in result.structured_content["downloads"]:
            print(d["format"], d["url"])

asyncio.run(main())
```

**TypeScript, official MCP SDK** (`npm i @modelcontextprotocol/sdk`)

```ts
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";

const client = new Client({ name: "my-agent", version: "1.0.0" });
await client.connect(new StreamableHTTPClientTransport(new URL("https://mcp.terra-lab.ai/mcp")));
const result = await client.callTool({
  name: "get_elevation",
  arguments: { mode: "point", points: ["Mont Blanc summit"] },
});
console.log(result.content[0].text);
```

**OpenAI Agents SDK** (`pip install openai-agents`)

```python
from agents import Agent, Runner
from agents.mcp import MCPServerStreamableHttp

async with MCPServerStreamableHttp(
    name="terralab", params={"url": "https://mcp.terra-lab.ai/mcp", "timeout": 120},
    client_session_timeout_seconds=300,
) as terralab:
    agent = Agent(name="GIS assistant", mcp_servers=[terralab])
    print((await Runner.run(agent, "Roads of Nairobi CBD as GeoJSON")).final_output)
```

**OpenAI Responses API** (OpenAI calls the server for you)

```python
from openai import OpenAI

response = OpenAI().responses.create(
    model="gpt-5.5",
    tools=[{
        "type": "mcp",
        "server_label": "terralab",
        "server_url": "https://mcp.terra-lab.ai/mcp",
        "require_approval": "never",
    }],
    input="Contour lines every 10 m around Annecy old town, as GeoJSON.",
)
print(response.output_text)
```

**Anthropic Messages API, MCP connector**

```python
import anthropic

response = anthropic.Anthropic().beta.messages.create(
    model="claude-opus-5-5",
    max_tokens=2000,
    betas=["mcp-client-2025-11-20"],
    mcp_servers=[{"type": "url", "url": "https://mcp.terra-lab.ai/mcp", "name": "terralab"}],
    tools=[{"type": "mcp_toolset", "mcp_server_name": "terralab"}],
    messages=[{"role": "user", "content": "Which cadastral parcel is at 12 rue de la Paix, Annecy?"}],
)
```

**LangChain / LangGraph** (`pip install langchain-mcp-adapters langchain`)

```python
from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

client = MultiServerMCPClient(
    {"terralab": {"url": "https://mcp.terra-lab.ai/mcp", "transport": "streamable_http"}}
)
tools = await client.get_tools()
agent = create_agent("openai:gpt-5.5", tools)
```

**Vercel AI SDK** (`npm i ai @ai-sdk/mcp`)

```ts
import { createMCPClient } from "@ai-sdk/mcp";

const terralab = await createMCPClient({
  transport: { type: "http", url: "https://mcp.terra-lab.ai/mcp" },
});
const tools = await terralab.tools(); // pass to generateText / streamText
```

**Google ADK** (`pip install "google-adk[mcp]"`; without the `mcp` extra, `McpToolset` does not import)

```python
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams

root_agent = LlmAgent(
    model="gemini-flash-latest", name="gis_assistant",
    tools=[McpToolset(connection_params=StreamableHTTPConnectionParams(
        url="https://mcp.terra-lab.ai/mcp", timeout=120))],
)
```

Other frameworks take the same URL as a Streamable HTTP server: CrewAI
(`mcps=["https://mcp.terra-lab.ai/mcp"]`), Pydantic AI (`MCPToolset(url)`), LlamaIndex
(`BasicMCPClient(url)`), Mastra (`MCPClient` with `url: new URL(...)`), smolagents
(`MCPClient({"url": ..., "transport": "streamable-http"})`). We have not run these five yet.

Large areas take time: give your MCP client a timeout of at least 120 seconds. Download links
serve gzip when you send `Accept-Encoding: gzip` (httpx and requests do it for you).

## Examples

| Example | What it does | Needs |
| --- | --- | --- |
| [`examples/python/site_pack.py`](examples/python/site_pack.py) | Chains five calls into a folder of GIS files for any place (buildings, roads, water, DEM, hillshade, slope, contours) plus a summary with licences | `uv` only |
| [`examples/claude-code/site_brief.sh`](examples/claude-code/site_brief.sh) | A headless Claude Code agent that writes a site brief with download links | Claude Code |
| [`examples/python/quickstart.py`](examples/python/quickstart.py), [`examples/typescript/`](examples/typescript/) | List the tools and run one | `uv` or Node |
| [`examples/openai-agents/`](examples/openai-agents/), [`langgraph/`](examples/langgraph/), [`vercel-ai-sdk/`](examples/vercel-ai-sdk/), [`google-adk/`](examples/google-adk/) | The same agent in each framework | a model API key |

```bash
uv run examples/python/site_pack.py "Porto-Vecchio, Corsica"
```

## Plugins and skills

The product name is **TerraLab**. The package ID remains `terralab`, and the Claude
marketplace ID remains `terralab-ai-apps` so existing installation commands keep working.

Claude Code plugin (server plus four workflow skills):

```
/plugin marketplace add TerraLabAI/mcp
/plugin install terralab@terralab-ai-apps
```

The four workflows work for any place in the world:

- **map-data-for-a-place**: administrative boundaries, buildings, roads, railways, transit
  stops, addresses, points of interest, land use, rivers and lakes, power lines or protected
  areas for a place, as files that open directly in QGIS.
- **terrain-and-elevation**: altitude of places, elevation profiles along a route, contour
  lines and slope for an area.
- **site-study**: a first look at a site before a project: terrain, water, protected areas,
  land use and roads around it, and in France the cadastral parcel and the local urban
  plan (PLU) zone.
- **places-files-and-coordinates**: put an address, a list of up to 100 addresses or a
  GIS file on a map, convert it, convert coordinates and pick the right CRS for QGIS.

Install the skills alone with the Vercel skills CLI (they still need the server above):

```sh
npx skills add TerraLabAI/mcp
npx skills add TerraLabAI/mcp --skill map-data-for-a-place
```

Browse [TerraLab skills on skills.sh](https://skills.sh/terralabai/mcp).
This repository holds the Claude and Cursor plugin packages, the Gemini CLI extension,
the skills and the examples. The server itself is hosted by TerraLab.

## Data and limits

Elevation, profiles and contour lines come from Copernicus DEM. Map layers come from
OpenStreetMap and Overture Maps; French parcels from IGN and DGFiP open data. Every answer
names its sources and licences, and every download carries its licence.
Results are approximate and not for navigation, surveying or legal boundaries.

## Links

- Documentation and setup: https://terra-lab.ai/mcp
- Privacy policy: https://terra-lab.ai/privacy-policy#ai-assistants
- Terms of use: https://terra-lab.ai/terms-of-use
- Support: https://terra-lab.ai/support or yvann.barbot@terra-lab.ai

TerraLab also makes AI plugins for QGIS: AI Segmentation, AI Edit and AI Agent.

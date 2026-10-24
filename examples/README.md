# TerraLab examples

Every example talks to the production server `https://mcp.terra-lab.ai/mcp`.
Python examples run with [uv](https://docs.astral.sh/uv/)
(`uv run <file>` installs their dependencies); Node examples need `npm install` first.

| Example | Run | Needs | Last run |
| --- | --- | --- | --- |
| Site pack agent: a folder of GIS files for any place | `uv run python/site_pack.py "Kreuzberg, Berlin" --radius 300` | uv | 2026-10-23: Porto-Vecchio 500 m, 7 files in 18 s |
| Site brief agent, headless Claude Code | `./claude-code/site_brief.sh "Annecy old town, France"` | Claude Code | 2026-10-23: brief with 6 download links in 2 min |
| Python MCP SDK quickstart | `uv run python/quickstart.py` | uv | 2026-10-23 |
| TypeScript MCP SDK quickstart | `cd typescript && npm install && node quickstart.mjs` | Node 20+ | 2026-10-23 |
| OpenAI Agents SDK | `uv run openai-agents/agent.py "<prompt>"` | `OPENAI_API_KEY` | 2026-10-23: full agent run (gpt-5.4-mini) |
| LangChain / LangGraph | `uv run langgraph/agent.py "<prompt>"` | `OPENAI_API_KEY` (or any LangChain model) | 2026-10-23: full agent run (gpt-5.4-mini) |
| Vercel AI SDK | `cd vercel-ai-sdk && npm install && node agent.mjs "<prompt>"` | `OPENAI_API_KEY` | 2026-10-23: tools and a tool call; model call not run |
| Google ADK | `uv run google-adk/agent.py "<prompt>"` | `GOOGLE_API_KEY` | 2026-10-23: tools listed; model call not run |

The framework agents connect and list the tools even without a model key, so you can check
the connection first. Downloads ask for gzip (GeoJSON shrinks about 10x). Large extracts can still take a minute; the examples use a 120 s timeout.

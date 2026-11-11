# TerraLab examples

Every example talks to the production server `https://mcp.terra-lab.ai/mcp`. Set your
TerraLab API key first (`export TERRALAB_API_KEY=tlk_...`, keys at [terra-lab.ai/dashboard/agent-access](https://terra-lab.ai/dashboard/agent-access)): every example sends it as
`Authorization: Bearer` when the variable is set, and nothing otherwise.
Each example is one Markdown page: save its code blocks under the file names it gives, in one folder, then run the command below from that folder.
Python examples run with [uv](https://docs.astral.sh/uv/)
(`uv run <file>` installs their dependencies); Node examples need `npm install` first.

| Example | Run | Needs | Last run |
| --- | --- | --- | --- |
| [Site pack agent](python/README.md): a folder of GIS files for any place | `uv run site_pack.py "Kreuzberg, Berlin" --radius 300` | uv | 2026-10-23: Porto-Vecchio 500 m, 7 files in 18 s |
| [Site brief agent, headless Claude Code](claude-code/README.md) | `bash site_brief.sh "Annecy old town, France"` | Claude Code | 2026-10-23: brief with 6 download links in 2 min |
| [Python MCP SDK quickstart](python/README.md) | `uv run quickstart.py` | uv | 2026-10-24 |
| [TypeScript MCP SDK quickstart](typescript/README.md) | `npm install && node quickstart.mjs` | Node 20+ | 2026-10-24 |
| [OpenAI Agents SDK](openai-agents/README.md) | `uv run agent.py "<prompt>"` | `OPENAI_API_KEY` | 2026-10-23: full agent run (gpt-5.4-mini) |
| [LangChain / LangGraph](langgraph/README.md) | `uv run agent.py "<prompt>"` | `OPENAI_API_KEY` (or any LangChain model) | 2026-10-23: full agent run (gpt-5.4-mini) |
| [Vercel AI SDK](vercel-ai-sdk/README.md) | `npm install && node agent.mjs "<prompt>"` | `OPENAI_API_KEY` | 2026-10-23: tools and a tool call; model call not run |
| [Google ADK](google-adk/README.md) | `uv run agent.py "<prompt>"` | `GOOGLE_API_KEY` | 2026-10-23: tools listed; model call not run |

The framework agents connect and list the tools even without a model key, so you can check
the connection first. Downloads ask for gzip (GeoJSON shrinks about 10x). Large extracts can still take a minute; the examples use a 120 s timeout.

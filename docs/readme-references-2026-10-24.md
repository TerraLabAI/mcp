# README references: Krea and Mireye on GitHub (2026-10-24)

What two hosted MCP products show developers on GitHub and on their MCP pages, section by
section, and what the TerraLab README takes or leaves. Read on 2026-10-24 with `gh api
repos/<owner>/<repo>/readme -H "Accept: application/vnd.github.raw"`, the npm registry, and a
page fetch of krea.ai/mcp and its docs.

## Where each one lives

| | Krea | Mireye |
| --- | --- | --- |
| GitHub organisation | `krea-ai` (verified, 23 public repos) | `Mireye-Labs` (4 public repos) |
| Repo for agents | [`krea-ai/skills`](https://github.com/krea-ai/skills) (29 stars): skills, Claude, Cursor and Codex plugin packages, evals | [`Mireye-Labs/mireye-earth-mcp`](https://github.com/Mireye-Labs/mireye-earth-mcp): published source of the `mireye-mcp` setup helper (PyPI 0.7.3) |
| MCP server code | private | private ("snapshot-synced from a private monorepo") |
| CLI | `@krea-ai/cli` on npm (0.1.7, Go binary; its `krea-ai/cli` repo is not public) | the setup helper is the CLI (`uvx --from mireye-mcp==0.7.3 mireye-mcp ...`) |
| MCP page | [krea.ai/mcp](https://www.krea.ai/mcp) | [mireye.com/onboarding](https://www.mireye.com/onboarding) (behind sign-in), [docs.mireye.ai](https://docs.mireye.ai/llms.txt) |
| Ready-to-paste recipes | briefs on krea.ai/mcp with a "Recreate" button | [mireye.com/templates](https://www.mireye.com/templates): 12 skills with "Copy Skill" |

Neither README has a banner image. Krea uses four badges (licence, version, skill count,
Discord); Mireye none. The visual weight is on their web pages, not on GitHub.

## Krea, `krea-ai/skills` README, in order

1. **Title and badges**: "Krea AI Skills", licence, version, number of skills, Discord.
2. **One line**: "Three packaged Agent Skills for working with Krea.ai. Install once, get the
   Krea skill suite."
3. **Skill table**: skill name and "When to use", three rows.
4. **Which agents read the skills** (Cursor, Codex, Windsurf, OpenCode, Gemini, OpenClaw).
5. **Install the skills**: `npx skills add krea-ai/skills`.
6. **Prerequisites**: the MCP must be connected; OAuth, no key stored in the repo.
7. **Plugin packaging**: one paragraph per client package (Cursor `.cursor-plugin`, Codex
   `.codex-plugin`, Claude `.claude-plugin`), with the endpoint each one uses.
8. **Claude connector**: `/plugin marketplace add krea-ai/skills`, `/plugin install krea@krea`,
   then `/mcp` to sign in; the exact tool list of the restricted connector.
9. **Use the skills**: example prompts in blocks, grouped by which skill they trigger.
10. **Updates**: opt-in update check, how to disable it.
11. **Evals**: offline gate on every push, live suite gated by label; 47 regression scenarios.
12. **License**: MIT.

## Krea, krea.ai/mcp and docs

- Hero: "Krea MCP. All of Krea, inside your agent." then one sentence, then tabs per agent
  (Claude, ChatGPT, Claude Code, OpenClaw, Cursor, Grok Bot, Hermes, CLI), each in three steps.
- Exact install lines per agent, all against one URL `https://api.krea.ai/mcp`:
  - Claude: Settings, Connectors, Add, paste the URL, sign in.
  - ChatGPT: add the Krea plugin from the directory, sign in.
  - Claude Code: `claude mcp add --transport http krea https://api.krea.ai/mcp`, then `/mcp`.
  - OpenClaw: `openclaw mcp set krea-ai '{"transport": "streamable-http", "url": "https://api.krea.ai/mcp"}'`.
  - Cursor: Marketplace page or `/add-plugin krea`.
  - Hermes: `mcp_servers: krea-ai: url: ...` in `~/.hermes/config.yaml`.
  - CLI: `npm install -g @krea-ai/cli@latest`, `krea auth login`, `krea gen image -p "a cat" --wait`.
- Then: "How Krea MCP works" (persona chips that switch a demo), ready-to-run briefs with
  "Recreate" (opens `claude.ai/new?q=`), one section per capability with a real result, FAQ
  (8 questions, one is "Do I need an API key?"), last call to action.
- Docs page `krea.ai/docs/developers/mcp`: server details table (transport, URL, auth),
  billing by auth method, OAuth first and API token as fallback (`Authorization: Bearer`),
  one block per client (Claude Code, Codex, Cursor), example prompts, tool table.

## Mireye, `Mireye-Labs/mireye-earth-mcp` README, in order

1. **Title**: "Mireye hosted MCP setup helper".
2. **What the package is and is not**: configures Claude Code, Codex and Cursor for the hosted
   `https://api.mireye.com/mcp`, installs the `use-mireye` skill, runs no MCP server.
3. **How to start**: sign in on the onboarding page, accept terms, paste a private setup
   prompt into the agent; key passed on stdin only.
4. **Two commands**: `connect --all --api-key-stdin`, `doctor --proof`.
5. **What "proof" proves**: one free Fetch with source and timestamp; says plainly it does
   not verify the MCP OAuth grant.
6. **File table**: client, config file, skill and credentials path.
7. **Safety rules**: preserves other config, refuses conflicts, backs up, process lock.
8. **More commands**: dry run, one client, redacted report, remove, logout.
9. **Links to each client's own MCP docs** (Claude Code, Codex, Cursor).
10. **Registry note**: the official MCP registry entry is hosted-only.
11. **Result contract**: what `mireye_enrich` and `mireye_search` return, field by field.

## Mireye, docs and templates

- Docs index in one `llms.txt`: introduction, quickstart, authentication, pricing, one page
  per endpoint, hosted MCP installation, tools, troubleshooting.
- Templates page: "Copy-paste Agent Skills for Mireye's API. Each one is a real problem, a real
  endpoint, and a working skill file." Each template: the business case, "How it works" in
  three short paragraphs (the exact call, what comes back with its source, the trap to check),
  a full example response, variants "Single address" and "Batch (loop over a list)".
- The `use-mireye` skill: a "user need, tool" table; two distinct auth paths (MCP OAuth, API
  bearer token); read the field catalog before calling and never invent a field; resolve the
  place honestly (never invent coordinates, show ambiguous matches); report with sources,
  units and caveats; null means unknown, not zero risk; retry only retryable errors.

## What the TerraLab README takes

| From | We take | Why |
| --- | --- | --- |
| Krea page | One URL, then one exact line or three steps per client, in a table | The reader picks their client and copies one thing |
| Krea page | Example prompts right after install | Proves the install worked in one question |
| Krea skills README | Skill table with "When to use", `npx skills add`, plugin commands | Same tooling (skills CLI, Claude marketplace) |
| Krea docs | Server details table (transport, URL, auth) | A developer checks this before anything else |
| Mireye README | Say what the repo is and is not (the server is hosted, not here) | Avoids issues asking for the server code |
| Mireye README | Links to each client's own MCP docs | Lets the reader verify our lines |
| Mireye skill | A `use-terralab` skill: routing table, auth paths, reporting rules | Agents pick the right tool and cite sources |
| Mireye templates | Recipes: question, exact call, real dated answer, the trap to check | Our proof is a real file with its licence |
| Both | Tools named by verb with an example question each | The tool names are the product for agents |

## What it leaves

- **Banner as decoration**: neither uses one. If we add a header image, it is a real map from
  a real call, not artwork. Decision left to Yvann.
- **Badges**: kept to none. Our useful facts (12 tools, worldwide, sources) read better as text.
- **Evals section**: we have none public yet; not claimed.
- **Prices, plans, balances, "free"**: Mireye's README and skill talk about prices and
  balances; we name none (TerraLab rule).
- **Setup helper CLI and private setup prompt**: not built. The README offers one command per
  client; a `terralab` CLI is an open question in the gateway brief.
- **Single-country coverage**: Mireye is United States only; our recipes show France, Japan
  and the Alps on purpose.
- **Persona chips and "Recreate" buttons**: they belong to the web page (terra-lab.ai/mcp),
  not to GitHub markdown.

#!/usr/bin/env bash
# A headless Claude Code agent that writes a site brief for any place with TerraLab.
#   ./site_brief.sh "Porto-Vecchio, Corsica"
# Needs Claude Code (https://code.claude.com). No TerraLab key or account.
set -euo pipefail
place="${1:?usage: site_brief.sh \"<place>\"}"
here="$(cd "$(dirname "$0")" && pwd)"

prompt="You are a GIS assistant. For the place \"$place\":
1. Locate it with find_places.
2. Get its elevation range and slope with get_elevation (mode area, radius 500 m).
3. Count its buildings and roads within 500 m with extract_open_data.
Then write a short site brief in Markdown: location, terrain, built density, roads,
a table of download links (GeoJSON and GeoTIFF), and the sources and licences.
Do not invent numbers: use only what the tools return."

# The prompt goes first: --allowedTools takes several values and would swallow it.
claude -p "$prompt" \
  --mcp-config "$here/mcp.json" \
  --strict-mcp-config \
  --allowedTools "mcp__terralab"

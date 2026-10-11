# TerraLab MCP

Map data, ready for QGIS, from a conversation with your AI assistant.

This repository contains the Claude and Cursor plugin packages and the Gemini CLI extension
for TerraLab MCP (`https://mcp.terra-lab.ai/mcp`). The packages include three GIS workflows:

- **qgis-data-extract**: buildings, roads, addresses, administrative areas, land use,
  waterways, transit stops or protected areas around a place, as GeoJSON, Shapefile, KML
  or CSV that open directly in QGIS.
- **gis-file-and-crs**: open, check and convert GeoJSON, KML, KMZ, GPX, zipped Shapefile,
  CSV or WKT files, convert coordinates (DMS, UTM, MGRS, Lambert 93, EPSG codes) and pick
  the right projected CRS for a QGIS project.
- **french-site-check**: the cadastral parcel and the local urban plan (PLU) zone at an
  address in France.

Elevation, profiles and contour lines come from Copernicus DEM. Every answer names its
sources and licences (OpenStreetMap, Overture Maps, Copernicus, IGN and DGFiP open data),
and every download carries its licence. No account or sign-in is needed.

Results are approximate and not for navigation, surveying or legal boundaries.

## Install

The product name is **TerraLab MCP**. The package ID remains `terralab`, and the Claude
marketplace ID remains `terralab-ai-apps` so existing installation commands keep working.

In Claude Code:

```
/plugin marketplace add TerraLabAI/mcp
/plugin install terralab@terralab-ai-apps
```

In Gemini CLI:

```
gemini extensions install https://github.com/TerraLabAI/mcp
```

In Cursor: add a remote MCP server with the URL `https://mcp.terra-lab.ai/mcp`.
The marketplace listing has not been submitted yet.

In claude.ai or Claude Desktop you can also add the server alone: Settings, Connectors,
add a custom connector with the URL `https://mcp.terra-lab.ai/mcp`.

## Links

- Documentation and setup: https://terra-lab.ai/mcp
- Privacy policy: https://terra-lab.ai/privacy-policy#ai-assistants
- Terms of use: https://terra-lab.ai/terms-of-use
- Support: https://terra-lab.ai/support or yvann.barbot@terra-lab.ai

TerraLab also makes AI plugins for QGIS: AI Segmentation, AI Edit and AI Agent.

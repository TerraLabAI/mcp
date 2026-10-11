# TerraLab for Claude

Map data, ready for QGIS, from a conversation with Claude.

This plugin connects Claude to TerraLab's remote MCP server (`https://mcp.terra-lab.ai/mcp`)
and adds three skills that tell Claude how to use it well:

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

In Claude Code:

```
/plugin marketplace add TerraLabAI/terralab-ai-apps
/plugin install terralab@terralab-ai-apps
```

In claude.ai or Claude Desktop you can also add the server alone: Settings, Connectors,
add a custom connector with the URL `https://mcp.terra-lab.ai/mcp`.

## Links

- Website: https://terra-lab.ai
- Privacy policy: https://terra-lab.ai/privacy-policy
- Terms of use: https://terra-lab.ai/terms-of-use
- Support: https://terra-lab.ai/support or yvann.barbot@terra-lab.ai

TerraLab also makes AI plugins for QGIS: AI Segmentation, AI Edit and AI Agent.

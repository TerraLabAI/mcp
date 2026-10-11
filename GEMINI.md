# TerraLab MCP

The `terralab` MCP server gives map data ready for QGIS: open map data extracts (buildings,
roads, addresses, administrative areas, land use, waterways), GIS file reading and conversion,
coordinate conversion with a recommended local CRS, elevation, profiles and contour lines, and
French cadastral parcels with their PLU zone.

- Pass a place name straight to the tool that needs it; most tools locate the place themselves.
- Give the user the download links and the sources and licences each result returns.
- Results are approximate and not for navigation, surveying or legal boundaries.

Workflow details live in `skills/` (qgis-data-extract, gis-file-and-crs, french-site-check).

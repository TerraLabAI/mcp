---
name: qgis-data-extract
description: Get open map data such as buildings, roads, addresses, land use, waterways, transit stops or protected areas for a place or an area, as a file ready to open in QGIS. Use when the user asks for map layers, GIS data or an extract of features around a place, inside a bounding box or within a radius.
---

# Open map data for QGIS

Explicit instructions from the user take priority over this skill.

## Prerequisite

This skill uses [TerraLab MCP](https://terra-lab.ai/mcp). The agent needs a connection
to `https://mcp.terra-lab.ai/mcp`; installing the skill alone does not connect the server.
If its tools are unavailable, provide the setup link and stop before claiming results.
Use the connected tools' current input schemas; tool prefixes vary between clients.

## Steps

1. Identify the area. Accept a place name or address, a point, a place with a radius, or a bbox `[west, south, east, north]` in decimal degrees.
2. Do not call `find_places` first. `extract_open_data` locates the place itself: pass it in `area.place`, with `area.radius_m` when the user gives a distance.
3. If the user names no area size, use a radius of about 1 km for a town centre, less for a dense city.
4. Map each layer the user asks for to one `theme`: `buildings`, `places`, `roads`, `addresses`, `divisions`, `landuse`, `pois`, `waterways`, `water_areas`, `power`, `boundaries`, `railways`, `routes`, `transit_stops`, `protected_areas`.
5. Call `extract_open_data` once per theme. For several layers, make one call for each.
6. To keep only some kinds of feature inside a theme, set `kind` to one value or a list of up to 10 values in English, for example `"pharmacy"` or `["forest", "meadow", "grass"]`. Several kinds fit in one call.
7. If the user asks what data exists for a project, name the useful themes and let them choose before extracting several.
8. Set `formats` (see below). The default is `geojson`.

## Choosing the format

- `geojson`: one file, keeps every attribute, opens directly in QGIS. Default choice.
- `shapefile`: a zip for users or tools that expect Shapefile. Field names are shortened.
- `kml`: for Google Earth or sharing with non GIS users.
- `csv`: for spreadsheets and point data.
- Pass several values in `formats` when the user wants more than one.

## When the area is too large

1. The tool refuses an extract above its area limit for the theme, or above 20,000 features, with the error `area_too_large`.
2. Say so plainly. Never present a partial or invented result as complete.
3. Offer one of these: a smaller radius, a district instead of the whole city, a `kind` filter, or several smaller extracts.

## Missing or ambiguous input

1. If the place is ambiguous (several towns share the name), add the region or country and say which one you used.
2. If the user gives no place at all, ask for it. Do not use the user's own location unless they ask for it.
3. If a theme is reported unavailable, say so and suggest a related theme.

## Opening the file in QGIS

Give these short steps after the download links:

1. Download the file.
2. Drag it into the QGIS window, or use Layer > Add Layer > Add Vector Layer and pick the file. A Shapefile zip opens as is.
3. The data is in WGS 84 (EPSG:4326). To measure distances or areas, set a local projected CRS. Call `convert_coordinates` with a point of the area to get the recommended local CRS when the user needs it.

## What the answer must contain

- The feature count and a few sample attributes from the result.
- The download links returned by the tool.
- The sources and licences the tool returns, as given. Each download also carries its licence.
- One line saying the data is approximate and not for navigation, surveying or legal boundaries.

Done means: the requested checks or extraction completed, with the returned sources, warnings and download links. If the tool cannot complete the request, report the reason and stop without inventing an output.

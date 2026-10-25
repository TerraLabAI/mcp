---
name: places-files-and-coordinates
description: Puts addresses, coordinates or a GIS file on a map and converts them. Covers geocoding one address or a list of up to 100 (pasted or CSV) and the address at a point, opening and checking GeoJSON, KML, KMZ, GPX, zipped Shapefile, CSV or WKT files, converting between these formats, converting coordinates between decimal degrees, DMS, UTM, MGRS, Lambert 93 and EPSG codes, and choosing the right CRS for a GIS project, for example in QGIS. Use when someone wants a list of addresses or clients on a map, the coordinates of an address, a KML turned into a Shapefile, a GPX opened, coordinates converted, or data that lands in the wrong place.
---

# Places, files and coordinates

Explicit instructions from the user take priority over this skill.

## Prerequisite

This skill uses [TerraLab MCP](https://terra-lab.ai/mcp). The agent needs a connection
to `https://mcp.terra-lab.ai/mcp`; installing the skill alone does not connect the server.
If its tools are unavailable, provide the setup link and stop before claiming results.
Use the connected tools' current input schemas; tool prefixes vary between clients.

## Pick the tool

| The user has | Tool |
|---|---|
| One address or place name, or a point to name | `find_places` with `query`, or `latitude` and `longitude` |
| A list of addresses (up to 100), pasted or CSV with an address column | `find_places` with `addresses` or `text`, and a `title` |
| A file, a link to a file, pasted GeoJSON, KML, GPX or WKT | `open_gis_file` with `file`, `url` or `text` (up to 50 MB) |
| Points with coordinates already known, to map or export | `open_gis_file` with `points` |
| Coordinates to convert (up to 1,000 lines) | `convert_coordinates` with `text`, one per line |

Convert with the tool rather than by hand or from memory, so the result comes with a map
and files. Never pass a TerraLab download link back to a tool: list every output format in
one call.

## Addresses

1. Add the town and country to each address when the user gave them once for the whole list.
2. Report how many addresses were found and list the ones not found or matched loosely,
   so the user can fix them. Never place a missing address by guess.
3. The list comes back as a CSV with latitude and longitude added, plus KML and GeoJSON.
   In QGIS the CSV opens as a delimited text layer.

## Files

1. Set `convert_to` when the user wants another format: `geojson`, `kml`, `kmz`, `gpx`,
   `shapefile` or `csv`.
2. Report format, coordinate system, extent, feature count, geometry types, fields and
   any warning.

## Coordinates

1. Each line's format is detected. For a national grid the numbers cannot reveal, set
   `source_epsg`: EPSG:28992 (Dutch RD), EPSG:2056 (Swiss LV95), EPSG:27700 (British
   National Grid), EPSG:2180 (Poland 1992), EPSG:31370 (Belgian Lambert 72), or the UTM
   zone given apart from the numbers, for example EPSG:32632.
2. Set `target_epsg` for a specific output system.

## Data in the wrong place

1. Points in the sea or on another continent have two usual causes: latitude and longitude
   swapped, or projected values read as degrees.
2. The tool reads swapped values the other way round when it can tell, and warns. Otherwise
   ask the user to confirm the column order.
3. A zipped Shapefile without a .prj is read as WGS 84 longitude and latitude, with a
   warning. If the extent looks wrong, ask which system the data uses, or try the likely
   national grid with `source_epsg` and show the result for the user to confirm.
4. Never guess an EPSG code silently. Say which one you assumed.

## Choosing a CRS

1. Keep WGS 84 (EPSG:4326) for viewing and exchange.
2. For distances or areas, use a local projected CRS. `convert_coordinates` returns
   `recommended_crs` for the first point: in France Lambert 93 (EPSG:2154), elsewhere the
   national grid or the UTM zone of the area.
3. In QGIS, set it as the project CRS, or use Vector > Data Management Tools > Reproject Layer.

## What the answer must contain

- The result in a few lines, with any warning from the tool.
- The download links exactly as the tool returned them. Copy each one whole; never retype,
  shorten or rebuild a link, since one changed character breaks it. Shapefile, GeoJSON, KML
  and CSV open directly in QGIS or any GIS tool by drag and drop.
- The recommended CRS when relevant.
- One line saying results are approximate and not for navigation, surveying or legal boundaries.

Done means: the places, file or coordinates are on the map or converted, with links,
warnings and the CRS when relevant, and any item not found is listed. If the tool cannot
complete the request, report the reason and stop without inventing an output.

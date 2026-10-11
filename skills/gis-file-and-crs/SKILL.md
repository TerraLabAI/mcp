---
name: gis-file-and-crs
description: Check a GIS file or a set of coordinates on a map, convert it to another format, and pick the right coordinate reference system (CRS) for a QGIS project. Use when the user shares a GeoJSON, KML, KMZ, GPX, zipped Shapefile, CSV or WKT file, or gives coordinates in an unknown or national system.
---

# GIS files and coordinate systems

Explicit instructions from the user take priority over this skill.

## Steps for a file

1. Call `open_gis_file` with the uploaded `file`, a public `url`, or the pasted `text`. Files up to 50 MB.
2. Set `convert_to` when the user wants another format: `geojson`, `kml`, `kmz`, `gpx`, `shapefile` or `csv`.
3. Report what the tool returns: format, coordinate system, extent, feature count, geometry types, fields and any warning.
4. If the user will measure distances or areas, continue with the CRS steps below.

## Steps for coordinates

1. Call `convert_coordinates` with `text`, one coordinate per line, up to 1,000 lines.
2. The format of each line is detected. For a national grid the numbers cannot reveal, set `source_epsg`, for example EPSG:28992 (Dutch RD), EPSG:2056 (Swiss LV95), EPSG:27700 (British National Grid), EPSG:2180 (Poland 1992). Also set it for a UTM zone given apart from the numbers, for example EPSG:32632.
3. Set `target_epsg` when the user wants a specific output system.

## Unknown coordinate system

1. A zipped Shapefile without a .prj is read as WGS 84 longitude and latitude, and the tool warns about it. If the extent looks wrong, ask the user which system the data uses.
2. A CSV must have coordinate columns. Check the fields the tool reports. If the values are projected (large numbers), ask the user for the system, then convert the coordinates with `convert_coordinates` and `source_epsg`.
3. Never guess an EPSG code silently. Say which one you assumed.

## Data in the wrong place

1. If points land in the sea or on the wrong continent, check two causes.
2. Swapped latitude and longitude: the tool reads them the other way round when it can tell, and warns. Otherwise ask the user to confirm the column order.
3. Wrong EPSG: the file or the data is in a projected system read as degrees. Ask for the real system, or try the likely national grid with `source_epsg` and show the result on the map for the user to confirm.
4. If coordinates fall outside the valid range, the tool returns `invalid_coordinates`. Explain the two causes above.

## Choosing a CRS for QGIS

1. Keep WGS 84 (EPSG:4326) for viewing and exchange.
2. For distances or areas, use a local projected CRS. `convert_coordinates` returns `recommended_crs` for the first point.
3. In France, use Lambert 93 (EPSG:2154). Elsewhere, use the UTM zone of the area.
4. In QGIS, set it as the project CRS, or use Vector > Data Management Tools > Reproject Layer.

## What the answer must contain

- The checks above in a few lines, with any warning from the tool.
- The download links returned by the tool. Shapefile, GeoJSON, KML and CSV open directly in QGIS by drag and drop.
- The recommended CRS when relevant.
- One line saying results are approximate and not for navigation, surveying or legal boundaries.

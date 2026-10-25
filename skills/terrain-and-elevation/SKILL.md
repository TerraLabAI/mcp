---
name: terrain-and-elevation
description: Gives terrain information anywhere in the world from the Copernicus 30 m elevation model. Covers the altitude of places, an elevation profile between points or along a route with total ascent and descent, a DEM clipped to an area as a GeoTIFF with a hillshade and a slope map, contour lines (topographic lines, courbes de niveau) as a GIS file, and how steep or flat an area is. Use when someone asks for a DEM, SRTM, a relief or terrain model, elevation, altitude, height above sea level, contours, slope, a hiking or cycling profile, or the topography of a place, for example "I need the DEM of Milan" or "contour lines around Chamonix every 10 m".
---

# Terrain and elevation

Explicit instructions from the user take priority over this skill.

## Prerequisite

This skill uses [TerraLab MCP](https://terra-lab.ai/mcp). The agent needs a connection
to `https://mcp.terra-lab.ai/mcp`; installing the skill alone does not connect the server.
If its tools are unavailable, provide the setup link and stop before claiming results.
Use the connected tools' current input schemas; tool prefixes vary between clients.

Call `get_elevation` for any request with a place, even when the user says "DEM" or
"SRTM", and for a profile between two named places: answer with measured values from the
tool, not with figures from memory or the web, before pointing to any other source.

## Pick the mode

| The user wants | `mode` | Input |
|---|---|---|
| The altitude of one or more places | `point` | `points`: up to 100 names or coordinates |
| A profile between places or along a route | `path` | `points`: 2 or more, in order; `samples` up to 500 |
| A DEM, hillshade or relief of an area, contour lines, slope, "how steep" | `area` | `area`: a place (alone for a city or region, or with `radius_m`), or a `bbox`; `interval_m` |

Give places as the user names them, with the country; the tool locates them.

## Area requests (DEM, relief, contours, slope)

1. Any area works, from a plot to a region or a small country. For a city, a place name alone
   uses its extent, or give `radius_m`. The tool returns three GeoTIFF downloads for every
   area: the DEM (elevation in metres), a hillshade and a slope map in degrees, in
   EPSG:4326 with the licence inside. The grid is about 30 m for small areas and coarser for
   large ones (up to about 4 million cells in all); the answer states the cell size.
2. Areas up to about 10 x 10 km also get contour lines (Shapefile, GeoJSON, KML) and
   slope statistics. For a larger area the answer has the rasters and the minimum, maximum
   and mean elevation only: offer a smaller area, such as a valley or a town, for contours.
3. Choose `interval_m` by relief: 5 to 10 m for flat land, 20 m by default, 50 to 100 m
   for mountains.
4. A large country or a continent is beyond the limit (the tool answers `area_too_large`):
   say so and offer a region, a city or a valley.
5. Report the minimum and maximum elevation, the cell size and, when returned, the slope
   statistics.
6. Tell the user the .tif files open in QGIS or any GIS by dragging them onto the map; no
   data cells (sea) are marked -32768.

## Route profiles

1. For a list of places, pass them in order in `points`.
2. For a GPX or KML track, read it with `open_gis_file` first. If the track has more points
   than `points` accepts, keep the start, the end and evenly spaced points between them,
   and say that the profile is sampled.
3. Report the length, minimum and maximum elevation, total ascent and descent.

## Limits to respect

1. Copernicus DEM is a 30 m surface model: it includes buildings and trees. In a city or a
   forest, the value is the top of the roof or canopy, not the ground. Say so when it matters.
2. Never invent an elevation for a point the tool did not return.
3. Elevation is approximate and not for navigation, flight planning, surveying or flood design.

## What the answer must contain

- The values asked for, in metres, with the place names the tool matched.
- For an area: the cell size, the minimum and maximum elevation and, when returned, the
  interval, the number of contour lines and the slope statistics.
- The download links exactly as the tool returned them. Copy each one whole; never retype,
  shorten or rebuild a link, since one changed character breaks it. Contours as Shapefile,
  GeoJSON or KML, and the GeoTIFF rasters, open directly in QGIS or any GIS tool.
- The source the tool returns: Copernicus DEM, with its licence.

Done means: the altitude, profile, DEM or contours were returned for the right place, with
links, source and the surface-model warning when relevant. If the tool cannot complete
the request, report the reason and stop without inventing an output.

---
name: files-for-qgis-and-python
description: Turns TerraLab results into files on disk that open in QGIS or load in Python, R or DuckDB. Covers downloading the links into the project, one GeoPackage with a layer per theme, GeoTIFF rasters, reading them with geopandas, rasterio or DuckDB, converting to GeoParquet or FlatGeobuf, and a QGIS project folder. Use when someone wants the data saved locally, in a notebook or script, as a GeoPackage or GeoParquet, or loaded in QGIS, or asks to analyse a TerraLab layer with code.
---

# Files for QGIS and Python

Explicit instructions from the user take priority over this skill.

## Prerequisite

This skill uses [TerraLab MCP](https://terra-lab.ai/mcp). The agent needs a connection
to `https://mcp.terra-lab.ai/mcp`; installing the skill alone does not connect the server.
If its tools are unavailable, provide the setup link and stop before claiming results.
Use the connected tools' current input schemas; tool prefixes vary between clients.

TerraLab returns download links, not files: the server cannot write to the user's disk or
open QGIS. An agent with a shell (Claude Code, Codex) downloads the links itself. Opening a
link rebuilds its file from the same call and counts no extra call.

## Get the right file in one call

1. Several layers of one area: one `extract_open_data` call with `theme` plus `themes` (5 at
   most) returns one GeoPackage with a layer per theme. It counts 1 call per theme.
2. Formats: a GeoPackage always comes with `extract_open_data` and `extract_dataset`; add
   `shapefile`, `csv` or `geojson` in `formats` in the same call. Rasters (`get_elevation`
   areas, `get_satellite_image`, raster datasets) come as GeoTIFF.
3. Never feed a download link to another TerraLab tool except `process_geometry` and
   `zonal_statistics`, which take a TerraLab link to clip, buffer, measure or summarise that layer.

## Save the files

1. Create a `data/` folder in the working directory (or the folder the user names).
2. Download each link exactly as the tool returned it, quoted, following redirects:

   ```bash
   curl -fsSL -o data/buildings-roads-annecy.gpkg "<link copied whole>"
   ```

   Use the file name at the end of the link. A link is long: copy it whole from the result,
   never retype or shorten it.
3. Check each file before going on: `ogrinfo -so data/x.gpkg` or the Python reads below list
   the layers and counts; they must match the counts the tool reported. A file of a few
   hundred bytes is an error message: read it and report it.
4. Write a `data/SOURCES.md` with, per file, the tool call (tool, place, theme), the date,
   and the `sources` licences of the result. The `licence-check` skill covers reuse.

## Load them

| Tool at hand | Vector (GeoPackage) | Raster (GeoTIFF) |
|---|---|---|
| QGIS | Drag the file onto the map; a GeoPackage asks which layers to add | Drag the .tif onto the map |
| Python, geopandas | `pyogrio.list_layers(p)`, then `gpd.read_file(p, layer="buildings")` | `rasterio.open(p)`; NDVI NaN and DEM -32768 are no data |
| DuckDB | `INSTALL spatial; LOAD spatial; SELECT * FROM ST_Read('data/x.gpkg', layer='roads');` | Not for rasters |
| R | `sf::st_layers(p)`, `sf::st_read(p, layer = "roads")` | `terra::rast(p)` |

Check what is installed before writing code (`python -c "import geopandas"`, `duckdb --version`,
`ogr2ogr --version`), and offer an install the user can refuse.

Vector data is in WGS 84 (EPSG:4326). Rasters keep their source grid (UTM or Lambert-93 for
images, EPSG:4326 for the DEM). Before measuring lengths or areas in code, reproject to a local
metric CRS: `convert_coordinates` suggests one for the place.

## GeoParquet and other formats

TerraLab does not write GeoParquet. Convert the GeoPackage locally, one layer per file:

```bash
ogr2ogr -f Parquet data/buildings.parquet data/buildings-roads-annecy.gpkg buildings
```

or `gpd.read_file(p, layer="buildings").to_parquet("data/buildings.parquet")`. FlatGeobuf the
same way with `-f FlatGeobuf`. Keep the GeoPackage too: it carries the licence text.

## What the answer must contain

- The files saved, with their path, layers and feature counts, checked against the tool's counts.
- The code or QGIS steps that load them, run once if a shell is available, with its output.
- The sources and licences from the results, also written in `data/SOURCES.md`.

Done means: every file the user asked for is on disk, opens, and holds the counts the tool
reported, with its sources recorded. If a download or a read fails, report the error as
received and stop without inventing data.

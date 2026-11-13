---
name: buildings-and-heights
description: Gets building footprints for any place in the world, with their use and, where known, height, and in France the measured height, floors, main use and year built of each building around an address. Covers counting buildings, the built-up area, the tallest buildings, a 3D or shadow study input, urban density, and a building layer for QGIS. Use when someone asks for buildings, footprints, building heights, how tall or how old the buildings are, or how built-up a place is.
---

# Buildings and heights

Explicit instructions from the user take priority over this skill.

## Prerequisite

This skill uses [TerraLab MCP](https://terra-lab.ai/mcp). The agent needs a connection
to `https://mcp.terra-lab.ai/mcp`; installing the skill alone does not connect the server.
If its tools are unavailable, provide the setup link and stop before claiming results.
Use the connected tools' current input schemas; tool prefixes vary between clients.

Each call below counts as 1 call on the TerraLab account; `count_only` counts none, and a call
that finds nothing or fails on TerraLab's side is given back.

## Pick the tool

| The user wants | Tool | Area |
|---|---|---|
| Heights in metres, floors, use, year built, in France | `french_building_heights` | `radius_m` up to 2,000 (default 150), or a `bbox` up to 16 km² |
| Footprints anywhere, a count, built-up area | `extract_open_data` with `theme: "buildings"` | up to 20,000 buildings, about 1 km radius in a town centre |
| Buildings plus roads or land use of the same area | `extract_open_data` with `theme` and `themes` | one GeoPackage, a layer per theme |

Outside France, heights come only with the footprints that carry `height` or `num_floors`
(Overture Maps, from OpenStreetMap and national sources); say how many of the buildings
returned have one, and never fill the others with a guess such as 3 m per floor unless the
user asks for that estimate and you label it.

## Steps

1. Name the place with its country; the tools locate it. For a whole town, run
   `extract_open_data` with `count_only: true` first: it says whether the area fits one
   extract, at no cost.
2. Too many buildings (`area_too_large`): send `retry_with` as it is, or split the town into
   districts, one call each, and say so.
3. In France, when the user asks about heights or floors, call `french_building_heights`
   for the site even if a footprint layer already exists: BD TOPO heights are measured, not
   tagged by volunteers.
4. Ask for every format the user needs in the one call: `extract_open_data` always adds a
   GeoPackage; `french_building_heights` offers `shapefile` for QGIS, `csv` for a spreadsheet
   and `geojson` for code.

## What the answer must contain

- The count for the place the user meant, and for heights the summary the tool returns
  (count, median, tallest), with units.
- The share of buildings with no height. A missing height is unknown, never 0. BD TOPO
  measures from the ground to the gutter: a pitched roof rises above it.
- The download links exactly as the tool returned them. Copy each one whole; never retype,
  shorten or rebuild a link, since one changed character breaks it.
- The sources and licences as the tool returns them: IGN BD TOPO (Licence Ouverte 2.0) in
  France; Overture Maps elsewhere, whose buildings mix OpenStreetMap (ODbL), Microsoft and
  Google footprints. For reuse or publication, the `licence-check` skill gives the conditions.
- Footprints crossing the edge of the area come whole: say so when counting.

Done means: the footprints or heights were returned for the right place, with counts, the
share of unknown heights, links and sources. If the tool cannot complete the request, report
the reason and stop without inventing an output.

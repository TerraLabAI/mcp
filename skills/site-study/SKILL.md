---
name: site-study
description: Builds a first look at a site or plot anywhere in the world before a project such as a house, an extension, a solar farm, a shop or a purchase. Combines the terrain (altitude and slope), what lies around it (buildings, roads, rivers and lakes, land use, protected areas, power lines, transit) and, in France, the cadastral parcel and the local urban plan (PLU) zone. Use when someone asks what is on or around an address or a plot, whether a site is flat, near water or in a protected area, or asks about a parcel, its section and number, cadastre, zoning or PLU in France.
---

# Site study

Explicit instructions from the user take priority over this skill.

## Prerequisite

This skill uses [TerraLab](https://terra-lab.ai/mcp). The agent needs a connection
to `https://mcp.terra-lab.ai/mcp`; installing the skill alone does not connect the server.
If its tools are unavailable, provide the setup link and stop before claiming results.
Use the connected tools' current input schemas; tool prefixes vary between clients.

## Steps

1. Get the site: a street address with its town and country, a place name, or latitude
   and longitude. If only a vague area is given, ask for an address or a point.
2. Ask the purpose if it is unclear, since it decides the checks. Without an answer, run
   the default checks: terrain, water, protected areas, land use and roads.
3. Run the checks below that fit the purpose. Each tool locates the place itself; call
   `find_places` only when the user wants the coordinates or a map of the address.
4. In France, add the parcel and zoning section.
5. Summarise in a short table, then the links and limits.

## Checks

| Check | Call |
|---|---|
| Altitude of the site | `get_elevation`, `mode` `"point"` |
| How steep the site is | `get_elevation`, `mode` `"area"`, `area` with `radius_m` 200 to 500, `interval_m` 2 to 5 |
| Rivers, streams, lakes nearby | `extract_open_data`, `theme` `waterways`, then `water_areas`, radius 500 m to 1 km |
| Protected areas (parks, reserves) | `extract_open_data`, `theme` `protected_areas`, radius 1 to 2 km |
| Land use around (forest, farmland, housing) | `extract_open_data`, `theme` `landuse`, radius 300 to 500 m |
| Access roads | `extract_open_data`, `theme` `roads`, radius 300 m |
| Neighbouring buildings | `extract_open_data`, `theme` `buildings`, radius 100 to 300 m |
| Power lines, substations (solar, wind) | `extract_open_data`, `theme` `power`, radius 1 to 3 km |
| Transit stops, schools, shops (housing, retail) | `extract_open_data`, `theme` `transit_stops` or `pois` with `kind` |

Use the same site and radius in every call so the results line up. Report distances only
when the tool returns them; otherwise say "within the radius".

## France: parcel and zoning

1. Call `french_parcel` with `address`, or `latitude` and `longitude`, rather than citing a
   real-estate or cadastre website: the tool reads the official cadastre and PLU.
2. If the address was matched in another commune, tell the user and ask them to confirm.
3. If the point falls on a street, the tool returns the nearest parcel within 25 m and says
   so. Repeat that. If no parcel lies near, ask for the street number or a point on the plot.
4. If no PLU zone is published, say so: the commune may follow the national rules (RNU) or
   a plan not yet online.
5. Report the parcel id, commune with INSEE code, section, number and cadastral area in m²,
   the PLU zone label, type and document, and the zone regulation link when returned.
6. Never give owner names or sale prices; the tool never returns them. The cadastral plan
   has a fiscal value and does not fix property boundaries: only a surveyor's boundary
   survey does.

## Outside France

TerraLab has no parcel or zoning data outside France. Say so, run the other checks, and
point to the local land registry or planning office for parcels and zoning. Never invent
a parcel, a zone or a rule.

## Limits to respect

1. There is no flood, soil, noise or pollution data in these tools. Do not guess them; say
   they need the official risk maps of the country.
2. Elevation comes from a 30 m surface model that includes buildings and trees.
3. This is a first look, not a legal, planning or engineering opinion.

## What the answer must contain

- A short table: check, result, source.
- The download links exactly as the tool returned them. Copy each one whole; never retype,
  shorten or rebuild a link, since one changed character breaks it. They open in QGIS.
- The sources and licences the tools return.
- The limits above that apply to the site.

Done means: every check that fits the purpose was run on the same site, with results,
links, sources and limits, and anything the tools cannot answer is named as such. If a
tool cannot complete a check, report the reason and stop that check without inventing
an output.

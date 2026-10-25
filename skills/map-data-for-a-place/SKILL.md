---
name: map-data-for-a-place
description: Gets open map data for any place in the world as a map, a count and a GIS file, for example for QGIS. Covers administrative boundaries (countries, regions, departments, districts), building footprints, roads, railways, transit stops, addresses, points of interest such as schools, pharmacies or shops, land use, rivers and lakes, power lines and protected areas. Use when someone asks for GIS data, a layer, a shapefile or GeoJSON, OpenStreetMap or Overture data for an area, or simply where or how many of something there are in a place, for example all schools in Kisumu, the departments of Côte d'Ivoire or the buildings of Porto-Vecchio.
---

# Map data for a place

Explicit instructions from the user take priority over this skill.

## Prerequisite

This skill uses [TerraLab MCP](https://terra-lab.ai/mcp). The agent needs a connection
to `https://mcp.terra-lab.ai/mcp`; installing the skill alone does not connect the server.
If its tools are unavailable, provide the setup link and stop before claiming results.
Use the connected tools' current input schemas; tool prefixes vary between clients.

Call the tool rather than sending the user to a download portal, Overpass or a QGIS
plugin: the tool returns the data itself.

## Steps

1. Name the place with its country, and its region when the name is common. Pass it in
   `area.place` of `extract_open_data`; the tool locates it, so `find_places` is not needed.
2. Pick the area. A town, region or country alone: pass the name, no radius. "Around" or
   "near" a point: add `area.radius_m` (about 1 km for a town centre, less for a dense city).
   A box the user gives: `area.bbox` `[west, south, east, north]`.
3. Map the request to one `theme` per call (table below). For several layers, one call each.
4. Narrow with `kind` when the user wants one sort of feature: one English value or up to
   10 in a list, for example `"school"` or `["forest", "meadow", "grass"]`.
5. Set `formats` to what the user will open: `geojson` by default, `shapefile` for tools
   that expect it, `kml` for Google Earth, `csv` for a spreadsheet. List them all in this
   one call; never pass a download link to another tool, except `process_geometry`, which
   takes a TerraLab download link to clip, buffer or measure that layer.
6. Check the place the tool reports before answering (see Wrong place).

| The user asks for | `theme` | Useful `kind` |
|---|---|---|
| Countries, regions, departments, districts, communes, wards | `divisions` | `country`, `region`, `county` (departments, districts), `localadmin`, `locality`, `neighborhood` |
| Border lines only | `boundaries` | |
| Buildings, footprints | `buildings` | |
| Roads, streets, paths | `roads` | `motorway`, `primary`, `residential`, `footway` |
| Railways, tram lines | `railways` | |
| Bus or train stops | `transit_stops` | |
| Bus, hiking or cycling routes | `routes` | |
| Street addresses | `addresses` | |
| Schools, pharmacies, hospitals, shops (OpenStreetMap) | `pois` | `school`, `pharmacy`, `hospital`, `supermarket` |
| Businesses and named places (Overture) | `places` | |
| Land use, forest, farmland, vineyards | `landuse` | `forest`, `farmland`, `vineyard`, `residential` |
| Rivers, streams, canals | `waterways` | |
| Lakes, ponds, reservoirs | `water_areas` | |
| Power lines, substations | `power` | |
| National parks, reserves | `protected_areas` | |

If the user asks what data exists for a project, name the three or four useful themes and
let them choose before extracting several.

## Wrong place

1. Compare the `bbox`, `centre`, `area_km2` and sample names the tool returns with the place
   meant. A region that comes back as a few km² is a village with the same name: "Bretagne,
   France" can match a village in the Indre.
2. Then retry with a more precise name or a `bbox` of the real area, and say which one you used.
3. An extract by name or box keeps every feature that touches the area, so administrative
   units of neighbouring regions or countries come too. Say so, give the attribute that
   tells them apart (`country`, `region`), and the QGIS filter, for example
   `"country" = 'CI'`.
4. If several places share the name, ask which one, or pick the most likely and say so.

## When the area is too large

1. The tool refuses an area above its limit for the theme, or above 20,000 features, with
   `area_too_large`. Say so plainly; never present a partial or invented result as complete.
2. Offer one of: a smaller radius, one district or region instead of the whole country,
   a `kind` filter, or several smaller extracts.

## What the answer must contain

- The feature count, for the place the user meant, and a few sample names or attributes.
- The download links exactly as the tool returned them. Copy each one whole; never retype,
  shorten or rebuild a link, since one changed character breaks it.
- For QGIS users: drag the file into QGIS, or Layer > Add Layer > Add Vector Layer. Data is
  in WGS 84 (EPSG:4326).
- The sources and licences the tool returns, as given.
- One line saying the data is approximate and not for navigation, surveying or legal boundaries.

Done means: the requested layers were extracted for the right place, with counts, links,
sources and any warning. If the tool cannot complete the request, report the reason and
stop without inventing an output.

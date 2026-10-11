---
name: french-site-check
description: Find the cadastral parcel and the local urban plan (PLU) zone for an address or a point in France, with the site elevation when terrain matters. Use when the user asks about a parcel, a plot, its section and number, or the zoning of a site in France.
---

# French site check

Explicit instructions from the user take priority over this skill.

## Steps

1. Get the site. Use a street address in France, or a point with latitude and longitude.
2. Call `french_parcel` with `address`, or with `latitude` and `longitude`.
3. If the user asks about terrain, slope or altitude, call `get_elevation` with `mode` `"point"` and the same point in `points`. For how steep the site is, use `mode` `"area"` with a small `area` around it.
4. Answer with the fields listed below.

## Missing or ambiguous input

1. If the address has no postcode or commune and the tool cannot find it, ask for the postcode or the commune.
2. If the tool says the address was matched in another commune, tell the user and ask them to confirm the place.
3. If the point falls on the street, the tool returns the nearest parcel within 25 m and says so. Repeat that.
4. If no parcel lies near the point (road, square or water), ask for the street number or a point on the plot.
5. If no PLU zone is published, say so. The commune may follow the national rules (RNU) or a plan not yet online.

## Outside France

1. The French cadastre covers France only. If the tool reports the place is outside France, say so.
2. Never invent a parcel, a section or a zone for a place outside France.

## Limits to respect

1. Never give owner names or sale prices. The tool never returns them. Do not suggest where to find them.
2. Say that the cadastral plan has a fiscal value and does not fix property boundaries. Only a surveyor's boundary survey does.
3. Say that the answer does not replace the official urban planning documents. Point to the zone regulation link when the tool returns one.
4. Elevation comes from a 30 m surface model that includes buildings and trees. Results are approximate.

## What the answer must contain

- Parcel id, commune with INSEE code, section, number and cadastral area in m².
- PLU zone label, type and document, or the statement that none is published.
- The point in WGS 84 and in Lambert 93 (EPSG:2154), as returned.
- The elevation, when asked.
- The GeoJSON and KML download links returned by the tool.
- The sources the tool returns: the French cadastre (DGFiP open data), the Geoportail de l'Urbanisme, and Copernicus DEM for elevation.

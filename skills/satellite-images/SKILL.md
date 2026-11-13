---
name: satellite-images
description: Gets a satellite image or aerial photo of an area anywhere in the world as a GeoTIFF, from Sentinel-2 (10 m, a scene every few days) or, in France, IGN orthophotos (about 0.5 m). Covers true colour, false colour and NDVI for vegetation, crop or forest health, a scene for a chosen date or month, and a before/after pair of two dates (flood, fire, harvest, construction). Use when someone asks for a satellite or aerial image, imagery, NDVI, a vegetation map, or how a place looked on a date.
---

# Satellite images

Explicit instructions from the user take priority over this skill.

## Prerequisite

This skill uses [TerraLab MCP](https://terra-lab.ai/mcp). The agent needs a connection
to `https://mcp.terra-lab.ai/mcp`; installing the skill alone does not connect the server.
If its tools are unavailable, provide the setup link and stop before claiming results.
Use the connected tools' current input schemas; tool prefixes vary between clients.

Every image is one `get_satellite_image` call and counts as 10 calls on the TerraLab account.
A call that finds no scene or fails on TerraLab's side is given back. Ask for the exact area and
dates before the first call, so the user pays for the image they want, not for retries.

## Pick source, product and size

| The user wants | `source` | `product` | Largest area |
|---|---|---|---|
| A sharp photo of a site in mainland France, no date | `ign_ortho` (default there) | `true_color` | 2 x 2 km, `radius_m` 900 |
| A recent picture anywhere, or on a date | `sentinel2` | `true_color` | 20 x 20 km, `radius_m` 9,500 |
| Vegetation standing out in red (crops, wetlands, burn scars) | `sentinel2` | `false_color` | 20 x 20 km |
| Vegetation health as values from -1 to 1 | `sentinel2` | `ndvi` | 20 x 20 km |

Give the area as `area.place` with the country (and `radius_m`), or `area.bbox`
`[west, south, east, north]`. The tool locates the place itself. An area above the limit is
refused: offer a smaller radius or split it into tiles, one call each, and say what each costs.

## Dates

- No date: the clearest scene of the last 60 days with at most 20 % cloud over the scene; with
  nothing there, the tool goes further back by itself and says so.
- "Latest" or "most recent": the default picks the clearest scene of 60 days, which can be
  weeks old. Set `date_from` 20 days before today and `date_to` today in the first call, so the
  one image is recent; `alternatives` in the answer lists the other scenes and their dates.
- One day: `date`. A month or season: `date_from` and `date_to` (`YYYY-MM-DD`); the tool picks
  the scene clearest over the area itself inside that window.
- When no scene meets the cloud limit, the tool takes the least cloudy one and sets
  `cloud_limit_relaxed`, or one close to the dates and sets `date_widened_days`: report either,
  since the image then has more cloud or another date than asked.
- `no_scene` carries `retry_with` and `why`: send `retry_with` as it is once, then stop.

## Before and after

1. Fix one area for both images: the same `area` object, copied, so the two GeoTIFFs overlap.
2. Call once per date window, before and after the event, with the same `product`.
3. Report both scene dates. A pair 10 days apart in the same season shows the event; a pair
   in different seasons also shows the season, so say so.
4. Figures for the change (mean NDVI, share of area that lost vegetation) need index
   statistics. If the connected tool list has `get_satellite_index`, use it for the figures.
   Otherwise give the two NDVI GeoTIFFs and the QGIS steps below; never estimate a figure by
   looking at the image.

## Reading the file in QGIS or Python

- The GeoTIFF is in the source's projected CRS (UTM for Sentinel-2, Lambert-93 for IGN) with
  the licence inside. Drag it into QGIS; QGIS reprojects it on the fly.
- NDVI is float32, NaN where cloud, shadow, snow or no data. In QGIS: Properties > Symbology >
  Singleband pseudocolor, ramp RdYlGn, min 0, max 0.9. Above about 0.6 is dense vegetation,
  below 0.2 is bare soil, water or built-up land.
- Mean NDVI over a field: QGIS Processing > Zonal statistics with the field polygon, or in
  Python `rasterio` plus `numpy.nanmean` on the band.

## What the answer must contain

- The source, product and scene date the tool used, with the scene id, cloud cover and clear
  share it reports. The IGN service gives no shooting date: say so rather than guessing one.
- The download link exactly as the tool returned it. Copy it whole; never retype, shorten or
  rebuild a link, since one changed character breaks it.
- The licence the tool returns (Copernicus Sentinel data, or IGN Licence Ouverte), as given.
- What the image cannot show: not live, not street level, 10 m pixels for Sentinel-2 (a car
  or a single tree does not show).

Done means: one image per date the user asked for, for the right place, with scene date,
cloud cover, link and licence, or the tool's reason for no image. Never describe the content of
an image you did not receive.

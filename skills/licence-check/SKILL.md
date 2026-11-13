---
name: licence-check
description: Checks whether geodata from TerraLab may be reused for a given purpose, and writes the attribution to paste. Covers internal analysis, a published map or report, redistributing the data itself, a commercial product, and mixing sources, for OpenStreetMap (ODbL), Overture Maps, Copernicus (Sentinel-2, DEM), IGN and Etalab, Creative Commons and catalogue datasets. Use when someone asks whether they can use, publish, share or sell a layer, a map or an image, what licence or credit a dataset needs, or how to cite the sources.
---

# Licence check

Explicit instructions from the user take priority over this skill.

## Prerequisite

This skill uses [TerraLab MCP](https://terra-lab.ai/mcp). The agent needs a connection
to `https://mcp.terra-lab.ai/mcp`; installing the skill alone does not connect the server.
If its tools are unavailable, provide the setup link and stop before claiming results.
Use the connected tools' current input schemas; tool prefixes vary between clients.

The licence comes from the result, never from memory: every TerraLab answer carries a
`sources` list (`name`, `licence`, `url`, and `terms` when the server states them), and
every file carries its licence inside. Reading results already in the conversation counts
no call. A `find_datasets` call with `ids` to read a catalogue dataset's licence counts 1 call.

## Steps

1. **Collect.** List every source behind the work: each `sources` entry of each TerraLab
   result used, the `licence` and `attribution` that `find_datasets` or `extract_dataset`
   quote for a catalogue dataset, and, for a file the user brings from elsewhere, the source
   and licence they name (ask when they do not). If the user names a catalogue dataset with no result yet, call
   `find_datasets` with `ids: ["<id>"]`.
2. **Ask the use** when the user has not said it: internal analysis only, a map or report
   shown to others, the data itself shared or published, or a product sold.
3. **Classify** each source by its licence family with the table below. A licence outside the
   table, `other`, or a missing licence is **unclear**: give the source's own link and stop
   short of a verdict for that source.
4. **Combine.** The strictest condition of all sources applies to the combined work. Data
   that mixes an ODbL source with others and is shared as data stays ODbL.
5. **Write the verdict** per source and for the whole work, then the attribution block.

| Family, as the result names it | Internal use | Map, report, image shown | Data shared or published | Sold in a product |
|---|---|---|---|---|
| ODbL 1.0 (OpenStreetMap, most Overture themes) | Yes | Yes, with "© OpenStreetMap contributors" | Yes, under ODbL, with the licence; a derived database stays ODbL | Yes, same conditions |
| CDLA Permissive 2.0 (Overture places) | Yes | Yes, nothing required on results | Yes, with the licence text | Yes |
| CC BY 4.0, Licence Ouverte 2.0 (Etalab, IGN, French cadastre) | Yes | Yes, with the credit and date | Yes, with the credit | Yes, with the credit |
| Copernicus data terms (Sentinel-2, Copernicus DEM) | Yes | Yes, with "Contains modified Copernicus Sentinel data YEAR" or the DEM credit | Yes, with the credit | Yes, with the credit |
| CC BY-SA | Yes | Yes, with the credit | Yes, under CC BY-SA | Yes, under CC BY-SA |
| CC BY-NC, non-commercial terms | Yes, if not commercial | Only for non-commercial work | Only non-commercial | No |

## What the answer must contain

- One line per source: name, licence as quoted by the result, verdict for the stated use
  (allowed, allowed with conditions, not for this use, unclear) and the conditions.
- The verdict for the combined work and the condition that drives it.
- An attribution block ready to paste on the map or in the report, built from the `licence`
  texts of the results, one line per source, with the dataset date when the result gives one.
- For data shared or published: which licence file must travel with it (ODbL, CDLA text);
  the GeoPackage and GeoTIFF files from TerraLab already carry theirs.
- One closing line: this reads the licences as the sources publish them and is not legal
  advice; for a contract or a sale, the source's own terms page decides.

Done means: every source behind the work has a verdict for the stated use or is marked
unclear with its link, and the attribution block covers every source. Never declare a source
open, or a use allowed, that no result or licence text supports.

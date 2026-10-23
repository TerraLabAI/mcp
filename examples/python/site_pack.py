# /// script
# requires-python = ">=3.10"
# dependencies = ["mcp>=2.3,<3"]
# ///
"""Build a GIS starter pack for any place: buildings, roads, water and terrain files.

    uv run site_pack.py "Porto-Vecchio, Corsica"
    uv run site_pack.py "Kreuzberg, Berlin" --radius 800

Chains four TerraLab tools (find_places, extract_open_data x3, get_elevation),
downloads every file into ./site-pack-<place>/ and writes a summary.md with the
counts, sources and licences. Open the folder in QGIS. No key, no account.
"""
import argparse
import http.client
import asyncio
import gzip
import re
import urllib.request
from pathlib import Path

from mcp import Client

URL = "https://mcp.terra-lab.ai/mcp"
LAYERS = ["buildings", "roads", "waterways"]


def first_line(result) -> str:
    return result.content[0].text.splitlines()[0] if result.content else ""


def save(downloads: list[dict], folder: Path, wanted: set[str]) -> list[str]:
    saved = []
    for d in downloads:
        if d.get("format") not in wanted:
            continue
        target = folder / d["name"]
        # Ask for gzip: GeoJSON shrinks about 10x, which matters on slow links.
        # Retry once if a download is cut off.
        request = urllib.request.Request(d["url"], headers={"Accept-Encoding": "gzip"})
        for attempt in (1, 2):
            try:
                with urllib.request.urlopen(request, timeout=180) as r:
                    body = r.read()
                    if r.headers.get("Content-Encoding") == "gzip":
                        body = gzip.decompress(body)
                target.write_bytes(body)
                break
            except (OSError, http.client.IncompleteRead):
                if attempt == 2:
                    raise
        saved.append(target.name)
    return saved


async def main(place: str, radius: int) -> None:
    folder = Path("site-pack-" + re.sub(r"[^a-z0-9]+", "-", place.lower()).strip("-"))
    folder.mkdir(exist_ok=True)
    summary = [f"# Site pack: {place}", ""]
    sources: dict[str, str] = {}

    async with Client(URL) as client:
        # 1. Resolve the place once, then reuse the point so every layer covers the same area.
        found = await client.call_tool("find_places", {"query": place, "limit": 1})
        places = (found.structured_content or {}).get("places") or []
        if found.is_error or not places:
            raise SystemExit(f"Place not found: {first_line(found)}")
        hit = places[0]
        lat, lon = hit["latitude"], hit["longitude"]
        print(f"Located: {hit['address']} ({lat}, {lon})")
        summary += [f"Located at {lat}, {lon}: {hit['address']}", ""]
        area = {"place": {"latitude": lat, "longitude": lon}, "radius_m": radius}

        # 2. Vector layers from OpenStreetMap and Overture Maps.
        for theme in LAYERS:
            res = await client.call_tool(
                "extract_open_data", {"theme": theme, "area": area, "formats": ["geojson"]}
            )
            data = res.structured_content or {}
            print(f"{theme}: {first_line(res)}")
            summary.append(f"- **{theme}**: {first_line(res)}")
            if res.is_error:
                continue
            files = save(data.get("downloads", []), folder, {"geojson"})
            summary += [f"  - `{f}`" for f in files]
            sources.update({s["name"]: s.get("licence", "") for s in data.get("sources", [])})

        # 3. Terrain: elevation, hillshade and slope GeoTIFFs plus contour lines.
        res = await client.call_tool(
            "get_elevation", {"mode": "area", "area": area, "interval_m": 10}
        )
        data = res.structured_content or {}
        print(f"terrain: {first_line(res)}")
        summary.append(f"- **terrain**: {first_line(res)}")
        if not res.is_error:
            files = save(data.get("downloads", []), folder, {"geotiff", "hillshade", "slope", "geojson"})
            summary += [f"  - `{f}`" for f in files]
            sources.update({s["name"]: s.get("licence", "") for s in data.get("sources", [])})

    summary += ["", "## Sources and licences", ""]
    summary += [f"- {name}: {licence}" for name, licence in sources.items()]
    summary += ["", "Approximate data, not for navigation, surveying or legal boundaries."]
    (folder / "summary.md").write_text("\n".join(summary) + "\n")
    print(f"\nDone: {folder}/ ({len(list(folder.iterdir()))} files). Drag it into QGIS.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("place", help='A place name or address, e.g. "Annecy, France"')
    parser.add_argument("--radius", type=int, default=500, help="Radius in metres (default 500)")
    args = parser.parse_args()
    asyncio.run(main(args.place, args.radius))

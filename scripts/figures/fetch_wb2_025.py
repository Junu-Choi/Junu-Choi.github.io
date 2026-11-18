#!/usr/bin/env python3
"""Fetch official 0.25-degree (1440x721, 2020, Global) probabilistic benchmark
curves from Google Research's WeatherBench 2 Dash endpoint and save compact JSON
for the interactive WeatherBench 2 explorer on the site.
"""

from __future__ import annotations

import base64
import json
import math
import struct
import urllib.request
from pathlib import Path

DASH_ENDPOINT = (
    "https://researchsites.withgoogle.com/weatherbench/probabilistic/_dash-update-component"
)

VARIABLES = [
    ("z500", "Z500", "500 hPa Geopotential", "Geopotential", 500, "m²/s²", 1.0),
    ("mslp", "MSLP", "Sea Level Pressure", "Sea Level Pressure", 850, "Pa", 1.0),
    ("t850", "T850", "850 hPa Temperature", "Temperature", 850, "K", 1.0),
    ("t2m", "T2m", "2m Temperature", "2m Temperature", 850, "K", 1.0),
    ("q700", "Q700", "700 hPa Specific Humidity", "Specific Humidity", 700, "g/kg", 1000.0),
    ("ws850", "WS850", "850 hPa Wind Speed", "Wind Speed", 850, "m/s", 1.0),
    ("ws10", "WS10m", "10m Wind Speed", "10m Wind Speed", 850, "m/s", 1.0),
    ("tp24", "TP24h", "24h Precipitation", "24h Precipitation", 850, "mm", 1000.0),
]

KEEP_TRACES = [
    "Astra vs ERA5",
    "GenCast vs ERA5",
    "GenCast (oper.) vs ERA5",
    "IFS ENS vs ERA5",
]


def decode_array(obj):
    if isinstance(obj, list):
        return obj
    if isinstance(obj, dict) and "bdata" in obj:
        raw = base64.b64decode(obj["bdata"])
        fmt = {
            "f8": "d",
            "f4": "f",
            "i8": "q",
            "i4": "i",
            "i2": "h",
            "i1": "b",
            "u1": "B",
        }[obj["dtype"]]
        count = len(raw) // struct.calcsize(fmt)
        return list(struct.unpack("<" + fmt * count, raw))
    return obj


def query_wb2(
    variable: str,
    level: int,
    metric: str,
    relative: str = "Absolute scores",
    relative_to: str = "IFS ENS vs ERA5",
    scale: float = 1.0,
) -> dict[str, list[list[float]]]:
    payload = {
        "output": "..graph.figure...alert-relative.is_open...alert-seeps.is_open...alert-tbd.is_open..",
        "outputs": [
            {"id": "graph", "property": "figure"},
            {"id": "alert-relative", "property": "is_open"},
            {"id": "alert-seeps", "property": "is_open"},
            {"id": "alert-tbd", "property": "is_open"},
        ],
        "inputs": [
            {"id": "variable", "property": "value", "value": variable},
            {"id": "metric", "property": "value", "value": metric},
            {"id": "level", "property": "value", "value": level},
            {"id": "region", "property": "value", "value": "Global"},
            {"id": "year", "property": "value", "value": "2020"},
            {"id": "resolution", "property": "value", "value": "1440x721"},
            {"id": "relative", "property": "value", "value": relative},
            {"id": "relative_to", "property": "value", "value": relative_to},
            {"id": "markers", "property": "value", "value": [1]},
        ],
        "changedPropIds": ["year.value", "resolution.value"],
        "state": [{"id": "graph", "property": "figure", "value": None}],
    }
    req = urllib.request.Request(
        DASH_ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    fig = data["response"]["graph"]["figure"]
    out: dict[str, list[list[float]]] = {}
    for tr in fig.get("data", []):
        name = tr.get("name")
        if name not in KEEP_TRACES:
            continue
        xs = decode_array(tr.get("x", []))
        ys = decode_array(tr.get("y", []))
        pts = []
        for x_val, y_val in zip(xs, ys):
            if y_val is None or (isinstance(y_val, float) and math.isnan(y_val)):
                continue
            if x_val < 12 or int(x_val) % 12 != 0:
                continue
            pts.append([int(x_val), round(float(y_val) * scale, 4)])
        if pts:
            out[name] = pts
    return out


def main() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    out_file = repo_root / "public" / "figures" / "astra" / "wb2-025.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "benchmark": "WeatherBench 2",
        "year": 2020,
        "resolution": "0.25° (1440×721)",
        "region": "Global",
        "urls": {
            "leaderboard": "https://sites.research.google/gr/weatherbench/",
            "probabilistic": "https://sites.research.google/gr/weatherbench/probabilistic-scores/",
            "deterministic": "https://sites.research.google/gr/weatherbench/deterministic-scores/",
            "scorecards": "https://sites.research.google/gr/weatherbench/scorecards-2020/",
        },
        "models": [
            {
                "key": "Astra vs ERA5",
                "name": "Astra",
                "org": "Seoul National University",
                "init": "ERA5",
                "res": "0.25°",
                "role": "ours",
            },
            {
                "key": "GenCast vs ERA5",
                "name": "GenCast",
                "org": "Google DeepMind",
                "init": "ERA5",
                "res": "0.25°",
                "role": "peer",
            },
            {
                "key": "GenCast (oper.) vs ERA5",
                "name": "GenCast (oper.)",
                "org": "Google DeepMind",
                "init": "Operational IFS",
                "res": "0.25°",
                "role": "oper",
            },
            {
                "key": "IFS ENS vs ERA5",
                "name": "IFS ENS",
                "org": "ECMWF (Physics)",
                "init": "Operational",
                "res": "0.2° → 0.25°",
                "role": "baseline",
            },
        ],
        "variables": [],
    }

    for var_id, short, label, wb_var, lvl, unit, scale in VARIABLES:
        crps_rel = query_wb2(wb_var, lvl, "CRPS", "Compare to model", "IFS ENS vs ERA5", 1.0)
        crps_abs = query_wb2(wb_var, lvl, "CRPS", "Absolute scores", "IFS ENS vs ERA5", scale)
        rmse_rel = query_wb2(wb_var, lvl, "Mean RMSE", "Compare to model", "IFS ENS vs ERA5", 1.0)
        rmse_abs = query_wb2(wb_var, lvl, "Mean RMSE", "Absolute scores", "IFS ENS vs ERA5", scale)
        payload["variables"].append(
            {
                "id": var_id,
                "short": short,
                "label": label,
                "unit": unit,
                "crpsRel": crps_rel,
                "crpsAbs": crps_abs,
                "rmseRel": rmse_rel,
                "rmseAbs": rmse_abs,
            }
        )
        print(f"Fetched {short} ({label})")

    out_file.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
    print(f"Wrote {out_file} ({out_file.stat().st_size} bytes)")


if __name__ == "__main__":
    main()

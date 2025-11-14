#!/usr/bin/env python3
"""Utility to download a small ERA5 or CAMS slice for Aurora quick starts.

Requires:
    pip install cdsapi

Before running:
     1. Create an account at https://cds.climate.copernicus.eu/ (ERA5)
         or https://ads.atmosphere.copernicus.eu/ (CAMS).
     2. Accept the terms of use for the datasets you plan to download.
     3. Set credentials via environment variables (preferred):
          export CDS_API_KEY="<UID>:<API_KEY>"
          # Optional if you use a mirrored endpoint
          export CDS_API_URL="https://cds.climate.copernicus.eu/api"
         Existing ~/.cdsapirc or ~/.adsapirc files still work if you already have them configured.

Example:
    python download_era5_subset.py \
        --dataset reanalysis-era5-single-levels \
        --variables 2m_temperature 10m_u_component_of_wind 10m_v_component_of_wind mean_sea_level_pressure \
        --year 2024 --month 08 --days 15 16 \
        --hours 00 06 12 18 \
        --area 35 -75 20 -55 \
        --target data/era5-surface.nc

Switch --dataset to "reanalysis-era5-pressure-levels" and add --levels if you
need the atmospheric cube. For CAMS, change --dataset to
"cams-global-atmospheric-composition-forecasts" and point the --api-url flag
at the ADS endpoint.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path


DEFAULT_CDS_API_URL = "https://cds.climate.copernicus.eu/api"
DEFAULT_ADS_API_URL = "https://ads.atmosphere.copernicus.eu/api"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download ERA5/CAMS subset for Aurora")
    parser.add_argument("--dataset", required=True, help="CDS/ADS dataset name")
    parser.add_argument(
        "--variables", nargs="+", required=True, help="Variables to request"
    )
    parser.add_argument("--year", required=True, help="Year (YYYY)")
    parser.add_argument("--month", required=True, help="Month (MM)")
    parser.add_argument(
        "--days", nargs="+", required=True, help="Days of month (DD ...)"
    )
    parser.add_argument(
        "--hours",
        nargs="+",
        default=["00", "06", "12", "18"],
        help="Hours (HH ...) in UTC",
    )
    parser.add_argument(
        "--area",
        nargs=4,
        type=float,
        metavar=("NORTH", "WEST", "SOUTH", "EAST"),
        help="Bounding box (degrees) for subsetting",
    )
    parser.add_argument(
        "--levels",
        nargs="+",
        help="Pressure levels (hPa) when using pressure-level datasets (e.g. 1000 850 500)",
    )
    parser.add_argument(
        "--leadtime",
        nargs="+",
        help="Leadtime hours (needed for CAMS forecasts, e.g. 0 3 6)",
    )
    parser.add_argument(
        "--api-url",
        "--auth-url",
        dest="api_url",
        default=None,
        help="Override API URL (use ADS endpoint for CAMS datasets)",
    )
    parser.add_argument("--target", required=True, help="Output NetCDF/ZIP path")
    return parser.parse_args()


def infer_default_api_url(dataset: str) -> str:
    dataset_lower = dataset.lower()
    if "cams" in dataset_lower:
        return DEFAULT_ADS_API_URL
    return DEFAULT_CDS_API_URL


def build_request(args: argparse.Namespace) -> dict:
    request = {
        "variable": args.variables,
        "year": args.year,
        "month": args.month,
        "day": args.days,
        "time": args.hours,
        "format": "netcdf",
    }

    if args.area:
        request["area"] = [str(v) for v in args.area]

    if args.levels:
        request["pressure_level"] = args.levels

    if args.leadtime:
        request["leadtime_hour"] = args.leadtime

    # Some datasets require product/type settings; provide sane defaults, allow overrides later if needed.
    if "era5" in args.dataset and "product_type" not in request:
        request["product_type"] = "reanalysis"

    if "cams" in args.dataset and "type" not in request:
        request["type"] = "forecast"

    return request


def main() -> None:
    import cdsapi  # type: ignore  # deferred import; install via `pip install cdsapi`

    args = parse_args()
    target = Path(args.target).expanduser()
    target.parent.mkdir(parents=True, exist_ok=True)

    env_key = os.getenv("CDS_API_KEY") or os.getenv("ADS_API_KEY")
    env_url = os.getenv("CDS_API_URL") or os.getenv("ADS_API_URL")

    default_url = args.api_url or infer_default_api_url(args.dataset)
    client_url = env_url or default_url

    if env_key:
        print("Detected API key in environment; using explicit credential.")
        client = cdsapi.Client(url=client_url, key=env_key)
    else:
        client = cdsapi.Client(url=client_url)
    request = build_request(args)

    print(f"Submitting request to {client_url} for dataset {args.dataset}...")
    for key, value in request.items():
        print(f"  {key}: {value}")

    client.retrieve(args.dataset, request, str(target))
    print(f"Download complete: {target}")


if __name__ == "__main__":
    main()

#!/usr/bin/env -S uv run --script

# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "pypistats",
# ]
# ///

import json
from io import StringIO
from time import sleep

import httpx
from pypistats import recent


def get_last_month_downloads(package_name):
    try:
        results = recent(package_name, "month", format="json")
    except httpx.HTTPStatusError as err:
        print(err)
        sleep(2)
        results = recent(package_name, "month", format="json")

    tmp = json.load(StringIO(results))

    return tmp["data"]["last_month"]


packages = []
packages.extend(["pythran", "meson", "pdm", "mercurial", "pyfftw"])

packages.extend(
    [
        "fluiddyn",
        "transonic",
        "fluidfoam",
        "fluidsim",
        "fluidimage",
        "fluidfft",
        "fluidlab",
        "fluidsimfoam",
        "formattex",
        "formatbibtex",
        "hg-setup",
    ]
)

for name in packages:
    print(f"{name + ':':14s} {get_last_month_downloads(name):8d}")

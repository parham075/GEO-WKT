# GEO-WKT

[![PyPI - Version](https://img.shields.io/pypi/v/wkt.svg)](https://pypi.org/project/wkt)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/wkt.svg)](https://pypi.org/project/wkt)


# Description

**GEO-WKT CLI** is a Hatch-managed Python command-line utility for converting and reprojecting geospatial geometries. The tool supports converting **GeoJSON → WKT**, reading geometries from local or remote **STAC Item** files, and reprojecting **WKT → WKT** to user-defined EPSG coordinate systems.

## Table of Contents

- [Description](#description)
- [Key Features](#key-features)
- [Installation](#installation)
  - [Requirements](#requirements)
  - [Create the Hatch Environment](#create-the-hatch-environment)
- [Usage](#usage)
  - [Display Help](#display-help)
  - [Convert GeoJSON → WKT](#1-convert-geojson--wkt)
  - [Reproject WKT → WKT](#2-reproject-wkt--wkt)
- [Development](#development)
  - [Running the CLI During Development](#running-the-cli-during-development)
- [License](#license)

---

## Key Features

* **GeoJSON to WKT Conversion**
  Convert raw GeoJSON input or extract geometry from STAC Items (local JSON files or HTTP URLs).

* **WKT Reprojection**
  Reproject WKT geometries from the default `EPSG:4326` to any EPSG code specified by the user.


---

## Installation

### Requirements
* Hatch installed:

```bash
pip install hatch
```


### Create the Hatch Environment

```bash
hatch shell
```

---

## Usage

### Display Help

```bash
hatch run wkt --help
```

---

### 1. Convert GeoJSON → WKT

Using a GeoJSON string:

```bash
hatch run wkt \
    --recipe wkt \
    --geo '{"type": "Point", "coordinates": [12.5, 41.9]}'
```

Using a local STAC Item file:

```bash
hatch run wkt --recipe wkt --stac ./item.json
```

Using a remote STAC Item:

```bash
hatch run wkt --recipe wkt --stac https://example.com/stac-item.json
```

---

### 2. Reproject WKT → WKT

Reproject geometry from EPSG:4326 to EPSG:3857:

```bash
hatch run wkt \
    --recipe epsg \
    --geo "POINT (12.5 41.9)" \
    --target-epsg 3857
```


---

## Development

### Running the CLI During Development

```bash
hatch run wkt --help
```


## License

`wkt` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

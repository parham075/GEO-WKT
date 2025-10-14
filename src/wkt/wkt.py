import json
import click
from shapely.geometry import shape
from shapely.ops import transform
from shapely import wkt
import pyproj
from pystac import read_file

@click.command()
@click.option(
    '--geo',
    '-g',
    type=str,
    required=False,
    help='Input geometry. For recipe "wkt" provide GeoJSON string, for "epsg" provide WKT string.'
)
@click.option(
    '--stac',
    '-s',
    type=str,
    required=False,
    help='Path to a STAC item JSON file containing a geometry field (GeoJSON format). Only used for recipe "wkt".'
)
@click.option(
    '--recipe',
    '-r',
    type=click.Choice(['wkt', 'epsg'], case_sensitive=False),
    default='wkt',
    help='Choose output format: "wkt" to convert GeoJSON to WKT, "epsg" to reproject WKT geometry.'
)
@click.option(
    '--target-epsg',
    '-e',
    type=int,
    required=False,
    help='Target EPSG code for reprojection (required if recipe="epsg").'
)
def main(geo, stac, recipe, target_epsg):
    """
    Converts a geometry to WKT format or reprojects a WKT geometry to target EPSG.
    """

    if recipe.lower() == 'wkt':
        # Input is GeoJSON (string) or STAC file with GeoJSON geometry
        if not geo and not stac:
            raise click.UsageError("You must provide either --geo or --stac for recipe 'wkt'")

        if geo:
            try:
                geometry = json.loads(geo)
            except json.JSONDecodeError:
                raise click.BadParameter("Invalid JSON format in --geo")
        elif stac:
            try:
                if "https" in stac:
                    stac_data = read_file(stac)
                    geometry = stac_data.geometry
                else:
                    with open(stac, 'r') as f:
                        stac_data = json.load(f)
                        geometry = stac_data.get("geometry")
                if not geometry:
                    raise click.ClickException("No 'geometry' field found in STAC file.")
            except Exception as e:
                raise click.ClickException(f"Failed to load STAC file: {e}")

        try:
            polygon = shape(geometry)
            print(polygon.wkt)
        except Exception as e:
            raise click.ClickException(f"Failed to parse geometry: {e}")

    elif recipe.lower() == 'epsg':
        # Input is WKT geometry string via --geo
        if not geo:
            raise click.UsageError("You must provide --geo with WKT geometry for recipe 'epsg'")

        if not target_epsg:
            raise click.UsageError("You must provide --target-epsg when using recipe 'epsg'")

        try:
            polygon = wkt.loads(geo)
        except Exception as e:
            raise click.BadParameter(f"Invalid WKT format in --geo: {e}")

        try:
            # Assume input is EPSG:4326 by default (or could add option to specify)
            transformer = pyproj.Transformer.from_crs("EPSG:4326", f"EPSG:{target_epsg}", always_xy=True)
            reprojected_polygon = transform(transformer.transform, polygon)
            print(reprojected_polygon.wkt)
        except Exception as e:
            raise click.ClickException(f"Failed to reproject geometry: {e}")

if __name__ == '__main__':
    main()

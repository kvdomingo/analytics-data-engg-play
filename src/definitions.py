from dagster import Definitions, load_assets_from_package_module

from src.assets import climate_air_quality, fires
from src.resources import RESOURCES

defs = Definitions(
    assets=[
        *load_assets_from_package_module(fires, "fires", "fires"),
        *load_assets_from_package_module(climate_air_quality, "caq", "caq"),
    ],
    resources=RESOURCES,
)

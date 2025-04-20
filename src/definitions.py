from dagster import Definitions, load_assets_from_package_module

from src.assets import fires
from src.assets.cchain.factory import build_cchain_job
from src.resources import RESOURCES
from src.schemas.climate_air_quality import ClimateAirQuality
from src.schemas.climate_atmosphere import ClimateAtmosphere
from src.schemas.disease_pidsr_totals import DiseasePidsrTotals

defs = Definitions.merge(
    build_cchain_job("climate_air_quality", ClimateAirQuality),
    build_cchain_job("climate_atmosphere", ClimateAtmosphere),
    build_cchain_job("disease_pidsr_totals", DiseasePidsrTotals),
    Definitions(
        assets=[
            *load_assets_from_package_module(fires, "fires", "fires"),
        ],
        resources=RESOURCES,
    ),
)

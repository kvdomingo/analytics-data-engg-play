from dagster import Definitions, load_assets_from_package_module

from src.assets import fires
from src.assets.cchain.factory import CCHAIN_DATASETS, build_cchain_job
from src.resources import RESOURCES

defs = Definitions.merge(
    *[build_cchain_job(name, schema) for name, schema in CCHAIN_DATASETS],
    Definitions(
        assets=[
            *load_assets_from_package_module(fires, "fires", "fires"),
        ],
        resources=RESOURCES,
    ),
)

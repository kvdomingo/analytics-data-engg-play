from datetime import datetime
from zoneinfo import ZoneInfo

from dagster import (
    DailyPartitionsDefinition,
    MultiPartitionsDefinition,
    StaticPartitionsDefinition,
)

from src.settings import settings

daily_partitions_def = DailyPartitionsDefinition(
    start_date=datetime(2024, 10, 1, tzinfo=ZoneInfo(settings.DEFAULT_TZ)),
    hour_offset=5,
    timezone=settings.DEFAULT_TZ,
)

country_iso3_partitions_def = StaticPartitionsDefinition(partition_keys=["PHL", "THA"])

country_daily_partitions_def = MultiPartitionsDefinition(
    partitions_defs={
        "country": country_iso3_partitions_def,
        "date": daily_partitions_def,
    }
)

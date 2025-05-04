from datetime import date, datetime
from zoneinfo import ZoneInfo

from asyncpg.pgproto.pgproto import timedelta
from dagster import (
    DailyPartitionsDefinition,
    MultiPartitionsDefinition,
    StaticPartitionsDefinition,
)

from src.settings import settings

daily_partitions_def = DailyPartitionsDefinition(
    start_date=datetime(2025, 2, 1, tzinfo=ZoneInfo(settings.DEFAULT_TZ)),
    timezone=settings.DEFAULT_TZ,
)


def nasa_firms_partitions_def_factory(start_date: date, end_date: date = None):
    return DailyPartitionsDefinition(
        start_date=datetime(
            start_date.year,
            start_date.month,
            start_date.day,
            tzinfo=ZoneInfo(settings.DEFAULT_TZ),
        ),
        end_date=None
        if end_date is None
        else datetime(
            end_date.year,
            end_date.month,
            end_date.day,
            tzinfo=ZoneInfo(settings.DEFAULT_TZ),
        ),
        timezone=settings.DEFAULT_TZ,
    )


nasa_firms_nrt_daily_partitions_def = nasa_firms_partitions_def_factory(
    start_date=date(2025, 2, 1)
)

nasa_firms_archive_daily_partitions_def = nasa_firms_partitions_def_factory(
    start_date=date.today() - timedelta(days=60),
)


country_iso3_partitions_def = StaticPartitionsDefinition(partition_keys=["PHL", "THA"])

country_daily_partitions_def = MultiPartitionsDefinition(
    partitions_defs={
        "country": country_iso3_partitions_def,
        "date": daily_partitions_def,
    }
)

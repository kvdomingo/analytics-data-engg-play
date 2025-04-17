import dagster as dg
import polars as pl
from botocore.response import StreamingBody
from dagster import MetadataValue, TableColumn, TableRecord, TableSchema
from dagster_aws.s3 import S3Resource
from mypy_boto3_s3.client import S3Client

from src.resources import IOManager
from src.schemas.climate_air_quality import ClimateAirQuality


@dg.asset(kinds={"s3"}, io_manager_key=IOManager.S3.value)
def caq__extract(context: dg.AssetExecutionContext, s3: S3Resource) -> list[dict]:
    client: S3Client = s3.get_client()
    data = client.get_object(
        Bucket="datasets",
        Key="project-cchain/climate_air_quality.csv",
    )
    body: StreamingBody = data.get("Body")

    data = pl.read_csv(body.read(), has_header=True, infer_schema=False)

    context.add_output_metadata(
        {
            "dagster/row_count": len(data),
            "preview": MetadataValue.table(
                [TableRecord(d) for d in data.head(10).to_dicts()]
            ),
        }
    )
    return data.to_dicts()


@dg.asset(kinds={"polars"}, io_manager_key=IOManager.S3.value)
def caq__transform(
    context: dg.AssetExecutionContext,
    caq__extract: list[dict],
) -> pl.DataFrame:
    df = pl.from_dicts(caq__extract)
    df = df.with_columns(
        {
            name: pl.col(name).cast(dtype)
            for name, dtype in ClimateAirQuality.to_schema().items()
        }
    )

    context.add_output_metadata(
        {
            "dagster/row_count": len(df),
            "preview": MetadataValue.table(
                [TableRecord(d) for d in df.head(10).to_dicts()],
                schema=TableSchema(
                    [
                        TableColumn(name, dtype.to_python().__name__)
                        for name, dtype in ClimateAirQuality.to_schema().items()
                    ]
                ),
            ),
        }
    )
    return df


@dg.asset(kinds={"duckdb"}, io_manager_key=IOManager.DUCKDB.value)
def caq__load(
    context: dg.AssetExecutionContext,
    caq__transform: pl.DataFrame,
) -> pl.DataFrame:
    df = caq__transform

    context.add_output_metadata(
        {
            "dagster/row_count": len(df),
            "preview": MetadataValue.table(
                [TableRecord(d) for d in df.head(10).to_dicts()]
            ),
        }
    )
    return df

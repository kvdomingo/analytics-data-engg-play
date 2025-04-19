import dagster as dg
import polars as pl
from botocore.response import StreamingBody
from dagster_aws.s3 import S3Resource
from mypy_boto3_s3.client import S3Client

from src.resources import IOManager
from src.schemas.climate_air_quality import ClimateAirQuality


@dg.asset(kinds={"s3", "polars"})
def caq__extract(context: dg.AssetExecutionContext, s3: S3Resource) -> pl.DataFrame:
    client: S3Client = s3.get_client()
    data = client.get_object(
        Bucket="datasets",
        Key="project-cchain/climate_air_quality.csv",
    )
    body: StreamingBody = data.get("Body")

    df = pl.read_csv(body.read(), has_header=True, infer_schema=False)

    context.add_output_metadata(
        {
            "dagster/row_count": len(df),
            "preview": dg.MetadataValue.table(
                [dg.TableRecord(d) for d in df.head(10).to_dicts()]
            ),
        }
    )
    return df


@dg.asset(kinds={"polars"})
def caq__transform(
    context: dg.AssetExecutionContext,
    caq__extract: pl.DataFrame,
) -> pl.DataFrame:
    df = caq__extract.with_columns(
        **{
            name: pl.col(name).cast(dtype)
            for name, dtype in ClimateAirQuality.to_schema().items()
        }
    )

    context.add_output_metadata(
        {
            "dagster/row_count": len(df),
            "preview": dg.MetadataValue.table(
                [
                    dg.TableRecord(d)
                    for d in df.with_columns(date=pl.col("date").cast(pl.String()))
                    .head(10)
                    .to_dicts()
                ],
                schema=dg.TableSchema(
                    [
                        dg.TableColumn(name, dtype.to_python().__name__)
                        for name, dtype in df.schema.items()
                    ]
                ),
            ),
        }
    )
    return df


@dg.asset(kinds={"polars", "duckdb"}, io_manager_key=IOManager.DUCKDB.value)
def climate_air_quality(
    context: dg.AssetExecutionContext,
    caq__transform: pl.DataFrame,
) -> pl.DataFrame:
    df = caq__transform

    context.add_output_metadata(
        {
            "dagster/row_count": len(df),
            "preview": dg.MetadataValue.table(
                [
                    dg.TableRecord(d)
                    for d in df.with_columns(date=pl.col("date").cast(pl.String()))
                    .head(10)
                    .to_dicts()
                ],
                schema=dg.TableSchema(
                    [
                        dg.TableColumn(name, dtype.to_python().__name__)
                        for name, dtype in df.schema.items()
                    ]
                ),
            ),
        }
    )
    return df

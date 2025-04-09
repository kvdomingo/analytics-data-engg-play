import dagster as dg
import polars as pl
from botocore.response import StreamingBody
from dagster import MetadataValue, TableRecord
from dagster_aws.s3 import S3Resource
from mypy_boto3_s3.client import S3Client

from src.resources import IOManager


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
                [TableRecord(**d) for d in data.head(10).to_dicts()]
            ),
        }
    )
    return data.to_dicts()

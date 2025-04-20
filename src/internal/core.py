import polars as pl
from botocore.response import StreamingBody
from dagster import (
    AssetExecutionContext,
    MetadataValue,
    TableColumn,
    TableRecord,
    TableSchema,
)
from dagster_aws.s3 import S3Resource
from mypy_boto3_s3 import S3Client

from src import schemas


def get_csv_from_s3_datasets(path: str, s3: S3Resource) -> bytes:
    client: S3Client = s3.get_client()
    data = client.get_object(
        Bucket="datasets",
        Key=path,
    )
    body: StreamingBody = data.get("Body")
    return body.read()


def cast_schema_types(df: pl.DataFrame, schema: pl.Struct) -> pl.DataFrame:
    return df.with_columns(
        **{name: pl.col(name).cast(dtype) for name, dtype in schema.to_schema().items()}
    )


def emit_standard_df_metadata(df: pl.DataFrame, preview_limit: int = 10) -> dict:
    return {
        "dagster/row_count": len(df),
        "preview": MetadataValue.table(
            [
                TableRecord(d)
                for d in df.with_columns(date=pl.col("date").cast(pl.String()))
                .head(preview_limit)
                .to_dicts()
            ],
            schema=TableSchema(
                [
                    TableColumn(name, dtype.to_python().__name__)
                    for name, dtype in df.schema.items()
                ]
            ),
        ),
    }


def extract_schema_from_partition_key(context: AssetExecutionContext) -> pl.Struct:
    schema_class_name = "".join(
        [
            "".join([s.upper() if i == 0 else s for i, s in enumerate(split)])
            for split in context.partition_key.split("_")
        ]
    )

    if not hasattr(schemas, schema_class_name):
        error = f"No such schema src.schemas.{schema_class_name}"
        context.log.error(error)
        raise ModuleNotFoundError(error)

    return getattr(schemas, schema_class_name)

from datetime import date
from functools import reduce

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


def drop_columns_not_in_schema(df: pl.DataFrame, schema: pl.Struct) -> pl.DataFrame:
    return df.select(schema.to_schema().keys())


def add_missing_columns(df: pl.DataFrame, schema: pl.Struct) -> pl.DataFrame:
    return df.with_columns(
        **{
            name: pl.lit(None).cast(dtype)
            for name, dtype in schema.to_schema().items()
            if name not in df.columns
        }
    )


def schema_transforms(df: pl.DataFrame, schema: pl.Struct) -> pl.DataFrame:
    return reduce(
        lambda x, f: f(x, schema),
        [
            drop_columns_not_in_schema,
            add_missing_columns,
            cast_schema_types,
        ],
        df,
    )


def emit_standard_df_metadata(df: pl.DataFrame, preview_limit: int = 10) -> dict:
    return {
        "dagster/row_count": len(df),
        "preview": MetadataValue.table(
            [
                TableRecord(
                    {k: str(v) if isinstance(v, date) else v for k, v in row.items()}
                )
                for row in df.head(preview_limit).iter_rows(named=True)
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

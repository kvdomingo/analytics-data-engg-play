from collections.abc import Mapping
from datetime import date
from decimal import Decimal

import polars as pl
from botocore.response import StreamingBody
from dagster import (
    AssetExecutionContext,
    MetadataValue,
    MultiPartitionKey,
    TableColumn,
    TableRecord,
    TableSchema,
)
from dagster_aws.s3 import S3Resource
from duckdb.duckdb import DuckDBPyConnection
from mypy_boto3_s3 import S3Client


def get_csv_from_s3_datasets(path: str, s3: S3Resource) -> bytes:
    client: S3Client = s3.get_client()
    data = client.get_object(
        Bucket="datasets",
        Key=path,
    )
    body: StreamingBody = data.get("Body")
    return body.read()


def emit_standard_df_metadata(
    df: pl.DataFrame, preview_limit: int = 10, row_count: int = None
) -> dict:
    records = []
    for row in df.head(preview_limit).iter_rows(named=True):
        record = {}
        for k, v in row.items():
            if isinstance(v, date):
                record[k] = v.isoformat()
            elif isinstance(v, Decimal):
                record[k] = float(v)
            else:
                record[k] = v
        records.append(TableRecord(record))

    return {
        "dagster/row_count": row_count or len(df),
        "preview": MetadataValue.table(
            records,
            schema=TableSchema(
                [
                    TableColumn(name, dtype.to_python().__name__)
                    for name, dtype in df.schema.items()
                ]
            ),
        ),
    }


def get_multi_partition_keys_from_context(
    context: AssetExecutionContext,
) -> Mapping[str, str]:
    partition_keys: MultiPartitionKey = context.partition_key
    return partition_keys.keys_by_dimension


def init_duckdb(conn: DuckDBPyConnection):
    conn.install_extension("spatial")
    conn.load_extension("spatial")

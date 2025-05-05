from typing import Union

from dagster import ConfigurableIOManager, InputContext, OutputContext
from dagster_deltalake import AzureConfig, GcsConfig, LocalConfig, S3Config
from deltalake import DeltaTable
from polars import DataFrame, from_arrow
from pydantic import Field


class DeltaLakePolarsIOManager(ConfigurableIOManager):
    path_prefix: list[str] = []
    storage_config: Union[AzureConfig, S3Config, GcsConfig, LocalConfig] = Field(  # noqa
        discriminator="provider"
    )
    table_config: dict[str, str | None] = {}

    def _get_path(self, context: InputContext | OutputContext) -> str:
        return "/".join([*self.path_prefix, *context.asset_key.path])

    def load_input(self, context: InputContext) -> DataFrame:
        return from_arrow(DeltaTable(self._get_path(context)).to_pyarrow_table())

    def handle_output(self, context: OutputContext, obj: DataFrame) -> None:
        if not DeltaTable.is_deltatable(self._get_path(context)):
            DeltaTable.create(
                self._get_path(context),
                name="__".join(context.asset_key.path),
                schema=obj.schema,
                configuration=self.table_config,
                storage_options=self.storage_config.model_dump(exclude={"provider"}),
            )

        dt = DeltaTable(self._get_path(context))
        (
            dt.merge(
                obj.to_arrow(),
                "src.id = dst.id",
                source_alias="src",
                target_alias="dst",
                error_on_type_mismatch=True,
            )
            .when_matched_update_all()
            .when_not_matched_insert_all()
            .execute()
        )

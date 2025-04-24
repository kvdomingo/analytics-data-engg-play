import dagster as dg
from dagster_dbt import DbtCliResource, dbt_assets, get_asset_key_for_model
from dagster_duckdb import DuckDBResource
from duckdb.duckdb import DuckDBPyConnection

from src.dbt_project import dbt_project
from src.internal.core import emit_standard_df_metadata


@dbt_assets(manifest=dbt_project.manifest_path)
def cchain_dbt_assets(context: dg.AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()


@dg.asset(
    group_name="cchain",
    kinds={"duckdb"},
    deps={
        get_asset_key_for_model([cchain_dbt_assets], "cchain__climate_atmosphere"),
        get_asset_key_for_model([cchain_dbt_assets], "cchain__location"),
    },
    metadata={"schema": dbt_project.name},
)
def cchain__climate_atmosphere_location(
    context: dg.AssetExecutionContext,
    duckdb: DuckDBResource,
):
    conn: DuckDBPyConnection
    with duckdb.get_connection() as conn:
        conn.sql(f"""
        CREATE OR REPLACE VIEW {dbt_project.name}.cchain__climate_atmosphere_location AS (
            SELECT
              ca.id,
              ca.date,
              ca.temperature_ave,
              ca.temperature_min,
              ca.temperature_max,
              ca.heat_index,
              ca.precipitation,
              ca.wind_speed,
              ca.relative_humidity,
              ca.solar_radiance,
              ca.uv_radiance,
              l.adm1_en,
              l.adm1_pcode,
              l.adm2_en,
              l.adm2_pcode,
              l.adm3_en,
              l.adm3_pcode
            FROM {dbt_project.name}.cchain__climate_atmosphere ca
            LEFT JOIN {dbt_project.name}.cchain__location l USING (adm4_pcode)
            ORDER BY date, adm4_pcode
        );
        """)
        df = conn.sql(
            f"SELECT * FROM {dbt_project.name}.cchain__climate_atmosphere_location LIMIT 10"
        ).pl()
        count = conn.sql(
            f"SELECT COUNT(*) AS count FROM {dbt_project.name}.cchain__climate_atmosphere_location"
        ).pl()["count"][0]

    context.add_output_metadata(emit_standard_df_metadata(df, row_count=count))


@dg.asset(
    group_name="cchain",
    kinds={"duckdb"},
    deps={
        get_asset_key_for_model([cchain_dbt_assets], "cchain__disease_pidsr_totals"),
        get_asset_key_for_model([cchain_dbt_assets], "cchain__location"),
    },
    metadata={"schema": dbt_project.name},
)
def cchain__disease_pidsr_location(
    context: dg.AssetExecutionContext,
    duckdb: DuckDBResource,
):
    conn: DuckDBPyConnection
    with duckdb.get_connection() as conn:
        conn.sql(f"""
        CREATE OR REPLACE VIEW {dbt_project.name}.cchain__disease_pidsr_location AS (
            SELECT
              dpt.id,
              dpt.date,
              dpt.disease_icd10_code,
              dpt.disease_common_name,
              dpt.case_total,
              l.adm1_en,
              l.adm1_pcode,
              l.adm2_en,
              l.adm2_pcode,
              l.adm3_en,
              l.adm3_pcode
            FROM {dbt_project.name}.cchain__disease_pidsr_totals dpt
            LEFT JOIN {dbt_project.name}.cchain__location l USING (adm3_pcode)
            ORDER BY date, disease_icd10_code, adm3_pcode
        );
        """)
        df = conn.sql(
            f"SELECT * FROM {dbt_project.name}.cchain__disease_pidsr_location LIMIT 10"
        ).pl()
        count = conn.sql(
            f"SELECT COUNT(*) AS count FROM {dbt_project.name}.cchain__disease_pidsr_location"
        ).pl()["count"][0]

    context.add_output_metadata(emit_standard_df_metadata(df, row_count=count))

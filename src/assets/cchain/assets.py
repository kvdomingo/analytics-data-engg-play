import dagster as dg
from dagster_duckdb import DuckDBResource
from duckdb.duckdb import DuckDBPyConnection

from src.internal.core import emit_standard_df_metadata


@dg.asset(
    group_name="cchain",
    kinds={"duckdb"},
    deps={"cchain__climate_atmosphere", "cchain__location"},
)
def cchain__climate_atmosphere_location(
    context: dg.AssetExecutionContext,
    duckdb: DuckDBResource,
):
    conn: DuckDBPyConnection
    with duckdb.get_connection() as conn:
        conn.sql("""
        CREATE OR REPLACE VIEW public.cchain__climate_atmosphere_location AS (
            SELECT
              ca.uuid,
              ca.date,
              ca.tave,
              ca.tmin,
              ca.tmax,
              ca.heat_index,
              ca.pr,
              ca.wind_speed,
              ca.rh,
              ca.solar_rad,
              ca.uv_rad,
              l.adm1_en,
              l.adm1_pcode,
              l.adm2_en,
              l.adm2_pcode,
              l.adm3_en,
              l.adm3_pcode
            FROM public.cchain__climate_atmosphere ca
            LEFT JOIN public.cchain__location l USING (adm4_pcode)
            ORDER BY date, adm4_pcode
        );
        """)
        df = conn.sql(
            "SELECT * FROM public.cchain__climate_atmosphere_location LIMIT 10"
        ).pl()
        count = conn.sql(
            "SELECT COUNT(*) AS count FROM public.cchain__climate_atmosphere_location"
        ).pl()["count"][0]

    context.add_output_metadata(emit_standard_df_metadata(df, row_count=count))


@dg.asset(
    group_name="cchain",
    kinds={"duckdb"},
    deps={"cchain__disease_pidsr_totals", "cchain__location"},
)
def cchain__disease_pidsr_location(
    context: dg.AssetExecutionContext,
    duckdb: DuckDBResource,
):
    conn: DuckDBPyConnection
    with duckdb.get_connection() as conn:
        conn.sql("""
        CREATE OR REPLACE VIEW public.cchain__disease_pidsr_location AS (
            SELECT
              dpt.uuid,
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
            FROM public.cchain__disease_pidsr_totals dpt
            LEFT JOIN public.cchain__location l USING (adm3_pcode)
            ORDER BY date, disease_icd10_code, adm3_pcode
        );
        """)
        df = conn.sql(
            "SELECT * FROM public.cchain__disease_pidsr_location LIMIT 10"
        ).pl()
        count = conn.sql(
            "SELECT COUNT(*) AS count FROM public.cchain__disease_pidsr_location"
        ).pl()["count"][0]

    context.add_output_metadata(emit_standard_df_metadata(df, row_count=count))


@dg.asset(
    group_name="cchain",
    kinds={"duckdb"},
    deps={cchain__disease_pidsr_location, cchain__climate_atmosphere_location},
)
def cchain__disease_climate_atmosphere(
    context: dg.AssetExecutionContext,
    duckdb: DuckDBResource,
):
    conn: DuckDBPyConnection
    with duckdb.get_connection() as conn:
        conn.sql("""
        CREATE OR REPLACE VIEW public.cchain__disease_climate_atmosphere AS (
            SELECT
              pdl.uuid AS disease_id,
              cal.uuid AS climate_id,
              date,
              cal.tave,
              cal.tmin,
              cal.tmax,
              cal.heat_index,
              cal.pr,
              cal.wind_speed,
              cal.rh,
              cal.solar_rad,
              cal.uv_rad,
              pdl.disease_icd10_code,
              pdl.disease_common_name,
              pdl.case_total,
              pdl.adm1_en,
              pdl.adm1_pcode,
              pdl.adm2_en,
              pdl.adm2_pcode,
              pdl.adm3_en,
              pdl.adm3_pcode
            FROM public.cchain__disease_pidsr_location pdl
            LEFT JOIN public.cchain__climate_atmosphere_location cal USING (date, adm3_pcode)
            ORDER BY date
        );
        """)
        df = conn.sql(
            "SELECT * FROM public.cchain__disease_climate_atmosphere LIMIT 10"
        ).pl()
        count = conn.sql(
            "SELECT COUNT(*) AS count FROM public.cchain__disease_climate_atmosphere"
        ).pl()["count"][0]

    context.add_output_metadata(emit_standard_df_metadata(df, row_count=count))

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
            SELECT *
            FROM public.cchain__climate_atmosphere ca
            LEFT JOIN public.cchain__location l USING (adm4_pcode)
            ORDER BY date
        );
        """)
        df = conn.sql(
            "SELECT * FROM public.cchain__climate_atmosphere_location LIMIT 10"
        ).pl()
        count = conn.sql(
            "SELECT COUNT(*) AS count FROM public.cchain__climate_atmosphere_location"
        ).pl()["count"][0]

    context.add_output_metadata(emit_standard_df_metadata(df, row_count=count))

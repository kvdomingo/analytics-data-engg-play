import dagster as dg
from dagster_duckdb import DuckDBResource


@dg.asset(kinds={"duckdb"})
def gigcal__create_tables(duckdb: DuckDBResource) -> None:
    with duckdb.get_connection() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS ae_de_play.gigcal__accounts (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            platform TEXT NOT NULL,
            account_type TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS ae_de_play.gigcal__posts_raw (
            id TEXT PRIMARY KEY,
            account_id TEXT,
            posted_at TIMESTAMP NOT NULL,
            retrieved_at TIMESTAMP NOT NULL,
            caption TEXT NOT NULL,

            FOREIGN KEY (account_id) REFERENCES ae_de_play.gigcal__accounts(id)
        );
        """)


@dg.asset(kinds={"duckdb"}, deps=[gigcal__create_tables])
def gigcal__scrape_recent_posts_for_accounts(duckdb: DuckDBResource) -> None:
    pass

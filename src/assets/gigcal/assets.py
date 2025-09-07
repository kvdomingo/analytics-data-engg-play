from datetime import datetime
from time import sleep

import dagster as dg
import pandas as pd
from dagster_duckdb import DuckDBResource
from pydantic import ValidationError

from src.assets.gigcal.schemas import AccountPlatform, Post
from src.resources.instagram_api import InstagramApi


@dg.asset(kinds={"duckdb"})
def gigcal__create_tables(duckdb: DuckDBResource) -> None:
    with duckdb.get_connection() as conn:
        conn.sql("""
        INSTALL ulid FROM community;
        LOAD ulid;

        DROP TABLE IF EXISTS ae_de_play.gigcal__posts_raw CASCADE;
        DROP TABLE IF EXISTS ae_de_play.gigcal__accounts CASCADE;
        DROP TYPE IF EXISTS ae_de_play.gigcal__account_category;
        DROP TYPE IF EXISTS ae_de_play.gigcal__platform;

        CREATE TYPE ae_de_play.gigcal__account_category AS ENUM (
            'artist', 'venue', 'production', 'agency', 'event'
        );
        CREATE TYPE ae_de_play.gigcal__platform AS ENUM (
            'instagram'
        );

        CREATE TABLE ae_de_play.gigcal__accounts (
            name TEXT NOT NULL,
            platform ae_de_play.gigcal__platform NOT NULL,
            account_category ae_de_play.gigcal__account_category NOT NULL,

            PRIMARY KEY (name, platform)
        );

        CREATE TABLE ae_de_play.gigcal__posts_raw (
            id TEXT PRIMARY KEY,
            account_name TEXT,
            account_platform ae_de_play.gigcal__platform,
            posted_at TIMESTAMP NOT NULL,
            retrieved_at TIMESTAMP NOT NULL,
            caption TEXT NOT NULL,
            image_url TEXT,
            tagged_accounts STRUCT(
                id TEXT,
                name TEXT
            )[],

            FOREIGN KEY (account_name, account_platform) REFERENCES ae_de_play.gigcal__accounts(name, platform)
        );
        """)


@dg.asset(kinds={"duckdb"}, deps=[gigcal__create_tables])
def gigcal__scrape_recent_posts_for_accounts(
    context: dg.AssetExecutionContext,
    instagram_api: InstagramApi,
    duckdb: DuckDBResource,
) -> None:
    with duckdb.get_connection() as conn:
        accounts = conn.sql("SELECT * FROM ae_de_play.gigcal__accounts").pl()

    parsed_posts: list[Post] = []
    retrieved_at = datetime.now()
    with instagram_api.get_client() as client:
        for account in accounts.iter_rows(named=True):
            res = client.get(
                "/v1/posts", params={"username_or_id_or_url": account["name"]}
            )
            if res.is_error:
                context.log.error(res.text)
                continue
            raw_post = res.json()["data"]["items"]

            for post in raw_post:
                try:
                    parsed_post = Post.model_validate(
                        {
                            **post,
                            "account_platform": AccountPlatform.INSTAGRAM,
                            "retrieved_at": retrieved_at,
                        }
                    )

                    # coerce account_name for instances where account is a co-author but
                    # not the creator of the post
                    parsed_post.account_name = account["name"]
                    parsed_posts.append(parsed_post)
                except ValidationError as e:
                    context.log.error(f"Parsing failed for post: {post}")
                    context.log.error(e)

            sleep(1 / 20)  # IG public rate limit

    if len(parsed_posts) == 0:
        context.log.info("No posts were parsed. Exiting")
        return

    context.log.info(f"Retrieved {len(parsed_posts)} posts")
    serialized_posts = [post.model_dump() for post in parsed_posts]
    serialized_df = pd.DataFrame(data=serialized_posts)  # noqa: F841
    with duckdb.get_connection() as conn:
        conn.sql("""
        INSERT INTO ae_de_play.gigcal__posts_raw
        SELECT * FROM serialized_df
        ON CONFLICT (id) DO NOTHING;
        """)

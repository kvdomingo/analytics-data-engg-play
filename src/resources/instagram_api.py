from contextlib import asynccontextmanager, contextmanager

from dagster import ConfigurableResource
from httpx import AsyncClient, Client


class InstagramApi(ConfigurableResource):
    api_key: str

    def get_common_headers(self):
        return {
            "x-rapidapi-host": "instagram-social-api.p.rapidapi.com",
            "x-rapidapi-key": self.api_key,
        }

    @contextmanager
    def get_client(self):
        yield Client(
            base_url="https://instagram-social-api.p.rapidapi.com",
            headers=self.get_common_headers(),
        )

    @asynccontextmanager
    async def get_async_client(self):
        yield AsyncClient(
            base_url="https://instagram-social-api.p.rapidapi.com",
            headers=self.get_common_headers(),
        )

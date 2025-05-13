from contextlib import asynccontextmanager, contextmanager

from dagster import ConfigurableResource
from fake_useragent import UserAgent
from httpx import AsyncClient, Client

_ua = UserAgent()


class GmaApi(ConfigurableResource):
    base_url: str

    @staticmethod
    def get_common_headers():
        return {
            "Origin": "https://www.gmanetwork.com",
            "Referer": "https://www.gmanetwork.com/",
            "User-Agent": _ua.firefox,
        }

    @contextmanager
    def get_client(self):
        yield Client(base_url=self.base_url, headers=self.get_common_headers())

    @asynccontextmanager
    async def get_async_client(self):
        yield AsyncClient(base_url=self.base_url, headers=self.get_common_headers())

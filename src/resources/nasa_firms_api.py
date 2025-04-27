from dagster import ConfigurableResource
from httpx import AsyncClient

from src.settings import settings


class NasaFirmsApi(ConfigurableResource):
    map_key: str

    async def get_bytes(self, country: str, date: str, satellite_code: str) -> bytes:
        async with AsyncClient(base_url=settings.NASA_FIRMS_BASE_URL) as client:
            res = await client.get(
                f"/api/country/csv/{self.map_key}/VIIRS_{satellite_code.upper()}_NRT/{country}/1/{date}"
            )
            res.raise_for_status()
            return res.content

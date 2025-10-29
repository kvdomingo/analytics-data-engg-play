from datetime import datetime

from pydantic import AnyHttpUrl, BaseModel


class GraphicsCardVariant(BaseModel):
    id: str
    source_domain: str
    source_id: str
    source_created_at: datetime
    source_updated_at: datetime
    title: str
    description: str
    brand: str
    images: list[AnyHttpUrl]


class GraphicsCardProduct(BaseModel):
    id: str
    source_domain: str
    source_id: str
    source_created_at: datetime
    source_updated_at: datetime
    title: str
    description: str
    brand: str
    images: list[AnyHttpUrl]

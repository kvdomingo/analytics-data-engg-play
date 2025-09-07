from datetime import datetime
from enum import Enum

from pydantic import (
    AliasPath,
    AnyHttpUrl,
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)


class AccountPlatform(Enum):
    INSTAGRAM = "instagram"


class AccountCategory(Enum):
    ARTIST = "artist"
    VENUE = "venue"
    PRODUCTION = "production"
    AGENCY = "agency"
    EVENT = "event"


class Account(BaseModel):
    name: str
    platform: AccountPlatform
    account_category: AccountCategory | None = Field(None)


class PostTaggedAccount(BaseModel):
    id: str = Field(alias=AliasPath("user", "id"))
    name: str = Field(alias=AliasPath("user", "username"))


class Post(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str
    account_name: str = Field(alias=AliasPath("user", "username"))
    account_platform: str
    posted_at: datetime = Field(alias=AliasPath("taken_at_date"))
    retrieved_at: datetime
    caption: str = Field(alias=AliasPath("caption", "text"))
    image_url: AnyHttpUrl = Field(alias=AliasPath("image_versions", "items"))
    tagged_accounts: list[PostTaggedAccount] = Field(alias=AliasPath("tagged_users"))

    @field_validator("image_url", mode="before")
    def validate_image_url(cls, items):
        max_height = max([i["height"] for i in items])
        return next((it["url"] for it in items if it["height"] == max_height), None)

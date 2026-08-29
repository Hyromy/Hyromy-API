from typing import (
    Any,
)

from pydantic import (
    Field,
    ValidationInfo,
    field_validator,
)
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_ignore_empty=True,
        env_parse_none_str="null",
    )

    # --------------------------
    #      General Settings
    # --------------------------
    DEBUG: bool = Field(default=False)
    DJANGO_SECRET_KEY: str = Field(default="django-secret-key")

    # --------------------------
    #      Network Settings
    # --------------------------
    HOSTS: Any = Field(default_factory=list, validate_default=True)
    CORS_ALLOWED: Any = Field(default_factory=list, validate_default=True)
    CSRF_TRUSTED: Any = Field(default_factory=list, validate_default=True)
    SESSION_DOMAIN: str | None = Field(default=None)
    USE_SSL: bool = Field(default=False)

    # -------------------------
    #     Database Settings
    # -------------------------
    DB_NAME: str | None = Field(default=None)
    DB_USER: str | None = Field(default=None)
    DB_PASS: str | None = Field(default=None)
    DB_HOST: str | None = Field(default=None)
    DB_PORT: int | None = Field(default=None)

    # ---------------------------
    #     GITHUB API SETTINGS
    # ---------------------------
    GH_USERNAME: str = Field(default="Hyromy")
    GH_API_TOKEN: str | None = Field(default=None)

    # ----------------------
    #     CACHE SETTINGS
    # ----------------------
    CACHE_HOST: str = Field(default="localhost")
    CACHE_PORT: int = Field(default=6379)
    CACHE_DB: int = Field(default=0)

    @field_validator("DJANGO_SECRET_KEY")
    @classmethod
    def validate_secret_key(cls, value: str, info: ValidationInfo) -> str:
        if not info.data.get("DEBUG") and len(value) < 64:
            raise ValueError(
                "DJANGO_SECRET_KEY must be at least 64 characters long in production."
            )
        return value

    @field_validator("HOSTS", "CORS_ALLOWED", "CSRF_TRUSTED", mode="before")
    @classmethod
    def parse_comma_separated_list(cls, value: Any, info: ValidationInfo) -> list[str]:
        if isinstance(value, str):
            parsed = [item.strip() for item in value.split(",") if item.strip()]
            if parsed:
                return parsed

        elif isinstance(value, list) and value:
            return value

        return ["*"] if info.data.get("DEBUG", False) else []

    @field_validator("GH_API_TOKEN")
    @classmethod
    def check_gh_token(cls, value: str | None, info: ValidationInfo) -> str | None:
        no_token = value is None
        key = "GH_API_TOKEN"

        if not info.data.get("DEBUG", False) and no_token:
            raise ValueError(f"{key} must to be set in DEBUG=False")

        if no_token:
            print(f"{key} is not set. The request rate will be low")

        return value


config = Config()

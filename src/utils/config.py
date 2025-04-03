"""
Module holding the application configuration.
"""

from functools import lru_cache

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    """
    Application configuration loaded from environment variables.
    """

    # Application
    app_name: str = Field(description="Application name", default="postgres-mcp-server")

    # Database
    db_host: str = Field(description="Postgres Database host URL", default="localhost")
    db_port: int = Field(description="Postgres Database port", default=5432)
    db_user: str = Field(description="Postgres Database user", default="postgres")
    db_password: SecretStr = Field(
        description="Postgres Database password",
        default=SecretStr("postgres-password"),
    )
    db_name: str = Field(description="Postgres Database name", default="postgres")


@lru_cache
def get_config() -> Config:
    return Config()  # type: ignore

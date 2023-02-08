import logging
from pydantic import BaseSettings, Field, validator


class Settings(BaseSettings):
    app_name: str = Field("convergent")
    http_host: str = Field("0.0.0.0")
    http_port: int = Field(8000)
    log_level: str = Field("INFO")

    postgres_host: str
    postgres_port: str
    postgres_user: str
    postgres_password: str
    postgres_database: str

    @validator("log_level")
    def _validate_log_level(cls, v):
        v_upper = v.upper()
        if v_upper not in logging._nameToLevel:
            raise ValueError(f'invalid value "{v}"')
        return v_upper


_settings = None


def init_settings(settings: Settings):
    global _settings
    if _settings is not None:
        raise RuntimeError("settings already initialized")
    _settings = settings


def get_settings():
    if _settings is None:
        raise RuntimeError("settings not initialized")
    return _settings

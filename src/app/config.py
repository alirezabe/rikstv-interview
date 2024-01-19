from cachetools import cached, TTLCache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    clickhouse_host: str
    clickhouse_port: int
    clickhouse_user: str
    clickhouse_password: str
    clickhouse_db: str
    clickhouse_table: str

    class Config:
        env_file = ".env"
        extra = "ignore"


@cached(cache=TTLCache(maxsize=1024, ttl=600))
def get_settings():
    _settings = Settings()
    # _settings.update_secrets()
    return _settings

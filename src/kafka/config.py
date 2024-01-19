import requests
from cachetools import cached, TTLCache
from pydantic_settings import BaseSettings
from typing import List
from provider.vault import Vault


class Settings(BaseSettings):
    kafka_topic_name: str
    kafka_group_id: str
    partitions: int
    replication_factor: int
    bootstrap_servers: List[str]
    clickhouse_host: str
    clickhouse_port: int
    clickhouse_user: str
    clickhouse_password: str
    clickhouse_db: str
    clickhouse_table: str

    # vault_token: str
    # vault_path: List[str]
    # vault_url: Optional[AnyHttpUrl] = None

    class Config:
        env_file = ".env"
        extra = "ignore"

    def update_secrets(self):
        try:
            vault = Vault(self.vault_url, self.vault_token, self.vault_mount_point)
            vault_data = vault.get_keys_for_path(self.vault_path)
            keys = [k for k, v in self.__dict__.items() if v == "VAULT"]
            for i in keys:
                try:
                    setattr(self, i.lower(), vault_data[i])
                except KeyError as exc:
                    raise RuntimeError(f"no {i.lower()} in Vault") from exc

        except requests.exceptions.ConnectionError as exc:
            raise RuntimeError(f"Invalid Vault Url {self.vault_url}") from exc


@cached(cache=TTLCache(maxsize=1024, ttl=600))
def get_settings():
    _settings = Settings()
    # _settings.update_secrets()
    return _settings

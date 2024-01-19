import logging
import os

import hvac.exceptions
from hvac import Client
from hvac.exceptions import VaultError

logger = logging.getLogger("uvicorn.error")


class Vault:
    client: Client = None

    def __init__(self, url=None, token=None, mount_point=None):
        self.mount_point = mount_point
        if "PYTEST_RUN_CONFIG" in os.environ and url is None:
            return
        self.client = Client(url, token)
        if not self.client.is_authenticated():
            raise RuntimeError("Invalid Vault Token")
        if self.client.sys.is_sealed():
            raise RuntimeError("Vault Sealed, Unable to continue")
        try:
            self.client.auth.token.renew_self()
        except hvac.exceptions.VaultError as exc:
            logger.exception("Error in vault")
            raise exc

    def get_keys_for_path(self, vault_path):
        vault_data = {}
        try:
            for path in vault_path:
                data = self.client.secrets.kv.v2.read_secret(mount_point=self.mount_point, path=path)["data"]["data"]
                vault_data.update(data)
            vault_data = {k.lower(): v for k, v in vault_data.items()}
            return vault_data
        except VaultError:
            logger.exception("Error reading data from Vault")
            return vault_data
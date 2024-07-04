"""
secrectsmanager.py

Module with the Class to be used in python modules to decrypt secrets
"""

import os
from .libs.crypto_utils import decrypt_value


class SecretsManager(object):
    """
    Class to decrypt secrets

    1. Create your secrets manager providing to the constructor either:
        - the environment variable with the key value
        - or the key value
    2. Use your secrets manager to decrypt secrets
    """

    def __init__(self, key_env: str = "MKEYPASSWD", key: str = None) -> None:
        """Constructor
        Args:
            key_env (str): The environment variable that holds the key value to decrypt the secrets
            key (str): The key value to decrypt the secrets. If not provided, the key will be taken from the environment variable (default)
        """
        self.key_env = key_env
        self.key = key
        if not self.key:
            self.key = os.getenv(self.key_env)
            if not self.key:
                raise ValueError(
                    f"Error: {self.key_env} is empty. Set the key value in the variable first"
                )

    def decrypt_secret(self, value: str) -> str:
        """Decrypts a secret
        Args:
            value (str): The value to decrypt
        Returns:
            str: The decrypted value
        """
        return decrypt_value(value, self.key)

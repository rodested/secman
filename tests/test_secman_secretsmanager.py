"""
Test cases for the secman specific crypto module

References:
  https://stackoverflow.com/questions/71918703/visual-studio-code-pylance-report-missing-imports
  https://stackoverflow.com/questions/76036074/cannot-debug-test-case-in-vs-code-found-duplicate-in-env-path
"""

import os
import sys
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from secman.secretsmanager import SecretsManager


class TestSecretsManager(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        """Run ONLY ONCE before all tests are run"""
        # Set the environment variable for the master key password
        os.environ["MKEYPASSWD"] = "FQRDX23t2Gp0C_BlpgOLG6-uHLxxAN4P2bl4qrp4sBY="

    def test_secretsmanager_decrypt(self):
        """Validate the decrypt_secret method of the SecretsManager class"""
        mysecman = SecretsManager()
        expected_value = "hello"
        encrypted_value = "gAAAAABmfDNjcB_dUdvMkvrZXCHqTwB2k56wOPsbo-d0roY7igZJWRmjlAEZSyq91TaI4n-lA2Sp3z6OOZZTMTIxYUagPrUa6Q=="
        decrypted_value = mysecman.decrypt_secret(encrypted_value)
        self.assertEqual(decrypted_value, expected_value)


if __name__ == "__main__":
    unittest.main()

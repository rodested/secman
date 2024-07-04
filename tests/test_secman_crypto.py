"""
Test cases for the secman specific crypto module

References:
  https://stackoverflow.com/questions/71918703/visual-studio-code-pylance-report-missing-imports
  https://stackoverflow.com/questions/76036074/cannot-debug-test-case-in-vs-code-found-duplicate-in-env-path
"""

import sys
import os
import unittest
from cryptography.fernet import Fernet
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from secman.libs.crypto_utils import decrypt_value
from secman.libs.crypto_utils import derive_key, encrypt_value
from secman.libs.crypto_utils import is_valid_fernet_key


class TestCrypto_FernetKeyValidation(unittest.TestCase):
    def test_valid_fernet_key(self):
        # Generate a valid Fernet key
        valid_key = Fernet.generate_key()
        self.assertTrue(is_valid_fernet_key(valid_key))

    def test_invalid_fernet_key(self):
        # Use an invalid Fernet key
        invalid_key = b"invalid_key"
        self.assertFalse(is_valid_fernet_key(invalid_key))


class TestCrypto_EncDecWithFernetKey(unittest.TestCase):
    def setUp(self):
        # self.master_key = 'my_master_key'
        self.master_key = Fernet.generate_key().decode()
        self.value = "Hello, World!"

    def test_encryption_decryption(self):
        # Encrypt the value
        encrypted_value = encrypt_value(self.value, self.master_key)
        # Decrypt the value
        decrypted_value = decrypt_value(encrypted_value, self.master_key)
        # Check if the decrypted value is the same as the original value
        self.assertEqual(self.value, decrypted_value)


class TestCrypto_InvalidCustomKey(unittest.TestCase):
    def setUp(self):
        self.master_key = "my_master_key"
        self.value = "Hello, World!"

    def test_encryption_decryption(self):
        with self.assertRaises(Exception):
            # Encrypt the value
            encrypted_value = encrypt_value(self.value, self.master_key)
            # Decrypt the value
            decrypted_value = decrypt_value(encrypted_value, self.master_key)
            # Check if the decrypted value is the same as the original value
            self.assertEqual(self.value, decrypted_value)


class TestEncryption_derived_key(unittest.TestCase):
    def setUp(self):
        self.master_key = "my_master_key"
        self.value = "Hello, World!"
        self.key = derive_key(self.master_key)

    def test_encryption_decryption(self):
        # Encrypt the value
        encrypted_value = encrypt_value(self.value, self.key)
        # Decrypt the value
        decrypted_value = decrypt_value(encrypted_value, self.key)
        # Check if the decrypted value is the same as the original value
        self.assertEqual(self.value, decrypted_value)


if __name__ == "__main__":
    unittest.main()

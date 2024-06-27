import unittest
from cryptography.fernet import Fernet
from libs.crypto_utils import decrypt_value
from libs.crypto_utils import derive_key, encrypt_value
from libs.crypto_utils import is_valid_fernet_key


class TestFernetKeyValidation(unittest.TestCase):
    def test_valid_fernet_key(self):
        # Generate a valid Fernet key
        valid_key = Fernet.generate_key()
        self.assertTrue(is_valid_fernet_key(valid_key))

    def test_invalid_fernet_key(self):
        # Use an invalid Fernet key
        invalid_key = b"invalid_key"
        self.assertFalse(is_valid_fernet_key(invalid_key))


class TestEncryption_fernet_key(unittest.TestCase):
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


class TestEncryption_custom_key(unittest.TestCase):
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

# TODO: Test 01: Secrets file with 3 secrets to encrypt, overwriting original file: 3 secrets must be encrypted
# TODO: Test 02: Secrets file with 2 secrets to encrypt and 1 encrypted, overwriting original file: 2 secrets must be encrypted, 1 kept as is
# TODO: Test 03: Secrets file with 2 secrets to encrypt and 1 encrypted, selecting an output file which does not exist: 2 secrets must be encrypted, 1 kept as is in the original file
# TODO: Test 04: Secrets file with 2 secrets to encrypt and 1 encrypted, selecting an output file and that file exists, no secret to encrypt is the same as the encrypted in the target file, one secret alredy encrypted in the input file: 2 secrets must be encrypted, if any encrypted secret is found in the origin file and in the target file the one in the origin file is the one prevailing, all encrypted secrets in the output file which are not either included encrypted in the origin file must be kept as is
# TODO: Test 05: Secrets file with 2 secrets to encrypt and 1 encrypted, selecting an output file and that file exists, one secret to encrypt is the same as the encrypted in the target file: 2 secrets must be encrypted, , one secret alredy encrypted in the input file: 2 secrets must be encrypted, if any encrypted secret is found in the origin file and in the target file the one in the origin file is the one prevailing, all encrypted secrets in the output file which are not either included encrypted in the origin file must be kept as is

if __name__ == "__main__":
    unittest.main()

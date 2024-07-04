"""
This module provides utility functions for encryption and decryption using the Fernet symmetric encryption algorithm.

It includes functions for generating encryption keys, deriving keys from passwords, checking the validity of Fernet keys,
and encrypting/decrypting values using the Fernet algorithm.

Dependencies:
- cryptography (https://pypi.org/project/cryptography/)

Example usage:
    # Generate a new encryption key
    key = generate_key()

    # Derive a key from a password
    password = "mysecretpassword"
    salt = b'somesaltvalue'
    derived_key = derive_key(password, salt)

    # Check if a key complies with the Fernet key definition
    is_compliant = complies_with_fernet_key_definition(key)

    # Check if a key is a valid Fernet key
    is_valid = is_valid_fernet_key(key)

    # Encrypt a value using a Fernet key
    encrypted_value = encrypt_value("mysecretvalue", key)

    # Decrypt a value using a Fernet key
    decrypted_value = decrypt_value(encrypted_value, key)
"""

import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend


def generate_key():
    """
    Generates a new encryption key using the Fernet symmetric encryption algorithm.

    Returns:
        str: The generated encryption key.
    """
    print(Fernet.generate_key().decode())


def derive_key(password: str, salt: bytes = None):
    """
    Derives a key from the given password and salt using PBKDF2-HMAC algorithm.

    Args:
        password (str): The password to derive the key from.
        salt (bytes, optional): The salt value used in the key derivation process. If not provided, a random salt will be generated.

    Returns:
        bytes: The derived key.

    """
    password = password.encode()  # Convert to type bytes
    salt = salt or os.urandom(16)  # Use provided salt or generate new one

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend(),
    )

    key = base64.urlsafe_b64encode(kdf.derive(password))  # Can only use kdf once
    return key


def complies_with_fernet_key_definition(key):
    """
    Check if a key is a valid Fernet key, as per the Fernet specification

    Parameters:
    key (str): The key to be checked

    Returns:
    bool: True if the key is a valid Fernet key, False otherwise
    """
    try:
        # Decode the key
        decoded_key = base64.urlsafe_b64decode(key)
        # Check if the key is 32 bytes long
        return len(decoded_key) == 32
    except (base64.binascii.Error, TypeError):
        return False


def is_valid_fernet_key(key):
    """
    Check if a key is a valid Fernet key, by attempting to encrypt a test message with it

    Parameters:
    - key (bytes): The key to be checked

    Returns:
    - bool: True if the key is a valid Fernet key, False otherwise
    """
    try:
        fernet = Fernet(key)
        fernet.encrypt(b"test")
        return True
    except Exception:
        return False


def encrypt_value(value, master_key):
    """
    Encrypt a value using the Fernet symmetric encryption algorithm.

    Parameters:
    - value (str): The value to be encrypted.
    - master_key (str): The Fernet key used for encryption.

    Returns:
    - str: The encrypted value.

    Raises:
    - Exception: If the provided master_key is invalid.
    """
    if not complies_with_fernet_key_definition(master_key):
        raise Exception("Invalid Fernet key")
    fernet = Fernet(master_key)
    encrypted_value = fernet.encrypt(value.encode())
    return encrypted_value.decode()


def decrypt_value(encrypted_value, master_key):
    """
    Decrypt a value using the Fernet symmetric encryption algorithm.

    Parameters:
    - encrypted_value (bytes): The encrypted value to be decrypted.
    - master_key (bytes): The Fernet key used for decryption.

    Returns:
    - decrypted_value (str): The decrypted value as a string.

    Raises:
    - Exception: If the provided master_key is not a valid Fernet key.
    """
    if not complies_with_fernet_key_definition(master_key):
        raise Exception("Invalid Fernet key")
    fernet = Fernet(master_key)
    decrypted_value = fernet.decrypt(encrypted_value).decode()
    return decrypted_value

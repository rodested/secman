"""
easysecrets.py

Easy to use secrets manager importer for your project.

*ONLY* works with project_secrets.py
If you want to use this script, you need to have a project_secrets.py file
Otherwise, you will get an ImportError.

If you want to use a different file, you then should use the class
SecretsManager from secman.secretsmanager directly.
"""

import sys
from secman import secretsmanager

try:
    import project_secrets
except ImportError:
    print(
        "Error importing project_secrets. easysecrets ONLY works with project_secrets.py"
    )
    exit(1)

# Initialize the SecretsManager
mysecman = secretsmanager.SecretsManager()


def __decrypt_secret(encrypted_secret):
    """Decrypts the provided secret using the secrets manager."""
    return mysecman.decrypt_secret(encrypted_secret)


def __get_defined_variables():
    """Finds dinamically and Returns the encrypted variables from
    the secrets file."""
    variables_dict = {
        name: value
        for name, value in project_secrets.__dict__.items()
        if not name.startswith("_")
    }
    variables = set(variables_dict.keys())
    return variables


def __get_encrypted_secrets():
    """Finds dinamically and Returns the encrypted variables from
    the secrets file."""
    variables_dict = {
        name: value
        for name, value in project_secrets.__dict__.items()
        if not name.startswith("_")
    }
    secrets = set([key for key in variables_dict if key.endswith("_ENCRYPTED")])
    return secrets


secrets = __get_encrypted_secrets()
decrypted_secrets = set([secret.replace("_ENCRYPTED", "") for secret in secrets])
for secret in secrets:
    secret_name = secret.replace("_ENCRYPTED", "")
    secret_value = __decrypt_secret(getattr(project_secrets, secret))
    setattr(sys.modules[__name__], secret_name, secret_value)

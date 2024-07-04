"""Test cases for the secman command line encryption actions"""

import os
import sys
import unittest
import logging
import subprocess
import shutil
from pathlib import Path
from importlib import util
from .libs import are_files_equal


# TODO: Test 04: Secrets file with 2 secrets to encrypt and 1 encrypted, selecting an output file and that file exists,
# no secret to encrypt is the same as the encrypted in the target file,
# one secret alredy encrypted in the input file: 2 secrets must be encrypted,
# if any encrypted secret is found in the origin file and in the target file the one in the origin file is the one prevailing,
# all encrypted secrets in the output file which are not either included encrypted in the origin file must be kept as is

# TODO: Test 05: Secrets file with 2 secrets to encrypt and 1 encrypted, selecting an output file and that file exists,
# one secret to encrypt is the same as the encrypted in the target file: 2 secrets must be encrypted,
# one secret alredy encrypted in the input file: 2 secrets must be encrypted,
# if any encrypted secret is found in the origin file and in the target file the one in the origin file is the one prevailing,
# all encrypted secrets in the output file which are not either included encrypted in the origin file must be kept as is

# TODO: All generated output files should be written to the tests/output directory,
# and include this directory in the .gitignore file

# TODO: Move the test keys to a separate file and import them in the test cases

# Configure logging when running tests:
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
# Now we can use logging.info(), logging.debug(), logging.error(), etc.
# in our code to print log messages to the console.
# To see the log messages when running the tests, do it with the next parameters:
#   python -m unittest -b -v
#   python -m pytest -v --log-cli-level=INFO


class TestSecmanCLI(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        """Run ONLY ONCE before all tests are run"""
        # Set the environment variable for the master key password
        os.environ["MKEYPASSWD"] = "FQRDX23t2Gp0C_BlpgOLG6-uHLxxAN4P2bl4qrp4sBY="
        # Change the current working directory to src/secman to run the scripts
        os.chdir("src/secman")

    @classmethod
    def tearDownClass(self):
        """Run after all tests are run
        Note: use "tearDown" to run after each test if needed"""
        # Remove the output files:
        output_files = [
            "../../tests/input/project_secrets_test_01inp_encrypted.py",
            "../../tests/input/project_secrets_test_01inp_encrypted_decrypted.py",
            "../../tests/input/project_secrets_test_02inp.py",
            "../../tests/input/project_secrets_test_03inp_encrypted.py",
        ]
        for file in output_files:
            if Path(file).exists():
                Path(file).unlink()

    def test_help_option(self):
        """Run the main file and get the help message"""

        # Run the secman.py script with the -h option to get help
        # with the same Python interpreter that is used to run this test
        result = subprocess.run(
            [sys.executable, "secman.py", "-h"], capture_output=True, text=True
        )
        # Check if the help message is in the output
        self.assertIn("usage:", result.stdout)

    def test_encrypt_file(self):
        """
        Test 01: Secrets file with 3 secrets to encrypt, overwriting original file:
        3 secrets must be encrypted.
        We ensure that the new file has the required keys created.
        """

        # Ensure that we start with the correct file:
        shutil.copyfile(
            "../../tests/input/project_secrets_test_01inp_base.py",
            "../../tests/input/project_secrets_test_01inp.py",
        )
        # Run the secman.py script to encrypt the file:
        result = subprocess.run(
            [
                sys.executable,
                "secman.py",
                "-e",
                "-f",
                "../../tests/input/project_secrets_test_01inp.py",
            ],
            capture_output=True,
            text=True,
        )
        # Check if the encryption was successful:
        self.assertEqual(result.returncode, 0)
        # Check that the encrypted file has the expected keys:
        file_locations = [
            (
                "environment01",
                "../../tests/input/project_secrets_test_01inp_encrypted.py",
            ),
        ]
        variable_names = []
        for name, file_location in file_locations:
            spec = util.spec_from_file_location(name, file_location)
            config = util.module_from_spec(spec)
            spec.loader.exec_module(config)
            variables = {
                name: value
                for name, value in config.__dict__.items()
                if not name.startswith("_")
            }
            variable_names.append(variables)
        # logging.info(variable_names)
        self.assertEqual(len(variable_names[0]), 7)
        expected_keys = set(
            [
                "MASTER_KEY_ENV",
                "AAA",
                "BBB",
                "CCC",
                "AAA_ENCRYPTED",
                "BBB_ENCRYPTED",
                "CCC_ENCRYPTED",
            ]
        )
        variables_dict = {
            name: value
            for name, value in config.__dict__.items()
            if not name.startswith("_")
        }
        keys = set(variables_dict.keys())
        assert (
            keys == expected_keys
        ), f"Keys in variables are not exactly {expected_keys}"
        # Check that the original file has not been changed:
        self.assertTrue(
            are_files_equal(
                "../../tests/input/project_secrets_test_01inp.py",
                "../../tests/input/project_secrets_test_01inp_base.py",
            )
        )

    def test_encrypt_decrypt_file(self):
        """
        Test 01.1: Secrets file with 3 secrets to encrypt, overwriting original file:
        3 secrets must be encrypted
        The original file must be kept as is
        The encrypted file must be decrypted successfully
        The decrypted files has the same keys and values as the original file
        """

        # Ensure that we start with the correct file to encrypt:
        shutil.copyfile(
            "../../tests/input/project_secrets_test_01inp_base.py",
            "../../tests/input/project_secrets_test_01inp.py",
        )
        # Encrypt the file:
        result = subprocess.run(
            [
                sys.executable,
                "secman.py",
                "-e",
                "-f",
                "../../tests/input/project_secrets_test_01inp.py",
            ],
            capture_output=True,
            text=True,
        )
        # Check if the encryption was successful:
        self.assertEqual(result.returncode, 0)
        # Check that the original file has not been changed:
        self.assertTrue(
            are_files_equal(
                "../../tests/input/project_secrets_test_01inp.py",
                "../../tests/input/project_secrets_test_01inp_base.py",
            )
        )
        # Delete the original file and check that decryption doesn't
        # overwrite the original decrypted input file:
        file_path = Path("../../tests/input/project_secrets_test_01inp.py")
        file_path.unlink()
        self.assertFalse(file_path.exists())
        # Decrypt the previously created encrypted file:
        result = subprocess.run(
            [
                sys.executable,
                "secman.py",
                "-d",
                "-f",
                "../../tests/input/project_secrets_test_01inp_encrypted.py",
            ],
            capture_output=True,
            text=True,
        )
        # Check if the decryption was successful:
        self.assertEqual(result.returncode, 0)
        # Check that the decrypted file has the correct keys and values:
        file_locations = [
            (
                "environment01_1_1",
                "../../tests/input/project_secrets_test_01inp_base.py",
            ),
            (
                "environment01_1_2",
                "../../tests/input/project_secrets_test_01inp_encrypted_decrypted.py",
            ),
        ]
        variable_names = []
        for name, file_location in file_locations:
            spec = util.spec_from_file_location(name, file_location)
            config = util.module_from_spec(spec)
            spec.loader.exec_module(config)
            variables = {
                name: value
                for name, value in config.__dict__.items()
                if not name.startswith("_")
            }
            variable_names.append(variables)
        self.assertEqual(len(variable_names), 2)
        expected_keys = set(variable_names[0].keys())
        excepted_keys_new = set(variable_names[1].keys())
        self.assertEqual(expected_keys, excepted_keys_new)
        for key in expected_keys:
            self.assertEqual(variable_names[0][key], variable_names[1][key])

    def test_encrypt_file_2toenc_1enc_overw(self):
        """
        Test 02:
        Secrets file with 2 secrets to encrypt and 1 encrypted, overwriting original file:
        2 secrets must be encrypted, 1 kept as is
        We ensure that the new file has the required keys created.
        """

        # Ensure that we start with the correct file:
        shutil.copyfile(
            "../../tests/input/project_secrets_test_02inp_base.py",
            "../../tests/input/project_secrets_test_02inp.py",
        )
        # Run the secman.py script to encrypt the file:
        result = subprocess.run(
            [
                sys.executable,
                "secman.py",
                "-e",
                "-o",
                "-f",
                "../../tests/input/project_secrets_test_02inp.py",
            ],
            capture_output=True,
            text=True,
        )
        # Check if the encryption was successful:
        self.assertEqual(result.returncode, 0)
        # Check that the encrypted file has the expected keys:
        file_locations = [
            ("environment02.1", "../../tests/input/project_secrets_test_02inp.py"),
            ("environment02.2", "../../tests/input/project_secrets_test_02out.py"),
        ]
        variable_names = []
        for name, file_location in file_locations:
            spec = util.spec_from_file_location(name, file_location)
            config = util.module_from_spec(spec)
            spec.loader.exec_module(config)
            variables = {
                name: value
                for name, value in config.__dict__.items()
                if not name.startswith("_")
            }
            variable_names.append(variables)
        self.assertEqual(len(variable_names), 2)
        expected_keys = set(variable_names[0].keys())
        excepted_keys_new = set(variable_names[1].keys())
        self.assertEqual(expected_keys, excepted_keys_new)
        for key in expected_keys:
            self.assertEqual(bool(variable_names[0][key]), bool(variable_names[1][key]))

    def test_encrypt_file_2toenc_1enc(self):
        """
        Test 03:
        Secrets file with 2 secrets to encrypt and 1 encrypted, selecting an output file which does not exist:
        2 secrets must be encrypted, 1 kept as is in the original file
        We ensure that the new file has the required keys created.
        """

        # Delete the output file if it exists:
        file_delete = Path("../../tests/input/project_secrets_test_03inp_encrypted.py")
        if file_delete.exists():
            file_delete.unlink()
        # Run the secman.py script to encrypt the file:
        result = subprocess.run(
            [
                sys.executable,
                "secman.py",
                "-e",
                "-f",
                "../../tests/input/project_secrets_test_03inp.py",
            ],
            capture_output=True,
            text=True,
        )
        # Check if the encryption was successful:
        self.assertEqual(result.returncode, 0)
        # Check that the encrypted file has the expected keys:
        file_locations = [
            (
                "environment02.1",
                "../../tests/input/project_secrets_test_03inp_encrypted.py",
            ),
            ("environment02.2", "../../tests/input/project_secrets_test_03out.py"),
        ]
        variable_names = []
        for name, file_location in file_locations:
            spec = util.spec_from_file_location(name, file_location)
            config = util.module_from_spec(spec)
            spec.loader.exec_module(config)
            variables = {
                name: value
                for name, value in config.__dict__.items()
                if not name.startswith("_")
            }
            variable_names.append(variables)
        self.assertEqual(len(variable_names), 2)
        expected_keys = set(variable_names[0].keys())
        excepted_keys_new = set(variable_names[1].keys())
        self.assertEqual(expected_keys, excepted_keys_new)
        for key in expected_keys:
            self.assertEqual(bool(variable_names[0][key]), bool(variable_names[1][key]))


if __name__ == "__main__":
    unittest.main()

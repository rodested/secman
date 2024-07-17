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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))


class TestSecmanCLISetter(unittest.TestCase):
    """
    Class which includes the environment set up for the tests
    Subclass from this class to build the specific CLI tests
    """
    @classmethod
    def setUpClass(self):
        """Run ONLY ONCE before all tests are run"""
        # 1. Set the environment variable for the master key password
        os.environ["MKEYPASSWD"] = "FQRDX23t2Gp0C_BlpgOLG6-uHLxxAN4P2bl4qrp4sBY="
        # Change the current working directory to src/secman to run the scripts:
        # os.chdir("src")  # This works, with no need of passing PYTHONPATH
        #
        # 2. Adapt the PYTHONPATH environment variable:
        # Copy the current environment variables:
        self.env = os.environ.copy()
        self.current_dir = os.getcwd()
        # Construct the path to "src" directory correctly for the operating system
        src_path = os.path.join(".", "src")
        # Get the current PYTHONPATH from the environment, defaulting to an empty string if not set
        current_pythonpath = self.env.get("PYTHONPATH", "")
        # Use os.pathsep to get the correct separator for the operating system
        # This ensures the correct separator is used when modifying PYTHONPATH
        new_pythonpath = src_path + (
            os.pathsep + current_pythonpath if current_pythonpath else ""
        )
        # Update the PYTHONPATH in the environment
        self.env["PYTHONPATH"] = new_pythonpath


class TestSecmanCLI(TestSecmanCLISetter):
    @classmethod
    def tearDownClass(self):
        """Run after all tests are run
        Note: use "tearDown" to run after each test if needed"""
        # Remove the output files:
        os.chdir(self.current_dir)
        output_files = [
            "tests/input/project_secrets_test_01inp_encrypted.py",
            "tests/input/project_secrets_test_01inp_encrypted_decrypted.py",
            "tests/input/project_secrets_test_02inp.py",
            "tests/input/project_secrets_test_03inp_encrypted.py",
        ]
        for file in output_files:
            if Path(file).exists():
                Path(file).unlink()

    def test_help_option(self):
        """Run the main file and get the help message"""

        # Run the secman.py script with the -h option to get help
        # with the same Python interpreter that is used to run this test
        # logging.info("\n")
        # logging.info(os.getcwd())
        # logging.info("\n")
        result = subprocess.run(
            [sys.executable, "-m", "secman", "-h"],
            capture_output=True,
            text=True,
            env=self.env,
        )
        # logging.info("\n")
        # logging.info(f'env: {self.env.get("PYTHONPATH", "")}')
        # logging.info("\n")
        # logging.info(os.getcwd())
        # logging.info("\n")
        # logging.info(f"stdout: {result.stderr}")
        # logging.info("\n")
        # logging.info(f"stdout: {result.stdout}")
        # logging.info("\n")
        # Check if the help message is in the output:
        self.assertEqual(result.returncode, 0)
        self.assertIn("usage:", result.stdout)

    def test_encrypt_file(self):
        """
        Test 01: Secrets file with 3 secrets to encrypt, overwriting original file:
        3 secrets must be encrypted.
        We ensure that the new file has the required keys created.
        """

        # Ensure that we start with the correct file:
        shutil.copyfile(
            "tests/input/project_secrets_test_01inp_base.py",
            "tests/input/project_secrets_test_01inp.py",
        )
        # Run the secman.py script to encrypt the file:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "secman",
                "-e",
                "-f",
                "tests/input/project_secrets_test_01inp.py",
            ],
            capture_output=True,
            text=True,
            env=self.env,
        )
        # Check if the encryption was successful:
        self.assertEqual(result.returncode, 0)
        # Check that the encrypted file has the expected keys:
        file_locations = [
            (
                "environment01",
                "tests/input/project_secrets_test_01inp_encrypted.py",
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
                "tests/input/project_secrets_test_01inp.py",
                "tests/input/project_secrets_test_01inp_base.py",
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
            "tests/input/project_secrets_test_01inp_base.py",
            "tests/input/project_secrets_test_01inp.py",
        )
        # Encrypt the file:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "secman",
                "-e",
                "-f",
                "tests/input/project_secrets_test_01inp.py",
            ],
            capture_output=True,
            text=True,
            env=self.env,
        )
        # Check if the encryption was successful:
        self.assertEqual(result.returncode, 0)
        # Check that the original file has not been changed:
        self.assertTrue(
            are_files_equal(
                "tests/input/project_secrets_test_01inp.py",
                "tests/input/project_secrets_test_01inp_base.py",
            )
        )
        # Delete the original file and check that decryption doesn't
        # overwrite the original decrypted input file:
        file_path = Path("tests/input/project_secrets_test_01inp.py")
        file_path.unlink()
        self.assertFalse(file_path.exists())
        # Decrypt the previously created encrypted file:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "secman",
                "-d",
                "-f",
                "tests/input/project_secrets_test_01inp_encrypted.py",
            ],
            capture_output=True,
            text=True,
            env=self.env,
        )
        # Check if the decryption was successful:
        self.assertEqual(result.returncode, 0)
        # Check that the decrypted file has the correct keys and values:
        file_locations = [
            (
                "environment01_1_1",
                "tests/input/project_secrets_test_01inp_base.py",
            ),
            (
                "environment01_1_2",
                "tests/input/project_secrets_test_01inp_encrypted_decrypted.py",
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
            "tests/input/project_secrets_test_02inp_base.py",
            "tests/input/project_secrets_test_02inp.py",
        )
        # Run the secman.py script to encrypt the file:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "secman",
                "-e",
                "-o",
                "-f",
                "tests/input/project_secrets_test_02inp.py",
            ],
            capture_output=True,
            text=True,
            env=self.env,
        )
        # Check if the encryption was successful:
        self.assertEqual(result.returncode, 0)
        # Check that the encrypted file has the expected keys:
        file_locations = [
            ("environment02.1", "tests/input/project_secrets_test_02inp.py"),
            ("environment02.2", "tests/input/project_secrets_test_02out.py"),
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
        file_delete = Path("tests/input/project_secrets_test_03inp_encrypted.py")
        if file_delete.exists():
            file_delete.unlink()
        # Run the secman.py script to encrypt the file:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "secman",
                "-e",
                "-f",
                "tests/input/project_secrets_test_03inp.py",
            ],
            capture_output=True,
            text=True,
            env=self.env,
        )
        # Check if the encryption was successful:
        self.assertEqual(result.returncode, 0)
        # Check that the encrypted file has the expected keys:
        file_locations = [
            (
                "environment02.1",
                "tests/input/project_secrets_test_03inp_encrypted.py",
            ),
            ("environment02.2", "tests/input/project_secrets_test_03out.py"),
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


class TestSecmanCLIExamples(TestSecmanCLISetter):
    def tearDown(self):
        """Run after each test is run

        Eventually, deleting the files after each test has proven
        to be necessary to avoid conflicts between tests, as the
        underlying OS (windows) was not releasing the files
        """
        # Remove the output files:
        os.chdir(self.current_dir)
        output_files = [
            "tests/output/existing_secrets.py",
            "tests/output/new_secrets.py",
            "tests/output/project_secrets.py",
        ]
        for file in output_files:
            if Path(file).exists():
                Path(file).unlink()

    def test_example_with_existing_file(self):
        """
        Test 04:
        Try to create an example project_secrets.py file, but the file
        already exists.
        Should return an error and do not overwrite the existing file.
        """
        os.chdir(self.current_dir)
        # Create a dummy file to simulate an existing file
        existing_file = "tests/output/existing_secrets.py"
        with open(existing_file, "w") as f:
            f.write("This is an existing file")

        # Run the secman.py script to export secrets
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "secman",
                "-x",
                "-f",
                existing_file,
            ],
            capture_output=True,
            text=True,
            env=self.env,
        )
        # Check if the export failed and returned 1
        self.assertEqual(result.returncode, 1)
        # Check if the existing file was not overwritten and still contains the original content
        with open(existing_file, "r") as f:
            self.assertEqual(f.read(), "This is an existing file")

    def test_example_with_new_file(self):
        """
        Test 05:
        Creating an example project_secrets.py file
        Before creating the new file, ensure that the file to be created does not exist,
        and delete it if it does
        Ensure that the file is created and contains the expected content
        """
        # Delete the output file if it exists
        new_file = Path("tests/output/new_secrets.py")
        if new_file.exists():
            new_file.unlink()
        if os.path.exists(new_file):
            os.remove(new_file)

        # Run the secman.py script to export secrets
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "secman",
                "-x",
                "-f",
                new_file,
            ],
            capture_output=True,
            text=True,
            env=self.env,
        )

        # Check if the export was successful and the file was generated
        self.assertEqual(result.returncode, 0)
        self.assertTrue(os.path.exists(new_file))
        # Check if the file contains the expected content,
        # just by checking if the MASTER_KEY_ENV is present
        with open(new_file, "r") as f:
            self.assertIn("MASTER_KEY_ENV", f.read())

    def test_example_with_default_file(self):
        """
        Test 06:
        Creating an example project_secrets.py file without providing the "-f" parameter
        Ensure that the default file is created and contains the expected content
        """
        # Change the current working directory to output to create the default file there
        output_dir = Path("tests/output")
        os.chdir(output_dir)
        # Delete the default file if it exists
        default_file = "project_secrets.py"
        if os.path.exists(default_file):
            os.remove(default_file)

        env = os.environ.copy()
        self.current_dir = os.getcwd()
        # Construct the path to "src" directory correctly for the operating system
        src_path = os.path.join("..", "..", "src")
        # Get the current PYTHONPATH from the environment, defaulting to an empty string if not set
        current_pythonpath = env.get("PYTHONPATH", "")
        # Use os.pathsep to get the correct separator for the operating system
        # This ensures the correct separator is used when modifying PYTHONPATH
        new_pythonpath = src_path + (
            os.pathsep + current_pythonpath if current_pythonpath else ""
        )
        # Update the PYTHONPATH in the environment
        env["PYTHONPATH"] = new_pythonpath

        # Run the secman.py script to export secrets without providing the "-f" parameter
        result = subprocess.run(
            [sys.executable, "-m", "secman", "-x"],
            capture_output=True,
            text=True,
            env=env,
        )
        # Check if the export was successful and the default file was generated
        self.assertEqual(result.returncode, 0)
        self.assertTrue(os.path.exists(default_file))
        # Check if the default file contains the expected content,
        # just by checking if the MASTER_KEY_ENV is present
        with open(default_file, "r") as f:
            self.assertIn("MASTER_KEY_ENV", f.read())


if __name__ == "__main__":
    unittest.main()

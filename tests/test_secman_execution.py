import os
import sys
import unittest
import logging
import subprocess
import shutil
from importlib import util, import_module


# TODO: Test 01: Secrets file with 3 secrets to encrypt, overwriting original file: 3 secrets must be encrypted
# TODO: Test 02: Secrets file with 2 secrets to encrypt and 1 encrypted, overwriting original file: 2 secrets must be encrypted, 1 kept as is
# TODO: Test 03: Secrets file with 2 secrets to encrypt and 1 encrypted, selecting an output file which does not exist: 2 secrets must be encrypted, 1 kept as is in the original file
# TODO: Test 04: Secrets file with 2 secrets to encrypt and 1 encrypted, selecting an output file and that file exists, no secret to encrypt is the same as the encrypted in the target file, one secret alredy encrypted in the input file: 2 secrets must be encrypted, if any encrypted secret is found in the origin file and in the target file the one in the origin file is the one prevailing, all encrypted secrets in the output file which are not either included encrypted in the origin file must be kept as is
# TODO: Test 05: Secrets file with 2 secrets to encrypt and 1 encrypted, selecting an output file and that file exists, one secret to encrypt is the same as the encrypted in the target file: 2 secrets must be encrypted, , one secret alredy encrypted in the input file: 2 secrets must be encrypted, if any encrypted secret is found in the origin file and in the target file the one in the origin file is the one prevailing, all encrypted secrets in the output file which are not either included encrypted in the origin file must be kept as is


# Configure logging:
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
# ... now we can use logging.info(), logging.debug(), logging.error(), etc.
# To see the log messages, run the tests with the -s option:
#   python -m unittest -b -v
#   python -m pytest -v --log-cli-level=INFO


class TestSecmanCLI(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        # Set the environment variable for the master key password
        os.environ["MKEYPASSWD"] = "FQRDX23t2Gp0C_BlpgOLG6-uHLxxAN4P2bl4qrp4sBY="
        os.chdir("src/secman")

    def test_help_option(self):
        # Test: Run the main file and get the help message

        # Set the environment variable for the master key password
        # Change the current working directory to src/secman
        # Run the secman.py script with the -h option to get help
        # with the same Python interpreter that is used to run this test
        result = subprocess.run(
            [sys.executable, "secman.py", "-h"], capture_output=True, text=True
        )
        # Check if the help message is in the output
        # logging.info(result.stdout)
        # logging.info(result.stderr)
        # logging.info(sys.path)
        self.assertIn("usage:", result.stdout)

    def test_encrypt_file(self):
        # Test: Encrypt the file at tests/input/project_secrets_test_01inp.py

        # Set the environment variable for the master key password
        # Change the current working directory to src/secman
        # Run the secman.py script to encrypt the file
        # Replace 'source_file_path' and 'destination_file_path' with the actual file paths
        shutil.copyfile(
            "../../tests/input/project_secrets_test_01inp_base.py",
            "../../tests/input/project_secrets_test_01inp.py",
        )
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
        # Check if the encryption was successful
        self.assertEqual(result.returncode, 0)
        # import the module and check the encrypted secrets
        #import_module(../../tests/input/project_secrets_test_01inp.py)
        #config = sys.modules[module_name]
        #
        # spec1 = util.spec_from_file_location("ev1", "../../tests/input/project_secrets_test_01out.py")
        # config1 = util.module_from_spec(spec1)
        # spec1.loader.exec_module(config1)
        # variable_names1 = [name for name, value in config1.__dict__.items() if not name.startswith('_')]
        # logging.info(variable_names1)
        # spec2 = util.spec_from_file_location("ev2", "../../tests/input/project_secrets_test_01inp_encrypted.py")
        # config2 = util.module_from_spec(spec2)
        # spec2.loader.exec_module(config2)
        # variable_names2 = [name for name, value in config2.__dict__.items() if not name.startswith('_')]
        # logging.info(variable_names2)
        # self.assertEqual(variable_names1, variable_names2)
        file_locations = [
            ("ev1", "../../tests/input/project_secrets_test_01out.py"),
            ("ev2", "../../tests/input/project_secrets_test_01inp_encrypted.py")
        ]

        variable_names = []
        for name, file_location in file_locations:
            spec = util.spec_from_file_location(name, file_location)
            config = util.module_from_spec(spec)
            spec.loader.exec_module(config)
            variables = {name: value for name, value in config.__dict__.items() if not name.startswith('_')}
            variable_names.append(variables)
        #logging.info(variable_names)
        self.assertEqual(len(variable_names), 2)
        # self.assertEqual(variable_names[0], variable_names[1])
        # self.assertEqual(variable_names[::2], variable_names[1::2])

    def test_encrypt_decrypt_file(self):
        # Test: Decrypt the file at tests/input/project_secrets_test_01inp_encrypted.py

        # Set the environment variable for the master key password
        # Change the current working directory to src/secman
        # Run the secman.py script to encrypt the file
        # Replace 'source_file_path' and 'destination_file_path' with the actual file paths
        shutil.copyfile(
            "../../tests/input/project_secrets_test_01inp_base.py",
            "../../tests/input/project_secrets_test_01inp.py",
        )
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
        # Check if the encryption was successful
        self.assertEqual(result.returncode, 0)
        # import the module and check the encrypted secrets
        #import_module(../../tests/input/project_secrets_test_01inp.py)
        #config = sys.modules[module_name]
        #
        # spec1 = util.spec_from_file_location("ev1", "../../tests/input/project_secrets_test_01out.py")
        # config1 = util.module_from_spec(spec1)
        # spec1.loader.exec_module(config1)
        # variable_names1 = [name for name, value in config1.__dict__.items() if not name.startswith('_')]
        # logging.info(variable_names1)
        # spec2 = util.spec_from_file_location("ev2", "../../tests/input/project_secrets_test_01inp_encrypted.py")
        # config2 = util.module_from_spec(spec2)
        # spec2.loader.exec_module(config2)
        # variable_names2 = [name for name, value in config2.__dict__.items() if not name.startswith('_')]
        # logging.info(variable_names2)
        # self.assertEqual(variable_names1, variable_names2)
        file_locations = [
            ("ev2", "../../tests/input/project_secrets_test_01inp_encrypted.py")
        ]

        variable_names = []
        for name, file_location in file_locations:
            spec = util.spec_from_file_location(name, file_location)
            config = util.module_from_spec(spec)
            spec.loader.exec_module(config)
            variables = {name: value for name, value in config.__dict__.items() if not name.startswith('_')}
            variable_names.append(variables)
        # logging.info(variable_names)
        # Assert that keys in variables are exactly: AAA, BBB, CCC
        expected_keys = set(["MASTER_KEY_ENV", "AAA", "BBB", "CCC", "AAA_ENCRYPTED", "BBB_ENCRYPTED", "CCC_ENCRYPTED"])
        variables_dict = {name: value for name, value in config.__dict__.items() if not name.startswith('_')}
        logging.info(variables_dict.keys())
        keys = set(variables_dict.keys())
        assert keys == expected_keys, f"Keys in variables are not exactly {expected_keys}"
        # self.assertEqual(variable_names[0], variable_names[1])
        # self.assertEqual(variable_names[::2], variable_names[1::2])
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
        # Check if the encryption was successful
        self.assertEqual(result.returncode, 0)
        file_locations = [
            ("ev1", "../../tests/input/project_secrets_test_01inp_base.py"),
            ("ev2", "../../tests/input/project_secrets_test_01inp.py")
        ]

        variable_names = []
        for name, file_location in file_locations:
            spec = util.spec_from_file_location(name, file_location)
            config = util.module_from_spec(spec)
            spec.loader.exec_module(config)
            variables = {name: value for name, value in config.__dict__.items() if not name.startswith('_')}
            variable_names.append(variables)
        # logging.info(variable_names)
        self.assertEqual(len(variable_names), 2)
        self.assertEqual(variable_names[0], variable_names[1])
        self.assertEqual(variable_names[::2], variable_names[1::2])



if __name__ == "__main__":
    unittest.main()

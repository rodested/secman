"""
Test cases for the secman specific crypto module

References:
  https://stackoverflow.com/questions/71918703/visual-studio-code-pylance-report-missing-imports
  https://stackoverflow.com/questions/76036074/cannot-debug-test-case-in-vs-code-found-duplicate-in-env-path
"""

import os
import sys
import unittest

# Add the src directory to the path to have secman module available
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
# Add the input/variant1 directory to the path to have project_secrets.py available
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "input/variant1"))
)


class TestSecretsManager(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        """Run ONLY ONCE before all tests are run"""
        # Set the environment variable for the master key password
        os.environ["MKEYPASSWD"] = "FQRDX23t2Gp0C_BlpgOLG6-uHLxxAN4P2bl4qrp4sBY="

    def test_easysecrets_works(self):
        """Validate the import and secrets auto discovery of the easysecrets module"""
        from secman import easysecrets

        self.assertEqual(
            easysecrets.secrets, {"AAA_ENCRYPTED", "BBB_ENCRYPTED", "CCC_ENCRYPTED"}
        )
        self.assertEqual(easysecrets.decrypted_secrets, {"AAA", "BBB", "CCC"})
        self.assertEqual(easysecrets.AAA, "hello")
        self.assertEqual(easysecrets.BBB, "bye")
        self.assertEqual(easysecrets.CCC, "secret")


if __name__ == "__main__":
    unittest.main()

README.MD

# secman

[![PyPI version](https://badge.fury.io/py/secman.svg)](https://badge.fury.io/py/secman)
[![Tests](https://github.com/username/project-name/actions/workflows/tests.yml/badge.svg)](https://github.com/username/project-name/actions/workflows/tests.yml)

This is **secman**, a practical and easy to use **sec**rets **man**ager for your python projects.

It allows you to easily and safely manage your project secrets without the need of having them
in clear, and even allowing you to add the secrets to your versioning tracking.

You can use a global password for your secrets, or even configure one password per project.

**secman** provides both:

- a module which you can run to provide you valid cyphering passwords and manage your secrets in the secrets file
- a class which you can import from the module, to decrypt the secrets in your project, in an easy way

## Status

Code is Working.
To see next improvements or request functionalities see the project page and issue tracker in github

## Considerations

### Main Project Folder

- [PROJECT_FOLDER] is the folder which holds the whole project.

You're in the right folder if it's the one containing the folders ".git", "tests" and "src".

## How to Use

### Installation

You can install the project using pip:

```shell
$ pip install secman
```

### Quick Usage

#### Create a valid password using the secman module

Run the next command to get a valid password:

```shell
$ python -m secman -k
```

#### Create an environment variable as main password

Create an environment variable named MKEYPASSWD and assign it the value obtained in the previous step.
I suggest you to add it to your .bashrc or .bash_profile and "source" the file once you have added it.
This is the password that you'll use to cypher and decypher your secrets.

Note: You can use different names for your environment variables, and per project

#### Create a project_secrets.py file and declare your secrets there

This is a python file, so it needs to be valid python code.
Declare the variables you will use here:

- Provide in "MASTER_KEY_ENV" The name of the environment variable containing the password
- The project secrets
  You can also include in independent lines any comments you need. These will be kept.
  Do not include anything else.

Example:

```python
# Generated by secman.py. Do not edit manually, unless you know what you are doing
#  SECRET KEYS file
#
#  Remember to keep copies of your secrets in a safe place
#
#  Note: Only lines not processed by secman.py will be those starting with "#"
#

# This is the name of the environment variable you created in the previuos step
# You can change this per project if you want
MASTER_KEY_ENV = "MKEYPASSWD"

# Declare your project secrets here:
AAA = "hello"
BBB = "bye"
CCC = "secret"
```

#### Cypher your secrets file

Run the module to cypher your secrets, overwriting your original project_secrets.py file:

```shell
$ python -m secman -c -o
```

Now your secrets file is cyphered and safe.
You can check it doing:

```shell
$ cat project_secrets.py
```

Note: The module has more functionality, which you can check by running:

```shell
$ python -m secman -h
```

### Using the cyphered keys in your project

Include a line to import the SecretsManager class, and create your own instance.
Also import your project_secrets.py file.

Then you just need to provide the ciphered values to your SecretsManager instance
and decrypt them.

Note that your python module needs to be able to read the same environment
variable declared in project_secrets.py (in this case MKEYPASSWD).

Example:

```python
import project_secrets
from secman import secretsmanager

# Initialize the SecretsManager
mysecman = secretsmanager.SecretsManager()

# You can define a local function:
def decrypt_secret(encrypted_secret):
    """Decrypts the provided secret using the secrets manager."""
    return mysecman.decrypt_secret(encrypted_secret)

# Read your encrypted secrets:
api_key_ENCRYPTED = project_secrets.api_key_ENCRYPTED
base_url_ENCRYPTED = project_secrets.base_url_ENCRYPTED

# Decrypt the secrets:
api_key = decrypt_secret(api_key_ENCRYPTED)
base_url = decrypt_secret(base_url_ENCRYPTED)(testpackage)

# Now your secrets are decrypted and ready to use
# ... continue with your code here
```

### Documentation

For more information, please refer to the [project documentation](https://github.com/username/project-name).

## Contributing

If you would like to contribute to the project, please follow the guidelines in [CONTRIBUTING.md](https://github.com/rodested/secman/CONTRIBUTING.md).

### Running Tests

You can run the tests using `unittest` or `pytest` from the command line.

```shell
$ python -m unittest
```

If you use pytest:

```shell
$ python -m pytest
```

Also you can run them from VSCode (see subsection below).

### Configuring tests in VSCode

Launch VSCode from the Main Project Folder (or open that folder as the main one for the project).

Then, to configure the "Testing" plugin, select as main folder for the tests the current folder
(the main one, do not select the tests folder) and from this folder then the test suite will
auto detect (auto discover) the tests in the tests folder and apply the correct configuration.
Done this, you'll be able to run tests directly from VSCode, performing all imports properly and
running fine.

Once set, you should be able to run them from VSCode directly.

### Run secman as module when coding

To test the module while you are coding, you can run it from the main project folder,
by providing the next path to PYTHONPATH, and running it:

Example for BASH:

```shell
$> PYTHONPATH="./src" python -m secman -h
```

### Run tests when coding on secman

So, you're coding on secman and want to test what you're doing.

In this case you want to import the secman module or modules within the package which you're
working on, either because they are not included in your python interpreter, or just want to
use this ones instead of the included ones.

You can run them in this way:
```shell
$> PYTHONPATH="./src" python -m unittest
```

```shell
$> PYTHONPATH="./src" python -m pytest
```

### Using PDM as python project manager

PDM allows you to manage the python dependencies and create custom python virtual environments
It even helps you to publish the project to pypi.

#### Set up to run "pdm shell" while having all other pdm commands available

I've included in utils a script you can use in BASH to have the option to run "pdm shell"
to load your pdm set virtual environment.
If you want to use it, source it in your shell, or from your .bashrc or .bashprofile

```shell
$> source utils/pdm_custom_call.sh
```

and now you can run the next to active or activate the environment:

```shell
$> pdm shell
... now the environment is enabled ...
$> deactivate
... and now it is deactivated
```

### Fixing the user providing the code

Sometimes you can mess with the user you're using to provide the code to github
and then need to set the correct user.

For this, you can find the script **utils/change-author.sh**.

1. Copy it to whatever local name -to avoid modifying the provided one-
2. Provide the name and email of the user to correct, and the correct ones
3. Run the script from within the code directory (the one containing the .git dir)
4. Verify the changes with the next line:
   1. `$ git log --pretty=format:"%h - %an <%ae> - %cn <%ce> - %s"`
5. Push the changes doing:
   1. `$ git push --force --tags origin 'refs/heads/*'`

## License

This project is licensed under the [MIT License](https://github.com/rodested/secman/LICENSE).

## Release Notes

### stable-0.1.4
- Documentation improved
- Added utils/change-author.sh
- utils/pdm_custom_shell.sh works in mac os, linux and windows


### stable-0.1.3

- Reviewed all paths, absolute and relative imports, to have all tests working
- Fixing issue with projec_secrets.py import
- Tests updated

### stable-0.1.2

- Reviewed to be launched as module (aka unittest, venv, etc.). Required files added
- Tests modified to work running it as module in the cli (-m)
- Now can be launched as $>python -m secman ... (include the secman folder in the PYTHONPATH)
- Fixes for upload to pypi.org and installation with pip done

### stable-0.1.1

- Added module with class SecretsManager. Create an object from this class and use it to decrypt secrets within your project
- Added tests for SecretsManager
- You can run secman.py from any directory (no import issues when running it), but need to provide full path to the script:
  - ```$> python [PROJECT_FOLDER]/src/secman/secman.py -h```

### stable-0.1.0

- Tests for cli working
- Tests for crypto utils working
- tests runnable from VSCode
- Tests runnable from inside the Main Project Folder:
  - ```[PROJECT_FOLDER] $> python -m unittest```
  - ```[PROJECT_FOLDER] $> python -m pytest```

## Links of Interest

- [PYPI - Test](https://test.pypi.org/project/secman/)
- [PYPI - Prod](https://pypi.org/project/secman/)
- [GitHub - secman](https://github.com/rodested/secman)
- [Pytest - Good Integration Practices](https://docs.pytest.org/en/7.1.x/explanation/goodpractices.html)
- [VSCode - Pylance reports missing imports](https://stackoverflow.com/questions/71918703/visual-studio-code-pylance-report-missing-imports)
- [VSCode - Error debugging Tests: Found duplicate in env PATH](https://stackoverflow.com/questions/76036074/cannot-debug-test-case-in-vs-code-found-duplicate-in-env-path)
- [PDM - Configure the Project](https://pdm-project.org/en/latest/usage/config/)
- [PDM - Working with Virtual Environments](https://pdm-project.org/latest/usage/venv/)
- [PDM - Build and Publish](https://pdm-project.org/en/latest/usage/publish/)

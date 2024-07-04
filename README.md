README.MD

### Considerations
- [PROJECT_FOLDER] is the folder which holds the whole project (ie. subdirs src, tests, README.md must be visible when running a "ls")


## Running Tests

To run the tests using `unittest` or `pytest`, you can use the following command in the terminal.

Run them from the main project folder (should be "secman_project"). You're in the right folder if
if can see at least as immediate subfolders "tests" and "src".

If you use unittest:
```
$ python -m unittest
```

If you use pytest:
```
$ python -m pytest
```

## Run the module

To test the module you can run it, by providing a path to where the module is and running it:

Linux:
```
<project_folder>$> PYTHONPATH="./src" python -m secman -h
```

### Configuring tests in VSCode

Launch VSCode from secman_project folder (or open that folder as the main one for the project).
Then, to configure the "Testing" plugin, select as main folder for the tests the current folder
(the main one, do not select the tests folder) and from this folder then the test suite will
auto detect (auto discover) the tests in the tests folder and apply the correct configuration.
Done this, you'll be able to run tests directly from VSCode, performing all imports properly and
running fine.

## Release Notes

### stable-0.1.0
- Tests for cli working
- Tests for crypto utils working
- tests runnable from VSCode
- Tests runnable from inside <project_folder>:
  - <project_folder>$> python -m unittest
  - <project_folder>$> python -m pytest

### stable-0.1.1
- Added module with class SecretsManager. Create an object from this class and use it to decrypt secrets within your project
- Added tests for SecretsManager
- You can run secman.py from any directory (no import issues when running it), but need to provide full path to the script:
  - $> python <whatever>/<project_folder>/src/secman/secman.py -h

### stable-0.1.2
- Reviewed to be launched as module (aka unittest, venv, etc.). Required files added
- Tests modified to work running it as module in the cli (-m)
- Now can be launched as $>python -m secman ... (include the secman folder in the PYTHONPATH)

## References
[Pytest - Good Integration Practices](https://docs.pytest.org/en/7.1.x/explanation/goodpractices.html)
[VSCode - Pylance reports missing imports](https://stackoverflow.com/questions/71918703/visual-studio-code-pylance-report-missing-imports)
[VSCode - Error debugging Tests: Found duplicate in env PATH](https://stackoverflow.com/questions/76036074/cannot-debug-test-case-in-vs-code-found-duplicate-in-env-path)

README.MD

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
$ python -m pytest tests/*
```
### Configuring tests in VSCode

Launch VSCode from secman_project folder (or open that folder as the main one for the project).
Then, to configure the "Testing" plugin, select as main folder for the tests the current folder
(the main one, do not select the tests folder) and from this folder then the test suite will
auto detect (auto discover) the tests in the tests folder and apply the correct configuration.
Done this, you'll be able to run tests directly from VSCode, performing all imports properly and
running fine.

## References
[Pytest - Good Integration Practices](https://docs.pytest.org/en/7.1.x/explanation/goodpractices.html)
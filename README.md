# Python Code Structure Report Generator

![Test](https://github.com/seandearnaley/python-code-outline/workflows/Run%20pytest/badge.svg)

This Python script generates a text-based report of the code structure for all Python files in a given folder. It's useful for getting a quick overview of the code structure of a Python project. This can be particularly helpful for ChatGPT/Large Language Model (LLM) applications where you need to ask high-level questions about your codebase.

[Example Report](example_report.txt?raw=true)

## Usage

To use this script, run the `python_report_generator.py` file and provide the path to the folder containing the Python files you want to analyze. You can also optionally specify a name for the report file, which defaults to `report.txt` if not provided, and a path to the ignore file. The ignore file should be a `.gitignore` file or a file with the same format as a `.gitignore` file. If provided, the script will parse the ignore patterns from the file and exclude the matching files and folders from the report.

```bash
python python_report_generator.py /path/to/folder --report_file_path custom_report.txt --ignore_file_path /path/to/folder/.gitignore
```

If the `--report_file_path` option is not specified, the report will be written to `report.txt` by default.

```bash
python python_report_generator.py /path/to/folder
```

## Output

The script will generate a text-based report of the code structure for each Python file in the specified folder. The report includes information about imports, classes, functions, and variables in each file.

## Optional Parameters

- `--report_file_path`: The name of the report file. Defaults to `report.txt` if not provided.
- `--ignore_file_path`: The path to the ignore file. If provided, the script will parse the ignore patterns from the file and exclude the matching files and folders from the report.

## Requirements

This script requires Python 3.x to run.

## Installation

This project uses [Poetry](https://python-poetry.org/) for dependency management. To install the dependencies, first install Poetry by following the [official installation guide](https://python-poetry.org/docs/#installation), and then run the following command in the project directory:

```bash
poetry install
```

This will create a virtual environment and install the required dependencies.

## Running Tests

This project uses `pytest` for testing. To run the tests, first activate the virtual environment created by Poetry:

```bash
poetry shell
```

Then, run the tests using the following command:

```bash
pytest
```

## Checking Test Coverage

This project uses the `coverage` package to generate test coverage reports. To check the test coverage, run the following command:

```bash
coverage run -m pytest
```

This will generate a `.coverage` file with the coverage data. To view the coverage report, run:

```bash
coverage report
```

To generate an HTML report, run:

```bash
coverage html
```

This will create an `htmlcov` directory containing the HTML report.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
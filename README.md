# Python Code Structure Report Generator

[![PyPI version](https://badge.fury.io/py/python-code-outline.svg)](https://badge.fury.io/py/python-code-outline)

![Test](https://github.com/seandearnaley/python-code-outline/workflows/Run%20pytest/badge.svg)

This Python script generates a text-based report of the code structure for all Python files in a given folder. It's useful for getting a quick overview of the code structure of a Python project. This can be particularly helpful for ChatGPT/Large Language Model (LLM) applications where you need to ask high-level questions about your codebase.

[Example Report](example_report.txt?raw=true)

## Usage

To use this script, run the `python_report_generator.py` file and provide the path to the folder containing the Python files you want to analyze. You can also optionally specify a name for the report file, which defaults to `report.txt` if not provided, and a path to the ignore file. The ignore file should be a `.gitignore` file or a file with the same format as a `.gitignore` file. If provided, the script will parse the ignore patterns from the file and exclude the matching files and folders from the report.

```bash
python python_code_outline/python_report_generator.py /path/to/folder --report_file_path custom_report.txt --ignore_file_path /path/to/folder/.gitignore
```

If the `--report_file_path` option is not specified, the report will be written to `report.txt` by default.

```bash
python python_report_generator.py /path/to/folder
```

## Usage as a pip module

After installing the package via pip, you can import and use the functionality in your own code as well. For example:

```python
from python_code_outline import python_report_generator

# Define the root folder
root_folder = "/path/to/folder"

# Specify the report and ignore file paths (optional)
report_file_path = "custom_report.txt"
ignore_file_path = "/path/to/folder/.gitignore"

# Generate the report
report = python_report_generator.get_report(root_folder, ignore_file_path)

# Write the report to a file
with open(report_file_path, "w", encoding="utf-8") as file:
    file.write(report)

print(f"Report generated successfully to {report_file_path}.")
```

Please replace "/path/to/folder" with the path to the folder you want to analyze, and update the report and ignore file paths as necessary.

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

You can install this module using pip:

```bash
pip install python-code-outline
```

This command will download the package from PyPI and install it in your current Python environment.

Absolutely, I can update the installation instructions. Here is the updated `readme.md`:

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

This project uses the `coverage` package to generate test coverage reports. Here's how to use it:

1. First, you need to install the `coverage` package if it's not already installed. You can do so by running the following command:

```bash
pip install coverage
```

2. After installing `coverage`, you can use it to run your tests and collect coverage data. If you're using `pytest` for testing, you can use the following command:

```bash
coverage run -m pytest
```

This command tells `coverage` to run `pytest` as a module (hence the `-m` flag), and `coverage` collects data about which parts of your code were executed during the test run.

3. Once you've collected coverage data, you can generate a report by running:

```bash
coverage report
```

This will print a coverage report to the terminal, showing the code coverage for each module in your project.

4. If you want a more detailed view, you can generate an HTML report using:

```bash
coverage html
```

This will generate an `htmlcov` directory in your project directory. Inside this directory, you'll find an `index.html` file. You can open this file in a web browser to view a detailed coverage report that shows which lines of each file were covered by the tests.

5. If you're finished checking coverage and want to clear the collected data, you can use the command:

```bash
coverage erase
```

This will delete the `.coverage` data file, clearing the collected coverage data.

Remember that code coverage is a useful tool for finding untested parts of your code, but achieving 100% code coverage doesn't necessarily mean your testing is perfect. It's important to write meaningful tests and not just strive for high coverage percentages.
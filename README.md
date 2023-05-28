# Python Code Structure Report Generator

This Python script generates a text-based report of the code structure for all Python files in a given folder. It's useful for getting a quick overview of the code structure of a Python project. This can be particularly helpful for ChatGPT/Large Language Model (LLM) applications where you need to ask high-level questions about your codebase.

[Example Report](example_report.txt?raw=true)

## Usage

To use this script, run the `main.py` file and provide the path to the folder containing the Python files you want to analyze. You can also optionally specify a name for the report file, which defaults to `report.txt` if not provided.

```bash
python main.py /path/to/folder --report_filename custom_report.txt
```

If the `--report_filename` option is not specified, the report will be written to `report.txt` by default.

```bash
python main.py /path/to/folder
```

## Output

The script will generate a text-based report of the code structure for each Python file in the specified folder. The report includes information about imports, classes, functions, and variables in each file.

## Requirements

This script requires Python 3.x to run.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

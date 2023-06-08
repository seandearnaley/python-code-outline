"""Tests for python_report_generator.py"""
import ast
from pathlib import Path

import pytest
from pytest import CaptureFixture, MonkeyPatch

from python_code_outline.python_report_generator import (
    generate_report,
    get_report,
    is_ignored,
    list_entries,
    main,
    parse_ignore_patterns,
    process_class_def,
    process_function_def,
    process_import,
    process_import_from,
    process_python_file,
)


@pytest.fixture(name="sample_ignore_file")
def fixture_sample_ignore_file(tmp_path: Path) -> Path:
    """Create a sample .gitignore file."""
    content = "*.txt\n*.log\n# This is a comment\n"
    ignore_file_path = tmp_path / ".gitignore"
    ignore_file_path.write_text(content)
    return ignore_file_path


@pytest.fixture(name="sample_directory")
def fixture_sample_directory(tmp_path: Path) -> Path:
    """Create a sample directory with files and folders."""
    (tmp_path / "folder1").mkdir()
    (tmp_path / "folder2").mkdir()
    (tmp_path / "file1.py").write_text("import os\n")
    (tmp_path / "file2.py").write_text("from pathlib import Path\n")
    return tmp_path


def test_parse_ignore_patterns(sample_ignore_file: Path) -> None:
    """Test that the ignore patterns are parsed correctly."""
    patterns = parse_ignore_patterns(sample_ignore_file)
    assert patterns == ["*.txt", "*.log"]


def test_is_ignored(sample_directory: Path) -> None:
    """Test that the ignore patterns are parsed correctly."""
    ignored_patterns = ["*.txt", "*.log"]
    assert is_ignored(sample_directory / "file1.py", ignored_patterns) is False
    assert is_ignored(sample_directory / "file2.py", ignored_patterns) is False


def test_list_entries(sample_directory: Path) -> None:
    """Test that the entries are listed correctly."""
    entries = list_entries(sample_directory)
    assert entries == [
        sample_directory / "folder1",
        sample_directory / "folder2",
        sample_directory / "file1.py",
        sample_directory / "file2.py",
    ]


def test_process_import() -> None:
    """Test that the import is processed correctly."""
    node = ast.parse("import os, sys")
    item = node.body[0]
    assert isinstance(item, ast.Import)
    assert process_import(item) == "imports os, sys"


def test_process_import_from() -> None:
    """Test that the import from is processed correctly."""
    node = ast.parse("from pathlib import Path")
    item = node.body[0]
    assert isinstance(item, ast.ImportFrom)
    assert process_import_from(item) == "from pathlib imports Path"


def test_process_function_def() -> None:
    """Test that the function definition is processed correctly."""
    code = """
def example_function(arg1, arg2):
    var1 = 1
    var2 = 2
    """
    node = ast.parse(code)
    item = node.body[0]
    assert isinstance(item, ast.FunctionDef)
    assert process_function_def(item) == [
        "func example_function(arg1, arg2)",
        "\tvar var1",
        "\tvar var2",
    ]


def test_process_class_def() -> None:
    """Test that the class definition is processed correctly."""
    code = """
class ExampleClass:
    def method1(self, arg1):
        var1 = 1
    """
    node = ast.parse(code)
    item = node.body[0]
    assert isinstance(item, ast.ClassDef)
    assert process_class_def(item) == [
        "class ExampleClass()",
        "\tfunc method1(self, arg1)",
        "\t\tvar var1",
    ]


def test_process_python_file(sample_directory: Path) -> None:
    """Test that the python file is processed correctly."""
    file_path = sample_directory / "file1.py"
    report = process_python_file(file_path, sample_directory)
    assert report == "- file1.py\nimports os"


def test_generate_report(sample_directory: Path, sample_ignore_file: Path) -> None:
    """Test that the report is generated correctly."""
    ignored_patterns = parse_ignore_patterns(sample_ignore_file)
    report = generate_report(sample_directory, sample_directory, ignored_patterns)
    expected_report = "- file1.py\nimports os\n\n- file2.py\nfrom pathlib imports Path"
    assert report == expected_report


def test_process_function_def_no_variables() -> None:
    """Test that the function definition is processed correctly with no variables."""
    code = """
def example_function(arg1, arg2):
    pass
    """
    node = ast.parse(code)
    item = node.body[0]
    assert isinstance(item, ast.FunctionDef)
    assert process_function_def(item) == [
        "func example_function(arg1, arg2)",
    ]


def test_process_class_def_no_methods() -> None:
    """Test that the class definition is processed correctly with no methods."""
    code = """
class ExampleClass:
    pass
    """
    node = ast.parse(code)
    item = node.body[0]
    assert isinstance(item, ast.ClassDef)
    assert process_class_def(item) == [
        "class ExampleClass()",
    ]


def test_generate_report_no_ignore_patterns(sample_directory: Path) -> None:
    """Test that the report is generated correctly when ignored_patterns is None."""
    report = generate_report(sample_directory, sample_directory, ignored_patterns=None)
    expected_report = "- file1.py\nimports os\n\n- file2.py\nfrom pathlib imports Path"
    assert report == expected_report


def test_generate_report_with_arguments(tmp_path: Path) -> None:
    """Test root_folder, ignore_file_path, and report_file_path arguments."""
    root_folder = tmp_path / "root"
    root_folder.mkdir()
    (root_folder / "file1.py").write_text("import os\n")
    (root_folder / "file2.py").write_text("from pathlib import Path\n")

    ignore_file_path = tmp_path / ".gitignore"
    ignore_file_path.write_text("*.txt\n*.log\n")

    report_file_path = tmp_path / "report.txt"

    report = get_report(root_folder, ignore_file_path)
    expected_report = "- file1.py\nimports os\n\n- file2.py\nfrom pathlib imports Path"

    with open(report_file_path, "w", encoding="utf-8") as file:
        file.write(report)

    assert report == expected_report
    assert report_file_path.read_text() == expected_report


def test_main(
    sample_directory: Path,
    sample_ignore_file: Path,
    capsys: CaptureFixture[str],
    monkeypatch: MonkeyPatch,
) -> None:
    """Test main function."""
    # Move the sample_ignore_file to the sample_directory
    sample_ignore_file.rename(sample_directory / sample_ignore_file.name)

    # Set command-line arguments
    monkeypatch.setattr(
        "sys.argv",
        [
            "python_report_generator.py",
            str(sample_directory),
            "--report_file_path",
            "test_report.txt",
            "--ignore_file_path",
            str(sample_ignore_file),
        ],
    )

    # Call main function
    main()

    # Check if the report file is created
    report_file_path = Path("test_report.txt")
    assert report_file_path.exists()

    # Read the report file content
    report_content = report_file_path.read_text(encoding="utf-8")

    # Check the report content
    expected_report_content = (
        "- file1.py\nimports os\n\n- file2.py\nfrom pathlib imports Path"
    )
    assert report_content == expected_report_content

    # Capture the output
    output = capsys.readouterr().out

    # Check the output
    expected_output = "Report generated successfully to test_report.txt.\n"
    assert output == expected_output

    # Clean up the report file
    report_file_path.unlink()


def test_process_python_file_function_def(sample_directory: Path) -> None:
    """Test that the python file with a function definition is processed correctly."""
    file_path = sample_directory / "file_with_function.py"
    file_path.write_text("def example_function(arg1, arg2):\n    pass\n")
    report = process_python_file(file_path, sample_directory)
    assert report == "- file_with_function.py\nfunc example_function(arg1, arg2)"


def test_process_python_file_class_def(sample_directory: Path) -> None:
    """Test that the python file with a class definition is processed correctly."""
    file_path = sample_directory / "file_with_class.py"
    file_path.write_text("class ExampleClass:\n    pass\n")
    report = process_python_file(file_path, sample_directory)
    assert report == "- file_with_class.py\nclass ExampleClass()"


def test_generate_report_with_subdir(sample_directory: Path) -> None:
    """Test that the report is generated correctly with a subdirectory."""
    subdir = sample_directory / "subdir"
    subdir.mkdir()
    (subdir / "file3.py").write_text("import math\n")
    ignored_patterns = ["*.txt", "*.log"]
    report = generate_report(sample_directory, sample_directory, ignored_patterns)
    expected_report_parts = [
        "- file1.py\nimports os",
        "- file2.py\nfrom pathlib imports Path",
        "subdir/file3.py\nimports math",
    ]
    # Check if all parts are present in the report, regardless of the order
    for part in expected_report_parts:
        assert part in report


def test_main_invalid_directory(monkeypatch: MonkeyPatch) -> None:
    """Test main function with an invalid directory."""
    # Set command-line arguments
    monkeypatch.setattr(
        "sys.argv",
        [
            "python_report_generator.py",
            "invalid_directory",
            "--report_file_path",
            "test_report.txt",
            "--ignore_file_path",
            ".gitignore",
        ],
    )

    # Call main function and expect a ValueError
    with pytest.raises(ValueError, match="invalid_directory is not a valid directory"):
        main()

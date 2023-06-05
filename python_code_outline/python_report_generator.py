"""Generate a text-based report of the code structure for Python code in a folder."""
import argparse
import ast
from pathlib import Path
from typing import List, Optional


def parse_ignore_patterns(ignorefile_path: Path) -> List[str]:
    """Parse the patterns to ignore from a .gitignore file."""
    with ignorefile_path.open(encoding="utf-8") as file:
        return [
            line.strip() for line in file if line.strip() and not line.startswith("#")
        ]


def is_ignored(entry: Path, ignored_patterns: List[str]) -> bool:
    """Check if a given entry should be ignored."""
    return entry.name == ".gitignore" or any(
        entry.match(pattern) for pattern in ignored_patterns
    )


def list_entries(root: Path) -> List[Path]:
    """List all entries in a given folder, sorted by type and name."""
    return sorted(root.iterdir(), key=lambda e: (e.is_file(), e.name.lower()))


def process_import(item: ast.Import) -> str:
    """Process an import statement."""
    return f"imports {', '.join([alias.name for alias in item.names])}"


def process_import_from(item: ast.ImportFrom) -> str:
    """Process an import-from statement."""
    return (
        f"from {item.module} imports {', '.join([alias.name for alias in item.names])}"
    )


def process_function_def(item: ast.FunctionDef) -> List[str]:
    """Process a function definition."""
    output = [f"func {item.name}({', '.join([arg.arg for arg in item.args.args])})"]
    for stmt in item.body:
        if isinstance(stmt, ast.Assign) and isinstance(stmt.targets[0], ast.Name):
            output.append(f"\tvar {stmt.targets[0].id}")
    return output


def process_class_def(item: ast.ClassDef) -> List[str]:
    """Process a class definition."""
    base_classes = ", ".join(
        [base.id for base in item.bases if isinstance(base, ast.Name)]
    )
    output = [f"class {item.name}({base_classes})"]
    for class_item in item.body:
        if isinstance(class_item, ast.FunctionDef):
            output.extend(["\t" + line for line in process_function_def(class_item)])
    return output


def process_python_file(file_path: Path, root_folder: Path) -> str:
    """Process a Python file and generate a report of its structure."""
    with file_path.open("r", encoding="utf-8") as file:
        node = ast.parse(file.read())

    relative_path = file_path.relative_to(root_folder)
    output = [f"- {relative_path}"]

    for item in node.body:
        if isinstance(item, ast.Import):
            output.append(process_import(item))
        elif isinstance(item, ast.ImportFrom):
            output.append(process_import_from(item))
        elif isinstance(item, ast.FunctionDef):
            output.extend(process_function_def(item))
        elif isinstance(item, ast.ClassDef):
            output.extend(process_class_def(item))

    return "\n".join(output)


# ...


def generate_report(
    root: Path, root_folder: Path, ignored_patterns: Optional[List[str]] = None
) -> str:
    """
    Generate a report of the code structure for all Python
    files in a given folder."""

    if ignored_patterns is None:
        ignored_patterns = []

    entries = list_entries(root)
    report: List[str] = []  # add type hint for report list

    for entry in entries:
        if (
            entry.is_file()
            and not is_ignored(entry, ignored_patterns)
            and entry.suffix == ".py"
        ):
            report.append(process_python_file(entry, root_folder))
        elif entry.is_dir() and not is_ignored(entry, ignored_patterns):
            subdir_report = generate_report(entry, root_folder, ignored_patterns)
            if subdir_report:
                report.append(subdir_report)

    return "\n\n".join(report)


def parse_arguments() -> argparse.Namespace:
    """Parse the command-line arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Generate a text-based report of the code structure for all Python files in"
            " a given folder."
        )
    )
    parser.add_argument("root_folder", type=str, help="Path to the root folder")
    parser.add_argument(
        "--report_file_path",
        type=str,
        default="report.txt",
        help="Name of the report file",
    )
    parser.add_argument(
        "--ignore_file_path",
        type=str,
        default=None,
        help="Path to the ignore file",
    )

    args = parser.parse_args()

    root_folder: str = args.root_folder

    if not Path(root_folder).is_dir():
        raise ValueError(f"{root_folder} is not a valid directory")

    return args


def get_report(root_folder: Path, ignore_file_path: Optional[Path] = None) -> str:
    """Get the report of the code structure for all Python files in a given folder."""
    ignored_patterns = (
        parse_ignore_patterns(ignore_file_path)
        if ignore_file_path and ignore_file_path.exists()
        else []
    )

    return generate_report(root_folder, root_folder, ignored_patterns)


def main() -> None:
    """Main function."""
    args = parse_arguments()
    root_folder = Path(args.root_folder)
    report_file_path = args.report_file_path
    ignore_file_path = Path(args.ignore_file_path) if args.ignore_file_path else None

    report = get_report(root_folder, ignore_file_path)

    with open(report_file_path, "w", encoding="utf-8") as file:
        file.write(report)

    print(f"Report generated successfully to {report_file_path}.")


if __name__ == "__main__":
    main()

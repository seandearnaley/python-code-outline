"""Generate a text-based report of the code structure for Python code in a folder."""
import argparse
import ast
from pathlib import Path
from typing import List, Optional


def parse_ignore_patterns(ignorefile_path: str) -> List[str]:
    """Parse the patterns to ignore from a .gitignore file."""
    with Path(ignorefile_path).open(encoding="utf-8") as file:
        return [
            line.strip() for line in file if line.strip() and not line.startswith("#")
        ]


def is_ignored(entry: Path, ignored_patterns: List[str]) -> bool:
    """Check if a given entry should be ignored."""
    return entry.name == ".gitignore" or any(
        entry.match(pattern) for pattern in ignored_patterns
    )


def list_entries(root: str) -> List[Path]:
    """List all entries in a given folder, sorted by type and name."""
    return sorted(Path(root).iterdir(), key=lambda e: (e.is_file(), e.name.lower()))


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


def generate_report(
    root: str, root_folder: str, ignored_patterns: Optional[List[str]] = None
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
            report.append(process_python_file(entry, Path(root_folder)))
        elif entry.is_dir() and not is_ignored(entry, ignored_patterns):
            subdir_report = generate_report(str(entry), root_folder, ignored_patterns)
            if subdir_report:
                report.append(subdir_report)

    return "\n\n".join(report)


def expand_user_path(path: Optional[str]) -> Optional[str]:
    """Expand the user home directory symbol '~' if it's part of the path."""
    if path is not None:
        path_obj = Path(path)
        if "~" in path:
            return str(path_obj.expanduser().resolve())

        return str(path_obj)
    return None


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

    args.root_folder = expand_user_path(args.root_folder)
    args.ignore_file_path = expand_user_path(args.ignore_file_path)

    return args


def get_report(root_folder: str, ignore_file_path: Optional[str] = None) -> str:
    """Get the report of the code structure for all Python files in a given folder."""

    if not Path(root_folder).is_dir():
        raise ValueError(f"{root_folder} is not a valid directory")

    if ignore_file_path is not None:
        if not Path(ignore_file_path).is_file():
            raise ValueError(f"{ignore_file_path} is not a valid file")

    ignored_patterns = (
        parse_ignore_patterns(ignore_file_path)
        if ignore_file_path and Path(ignore_file_path).exists()
        else []
    )

    return generate_report(root_folder, root_folder, ignored_patterns)


def main() -> None:
    """Main function."""
    args = parse_arguments()
    root_folder = args.root_folder
    report_file_path = args.report_file_path
    ignore_file_path = args.ignore_file_path if args.ignore_file_path else None

    report = get_report(root_folder, ignore_file_path)

    with open(report_file_path, "w", encoding="utf-8") as file:
        file.write(report)

    print(f"Report generated successfully to {report_file_path}.")


if __name__ == "__main__":
    main()

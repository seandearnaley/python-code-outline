""" Generate a text-based report of the code structure for all Python files 
    in a given folder. """
import argparse
import ast
from pathlib import Path
from typing import List, Optional


def parse_ignore_patterns(ignorefile_path: Path) -> List[str]:
    """Parse the patterns to ignore from a .gitignore file."""
    with open(ignorefile_path, encoding="utf-8") as file:
        return [
            line.strip()
            for line in file
            if line.strip() and not line.strip().startswith("#")
        ]


def is_ignored(entry: Path, ignored_patterns: List[str]) -> bool:
    """Check if a given entry should be ignored."""
    return entry.name == ".gitignore" or any(
        entry.match(pattern) for pattern in ignored_patterns
    )


def list_entries(root: Path) -> List[Path]:
    """List all entries in a given folder, sorted by type and name."""
    return sorted(root.iterdir(), key=lambda e: (e.is_file(), e.name.lower()))


def process_python_file(file_path: Path, root_folder: Path) -> str:
    """Process a Python file and generate a report of its structure."""
    with open(file_path, "r", encoding="utf-8") as file:
        node = ast.parse(file.read())

    relative_path = file_path.relative_to(root_folder)
    output = [f"----------------\n{relative_path}:\n----------------"]

    for item in node.body:
        if isinstance(item, ast.Import):
            output.append(f"imports {', '.join([alias.name for alias in item.names])}")
        elif isinstance(item, ast.ImportFrom):
            output.append(
                f"from {item.module} imports"
                f" {', '.join([alias.name for alias in item.names])}"
            )
        elif isinstance(item, ast.FunctionDef):
            output.append(
                f"func {item.name}({', '.join([arg.arg for arg in item.args.args])})"
            )
            for stmt in item.body:
                if isinstance(stmt, ast.Assign) and isinstance(
                    stmt.targets[0], ast.Name
                ):
                    output.append(f"\tvar {stmt.targets[0].id}")
        elif isinstance(item, ast.ClassDef):
            base_classes = ", ".join(
                [base.id for base in item.bases if isinstance(base, ast.Name)]
            )
            output.append(f"class {item.name}({base_classes})")
            for class_item in item.body:
                if isinstance(class_item, ast.FunctionDef):
                    output.append(
                        "\tfunc"
                        f" {class_item.name}("
                        f"{', '.join([arg.arg for arg in class_item.args.args])})"
                    )
                    for stmt in class_item.body:
                        if isinstance(stmt, ast.Assign) and isinstance(
                            stmt.targets[0], ast.Name
                        ):
                            output.append(f"\t\tvar {stmt.targets[0].id}")

    return "\n".join(output)


def generate_report(
    root: Path, root_folder: Path, ignored_patterns: Optional[List[str]] = None
) -> str:
    """
    Generate a report of the code structure for all Python
    files in a given folder."""
    if ignored_patterns is None:
        ignored_patterns = []

    entries = list_entries(root)
    report = []

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


def parse_arguments() -> str:
    """Parse the command-line arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Generate a text-based report of the code structure for all Python files in"
            " a given folder."
        )
    )
    parser.add_argument("root_folder", type=str, help="Path to the root folder")

    args = parser.parse_args()

    root_folder: str = args.root_folder

    if not Path(root_folder).is_dir():
        raise ValueError(f"{root_folder} is not a valid directory")

    return root_folder


def main() -> None:
    """Main function."""
    root_folder = parse_arguments()
    root = Path(root_folder)
    ignorefile_path = root / ".gitignore"
    ignored_patterns = (
        parse_ignore_patterns(ignorefile_path) if ignorefile_path.exists() else []
    )

    report = generate_report(root, root, ignored_patterns)

    with open("report.txt", "w", encoding="utf-8") as file:
        file.write(report)

    print("Report generated successfully.")


if __name__ == "__main__":
    main()

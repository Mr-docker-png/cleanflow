import json
from pathlib import Path


def generate_report(report: dict, output_path: str) -> str:
    """Save cleaning report as a JSON file."""

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4, default=str)

    return str(path)


def print_report(report: dict) -> None:
    """Display a readable cleaning report."""

    print("\n" + "=" * 40)
    print("       DATA CLEANING REPORT")
    print("=" * 40)

    print(f"Rows:              {report['original_rows']} → "
          f"{report['cleaned_rows']}")

    print(f"Columns:           {report['original_columns']} → "
          f"{report['cleaned_columns']}")

    print(f"Duplicates removed: {report['duplicates_removed']}")

    print(f"Empty columns:      "
          f"{len(report['empty_columns_removed'])}")

    print(f"Missing values handled: "
          f"{len(report['missing_values_filled'])}")

    print("=" * 40)
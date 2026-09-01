from pathlib import Path

import pandas as pd


SUPPORTED_OUTPUT_FORMATS = {
    ".csv",
    ".xlsx",
    ".xls",
    ".json",
    ".tsv",
}


def get_output_path(
    input_file: str,
    output_dir: str = "output",
) -> Path:
    """
    Create the output path while preserving the
    original file format where possible.
    """

    input_path = Path(input_file)

    output_directory = Path(output_dir)
    output_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    extension = input_path.suffix.lower()

    # XLS files are exported as XLSX because modern
    # Pandas environments may not have an XLS writer.
    if extension == ".xls":
        extension = ".xlsx"

    if extension not in SUPPORTED_OUTPUT_FORMATS:
        extension = ".csv"

    return output_directory / f"cleaned_{input_path.stem}{extension}"


def export_data(
    df: pd.DataFrame,
    input_file: str,
    output_dir: str = "output",
) -> str:
    """
    Export the cleaned DataFrame using the appropriate
    output format.
    """

    output_path = get_output_path(
        input_file,
        output_dir
    )

    extension = output_path.suffix.lower()

    if extension == ".csv":
        df.to_csv(
            output_path,
            index=False
        )

    elif extension == ".tsv":
        df.to_csv(
            output_path,
            sep="\t",
            index=False
        )

    elif extension == ".xlsx":
        df.to_excel(
            output_path,
            index=False
        )

    elif extension == ".json":
        df.to_json(
            output_path,
            orient="records",
            indent=4,
            date_format="iso"
        )

    else:
        raise ValueError(
            f"Unsupported output format: {extension}"
        )

    return str(output_path)
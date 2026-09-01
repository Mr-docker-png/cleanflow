from pathlib import Path
import pandas as pd

SUPPORTED_EXTENSIONS = {
    ".csv",
    ".xlsx",
    ".xls",
    ".json",
    ".tsv",
}

def get_file_extension(file_path:str) -> str:
    "Return the file extension in lowercase"
    return Path(file_path).suffix.lower()

def validate_file(file_path: str) -> None:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    extension=get_file_extension(file_path)

    if extension not in SUPPORTED_EXTENSIONS:
        supported = ", ".join(sorted(SUPPORTED_EXTENSIONS))
        raise ValueError(
            f"Unsupported file type: {extension}\n"
            f"Supported formats: {supported}"
        )

def load_file(file_path:str) -> pd.DataFrame:
    validate_file(file_path)
    extension=get_file_extension(file_path)

    if extension == ".csv":
        return pd.read_csv(file_path)
    if extension == ".tsv":
        return pd.read_csv(file_path,sep="\t")
    if extension in {".xlsx", ".xls"}:
        return pd.read_excel(file_path)

    if extension ==".json":
        return pd.read_json(file_path)

    raise ValueError(f"Unsupported file type: {extension}")
import pandas as pd


def detect_column_types(df: pd.DataFrame) -> dict:
    """Detect useful column categories."""

    numeric_columns = df.select_dtypes(
        include=["number"]
    ).columns.tolist()

    categorical_columns = df.select_dtypes(
        include=["object", "string", "category"]
    ).columns.tolist()

    boolean_columns = df.select_dtypes(
        include=["bool"]
    ).columns.tolist()

    return {
        "numeric": numeric_columns,
        "categorical": categorical_columns,
        "boolean": boolean_columns,
    }


def analyze_data(df: pd.DataFrame) -> dict:
    """Analyze the structure and quality of a dataset."""

    column_types = detect_column_types(df)

    missing_values = {
        column: int(value)
        for column, value in df.isnull().sum().items()
        if value > 0
    }

    unique_values = {
        column: int(df[column].nunique(dropna=True))
        for column in df.columns
    }

    empty_columns = [
        column
        for column in df.columns
        if df[column].isna().all()
    ]

    data_types = {
        column: str(dtype)
        for column, dtype in df.dtypes.items()
    }

    analysis = {
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": df.columns.tolist(),

        "missing_values": missing_values,

        "total_missing_values": int(
            df.isnull().sum().sum()
        ),

        "duplicate_rows": int(
            df.duplicated().sum()
        ),

        "empty_columns": empty_columns,

        "data_types": data_types,

        "unique_values": unique_values,

        "column_types": column_types,
    }

    return analysis
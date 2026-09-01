import pandas as pd


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize column names."""

    df = df.copy()

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace(r"\s+", "_", regex=True)
        .str.replace(r"[^\w_]", "", regex=True)
    )

    # Make duplicate column names unique
    new_columns = []
    counts = {}

    for column in df.columns:
        if column not in counts:
            counts[column] = 0
            new_columns.append(column)
        else:
            counts[column] += 1
            new_columns.append(
                f"{column}_{counts[column]}"
            )

    df.columns = new_columns

    return df


def clean_text_values(df: pd.DataFrame) -> pd.DataFrame:
    """Remove unnecessary whitespace from text columns."""

    df = df.copy()

    text_columns = df.select_dtypes(
        include=["object", "string"]
    ).columns

    for column in text_columns:
        df[column] = df[column].astype("string").str.strip()

        # Convert empty strings to missing values
        df[column] = df[column].replace(
            r"^\s*$",
            pd.NA,
            regex=True
        )

    return df


def remove_empty_columns(
    df: pd.DataFrame,
) -> tuple[pd.DataFrame, list]:

    """Remove completely empty columns."""

    df = df.copy()

    empty_columns = [
        column
        for column in df.columns
        if df[column].isna().all()
    ]

    if empty_columns:
        df = df.drop(columns=empty_columns)

    return df, empty_columns


def remove_empty_rows(
    df: pd.DataFrame,
) -> tuple[pd.DataFrame, int]:

    """Remove completely empty rows."""

    df = df.copy()

    empty_rows = int(df.isna().all(axis=1).sum())

    if empty_rows > 0:
        df = df.dropna(how="all")

    return df, empty_rows


def remove_duplicate_rows(
    df: pd.DataFrame,
) -> tuple[pd.DataFrame, int]:

    """Remove duplicate rows."""

    df = df.copy()

    duplicates = int(df.duplicated().sum())

    if duplicates > 0:
        df = df.drop_duplicates()

    return df, duplicates


def convert_numeric_columns(
    df: pd.DataFrame,
) -> tuple[pd.DataFrame, list]:

    """
    Convert text columns to numeric when most values
    can safely be interpreted as numbers.
    """

    df = df.copy()

    converted_columns = []

    for column in df.columns:

        if not (
            df[column].dtype == "object"
            or pd.api.types.is_string_dtype(df[column])
        ):
            continue

        original = df[column]

        converted = pd.to_numeric(
            original,
            errors="coerce"
        )

        non_missing = original.notna().sum()

        if non_missing == 0:
            continue

        valid_ratio = converted.notna().sum() / non_missing

        # Only convert when at least 90% of existing
        # values are numeric.
        if valid_ratio >= 0.90:

            df[column] = converted
            converted_columns.append(column)

    return df, converted_columns


def detect_and_convert_dates(
    df: pd.DataFrame,
) -> tuple[pd.DataFrame, list]:

    """
    Detect columns that mostly contain valid dates
    and convert them to datetime.
    """

    df = df.copy()

    converted_columns = []

    for column in df.columns:

        if not (
            df[column].dtype == "object"
            or pd.api.types.is_string_dtype(df[column])
        ):
            continue

        original = df[column]

        non_missing = original.dropna()

        if len(non_missing) == 0:
            continue

        converted = pd.to_datetime(
            original,
            errors="coerce"
        )

        valid_ratio = converted.notna().sum() / len(non_missing)

        # Avoid converting ordinary text columns
        # unless the majority looks like dates.
        if valid_ratio >= 0.90:

            df[column] = converted
            converted_columns.append(column)

    return df, converted_columns


def handle_missing_values(
    df: pd.DataFrame,
) -> tuple[pd.DataFrame, dict]:

    """Handle missing values using conservative rules."""

    df = df.copy()

    changes = {}

    for column in df.columns:

        missing_count = int(
            df[column].isna().sum()
        )

        if missing_count == 0:
            continue

        # Numeric columns → median
        if pd.api.types.is_numeric_dtype(df[column]):

            fill_value = df[column].median()

            if pd.isna(fill_value):
                fill_value = 0

            df[column] = df[column].fillna(
                fill_value
            )

            changes[column] = {
                "count": missing_count,
                "method": "median",
                "value": float(fill_value),
            }

        # Datetime columns → don't invent dates
        elif pd.api.types.is_datetime64_any_dtype(
            df[column]
        ):

            changes[column] = {
                "count": missing_count,
                "method": "left_missing",
                "value": None,
            }

        # Text columns → placeholder
        else:

            df[column] = df[column].fillna(
                "Not Provided"
            )

            changes[column] = {
                "count": missing_count,
                "method": "text_placeholder",
                "value": "Not Provided",
            }

    return df, changes


def clean_data(
    df: pd.DataFrame,
) -> tuple[pd.DataFrame, dict]:

    """Run the complete cleaning pipeline."""

    original_rows = len(df)
    original_columns = len(df.columns)

    # 1. Column names
    df = clean_column_names(df)

    # 2. Text cleanup
    df = clean_text_values(df)

    # 3. Empty rows
    df, empty_rows_removed = remove_empty_rows(df)

    # 4. Empty columns
    df, empty_columns_removed = remove_empty_columns(df)

    # 5. Duplicates
    df, duplicates_removed = remove_duplicate_rows(df)

    # 6. Numeric detection
    df, numeric_columns_converted = (
        convert_numeric_columns(df)
    )

    # 7. Date detection
    df, date_columns_converted = (
        detect_and_convert_dates(df)
    )

    # 8. Missing values
    df, missing_changes = handle_missing_values(df)

    report = {
        "original_rows": original_rows,
        "cleaned_rows": len(df),
        "original_columns": original_columns,
        "cleaned_columns": len(df.columns),

        "empty_rows_removed": empty_rows_removed,

        "empty_columns_removed": (
            empty_columns_removed
        ),

        "duplicates_removed": duplicates_removed,

        "numeric_columns_converted": (
            numeric_columns_converted
        ),

        "date_columns_converted": (
            date_columns_converted
        ),

        "missing_values_filled": missing_changes,
    }

    return df, report
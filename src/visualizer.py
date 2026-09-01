from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# Columns containing these words are usually identifiers
# and are not useful for general-purpose visualization.
IDENTIFIER_KEYWORDS = {
    "id",
    "email",
    "name",
    "phone",
    "mobile",
    "address",
    "code",
    "uuid",
}


def is_identifier_column(column: str) -> bool:
  

    column = column.lower().strip()

    for keyword in IDENTIFIER_KEYWORDS:
        if column == keyword or column.endswith(f"_{keyword}"):
            return True

    return False


def create_numeric_charts(
    df: pd.DataFrame,
    output_path: Path,
) -> list[str]:
   
    generated_files = []

    numeric_columns = df.select_dtypes(
        include=["number"]
    ).columns

    for column in numeric_columns:

        data = df[column].dropna()

        if len(data) < 2 or data.nunique() < 2:
            continue

        plt.figure(figsize=(8, 5))

        plt.hist(
            data,
            bins=min(10, max(3, data.nunique())),
        )

        plt.title(f"Distribution of {column}")
        plt.xlabel(column)
        plt.ylabel("Frequency")

        plt.tight_layout()

        file_path = (
            output_path / f"{column}_distribution.png"
        )

        plt.savefig(
            file_path,
            dpi=150,
            bbox_inches="tight",
        )

        plt.close()

        generated_files.append(str(file_path))

    return generated_files


def create_categorical_charts(
    df: pd.DataFrame,
    output_path: Path,
) -> list[str]:


    generated_files = []

    categorical_columns = df.select_dtypes(
        include=["object", "string", "category"]
    ).columns

    for column in categorical_columns:

  
        if is_identifier_column(column):
            continue

        data = df[column].dropna()

        if data.empty:
            continue

        unique_count = data.nunique()

 
        if unique_count < 2 or unique_count > 15:
            continue

        value_counts = (
            data.value_counts()
            .head(10)
        )

        plt.figure(figsize=(8, 5))

        value_counts.plot(
            kind="bar"
        )

        plt.title(f"Distribution of {column}")
        plt.xlabel(column)
        plt.ylabel("Count")

        plt.xticks(
            rotation=45,
            ha="right",
        )

        plt.tight_layout()

        file_path = (
            output_path / f"{column}_categories.png"
        )

        plt.savefig(
            file_path,
            dpi=150,
            bbox_inches="tight",
        )

        plt.close()

        generated_files.append(str(file_path))

    return generated_files


def create_correlation_chart(
    df: pd.DataFrame,
    output_path: Path,
) -> list[str]:
  

    generated_files = []

    numeric_columns = df.select_dtypes(
        include=["number"]
    ).columns

    if len(numeric_columns) < 2:
        return generated_files

    correlation = df[numeric_columns].corr()

    plt.figure(
        figsize=(
            max(6, len(numeric_columns) * 1.2),
            max(5, len(numeric_columns) * 1.0),
        )
    )

    plt.imshow(
        correlation,
        interpolation="nearest",
        aspect="auto",
    )

    plt.colorbar(
        label="Correlation"
    )

    plt.xticks(
        range(len(numeric_columns)),
        numeric_columns,
        rotation=45,
        ha="right",
    )

    plt.yticks(
        range(len(numeric_columns)),
        numeric_columns,
    )

    plt.title(
        "Numeric Feature Correlation"
    )

    plt.tight_layout()

    file_path = (
        output_path / "correlation_heatmap.png"
    )

    plt.savefig(
        file_path,
        dpi=150,
        bbox_inches="tight",
    )

    plt.close()

    generated_files.append(str(file_path))

    return generated_files


def create_visualizations(
    df: pd.DataFrame,
    output_dir: str = "output/visualizations",
) -> list[str]:
    """
    Automatically create useful visualizations.

    The function decides which charts are appropriate
    based on the structure of the dataset.
    """

    output_path = Path(output_dir)

    output_path.mkdir(
        parents=True,
        exist_ok=True,
    )

    generated_files = []

    # Numeric distributions
    generated_files.extend(
        create_numeric_charts(
            df,
            output_path,
        )
    )

    generated_files.extend(
        create_categorical_charts(
            df,
            output_path,
        )
    )

    generated_files.extend(
        create_correlation_chart(
            df,
            output_path,
        )
    )

    return generated_files
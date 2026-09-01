# CleanFlow 🧹📊

### Automatic Data Cleaning & Visualization Tool

CleanFlow is a Python-based data cleaning and analysis tool that automatically processes common data files, identifies common data-quality issues, cleans the dataset, generates useful visualizations, and creates a detailed cleaning report.

The project was built to demonstrate practical skills in **Python, Pandas, data preprocessing, data analysis, data visualization, file handling, and automation**.

---

## ✨ Features

- 📁 Supports multiple data formats
- 🔍 Automatic dataset analysis
- 🧹 Automatic data cleaning
- ♻️ Duplicate row detection and removal
- 🗑️ Empty row detection and removal
- 🧹 Empty column detection and removal
- ✨ Text whitespace cleaning
- 🏷️ Automatic column-name standardization
- 🔢 Numeric column detection
- 📅 Date column detection
- 🩹 Missing-value handling
- 📊 Automatic useful visualizations
- 📄 Automatic JSON cleaning report
- 💾 Cleaned dataset export
- ⚙️ Modular project architecture
- 🛡️ Conservative cleaning rules to avoid unnecessary data changes

---

## 📂 Supported File Formats

CleanFlow currently supports:

| Format | Extension |
|---|---|
| CSV | `.csv` |
| Excel | `.xlsx` |
| Excel | `.xls` |
| JSON | `.json` |
| TSV | `.tsv` |

---

## 🛠️ Technologies Used

- **Python**
- **Pandas**
- **NumPy**
- **Matplotlib**
- **OpenPyXL**
- **XLRD**

---

## 🏗️ Project Architecture

CleanFlow follows a modular architecture where each component has a specific responsibility.

```text
                    ┌─────────────────┐
                    │    User File    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │     Loader      │
                    │ File Detection  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    Analyzer     │
                    │ Data Inspection │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │     Cleaner     │
                    │ Cleaning Engine │
                    └────────┬────────┘
                             │
                             ▼
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
       ┌────────────┐ ┌────────────┐ ┌──────────────┐
       │  Exporter  │ │ Visualizer │ │   Reporter   │
       │ Clean File │ │   Charts   │ │ Quality Log │
       └────────────┘ └────────────┘ └──────────────┘
              │              │              │
              └──────────────┼──────────────┘
                             ▼
                    ┌─────────────────┐
                    │      Output     │
                    │ Clean Data +    │
                    │ Charts + Report │
                    └─────────────────┘
```

---

## 📁 Project Structure

```text
CleanFlow/
│
├── data/
│   └── messy_sales.csv
│
├── output/
│   └── visualizations/
│
├── src/
│   ├── __init__.py
│   ├── analyzer.py
│   ├── cleaner.py
│   ├── exporter.py
│   ├── loader.py
│   ├── main.py
│   ├── reporter.py
│   └── visualizer.py
│
├── tests/
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

# 🔍 How CleanFlow Works

The application follows a simple automated pipeline:

```text
Input File
    ↓
Detect File Type
    ↓
Load Dataset
    ↓
Analyze Dataset
    ↓
Clean Dataset
    ↓
Validate Cleaning
    ↓
Generate Visualizations
    ↓
Generate Cleaning Report
    ↓
Export Cleaned Dataset
```

---

# 🧹 Data Cleaning

CleanFlow performs several automatic cleaning operations.

## 1. Column Name Cleaning

Column names are standardized to make them easier to work with in Python.

Example:

```text
Customer Name
Product Price
Order Date
```

becomes:

```text
customer_name
product_price
order_date
```

---

## 2. Text Cleaning

Unnecessary whitespace is removed from text values.

Example:

```text
"   John Doe   "
```

becomes:

```text
"John Doe"
```

Empty text values are also treated as missing values.

---

## 3. Duplicate Row Removal

CleanFlow detects duplicate rows and removes them.

Example:

```text
John Doe | Laptop | 55000
John Doe | Laptop | 55000
```

The duplicate record is removed.

The number of removed duplicates is recorded in the cleaning report.

---

## 4. Empty Row Removal

Completely empty rows are automatically detected and removed.

---

## 5. Empty Column Removal

Columns containing no data are detected and removed.

---

## 6. Numeric Column Detection

CleanFlow attempts to detect columns that contain numeric values but are stored as text.

For example:

```text
"500"
"1200"
"55000"
```

can be converted into numeric values when the data strongly indicates that the column is numeric.

The conversion is performed conservatively rather than blindly converting every text column.

---

## 7. Date Detection

CleanFlow attempts to identify columns containing date-like values and convert them into a proper datetime format when the majority of the values can be interpreted as dates.

---

## 8. Missing Value Handling

Different strategies are used depending on the detected data type.

### Numeric columns

Missing numeric values are filled using the column median.

```text
10
20
NaN
30
40
```

The missing value can be replaced with the median rather than automatically assuming it is `0`.

### Text columns

Missing text values are replaced with:

```text
Not Provided
```

### Date columns

Dates are not automatically invented when the correct value cannot be determined.

This helps avoid introducing misleading information into the dataset.

---

# 📊 Automatic Visualizations

CleanFlow automatically creates useful visualizations based on the structure of the dataset.

The goal is **not to generate as many charts as possible**, but to generate charts that provide useful information.

---

## Numeric Data

Numeric columns can generate distribution histograms.

Example:

```text
Price
Quantity
Age
Salary
```

Possible output:

```text
price_distribution.png
quantity_distribution.png
```

---

## Categorical Data

Useful categorical columns can generate frequency bar charts.

Example:

```text
City
Product
Category
Department
```

Possible output:

```text
city_categories.png
product_categories.png
```

---

## Correlation Analysis

When the dataset contains multiple numeric columns, CleanFlow can generate a correlation heatmap.

Example:

```text
Price
Quantity
Revenue
Discount
```

Output:

```text
correlation_heatmap.png
```

---

## Smart Visualization Filtering

CleanFlow avoids generating unnecessary charts for columns that are unlikely to provide useful insights.

For example, columns such as:

```text
email
customer_name
phone
id
```

are generally treated as identifier-like columns and skipped.

Columns with extremely high numbers of unique values are also avoided to prevent unreadable charts.

---

# 📄 Cleaning Report

CleanFlow automatically generates a JSON report describing the cleaning process.

The report can contain information such as:

```text
Original rows
Cleaned rows
Original columns
Cleaned columns
Duplicates removed
Empty rows removed
Empty columns removed
Numeric columns converted
Date columns converted
Missing values handled
Generated visualizations
```

Example:

```json
{
    "original_rows": 100,
    "cleaned_rows": 95,
    "original_columns": 8,
    "cleaned_columns": 7,
    "duplicates_removed": 5,
    "empty_rows_removed": 0,
    "empty_columns_removed": [
        "unused_column"
    ]
}
```

---

# 💾 Output

After processing a dataset, CleanFlow creates an output directory containing the cleaned data, report, and visualizations.

Example:

```text
output/
│
├── cleaned_messy_sales.csv
├── cleaning_report.json
│
└── visualizations/
    ├── price_distribution.png
    ├── quantity_distribution.png
    ├── city_categories.png
    ├── product_categories.png
    └── correlation_heatmap.png
```

The exact files generated depend on the structure of the input dataset.

---

# 🚀 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/CleanFlow.git
```

Then move into the project directory:

```bash
cd CleanFlow
```

---

## 2. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

---

# ▶️ Usage

Run CleanFlow from the project root:

```bash
python src/main.py
```

The program will ask for the path of the input file.

Example:

```text
Enter your file path: data/messy_sales.csv
```

CleanFlow will then automatically:

```text
Load the file
    ↓
Analyze the dataset
    ↓
Clean the data
    ↓
Export the cleaned file
    ↓
Generate visualizations
    ↓
Generate the cleaning report
```

---

# 🧪 Example

Suppose the input dataset contains:

```text
Customer Name,Email,City,Product,Quantity,Price
John Doe,john@gmail.com,Guwahati,Laptop,1,55000
John Doe,john@gmail.com,Guwahati,Laptop,1,55000
Priya Sharma,,Jorhat,Monitor,1,15000
Amit Roy,amit@gmail.com,Dibrugarh,Mouse,,500
```

The dataset contains:

- Duplicate data
- Missing email
- Missing quantity

CleanFlow processes the dataset and produces a cleaned version along with a report and useful visualizations.

---

# 📈 Example Cleaning Process

```text
Original Dataset
----------------
Rows: 8
Columns: 6
Duplicates: 2
Missing Values: 2

          ↓

Cleaning

✓ Standardize column names
✓ Remove duplicate rows
✓ Remove empty rows
✓ Remove empty columns
✓ Detect numeric columns
✓ Detect date columns
✓ Handle missing values

          ↓

Clean Dataset
-------------
Rows: 6
Columns: 6
Duplicates: 0
Missing Values: 0
```

---

# 🎯 Project Goals

CleanFlow was created to demonstrate practical software development and data-processing skills.

The project focuses on:

- Python programming
- Pandas
- NumPy
- Data cleaning
- Data preprocessing
- Data analysis
- Data visualization
- File handling
- Automation
- Modular programming
- Error handling
- Reusable code design

---

# 🧠 Design Philosophy

CleanFlow follows a few important principles:

### 1. Don't blindly modify data

Automatic cleaning can be dangerous when the correct interpretation is unclear.

CleanFlow therefore uses conservative rules where possible.

### 2. Explain what changed

The cleaning report records important operations performed on the dataset.

### 3. Generate useful visualizations

The tool focuses on meaningful charts instead of creating charts for every column.

### 4. Keep the code modular

Different responsibilities are separated into different Python modules.

---

# 🔐 Data Safety

CleanFlow is designed as a local Python application.

Input files are processed locally by the program.

However, users should always review automatically cleaned data before using it for important decisions or production workflows.

Automatic cleaning rules may not be appropriate for every type of dataset.

---

# ⚠️ Limitations

This is a general-purpose data cleaning prototype.

It may not correctly understand domain-specific requirements such as:

- Financial accounting rules
- Medical data standards
- Complex business rules
- Specialized scientific datasets
- Highly structured databases
- Ambiguous missing values

For these situations, custom cleaning rules may be required.

---

# 🔮 Future Improvements

Possible future versions may include:

- 🖥️ Graphical user interface
- 📤 Drag-and-drop file upload
- 📚 Batch processing of multiple files
- 📊 Interactive dashboards
- 🔎 Advanced data validation
- 🧩 Custom cleaning rules
- 🗄️ Database support
- 📑 PDF reporting
- 📈 More advanced statistical analysis
- 🌐 Web-based version

---

# 📌 Project Status

**Status: Working Prototype**

CleanFlow currently provides a functional automated data cleaning and visualization workflow for supported file formats.

---

# 👨‍💻 Author

**Jaskaran Singh**

Student Developer interested in:

- Python
- Data Analysis
- Machine Learning
- AI
- Automation
- Robotics

---

# ⭐ Contributing

Suggestions and improvements are welcome.

If you find a bug or have an idea for improving CleanFlow, feel free to open an issue or submit a pull request.

---

# 📜 License

This project is available for educational and portfolio purposes.

---

## ⭐ If you find CleanFlow useful

Consider giving the repository a star on GitHub.

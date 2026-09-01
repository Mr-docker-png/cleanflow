from pathlib import Path

from loader import load_file
from analyzer import analyze_data
from cleaner import clean_data
from reporter import generate_report, print_report
from visualizer import create_visualizations
from exporter import export_data


def main():
    print("=" * 45)
    print("          CLEANFLOW DATA CLEANER")
    print("=" * 45)

    file_path = input("\nEnter your file path: ").strip()

    try:
   
        print("\n[1/6] Loading file...")

        df = load_file(file_path)

        if df.empty:
            print("\n❌ The file contains no data.")
            return

      
        print("[2/6] Analyzing data...")

        analysis = analyze_data(df)

    
        print("[3/6] Cleaning data...")

        cleaned_df, cleaning_report = clean_data(df)

     
        print("[4/6] Exporting cleaned data...")

        output_file = export_data(
            cleaned_df,
            file_path
        )

     
        print("[5/6] Creating visualizations...")

        visualization_files = create_visualizations(
            cleaned_df
        )

    
        print("[6/6] Generating report...")

        cleaning_report["analysis"] = analysis
        cleaning_report["visualizations"] = (
            visualization_files
        )

        report_file = Path(
            "output/cleaning_report.json"
        )

        generate_report(
            cleaning_report,
            str(report_file)
        )

    
        print_report(cleaning_report)

        print("\n" + "=" * 45)
        print("       CLEANING COMPLETED")
        print("=" * 45)

        print(f"\n✅ Cleaned file:")
        print(f"   {output_file}")

        print(f"\n📄 Cleaning report:")
        print(f"   {report_file}")

        print(
            f"\n📊 Visualizations: "
            f"{len(visualization_files)}"
        )

        if visualization_files:
            print("\nCharts:")

            for file in visualization_files:
                print(f"   • {file}")

        print()

    except FileNotFoundError as error:
        print(f"\n❌ File error: {error}")

    except ValueError as error:
        print(f"\n❌ Input error: {error}")

    except Exception as error:
        print(f"\n❌ Unexpected error: {error}")


if __name__ == "__main__":
    main()
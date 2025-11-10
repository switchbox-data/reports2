import polars as pl
import requests


def fetch_eia_hs861m(path_xlsx: str = "/workspaces/reports2/data/eia/HS861M/eia_hs861m.xlsx"):
    url = "https://www.eia.gov/electricity/data/state/xls/861m/HS861M%202010-.xlsx"
    response = requests.get(url)
    response.raise_for_status()
    try:
        with open(path_xlsx, "wb") as f:
            f.write(response.content)
        print(f"EIA HS861M data fetched and saved to {path_xlsx}")
        return response.content
    except Exception as e:
        print(f"Error: {e}")
        return None


def extract_residential_data(filepath: str, sheet_name: str = "Monthly-States") -> pl.DataFrame:
    """
    Extract residential electricity sector data from the EIA Excel file.

    Parameters:
    -----------
    filepath : str
        Path to the Excel file
    sheet_name : str
        Name of the sheet containing the data (default: "Monthly-States")

    Returns:
    --------
    pl.DataFrame
        DataFrame with columns:
        - Year
        - Month
        - State (2-letter abbreviation)
        - Data_Status
        - Residential_Revenue (million dollars)
        - Residential_Sales (million kWh)
        - Residential_Customers (thousands)
        - Residential_Price (cents/kWh)
    """

    # Read the Excel file without headers, skipping first 3 rows
    df = pl.read_excel(filepath, sheet_name=sheet_name, read_options={"skip_rows": 0, "header_row": 2})

    # Extract the base columns and residential sector columns
    residential_df = pl.DataFrame(
        {
            "Year": df[:, 0],  # Column A
            "Month": df[:, 1],  # Column B
            "State": df[:, 2],  # Column C
            "Data_Status": df[:, 3],  # Column D
            "residential_revenue": df[:, 4],  # Column E
            "residential_sales": df[:, 5],  # Column F
            "residential_customers": df[:, 6],  # Column G
            "residential_rate": df[:, 7],  # Column H
        }
    )

    # Clean up any null rows
    residential_df = residential_df.filter(pl.col("Year").is_not_null() & pl.col("State").is_not_null())

    # Convert Year and Month to integers
    residential_df = residential_df.with_columns(
        [
            pl.col("Year").cast(pl.Int64, strict=False),
            pl.col("Month").cast(pl.Int64, strict=False),
            pl.col("State").cast(pl.String),
        ]
    )

    # create a new column called "date", using the Year and Month columns, and assuming the first day of the month
    residential_df = residential_df.with_columns(
        pl.datetime(year=pl.col("Year"), month=pl.col("Month"), day=1).alias("date")
    )

    # Convert numeric columns to float, handling any non-numeric values
    numeric_columns = ["residential_revenue", "residential_sales", "residential_customers", "residential_rate"]

    residential_df = residential_df.with_columns(
        [pl.col(col).cast(pl.Float64, strict=False) for col in numeric_columns]
    )

    return residential_df


def main():
    filepath = "/workspaces/reports2/data/eia/HS861M/eia_hs861m.xlsx"

    fetch_eia_hs861m(filepath)

    # Extract residential data
    print("Extracting residential data...")
    residential_df = extract_residential_data(filepath)

    print(f"\nShape of residential data: {residential_df.shape}")
    print(f"Columns: {list(residential_df.columns)}")
    print("\nFirst few rows:")
    print(residential_df.head())

    print("\nData types:")
    print(residential_df.dtypes)

    print(f"Year range: {residential_df['Year'].min()} to {residential_df['Year'].max()}")
    print(f"Residential data shape: {residential_df.shape}")

    # save the residential_df to a parquet file
    path_parquet = filepath.replace(".xlsx", "_residential.parquet")
    residential_df.write_parquet(path_parquet)
    print(f"Residential data saved to {path_parquet}")

    return residential_df


if __name__ == "__main__":
    main()

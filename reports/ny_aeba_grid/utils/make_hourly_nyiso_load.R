#!/usr/bin/env Rscript

# Utility script to process NYISO hourly load data from S3
# Reads raw CSV, processes it, and uploads parquet to S3

library(tidyverse)
library(arrow)
library(lubridate)

# Set up S3 filesystem
s3_bucket <- arrow::s3_bucket(
    bucket = "data.sb",
    region = "us-west-2"
)

# S3 file paths (without bucket prefix)
s3_csv_file <- "ny_aeba_grid/nyiso/hourly/20151025-20251026 NYISO Hourly Actual Load.csv"
s3_parquet_file <- "ny_aeba_grid/nyiso/hourly/nyiso_hourly_load.parquet"

cat("Starting NYISO hourly load data processing...\n")
cat("Reading CSV from S3: data.sb/", s3_csv_file, "\n", sep = "")

# Read CSV from S3
nyiso_hourly_load <- arrow::read_csv_arrow(s3_bucket$path(s3_csv_file))

cat("CSV loaded. Processing data...\n")

# Apply transformations
nyiso_hourly_load <- nyiso_hourly_load |>
    # Rename columns to lowercase for easier handling if needed
    rename(
        datetime = Date,
        load = Load,
        zone = Zone
    ) |>
    # ensure load is numeric
    mutate(load = as.numeric(load)) |>
    # Parse the datetime (given as e.g. "10/25/2015  7:00:00 PM" -- note double space between date and hour)
    mutate(
        datetime = lubridate::mdy_hms(
            datetime,
            tz = "America/New_York",
            quiet = TRUE
        ),
        year = lubridate::year(datetime),
        month = lubridate::month(datetime),
        day = lubridate::day(datetime),
        hour = lubridate::hour(datetime)
    ) |>
    select(-datetime)

cat("Data processed successfully.\n")
cat("Writing parquet to S3: data.sb/", s3_parquet_file, "\n", sep = "")

# Write parquet to S3
arrow::write_parquet(
    nyiso_hourly_load,
    s3_bucket$path(s3_parquet_file)
)

cat("✓ Parquet file uploaded to S3 successfully!\n")
cat("Summary:\n")
cat("  - Total rows:", nrow(nyiso_hourly_load), "\n")
cat("  - Columns:", paste(names(nyiso_hourly_load), collapse = ", "), "\n")
cat("  - Year range:", min(nyiso_hourly_load$year), "to", max(nyiso_hourly_load$year), "\n")

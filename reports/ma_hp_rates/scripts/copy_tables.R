library(DBI)
library(duckdb)

# Paths to the databases
source_db_path <- "/workspaces/reports/data/ResStock/2022_resstock_amy2018_release_1.1/rs_ma_hp_rates.db"
target_db_path <- "/workspaces/reports/data/ResStock/2022_resstock_amy2018_release_1.1/rs_ma_hp_targeted.db"

# Connect to both databases
source_con <- DBI::dbConnect(duckdb::duckdb(), source_db_path)
target_con <- DBI::dbConnect(duckdb::duckdb(), target_db_path)

# Tables to copy
tables_to_copy <- c(
  "delivery_tariffs_gas",
  "delivery_tariffs_fueloil",
  "delivery_tariffs_propane",
  "supply_rates_elec",
  "supply_rates_gas",
  "supply_rates_fueloil",
  "supply_rates_propane"
)

# Copy each table
for (table in tables_to_copy) {
  # Read data from source
  data <- DBI::dbGetQuery(source_con, paste0("SELECT * FROM ", table))

  # Write to target
  DBI::dbWriteTable(target_con, table, data, overwrite = TRUE)

  # Print confirmation
  cat(sprintf("Copied table '%s' with %d rows\n", table, nrow(data)))
}

# Disconnect from both databases
DBI::dbDisconnect(source_con)
DBI::dbDisconnect(target_con)

#cat("Table copying completed successfully!\n")

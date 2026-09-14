source("lib/utility_mapping.R")

#create_hh_utilities("NY")

library(tigris)
pumas <- pumas(
  state = "NY",
  year = 2019,
  cb = TRUE # Use cartographic boundaries (simplified)
)

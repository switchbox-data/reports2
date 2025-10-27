
# =============================================================================
# P3M (Posit Package Manager) Configuration - Cross-Platform
# =============================================================================
# Strategy: Prefer binaries on Windows/macOS/Ubuntu, optimized source builds on other Linux
# Fallback: CRAN source builds if P3M fails

# Function to detect Ubuntu release codename
get_ubuntu_codename <- function() {
  if (!file.exists("/etc/os-release")) {
    return(NULL)
  }

  os_info <- readLines("/etc/os-release")
  if (!any(grepl("^ID=ubuntu", os_info))) {
    return(NULL)
  }

  version_codename <- grep("^VERSION_CODENAME=", os_info, value = TRUE)
  if (length(version_codename) > 0) {
    gsub("VERSION_CODENAME=", "", version_codename)
  } else {
    NULL
  }
}

# Find the correct P3M URL
cran_url <- if (Sys.info()["sysname"] == "Linux" && !is.null(get_ubuntu_codename())) {
  # Ubuntu: Use Ubuntu-specific URL for binary access
  # P3M has binaries for Ubuntu 24.04 for x86_64 and arm64
  sprintf("https://p3m.dev/cran/latest/bin/linux/%s-%s/%s", get_ubuntu_codename(), R.version["arch"], substr(getRversion(), 1, 3))
} else {
  # Windows, macOS, and non-Ubuntu Linux: Use standard P3M URL
  "https://p3m.dev/cran/latest"
}

p3m_url <- if (Sys.info()["sysname"] == "Linux" && !is.null(get_ubuntu_codename())) {
  # Ubuntu: Use Ubuntu-specific URL for binary access
  # P3M has binaries for Ubuntu 24.04 for x86_64 and arm64
  sprintf("https://p3m.dev/cran/__linux__/%s/latest", get_ubuntu_codename())
} else {
  # Windows, macOS, and non-Ubuntu Linux: Use standard P3M URL
  "https://p3m.dev/cran/latest"
}



# Configure install.packages() repositories
# Primary repository: P3M with platform-specific URL
# Fallback: CRAN for packages not available in P3M
options(repos = c( # Will get binaries on Windows/macOS/Ubuntu, optimized source builds on other Linux
  CRAN = cran_url, # for install.packages() to get binaries
  P3M = p3m_url # for pak to get binaries
))

# Enable automatic system dependency installation
options(pkg.sysreqs = TRUE)

# Configure pak to use the same repository configuration
if (requireNamespace("pak", quietly = TRUE)) {
  options(pak.repos = getOption("repos"))
}

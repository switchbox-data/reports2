import requests


def fetch_eia_hs861m():
    url = "https://www.eia.gov/electricity/data/state/xls/861m/HS861M%202010-.xlsx"
    response = requests.get(url)
    response.raise_for_status()
    try:
        with open("/workspaces/reports2/data/eia/HS861M/eia_hs861m.xlsx", "wb") as f:
            f.write(response.content)
        print("EIA HS861M data fetched and saved to /workspaces/reports2/data/eia/HS861M/eia_hs861m.xlsx")
        return response.content
    except Exception as e:
        print(f"Error: {e}")
        return None


def main():
    fetch_eia_hs861m()


if __name__ == "__main__":
    main()

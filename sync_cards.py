import requests
import pandas as pd

print("Fetching Scryfall bulk metadata...")

bulk = requests.get(
    "https://api.scryfall.com/bulk-data",
    headers={"User-Agent": "MTG Tracker/1.0"}
).json()

default_cards = next(
    (x for x in bulk["data"] if x["type"] == "default_cards"),
    None
)

if not default_cards:
    raise Exception("default_cards bulk file not found")

download_url = default_cards["download_uri"]

print("Downloading bulk file...")

response = requests.get(
    download_url,
    headers={"User-Agent": "MTG Tracker/1.0"}
)

print("Status:", response.status_code)
print(response.text[:500])

response.raise_for_status()

cards = response.json()

print("Filtering cards...")

filtered = []

for c in cards:
    if c.get("lang") != "en":
        continue

    price = c.get("prices", {}).get("usd")
    if not price:
        continue

    try:
        if float(price) < 1:
            continue
    except:
        continue

    filtered.append([
        c["id"],
        c["name"],
        c["set"].upper(),
        c["collector_number"],
        price.get("usd")
    ])

df = pd.DataFrame(filtered, columns=[
    "id", "name", "set", "collector"
])

output_file = "mtg_cards_filtered.csv"
df.to_csv(output_file, index=False)

print("Done:", len(df))
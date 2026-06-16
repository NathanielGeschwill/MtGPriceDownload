import requests
import pandas as pd

print("Fetching Scryfall bulk metadata...")

bulk = requests.get(
    "https://api.scryfall.com/bulk-data",
    headers={"User-Agent": "MTG Tracker/1.0"}
).json()

download_url = next(
    x["download_uri"]
    for x in bulk["data"]
    if x["type"] == "default_cards"
)

print("Downloading bulk file...")

cards = requests.get(download_url).json()

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
        c["collector_number"]
    ])

df = pd.DataFrame(filtered, columns=[
    "id", "name", "set", "collector"
])

output_file = "mtg_cards_filtered.csv"
df.to_csv(output_file, index=False)

print("Done:", len(df))


import pandas as pd
import time
import requests

URL = "https://api.gbif.org/v1/occurrence/search"
MATCH = "https://api.gbif.org/v1/species/match"

SPECIES = [
    "Acridotheres tristis",
    "Copsychus saularis",
    "Orthotomus sutorius",
    "Microcarbo niger",
    "Alcedo atthis",
    "Cinnyris asiaticus",
    "Merops orientalis",
    "Psilopogon haemacephalus"
]

PAGES_PER_YEAR = 2


def get_json(url, params):
    for attempt in range(5):
        try:
            r = requests.get(url, params=params, timeout=60)

            if r.status_code == 200:
                return r.json()

            print("  HTTP", r.status_code, "for", r.url)
            print("  Reply:", r.text[:200])

            if 400 <= r.status_code < 500 and r.status_code != 429:
                raise SystemExit("Request rejected. Fix the request, don't retry.")

        except requests.exceptions.RequestException as e:
            print("  Problem, attempt", attempt + 1, "-", type(e).__name__)

        time.sleep(5 * (attempt + 1))

    raise SystemExit("GBIF did not answer after 5 attempts. Try again later.")


rows = []

for name in SPECIES:
    key = get_json(MATCH, {"name": name})["usageKey"]

    before = len(rows)

    for year in range(2015, 2026):
        for page in range(PAGES_PER_YEAR):

            res = get_json(URL, {
                "country": "BD",
                "taxonKey": key,
                "hasCoordinate": "true",
                "hasGeospatialIssue": "false",
                "year": year,
                "limit": 300,
                "offset": page * 300
            })

            for rec in res["results"]:
                rows.append({
                    "species": name,
                    "year": rec.get("year"),
                    "decimalLatitude": rec.get("decimalLatitude"),
                    "decimalLongitude": rec.get("decimalLongitude")
                })

            if res["endOfRecords"]:
                break

    print(name, ":", len(rows) - before, "records")


df = pd.DataFrame(rows)

df.to_csv("data/background_birds.csv", index=False)

print()
print("Total background records:", len(df))

print(
    "Unique locations (rounded to about 100m):",
    len(
        df[["decimalLatitude", "decimalLongitude"]]
        .round(3)
        .drop_duplicates()
    )
)

print("Saved data/background_birds.csv")


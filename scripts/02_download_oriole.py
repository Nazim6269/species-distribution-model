import time
import warnings
import pandas as pd
from pygbif import occurrences as occ

warnings.filterwarnings("ignore", category=DeprecationWarning)

KEY = 2488963   # Oriolus xanthornus

KEEP = ["gbifID", "species", "decimalLatitude", "decimalLongitude",
        "coordinateUncertaintyInMeters", "year", "month",
        "stateProvince", "basisOfRecord", "datasetName"]

rows = []
offset = 0

while True:
    res = occ.search(
        country="BD",
        taxonKey=KEY,
        hasCoordinate=True,
        hasGeospatialIssue=False,
        year="2010,2025",
        limit=300,
        offset=offset,
    )
    rows.extend(res["results"])
    print("Downloaded", len(rows), "records")
    if res["endOfRecords"]:
        break
    offset += 300
    time.sleep(0.5)

# Check that every column we asked for really exists in the downloaded data
missing = [c for c in KEEP if c not in rows[0]]
print("Columns not found in the first record:", missing)

df = pd.DataFrame(rows).reindex(columns=KEEP)
df.to_csv("data/raw_oriole.csv", index=False)
print("Saved to data/raw_oriole.csv")

print()
print("Total records:", len(df))
print()
print("Record types:")
print(df["basisOfRecord"].value_counts())
print()
print("Top datasets:")
print(df["datasetName"].value_counts().head(5))
print()
print("Records per year:")
print(df["year"].value_counts().sort_index())
print()

if df["coordinateUncertaintyInMeters"].notna().any():
    print("Coordinate uncertainty (m):")
    print(df["coordinateUncertaintyInMeters"].describe())
else:
    print("No record has a coordinate uncertainty value")

print()
df["lat3"] = df["decimalLatitude"].round(3)
df["lon3"] = df["decimalLongitude"].round(3)
per_spot = df.groupby(["lat3", "lon3"]).size().sort_values(ascending=False)

print("Unique locations (rounded to about 100 m):", len(per_spot))
print("Records in the 5 busiest locations:")
print(per_spot.head(5))
print("Share of records in the top 20 locations:",
      round(per_spot.head(20).sum() / len(df), 2))

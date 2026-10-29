import time
import pandas as pd
import warnings
from pygbif import occurrences as occ

warnings.filterwarnings("ignore",category=DeprecationWarning)

KEY=2488963
KEEP=['gbifID','species','decimalLatitude','decimalLongitude','coordinateUncetainityMeters','year','month','sateProvince','basisOfRecord','datasetName']

rows = []
offset=0

while True:
    res = occ.search(
        country="BD",
        taxonKey=KEY,
        hasCoordinate=True,
        hasGeospatialIssue=False,
        year='2010,2025',
        limit=300,
        offset=offset
    )
    rows.extend(res['results'])
    print("Downloaded", len(rows), "records")
    if res['endOfRecords']:
        break
    offset +=300
    time.sleep(0.5)
df = pd.DataFrame(rows).reindex(columns=KEEP)

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
print("Coordinate uncertainty (m):")
print(df["coordinateUncertaintyInMeters"].describe())
print("Records with no uncertainty value:",
      df["coordinateUncertaintyInMeters"].isna().sum())
print()
unique_spots = df[["decimalLatitude", "decimalLongitude"]].round(3).drop_duplicates()
print("Unique locations (rounded to about 100 m):", len(unique_spots))

df.to_csv("data/raw_oriole.csv", index=False)
print()
print("Saved to data/raw_oriole.csv")

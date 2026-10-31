import glob
import rasterio
import numpy as np

import pandas as pd

df = pd.read_csv("data/thinned_oriole.csv")

files = glob.glob("data/worldclim/*bio_*.tif")
files = sorted(
    files,
    key=lambda f: int(f.split("bio_")[1].split(".")[0])
)
print("Layers found: ", files)

coords = list(zip(df["decimalLongitude"],df["decimalLatitude"]))

for f in files:
    number = f.split("bio_")[1].split(".")[0]
    with rasterio.open(f) as src:
        values= np.array([v[0] for v in src.sample(coords)],dtype=float)
        if src.nodata is not None:
            values[values == src.nodata] = np.nan
    df["bio"+  number] = values
bio_cols = [c for c in df.columns if c.startswith("bio")]

print()
print("Records with missing climate value: ", df[bio_cols].isna().any(axis=1).sum())
df = df.dropna(subset=bio_cols)
print("Records kep: ", len(df))

print()
print("Range of each layers accross records")
print(df[bio_cols].describe().loc[["min","max"]].round(1).T)

corr = df[bio_cols].corr().abs()
pairs = []
for i, a in enumerate(bio_cols):
    for b in bio_cols[i +1 :]:
        if corr.loc[a,b] > 0.8:
            pairs.append((a,b,round(corr.loc[a,b],2)))
print()
print("Pairs with coorelation above 0.8: ", len(pairs),"of", len(bio_cols)*(len(bio_cols) -1 )//2)
for p in pairs[:15]:
    print(p)

df.to_csv("data/oriole_climate.csv")
print()

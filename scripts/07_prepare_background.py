import pandas as pd
import rasterio
import glob
import numpy as np

KEEP_VARS = ["bio12","bio1","bio15","bio14","bio3","bio2"]

bg = pd.read_csv("data/background_birds.csv")
print("Start: " ,len(bg), "records")


# 1. Remove records without coordinates, and keep the same box as before
bg=bg.dropna(subset=["decimalLatitude","decimalLongitude"])
bg = bg[bg["decimalLatitude"].between(20.5,26.7) & bg["decimalLongitude"].between(88.0,92.8)]
print("Inside the box: ", len(bg))


# 2. Thin to one record per 5 km cell (same rule as for the oriole)
cell = 5/111
gx = np.floor(bg["decimalLatitude"] / cell)
gy = np.floor(bg["decimalLongitude"] / cell)
bg= bg.groupby([gx,gy]).head(1).copy()


# 3. Extract the same climate variables
coords = list(zip(bg["decimalLatitude"],bg["decimalLongitude"]))
for v in KEEP_VARS:
    number = v.replace("bio","")
    f = glob.glob(f"data/worldclim/*bio_{number}.tif")[0]
    with rasterio.open(f) as src:
        values = np.array([x[0] for x in src.sample(coords)],dtype=float)
        if src.nodata is not None:
            values[values == src.nodata] = np.nan
    bg[v]=values

print("Missing climate values: ", bg[KEEP_VARS].isna().any(axis=1).sum())
bg = bg.dropna(subset=KEEP_VARS)
print("Background point keep", len(bg))

# Compare presence and background
pres = pd.read_csv("data/oriole_selected.csv")
print()
print("Mean Climae values")
comp = pd.DataFrame({"oriole":pres[KEEP_VARS].mean(),"background":bg[KEEP_VARS].mean()})

print(comp.round(1))

bg[["decimalLatitude", "decimalLongitude"] + KEEP_VARS].to_csv(
    "data/background_selected.csv", index=False)
print()
print("Saved data/background_selected.csv")

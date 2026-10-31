import pandas as pd
import numpy as np

df=pd.read_csv("data/raw_oriole.csv")
print("Start: ", len(df), "records")

df =  df[df["year"] >= 2015]
print("From 2015",len(df))

df = df[df["basisOfRecord"] == "HUMAN_OBSERVATION"]
print('Sighitings only: ', len(df))

df = df[df["decimalLatitude"].between(20.5,26.7) & df["decimalLongitude"].between(88.0,92.8)]
print("Inside the Bangladesh Bound Box: ", len(df))

for cell_km in [1,5,10]:
    cell = cell_km/111
    gx = np.floor(df['decimalLongitude']/ cell)
    gy = np.floor(df['decimalLatitude']/cell)
    thinned = df.groupby([gx,gy]).head(1)
    print("Cell size: ", cell_km, len(thinned), "rcords kept")


cell = 5/111
gx = np.floor(df["decimalLongitude"]/cell)
gy = np.floor(df["decimalLatitude"]/cell)
thinned = df.groupby([gx,gy]).head(1)
thinned.to_csv("data/thinned_oriole.csv",index=False)
print()
print("Saved thinnned Oriole",len(thinned))


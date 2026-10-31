import pandas as pd

df = pd.read_csv("data/oriole_climate.csv")


priority = ["bio12", "bio1", "bio15", "bio14", "bio7", "bio3", "bio2",
            "bio4", "bio5", "bio6", "bio8", "bio9", "bio10", "bio11",
            "bio13", "bio16", "bio17", "bio18", "bio19"]

corr = df[priority].corr().abs()

keep = []
for v in priority:
    if all(corr.loc(v,k) < 0.7 for k in keep):
        keep.append(v)

print("Kept variables:", keep)
print()
print("Correlations among kept variables:")
print(corr.loc[keep, keep].round(2))
print()
print("Spread of kept variables:")
print(df[keep].describe().loc[["min", "max", "std"]].round(1).T)

cols = ["decimalLatitude", "decimalLongitude"] + keep
df[cols].to_csv("data/oriole_selected.csv", index=False)
print()
print("Saved data/oriole_selected.csv with", len(df), "records")

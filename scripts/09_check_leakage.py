import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GroupKFold, train_test_split
from sklearn.metrics import roc_auc_score

VARS = ["bio12", "bio1", "bio15", "bio14", "bio3", "bio2"]

pres = pd.read_csv("data/oriole_selected.csv")
bg = pd.read_csv("data/background_selected.csv")
pres["y"] = 1
bg["y"] = 0
data = pd.concat([pres, bg], ignore_index=True)

# 1. How many identical climate vectors are there?
key = data[VARS].round(3).astype(str).agg("|".join, axis=1)
print("Rows:", len(data), "| unique climate vectors:", key.nunique())
labels_per_vec = data.groupby(key)["y"].nunique()
print("Vectors shared by both oriole and background:", (labels_per_vec > 1).sum())
print()


def make_rf():
    return RandomForestClassifier(n_estimators=300, min_samples_leaf=5,
                                  class_weight="balanced", random_state=42)


X, y = data[VARS], data["y"]

# 2. Random split, real labels vs shuffled labels
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3,
                                          random_state=42, stratify=y)
rf = make_rf().fit(X_tr, y_tr)
print("Random split, real labels AUC:", round(roc_auc_score(y_te, rf.predict_proba(X_te)[:, 1]), 3))

y_shuf = y.sample(frac=1, random_state=1).reset_index(drop=True)
X_tr, X_te, ys_tr, ys_te = train_test_split(X, y_shuf, test_size=0.3,
                                            random_state=42, stratify=y_shuf)
rf = make_rf().fit(X_tr, ys_tr)
print("Random split, SHUFFLED labels AUC:", round(roc_auc_score(ys_te, rf.predict_proba(X_te)[:, 1]), 3))

# 3. Spatial block split: whole 0.5 degree blocks go to train or test
bx = np.floor(data["decimalLongitude"] / 0.5).astype(int)
by = np.floor(data["decimalLatitude"] / 0.5).astype(int)
groups = pd.factorize(bx.astype(str) + "_" + by.astype(str))[0]
print()
print("Number of blocks:", len(set(groups)))

aucs = []
for tr, te in GroupKFold(n_splits=5).split(X, y, groups):
    rf = make_rf().fit(X.iloc[tr], y.iloc[tr])
    if y.iloc[te].nunique() == 2:
        aucs.append(roc_auc_score(y.iloc[te], rf.predict_proba(X.iloc[te])[:, 1]))
print("Block CV AUC per fold:", [round(a, 3) for a in aucs])
print("Block CV mean AUC:", round(float(np.mean(aucs)), 3))

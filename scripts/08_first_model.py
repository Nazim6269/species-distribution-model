import pandas as pd
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

VARS = ["bio12","bio1","bio15","bio14","bio3","bio2"]

pres = pd.read_csv('data/oriole_selected.csv')
bg = pd.read_csv('data/background_selected.csv')

pres['y']=1
bg['y']=0

data = pd.concat([pres,bg],ignore_index=True)
print("Presences: ", len(pres), "| Background: ", len(bg))

X =data[VARS]
y= data['y']

X_tr,X_te,y_tr,y_te = train_test_split(X,y,test_size=0.3,random_state=42,stratify=y)

models = {
    "Logistic regression": make_pipeline(
       StandardScaler(),
        LogisticRegression(class_weight="balanced",max_iter=1000)
    ),
    "Random Forest":RandomForestClassifier(n_estimators=300,min_samples_leaf=5,class_weight="balanced",random_state="42")
}

for name,model in models.items():
    model.fit(X_tr,y_tr)
    auc = roc_auc_score(y_te,model.predict_proba(X_te)[:,1])
    print(name, "test AUC",round(auc,3))


rf = models["Random forest"]
print()
print("Varibale importance (random forest):")
for v, imp in sorted(zip(VARS,rf.feature_importances_),key=lambda t:-t[1]):
    print(" ", v, round(imp,3))


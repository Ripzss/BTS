import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, KFold, GridSearchCV
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, f1_score,confusion_matrix,recall_score,precision_score, classification_report, roc_curve, roc_auc_score
from sklearn.datasets import load_wine
pd.set_option("display.max_columns", None)  # viser alle kolonner
pd.set_option("display.width", None)        # unngår linjebryting

data = load_wine()
#intro
y = data["target"]
X = data["data"]
stoy = np.random.normal(loc=0, scale=1, size=X.shape)
plt.title("Støy lagt til input-dataene")
plt.hist(stoy.flatten(), bins=50)
plt.show()
X_stoy = X + stoy

#1Lag en dataframe og legg til korrekte variabel-navn
df = pd.DataFrame(X_stoy, columns= data["feature_names"])
df["Target"] = y
df["TargetNames"]= df["Target"].map({0:data["target_names"][0],1:data["target_names"][1],2:data["target_names"][2]})
print(df.head())

#2Splitt dataene i trening og test
X_train, X_test, y_train, y_test = train_test_split(df,df["Target"],random_state=42)


#3 Lag et korrelasjonsdiagram av treningsdataene
X_corr = X_train.select_dtypes(include=[np.number]).corr()
mask = np.triu(np.ones_like(X_corr, dtype=bool))

plt.figure(figsize=(10,10))
sns.heatmap(X_corr, mask=mask, annot=True, fmt=".2f", square=True)
plt.show()

#4 Velg en modelltype fra Sklearn med minst 3 hyperparametre og sett opp grid search og 5-folds kryss-validering
Modell = RandomForestClassifier(random_state=42)

parametre = {
    "n_estimators": range(50,100,150),
    "max_depth": range(3,5,7),
    "min_samples_split": range(2,5,10),
}

cv = KFold(n_splits=3, shuffle=True, random_state=42)

grid_search = GridSearchCV(
    estimator=Modell,
    param_grid=parametre,
    cv=cv,
    scoring= "accuracy",
    verbose=1
)
grid_search.fit(X_train.iloc[:,:-2], y_train)

print("Beste parametre", grid_search.best_params_)
print("Beste Kryss-validering", grid_search.best_score_)

for fold, (train_idx, val_idx) in enumerate(cv.split(X, y), 1):
    best_acc = 0
for n_estimators in [50, 100, 150]:
    for max_depth in [3, 5, 7]:
        for min_samples_split in [2, 5, 10]:
            cv_score = []
            for train_idx, val_idx in cv.split(X_train, y_train):
                X_train_cv, X_val_cv = X_train.iloc[train_idx], X_train.iloc[val_idx]
                y_train_cv, y_val_cv = y_train.iloc[train_idx], y_train.iloc[val_idx]

                rf = RandomForestClassifier(n_estimators=n_estimators,
                                            max_depth=max_depth,
                                            min_samples_split=min_samples_split)

                rf.fit(X_train_cv.iloc[:, :-2], y_train_cv)
                y_hat_val_cv = rf.predict(X_val_cv.iloc[:, :-2])
                acc = accuracy_score(y_val_cv, y_hat_val_cv)
                cv_score.append(acc)
            mean_cv_score = np.asarray(cv_score).mean()
            if mean_cv_score > best_acc:
                best_acc = mean_cv_score
                print(best_acc)
                print(
                    f"Parameters: n_estimators={n_estimators}, max_depth={max_depth}, min_samples_split={min_samples_split}")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import  train_test_split
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
import seaborn as sns
from sklearn.metrics import accuracy_score, f1_score,confusion_matrix,recall_score,precision_score, classification_report, roc_curve, roc_auc_score
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import log_loss, accuracy_score

iris = load_iris()

#1 laster in modellen
df = pd.DataFrame(data=iris["data"], columns=iris["feature_names"])
df["Target"] = iris["target"]
df["TargetNames"]= df["Target"].map({0:iris["target_names"][0],1:iris["target_names"][1],2:iris["target_names"][2]})
print(df.head())

#2 Split data i trening/utvikling og test
X_train, X_test, y_train, y_test = train_test_split(df.iloc[:,:4],df["Target"],random_state=42)

#3 Tren modellen
logreg = LogisticRegression(solver='lbfgs',max_iter=10)
logreg.fit(X_train, y_train)
print("Nøyaktighet = {:.2f}".format(logreg.score(X_test,y_test)))
y_test_hat=logreg.predict(X_test)

#4 Print/plot relevant metricts/plots
sns.heatmap(confusion_matrix(y_test,y_test_hat), annot=True, cbar=False,cmap="Blues")
plt.ylabel("Faktisk verdi")
plt.xlabel("Predikert verdi")
plt.xticks([0.5,1.5,2.5],iris["target_names"])
plt.yticks([0.5,1.5,2.5],iris["target_names"])
plt.show()


y_test_hat = logreg.predict_proba(X_test)
y_test_cat = pd.get_dummies(y_test)


def plot_roc_curve(y_test, y_test_hat, name):
    fpr, tpr, _ = roc_curve(y_test, y_test_hat)
    plt.plot(fpr, tpr, label=name)

    plt.xlabel("FPR / 1 - Spesifisitet ")
    plt.ylabel("TPR / Sensitivitet ")


for n in range(3):
    X_test_class_n = X_test
    y_test_class_n_hat = logreg.predict_proba(X_test_class_n)

    roc_score = roc_auc_score(y_test_cat.iloc[:, n], y_test_class_n_hat[:, n])
    plot_roc_curve(y_test_cat.iloc[:, n], y_test_class_n_hat[:, n], name=iris["target_names"][n])
    print(roc_score)
plt.legend()
plt.show()
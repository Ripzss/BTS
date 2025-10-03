import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.optimize import linear_sum_assignment
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import confusion_matrix, classification_report, f1_score, accuracy_score
from sklearn.model_selection import  train_test_split
pd.set_option("display.max_columns", None)  # viser alle kolonner
pd.set_option("display.width", None)        # unngår linjebryting
from sklearn.datasets import load_breast_cancer, make_blobs






#Intro
cancer = load_breast_cancer(as_frame=True)
X_data = cancer.data
y_data = cancer.target
X_train, X_test, y_train, y_test = train_test_split(X_data,y_data,random_state=42)

#1
kmeans = KMeans(n_clusters=2, random_state=42)
kmeans.fit(X_train)

y_hat_test = kmeans.predict(X_test)

#2
cm = confusion_matrix(y_test, y_hat_test)
sns.heatmap(cm, annot=True)
plt.ylabel("Faktisk verdi")
plt.xlabel("Predikert verdi")
plt.show()

#3
def hungarian_match(y_true, y_pred):
    """
    Matches predicted cluster labels to true labels using the Hungarian algorithm.
    Returns remapped y_pred and accuracy score.
    """

    cm = confusion_matrix(y_true, y_pred)
    row_ind, col_ind = linear_sum_assignment(-cm)

    # Create a mapping from cluster -> label
    mapping = {col: row for row, col in zip(row_ind, col_ind)}

    # Remap y_pred
    y_pred_remapped = np.array([mapping[cluster] for cluster in y_pred])
    acc = accuracy_score(y_true, y_pred_remapped)

    return y_pred_remapped, acc, mapping


_, acc, mapping = hungarian_match(y_test, y_hat_test)
print("Mapping (cluster -> label):", mapping)
print("Accuracy:", acc)

y_hat_test = (y_hat_test==0)*1
f1_score(y_test, y_hat_test)

cm = confusion_matrix(y_test, y_hat_test)
sns.heatmap(cm, annot=True)
plt.ylabel("Faktisk verdi")
plt.xlabel("Predikert verdi")
plt.show()

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_test)

colors = {0: 'red', 1: 'blue'}

scatter_colors = [colors[cluster] for cluster in y_hat_test]
scatter_colors = np.asarray(scatter_colors)


plt.figure(figsize=(8, 6))

markers = ["o","*"]
for i in range(2):


    plt.scatter(X_pca[:, 0][y_test==i], X_pca[:, 1][y_test==i], c=scatter_colors[y_test==i], marker=markers[i], edgecolor='k', s=200, label=f"class_{i}")
    #plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], c='red', marker='X', s=200, label='Centroids')
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.title("K-means Clustering on Breast Cancer Dataset (PCA-reduced data)")
    plt.legend()
plt.show()

#4
X_test["mean radius thr"] = (X_test["mean radius"] > X_test["mean radius"].mean())*1
colors = {0: 'red', 1: 'blue'}

scatter_colors = [colors[cluster] for cluster in y_hat_test]
scatter_colors = np.asarray(scatter_colors)


plt.figure(figsize=(8, 6))

markers = ["o","*"]
for i in np.asarray(X_test["mean radius thr"]):


    plt.scatter(X_pca[:, 0][X_test["mean radius thr"]==i], X_pca[:, 1][X_test["mean radius thr"]==i], c=scatter_colors[X_test["mean radius thr"]==i], marker=markers[i], edgecolor='k', s=200, label=f"class_{i}")
    #plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], c='red', marker='X', s=200, label='Centroids')
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.title("K-means Clustering on Breast Cancer Dataset (PCA-reduced data)")
    #plt.legend()
plt.show()
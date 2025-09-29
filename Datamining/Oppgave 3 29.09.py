import numpy as np
import pandas as pd
from sklearn.model_selection import  train_test_split
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, f1_score,confusion_matrix,recall_score,precision_score, classification_report, roc_curve, roc_auc_score
from sklearn.datasets import load_wine
data = load_wine()

#intro
y = data["target"]
X = data["data"]
stoy = np.random.normal(loc=0, scale=1, size=X.shape)
plt.title("Støy lagt til input-dataene")
plt.hist(stoy.flatten(), bins=50)
plt.show()


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Oppgave 1 del 1 og 2
df_tot = pd.read_csv("tot_pop.csv")
df_sub = pd.read_csv("sub_pop.csv")

gender_tot = df_tot["Sex"].value_counts(normalize=True)
gender_sub = df_sub["Sex"].value_counts(normalize=True)

print(gender_tot)
print(gender_sub)


#Oppgave 1 del 3
embarked_count = df_tot["Embarked"].value_counts()
plt.figure(figsize = (6,4))
embarked_count.plot(kind = "bar")
plt.title("Antall")
plt.xlabel("havn")
plt.ylabel("count")
plt.show()

#Oppgave 1 del 4
all_fares = df_tot["Fare"]
subset_fares = df_tot[df_tot["Embarked"] == "S"]["Fare"]
plt.figure(figsize=(8,5))
plt.hist(all_fares, bins=50, alpha=0.6, label="Total populasjon")
plt.hist(subset_fares, bins=50, alpha=0.6, label="Utvalg (Embarked = S)")
plt.title("Fordeling av billettpris (Fare)")
plt.xlabel("Billettpris")
plt.ylabel("Antall passasjerer")
plt.legend()
plt.show()

#Oppgave 1 del 5

stat_tot = {
    "Gjennomsniit": all_fares.mean(),
    "Median": all_fares.median(),
    "Standardavvik": all_fares.std(),
}
stat_sub = {
    "Gjennomsniit": subset_fares.mean(),
    "Median": subset_fares.median(),
    "Standardavvik": subset_fares.std(),
}
stats_df = pd.DataFrame([stat_tot, stat_sub], index =["Total", "Utvalig (S)"])

print(stats_df)

#oppgave 1 del 6
cor_tot = df_tot.corr(numeric_only=True)
subset = df_tot[df_tot["Embarked"] == "S"]
corr_subset = subset.corr(numeric_only=True)

fig, axes = plt.subplots(1,2,figsize=(14,6))

sns.heatmap(cor_tot,annot=True,cmap="coolwarm",center=0,ax=axes[0])
axes[0].set_title("Correlation")

sns.heatmap(corr_subset,annot=True,cmap="coolwarm",ax=axes[1])
axes[1].set_title("Correlation")
plt.tight_layout()
plt.show()
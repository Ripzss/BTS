import pandas as pd

df_tot = pd.read_csv("tot_pop.csv")
df_sub = pd.read_csv("sub_pop.csv")

df_tot = df_tot.drop(columns="Survived")

print(df_tot)
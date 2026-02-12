import pandas as pd
import os

df = pd.read_excel("PtX_demand_DK.xlsx")
df.to_csv("PtX_demand_DK.csv", index=False)

df = pd.read_excel("2030_DK.xlsx")
df.to_csv("2030_DK.csv", index=False)

df = pd.read_excel("2040_DK.xlsx")
df.to_csv("2040_DK.csv", index=False)

df = pd.read_excel("2050_DK.xlsx")
df.to_csv("2050_DK.csv", index=False)
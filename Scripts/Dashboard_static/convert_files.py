import pandas as pd
import os

df = pd.read_excel("PtX_demand_EU27.xlsx")
df.to_csv("PtX_demand_EU27.csv", index=False)

df = pd.read_excel("2030_EU27.xlsx")
df.to_csv("2030_EU27.csv", index=False)

df = pd.read_excel("2040_EU27.xlsx")
df.to_csv("2040_EU27.csv", index=False)

df = pd.read_excel("2050_EU27.xlsx")
df.to_csv("2050_EU27.csv", index=False)
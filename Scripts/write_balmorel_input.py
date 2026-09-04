import pandas as pd
import numpy as np
import os
import functions as fn
import mappings as mp
from pybalmorel import IncFile

### SETTINGS
# Initial setting, how should renewable fuels be distributed between types?
# Shipping
ammonia_share_shipping = 0.5
methanol_share_shipping = 1 - ammonia_share_shipping
# Aviation
e_kerosene_share_aviation = 0.5
bio_kerosene_share_aviation = 1 - e_kerosene_share_aviation
# Model years
model_years = [2030, 2040, 2050]
# END OF SETTINGS

# Read input data from the Outputs folder.
input_path = os.path.join('Outputs')

df_all = fn.read_country_files(input_path)  # Use the function to read and process country files

# Get the list of countries, sectors, fuels, and years from the dataframes
countries = df_all['Country'].unique().tolist()
sectors = df_all['Sector'].unique().tolist()
fuels = df_all['FuelGroup'].unique().tolist()
years = df_all['Year'].unique().tolist()

print("Data summary:")
print("- Countries: ", countries)
print("- Sectors: ", sectors)
print("- Fuels: ", fuels)
print("- Years: ", years)

# Load initial electricity demand data from the Outputs folder
initial_electricity_demand = pd.read_excel(os.path.join("data", 'demand_electricity.xlsx'), index_col=0)
# Get demands from the main dataframe using the extract_demands function
# Gases in sectors other than non-metal minerals are excluded, these account for a very small share of the total demand and are not relevant for the model.
pd.options.display.float_format = '{:.2f}'.format
dict_demands_1 = fn.extract_demands(df_all, model_years, initial_electricity_demand,0,0, ammonia_share_shipping, methanol_share_shipping, e_kerosene_share_aviation, bio_kerosene_share_aviation)
dict_demands_2 = fn.extract_demands(df_all, model_years, initial_electricity_demand,0.7,0.8, ammonia_share_shipping, methanol_share_shipping, e_kerosene_share_aviation, bio_kerosene_share_aviation)

print("Demands extracted:")
for category, demand_df in dict_demands_1.items():
    print(f"- {category}: {demand_df.shape[0]} rows")

electricity_demand_transport = dict_demands_1['electricity_demand_transport']
electricity_demand = dict_demands_1['electricity_demand']

fn.write_incfile(filename='TRANSPORT_DE',
                dataframe=electricity_demand_transport,
                prefix="TABLE   DE1_TRANS(RRR,DEUSER,YYY)   'Annual electricity consumption (MWh)'\n",
                suffix="\n;\nDE(YYY,RRR,DEUSER)$(DE1_TRANS(RRR,DEUSER,YYY))   = DE1_TRANS(RRR,DEUSER,YYY);",
                path="incfiles")

fn.write_incfile(filename='DE',
                dataframe=electricity_demand,
                prefix="TABLE   DE1(RRR,DEUSER,YYY)   'Annual electricity consumption (MWh)'\n",
                suffix="\n;\nDE(YYY,RRR,DEUSER)$(DE1(RRR,DEUSER,YYY))   = DE1(RRR,DEUSER,YYY);",
                path="incfiles")

hydrogen_demand = dict_demands_1['hydrogen_demand']

fn.write_incfile(filename='HYDROGEN_DH2',
                dataframe=hydrogen_demand,
                prefix="TABLE HYDROGEN_DH22(CCCRRRAAA,YYY) 'Hydrogen demand by region and year'\n",
                suffix="\n;\nHYDROGEN_DH2(YYY,CCCRRRAAA) = HYDROGEN_DH22(CCCRRRAAA,YYY);",
                path="incfiles")

industrial_demand = dict_demands_1['industry_demand']

fn.write_incfile(filename='GMINF',
                dataframe=industrial_demand,
                prefix="TABLE GMINF(YYY,CCCRRRAAA,FFF) 'Minimum fuel use (GJ) per year'\n",
                suffix="\n;",
                path="incfiles")

fuel_demand = dict_demands_1['fuel_demand']

fn.write_incfile(filename='OPTIFLOW_SOSIBUBOUND',
                dataframe=fuel_demand,
                prefix="TABLE SOSIBUBOUND1(AAA,PROC,FLOW,iLOUPFXSET,YYY) 'Bounds on Source, Sink and Buffer Process Flows - for each year'\n",
                suffix="\n;\nSOSIBUBOUND(YYY,AAA,PROC,FLOW,iLOUPFXSET)$(AAAOPTIFLOW(AAA)) = SOSIBUBOUND1(AAA,PROC,FLOW,iLOUPFXSET,YYY);",
                path="incfiles")

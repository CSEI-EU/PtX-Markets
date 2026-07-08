import pandas as pd
import numpy as np
import os

# Read input data from the Outputs folder.
input_path = os.path.join('Outputs')

# Make dictionary of dataframes for each country
dict_country_dataframes = {}

# Loop through all CSV files in the input path and read them into dataframes
for file in os.listdir(input_path):
    if file.endswith(".csv"):
        df = pd.read_csv(os.path.join(input_path, file))
        df.set_index(['FuelGroup','Year'], inplace=True)  # Set 'FuelGroup' column as index
        country_code = file.split('_')[2]  # Get the country code from the file name
        country_code = country_code.split('.')[0]  # Remove the file extension
        dict_country_dataframes[country_code] = df

# Get the list of countries, sectors, fuels, and years from the dataframes
countries = list(dict_country_dataframes.keys())        
sectors = dict_country_dataframes[countries[0]].columns.tolist()
fuels = dict_country_dataframes[countries[0]].index.get_level_values('FuelGroup').unique().tolist()
years = dict_country_dataframes[countries[0]].index.get_level_values('Year').unique().tolist()

print("Countries: ", countries)
print("Sectors: ", sectors)
print("Fuels: ", fuels)
print("Years: ", years)

# Electricity demand by year and country
electricity_demand = pd.DataFrame(index=years, columns=countries)
hydrogen_demand = pd.DataFrame(index=years, columns=countries)
methanol_demand = pd.DataFrame(index=years, columns=countries)
ammonia_demand = pd.DataFrame(index=years, columns=countries)
fossil_kerosene_demand = pd.DataFrame(index=years, columns=countries)
fossil_hfo_demand = pd.DataFrame(index=years, columns=countries)
fossil_diesel_demand = pd.DataFrame(index=years, columns=countries)
biogas_demand = pd.DataFrame(index=years, columns=countries)
renewable_fuels_demand = pd.DataFrame(index=years, columns=countries)
biomass_demand = pd.DataFrame(index=years, columns=countries)
for country in countries:
    df = dict_country_dataframes[country]
    for year in years:
        # Electricity demand is the sum of all sectors for the 'Power' fuel group
        try:
            value = df.loc[('Power', year), :].sum()  # Sum across all sectors for 'Power' fuel group
            electricity_demand.loc[year, country] = value
        except KeyError:
            electricity_demand.loc[year, country] = np.nan  # Assign NaN if the combination does not exist
        # Hydrogen demand is the sum of all sectors for the 'Hydrogen' fuel group
        try:
            value = df.loc[('Hydrogen', year), :].sum()  # Sum across all sectors for 'Hydrogen' fuel group
            hydrogen_demand.loc[year, country] = value
        except KeyError:
            hydrogen_demand.loc[year, country] = np.nan  # Assign NaN if the combination does not exist
        # Methanol demand is the sum of all sectors for the 'Methanol' fuel group
        try:
            value = df.loc[('Methanol', year), :].sum()  # Sum across all sectors for 'Methanol' fuel group
            methanol_demand.loc[year, country] = value
        except KeyError:
            methanol_demand.loc[year, country] = np.nan  # Assign NaN if the combination does not exist
        # Ammonia demand is the sum of all sectors for the 'Ammonia' fuel group
        try:
            value = df.loc[('Ammonia', year), :].sum()  # Sum across all sectors for 'Ammonia' fuel group
            ammonia_demand.loc[year, country] = value
        except KeyError:
            ammonia_demand.loc[year, country] = np.nan  # Assign NaN if the combination does not exist
        # Fossil fuel demands are specific to certain sectors
        try:
            value = df.loc[('Fossil Liquids', year), 'Pass Aviation']  # Pick the value for 'Fossil Liquids' fuel group and 'Pass Aviation' sector
            fossil_kerosene_demand.loc[year, country] = value
        except KeyError:
            fossil_kerosene_demand.loc[year, country] = np.nan  # Assign NaN if the combination does not exist
        try:
            value = df.loc[('Fossil Liquids', year), 'Maritime']  # Pick the value for 'Fossil Liquids' fuel group and 'Maritime' sector
            fossil_hfo_demand.loc[year, country] = value
        except KeyError:
            fossil_hfo_demand.loc[year, country] = np.nan  # Assign NaN if the combination does not exist
        try:
            value = df.loc[('Fossil Liquids', year), ['Pass Road','Pass Rail','Freight Road','Freight Rail']].sum()  # Sum the values for 'Fossil Liquids' fuel group and the specified sectors
            fossil_diesel_demand.loc[year, country] = value
        except KeyError:
            fossil_diesel_demand.loc[year, country] = np.nan  # Assign NaN if the combination does not exist
        # Biogas demand is only for the non-metallic minerals sector, but we add the 'Renewable Energy Carrier' fuel group because its unclear.
        try:
            value1 = df.loc[('Biogenic Gases', year), 'Non-metallic minerals']  # Pick the value for 'Biogas' fuel group and 'Non-Metallic Minerals' sector
            value2 = df.loc[('Renewable Energy Carrier', year), 'Non-metallic minerals']  # Pick the value for 'Biogas' fuel group and 'Chemicals' sector
            biogas_demand.loc[year, country] = value1 + value2
        except KeyError:
            biogas_demand.loc[year, country] = np.nan  # Assign NaN if the combination does not exist
        # Renewable fuels demand is the sum of 'Synthetic Liquids' and 'Biogenic Liquids' fuel groups across all sectors
        try:
            value1 = df.loc[('Synthetic Liquids', year), :].sum()  # Sum the values for 'Synthetic Liquids' fuel group and the specified sectors
            value2 = df.loc[('Biogenic Liquids', year), :].sum()  # Sum the values for 'Synthetic Gases' fuel group and the specified sectors
            renewable_fuels_demand.loc[year, country] = value1 + value2  # Sum the two values to get the total renewable fuels demand
        except KeyError:
            renewable_fuels_demand.loc[year, country] = np.nan  # Assign NaN if the combination does not exist
        # biomass demand is the sum of 'Biomass' fuel group across all sectors
        try:
            value = df.loc[('Biomass [Solid]', year), :].sum()  # Sum the values for 'Biomass' fuel group and the specified sectors
            biomass_demand.loc[year, country] = value
        except KeyError:
            biomass_demand.loc[year, country] = np.nan  # Assign NaN if the combination does not exist



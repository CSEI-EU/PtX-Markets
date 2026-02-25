import os 
import pandas as pd
import pycountry
import streamlit as st 
from mappings import iso_to_country

'''
This files contains all relevant functions to process files and folder with results. 
It ensures all outputs have consistent energy demand values in Exajoules (EJ), and Years as integer. 
Industry results are in MWh and converted to EJ for consistency.

Functions included:
- convert_to_alpha3: Converts alpha 2 country codes into alpha 2 using pycountry module.
- format_country_name: Gets the complete country name from its alpha 2 country code.
- load_transport_data: Load the csv file for transport and convert year colun into integer.
- load_industry_data: Load all country files from Results_per_Country folder for Industry data.
- load_combined_outputs: Load all excel files from Outputs into one Dataframe with countries and fuels projections.
'''

def convert_to_alpha3(iso2):
    try:
        return pycountry.countries.get(alpha_2=iso2).alpha_3
    except Exception:
        return None
    

def format_country_name(code):
    if code != "EU27":
        name = iso_to_country.get(code, code) 
    else:
        name = "European Union"
    return f"{name} ({code})" 


@st.cache_data
def load_transport_data(filepath):
    df = pd.read_csv(filepath)
    df['Year'] = df['Year'].astype(int)
    return df


@st.cache_data
def load_industry_data(filepath):
    MWH_TO_EJ = 3.6e-6
    industry_data = []
    industry_files = [f for f in os.listdir(filepath) if f.endswith(".xlsx")]

    for file_name in industry_files:
        year, country = file_name.replace(".xlsx", "").split("_")
        file_path = os.path.join(filepath, file_name)
        df = pd.read_excel(file_path, index_col=0)
        df = df.apply(pd.to_numeric, errors='coerce').fillna(0)

        for material in df.index:
            for sector in df.columns:
                industry_data.append({
                    "Year": int(year),
                    "Country": country,
                    "Category": sector,
                    "Material": material.strip(),
                    "Value": df.loc[material, sector] * MWH_TO_EJ})
    return pd.DataFrame(industry_data)


@st.cache_data
def load_combined_outputs(folder_path):
    all_data = []
    
    if not os.path.exists(folder_path):
        return pd.DataFrame()
        
    files = [f for f in os.listdir(folder_path) if f.endswith(('.xlsx', '.csv'))]

    for file in files:
        # Extract country code from 'PtX_demand_DE.xlsx' and conveet into dataframe
        country_code = file.split('_')[-1].split('.')[0]
        file_path = os.path.join(folder_path, file)
        df = pd.read_csv(file_path) if file.endswith('.csv') else pd.read_excel(file_path)
        sector_cols = [c for c in df.columns if c not in ['FuelGroup', 'Year']]
        df_long = df.melt(id_vars=['FuelGroup', 'Year'], value_vars=sector_cols, var_name='Sector', value_name='Value')
        
        # Remove pre-calculated subtotals to prevent double counting in plots
        df_long = df_long[df_long['FuelGroup'] != 'Overall Demand']
        df_long['Country'] = country_code
        all_data.append(df_long)
        
    return pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame()
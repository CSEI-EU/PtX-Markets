import pandas as pd
import numpy as np
import os
import mappings as mp
from pybalmorel import IncFile

def read_country_files(input_path):
    """
    Reads all CSV files in the specified input path and returns a concatenated DataFrame.
    
    Parameters:
    input_path (str): The path to the directory containing the CSV files.
    
    Returns:
    pd.DataFrame: A DataFrame containing all the data from the CSV files.
    """
    df_all = pd.DataFrame()  # Create an empty dataframe to hold all data

    # Loop through all CSV files in the input path and read them into dataframes
    for file in os.listdir(input_path):
        if file.endswith(".csv"):
            df = pd.read_csv(os.path.join(input_path, file))
            country_code = file.split('_')[2]  # Get the country code from the file name
            country_code = country_code.split('.')[0]  # Remove the file extension
            df_unpivot = pd.melt(df, id_vars=['Year','FuelGroup'], value_vars=df.columns.tolist(), var_name='Sector', value_name='Demand')
            df_unpivot.fillna(0, inplace=True)  # Fill NaN values with 0
            try:
                df_unpivot['Country'] = mp.region_map[country_code]  # Add a 'Country' column with the country code
            except KeyError:
                df_unpivot['Country'] = country_code  # Add a 'Country' column with the country code
            df_all = pd.concat([df_all, df_unpivot], ignore_index=True)

    df_all["FuelGroup"] = df_all["FuelGroup"].replace({"Renewable Energy Carrier":"Biogenic Gases"}) # we assume this carrier for industry is biogenic gases.
    df_all["Demand"] = df_all["Demand"] * 1e9 / 3.6  # EJ to MWh
    
    return df_all

def extract_demands(df_all,
                    model_years,
                    initial_electricity_demand,
                    set_custom_aviation_RES=0,
                    set_custom_shipping_RES=0,
                    ammonia_share_shipping=0.5,
                    methanol_share_shipping=0.5,
                    e_kerosene_share_aviation=0.5,
                    bio_kerosene_share_aviation=0.5):
    """
    Extracts various demand dataframes from the main dataframe.
    
    Parameters:
    df_all (pd.DataFrame): The main dataframe containing all data.
    
    Returns:
    dict: A dictionary containing various demand dataframes.
    """
    electricity_demand_light = df_all[(df_all['FuelGroup'] == 'Power') & (df_all['Country'] != 'EU27') & (df_all['Sector'] == 'Pass Road')].groupby(['Country', 'Year'])['Demand'].sum().reset_index()
    electricity_demand_light = electricity_demand_light.pivot(index='Country', columns='Year', values='Demand').fillna(0)
    electricity_demand_light = distribute_demand(electricity_demand_light, mp.germany, mp.denmark, mp.sweden)

    electricity_demand_heavy = df_all[(df_all['FuelGroup'] == 'Power') & (df_all['Country'] != 'EU27') & (df_all['Sector'] == 'Freight Road')].groupby(['Country', 'Year'])['Demand'].sum().reset_index()
    electricity_demand_heavy = electricity_demand_heavy.pivot(index='Country', columns='Year', values='Demand').fillna(0)
    electricity_demand_heavy = distribute_demand(electricity_demand_heavy, mp.germany, mp.denmark, mp.sweden)

    electricity_demand_rail = df_all[(df_all['FuelGroup'] == 'Power') & (df_all['Country'] != 'EU27') & (df_all['Sector'].isin(['Pass Rail', 'Freight Rail']))].groupby(['Country', 'Year'])['Demand'].sum().reset_index()
    electricity_demand_rail = electricity_demand_rail.pivot(index='Country', columns='Year', values='Demand').fillna(0)
    electricity_demand_rail = distribute_demand(electricity_demand_rail, mp.germany, mp.denmark, mp.sweden)

    electricity_demand_industry = df_all[(df_all['FuelGroup'] == 'Power') & (df_all['Country'] != 'EU27') & (~df_all['Sector'].isin(['Pass Road', 'Freight Road', 'Pass Rail', 'Freight Rail']))].groupby(['Country', 'Year'])['Demand'].sum().reset_index()
    electricity_demand_industry = electricity_demand_industry.pivot(index='Country', columns='Year', values='Demand').fillna(0)
    electricity_demand_industry = distribute_demand(electricity_demand_industry, mp.germany, mp.denmark, mp.sweden)

    light_duty_suffix =  ' . TRANS_EV     '
    heavy_duty_suffix =  ' . TRANS_BUS    '
    rail_suffix =        ' . TRANS_TRAINS '

    electricity_demand_light.index = electricity_demand_light.index + light_duty_suffix
    electricity_demand_heavy.index = electricity_demand_heavy.index + heavy_duty_suffix
    electricity_demand_rail.index = electricity_demand_rail.index + rail_suffix

    electricity_demand_transport = pd.concat([electricity_demand_light, electricity_demand_heavy, electricity_demand_rail], axis=0)

    initial_electricity_demand = initial_electricity_demand * 1e6 # Convert TWh to MWh
    initial_electricity_demand_residential = initial_electricity_demand['FC - RES'].copy()
    initial_electricity_demand_residential = pd.concat([initial_electricity_demand_residential]*len(model_years), axis=1)
    initial_electricity_demand_residential.columns = model_years
    initial_electricity_demand_commercial = initial_electricity_demand['FC - OTHER'].copy()
    initial_electricity_demand_commercial = pd.concat([initial_electricity_demand_commercial]*len(model_years), axis=1)
    initial_electricity_demand_commercial.columns = model_years
    initial_electricity_demand_industry = initial_electricity_demand['FC - IND'].copy()
    initial_electricity_demand_industry = pd.concat([initial_electricity_demand_industry]*len(model_years), axis=1)
    initial_electricity_demand_industry.columns = model_years

    residential_suffix = ' . RESE  '
    commercial_suffix =  ' . OTHER '
    industrial_suffix =  ' . PII   '

    initial_electricity_demand_residential.index = initial_electricity_demand_residential.index + residential_suffix
    initial_electricity_demand_commercial.index = initial_electricity_demand_commercial.index + commercial_suffix
    initial_electricity_demand_industry.index = initial_electricity_demand_industry.index + industrial_suffix
    electricity_demand_industry.index = electricity_demand_industry.index + industrial_suffix 

    electricity_demand_industry = electricity_demand_industry.reindex(initial_electricity_demand_industry.index, fill_value=0)
    electricity_demand_industry = electricity_demand_industry + initial_electricity_demand_industry

    electricity_demand = pd.concat([initial_electricity_demand_residential, initial_electricity_demand_commercial, electricity_demand_industry], axis=0) 
    
    hydrogen_demand = df_all[(df_all['FuelGroup'] == 'Hydrogen') & (df_all['Country'] != 'EU27')].groupby(['Country', 'Year'])['Demand'].sum().reset_index()
    hydrogen_demand = hydrogen_demand.pivot(index='Country', columns='Year', values='Demand').fillna(0)
    hydrogen_demand = distribute_demand(hydrogen_demand, mp.germany, mp.denmark, mp.sweden)

    industry_demand = df_all[(df_all['Sector'] == 'Non-metallic minerals') & (df_all['Country'] != 'EU27') & (df_all['FuelGroup'].isin(['Biogenic Gases', 'Biomass [Solid]']))].groupby(['Country', 'Year', 'FuelGroup'])['Demand'].sum().reset_index()
    industry_demand = industry_demand.pivot_table(index=['Country', 'Year'], columns='FuelGroup', values='Demand', fill_value=0).fillna(0)
    industry_demand = distribute_demand_industry(industry_demand, mp.germany, mp.denmark, mp.sweden)
    industry_demand_HT = industry_demand.copy()
    industry_demand_MT = industry_demand.copy()
    industry_demand_HT = industry_demand_HT * 0.7
    industry_demand_MT = industry_demand_MT * 0.3
    industry_demand_HT.reset_index(inplace=True)
    industry_demand_MT.reset_index(inplace=True)
    industry_demand_HT["Country"] = industry_demand_HT["Country"].replace(mp.region_to_industry_map_HT)  # Replace country codes with region names
    industry_demand_MT["Country"] = industry_demand_MT["Country"].replace(mp.region_to_industry_map_MT)  # Replace country codes with region names
    industry_demand_HT["Index"] = industry_demand_HT["Year"].astype(str) + " . " + industry_demand_HT["Country"]
    industry_demand_HT.set_index("Index", inplace=True)
    industry_demand_HT.drop(columns=["Country", "Year"], inplace=True)
    industry_demand_MT["Index"] = industry_demand_MT["Year"].astype(str) + " . " + industry_demand_MT["Country"]
    industry_demand_MT.set_index("Index", inplace=True)
    industry_demand_MT.drop(columns=["Country", "Year"], inplace=True)
    industry_demand_split = pd.concat([industry_demand_HT, industry_demand_MT], axis=0)
    industry_demand_split['Biogenic Gases'] = industry_demand_split['Biogenic Gases'] * 3.6 # MWh to GJ conversion factor
    industry_demand_split['Biomass [Solid]'] = industry_demand_split['Biomass [Solid]'] * 3.6 # MWh to GJ conversion factor
    
    fossil_kerosene = df_all[(df_all['FuelGroup'] == 'Fossil Liquids') & (df_all['Country'] != 'EU27') & (df_all['Sector'].isin(['Pass Aviation']))].groupby(['Country', 'Year'])['Demand'].sum().reset_index()
    fossil_kerosene = fossil_kerosene.pivot(index='Country', columns='Year', values='Demand').fillna(0)

    fossil_hfo = df_all[(df_all['FuelGroup'] == 'Fossil Liquids') & (df_all['Country'] != 'EU27') & (df_all['Sector'].isin(['Maritime']))].groupby(['Country', 'Year'])['Demand'].sum().reset_index()
    fossil_hfo = fossil_hfo.pivot(index='Country', columns='Year', values='Demand').fillna(0)

    fossil_diesel = df_all[(df_all['FuelGroup'] == 'Fossil Liquids') & (df_all['Country'] != 'EU27') & (df_all['Sector'].isin(['Pass Road','Pass Rail','Freight Road','Freight Rail']))].groupby(['Country', 'Year'])['Demand'].sum().reset_index()
    fossil_diesel = fossil_diesel.pivot(index='Country', columns='Year', values='Demand').fillna(0)

    ammonia_demand = df_all[(df_all['FuelGroup'] == 'Ammonia') & (df_all['Country'] != 'EU27')].groupby(['Country', 'Year'])['Demand'].sum().reset_index()
    ammonia_demand = ammonia_demand.pivot(index='Country', columns='Year', values='Demand').fillna(0)

    methanol_demand = df_all[(df_all['FuelGroup'] == 'Methanol') & (df_all['Country'] != 'EU27')].groupby(['Country', 'Year'])['Demand'].sum().reset_index()
    methanol_demand = methanol_demand.pivot(index='Country', columns='Year', values='Demand').fillna(0)

    renewable_aviation_demand = df_all[(df_all['FuelGroup'].isin(['Biogenic Liquids', 'Synthetic Liquids'])) & (df_all['Country'] != 'EU27') & (df_all['Sector'].isin(['Pass Aviation']))].groupby(['Country', 'Year'])['Demand'].sum().reset_index()
    renewable_aviation_demand = renewable_aviation_demand.pivot(index='Country', columns='Year', values='Demand').fillna(0)

    renewable_shipping_demand = df_all[(df_all['FuelGroup'].isin(['Biogenic Liquids', 'Synthetic Liquids'])) & (df_all['Country'] != 'EU27') & (df_all['Sector'].isin(['Maritime']))].groupby(['Country', 'Year'])['Demand'].sum().reset_index()
    renewable_shipping_demand = renewable_shipping_demand.pivot(index='Country', columns='Year', values='Demand').fillna(0)

    renewable_road_demand = df_all[(df_all['FuelGroup'].isin(['Biogenic Liquids', 'Synthetic Liquids'])) & (df_all['Country'] != 'EU27') & (df_all['Sector'].isin(['Pass Road','Pass Rail','Freight Road','Freight Rail']))].groupby(['Country', 'Year'])['Demand'].sum().reset_index()
    renewable_road_demand = renewable_road_demand.pivot(index='Country', columns='Year', values='Demand').fillna(0)

    if set_custom_aviation_RES > 0:
        total_aviation_demand = fossil_kerosene.add(renewable_aviation_demand, fill_value=0)
        renewable_aviation_demand = total_aviation_demand * set_custom_aviation_RES
        fossil_kerosene = total_aviation_demand * (1 - set_custom_aviation_RES)
    if set_custom_shipping_RES > 0:
        total_shipping_demand = fossil_hfo.add(renewable_shipping_demand, fill_value=0)
        renewable_shipping_demand = total_shipping_demand * set_custom_shipping_RES
        fossil_hfo = total_shipping_demand * (1 - set_custom_shipping_RES)
    
    bio_kerosene_demand = renewable_aviation_demand * bio_kerosene_share_aviation
    e_kerosene_demand = renewable_aviation_demand * e_kerosene_share_aviation

    maritime_ammonia_demand = renewable_shipping_demand * ammonia_share_shipping
    maritime_methanol_demand = renewable_shipping_demand * methanol_share_shipping

    ammonia_demand = ammonia_demand.add(maritime_ammonia_demand, fill_value=0)
    methanol_demand = methanol_demand.add(maritime_methanol_demand, fill_value=0)

    ammonia_demand = distribute_demand(ammonia_demand, mp.germany, mp.denmark, mp.sweden)
    ammonia_demand.rename(index=mp.region_to_area_map, inplace=True)
    methanol_demand = distribute_demand(methanol_demand, mp.germany, mp.denmark, mp.sweden)
    methanol_demand.rename(index=mp.region_to_area_map, inplace=True)
    bio_kerosene_demand = distribute_demand(bio_kerosene_demand, mp.germany, mp.denmark, mp.sweden)
    bio_kerosene_demand.rename(index=mp.region_to_area_map, inplace=True)
    e_kerosene_demand = distribute_demand(e_kerosene_demand, mp.germany, mp.denmark, mp.sweden)
    e_kerosene_demand.rename(index=mp.region_to_area_map, inplace=True)
    fossil_kerosene = distribute_demand(fossil_kerosene, mp.germany, mp.denmark, mp.sweden)
    fossil_kerosene.rename(index=mp.region_to_area_map, inplace=True)
    fossil_hfo = distribute_demand(fossil_hfo, mp.germany, mp.denmark, mp.sweden)
    fossil_hfo.rename(index=mp.region_to_area_map, inplace=True)
    fossil_diesel = distribute_demand(fossil_diesel, mp.germany, mp.denmark, mp.sweden)
    fossil_diesel.rename(index=mp.region_to_area_map, inplace=True)
    renewable_road_demand = distribute_demand(renewable_road_demand, mp.germany, mp.denmark, mp.sweden)
    renewable_road_demand.rename(index=mp.region_to_area_map, inplace=True)

    ammonia_suffix = " . AmmoniaBuffer       . AMMONIA_FLOW       . ILOUPFX_LO"
    methanol_suffix = " . EMethanolBuffer      . EMETHANOLFLOW       . ILOUPFX_LO"
    bio_kerosene_suffix = " . BioJetBuffer        . BIOJETFLOW         . ILOUPFX_LO"
    e_kerosene_suffix = " . E_FT_JetBuffer      . E_FT_JET_FLOW      . ILOUPFX_LO"
    fossil_kerosene_suffix = " . KeroseneBuffer      . KEROSENEFLOW       . ILOUPFX_LO"
    hfo_suffix = " . HFOBuffer           . HFOFLOW            . ILOUPFX_LO"
    fossil_diesel_suffix = " . DieselBuffer        . DIESELFLOW         . ILOUPFX_LO"
    bio_diesel_suffix = " . BioDieselBuffer        . BIODIESELFLOW         . ILOUPFX_LO"

    ammonia_demand.index = ammonia_demand.index + ammonia_suffix
    methanol_demand.index = methanol_demand.index + methanol_suffix
    bio_kerosene_demand.index = bio_kerosene_demand.index + bio_kerosene_suffix
    e_kerosene_demand.index = e_kerosene_demand.index + e_kerosene_suffix
    fossil_kerosene.index = fossil_kerosene.index + fossil_kerosene_suffix
    fossil_hfo.index = fossil_hfo.index + hfo_suffix
    fossil_diesel.index = fossil_diesel.index + fossil_diesel_suffix
    renewable_road_demand.index = renewable_road_demand.index + bio_diesel_suffix

    fuel_demand = pd.concat([ammonia_demand, methanol_demand, bio_kerosene_demand, e_kerosene_demand, fossil_kerosene, fossil_hfo, fossil_diesel, renewable_road_demand], axis=0)

    industry_demand_split.columns.name = None    
    industry_demand_split.index.name = None
    industry_demand_split.columns = ["BIOGAS", "WOODCHIPS"]
    electricity_demand_transport.columns.name = None
    electricity_demand_transport.index.name = None
    electricity_demand.columns.name = None
    electricity_demand.index.name = None
    hydrogen_demand.columns.name = None
    hydrogen_demand.index.name = None
    fuel_demand.columns.name = None
    fuel_demand.index.name = None

    dict_demands = {
        "electricity_demand_transport": electricity_demand_transport,
        "electricity_demand": electricity_demand,
        "hydrogen_demand": hydrogen_demand,
        "industry_demand": industry_demand_split,
        "fuel_demand": fuel_demand,
    }

    return dict_demands

def distribute_demand(demand=pd.DataFrame,
                        germany_map=mp.germany, 
                        denmark_map=mp.denmark, 
                        sweden_map=mp.sweden):
    """
    Creates a new electricity demand DataFrame by splitting the demand for Germany, Denmark, and Sweden into their respective regions.
    
    Parameters:
    electricity_demand (pd.DataFrame): The original electricity demand DataFrame.
    region_map (dict): A mapping of country codes to region names.
    germany_map (dict): A mapping of Germany's regions to their respective shares.
    denmark_map (dict): A mapping of Denmark's regions to their respective shares.
    sweden_map (dict): A mapping of Sweden's regions to their respective shares.
    
    Returns:
    pd.DataFrame: A new electricity demand DataFrame with split regions.
    """
    de_row = demand.loc['DE']
    split_rows = pd.DataFrame(
        {region: de_row * factor for region, factor in germany_map.items()}
    ).T
    demand = pd.concat([demand.drop(index='DE'), split_rows])

    dk_row = demand.loc['DK']
    split_rows = pd.DataFrame(
        {region: dk_row * factor for region, factor in denmark_map.items()}
    ).T
    demand = pd.concat([demand.drop(index='DK'), split_rows])

    se_row = demand.loc['SE']
    split_rows = pd.DataFrame(
        {region: se_row * factor for region, factor in sweden_map.items()}
    ).T
    demand = pd.concat([demand.drop(index='SE'), split_rows])

    return demand

def distribute_demand_industry(industry_demand=pd.DataFrame,
                        germany_map=mp.germany,
                        denmark_map=mp.denmark,
                        sweden_map=mp.sweden):
    """
    Creates a new industry demand DataFrame by splitting the demand for Germany, Denmark, and Sweden into their respective regions.
    
    Parameters:
    industry_demand (pd.DataFrame): The original industry demand DataFrame.
    region_map (dict): A mapping of country codes to region names.
    germany_map (dict): A mapping of Germany's regions to their respective shares.
    denmark_map (dict): A mapping of Denmark's regions to their respective shares.
    sweden_map (dict): A mapping of Sweden's regions to their respective shares.
    
    Returns:
    pd.DataFrame: A new industry demand DataFrame with split regions.
    """

    germany_demand = industry_demand.loc['DE']
    updated_germany_demand = pd.DataFrame()
    for region, factor in germany_map.items():
        industry_demand_temp = germany_demand * factor
        industry_demand_temp["Country"] = region
        updated_germany_demand = pd.concat([updated_germany_demand, industry_demand_temp])
    updated_germany_demand.reset_index(inplace=True)
    updated_germany_demand.set_index(["Country", "Year"], inplace=True)

    denmark_demand = industry_demand.loc['DK']
    updated_denmark_demand = pd.DataFrame()
    for region, factor in denmark_map.items():
        denmark_demand = industry_demand.loc['DK'] * factor
        denmark_demand["Country"] = region
        updated_denmark_demand = pd.concat([updated_denmark_demand, denmark_demand])
    updated_denmark_demand.reset_index(inplace=True)
    updated_denmark_demand.set_index(["Country", "Year"], inplace=True)

    sweden_demand = industry_demand.loc['SE']
    updated_sweden_demand = pd.DataFrame()
    for region, factor in sweden_map.items():
        sweden_demand = industry_demand.loc['SE'] * factor
        sweden_demand["Country"] = region
        updated_sweden_demand = pd.concat([updated_sweden_demand, sweden_demand])
    updated_sweden_demand.reset_index(inplace=True)
    updated_sweden_demand.set_index(["Country", "Year"], inplace=True)

    industry_demand = industry_demand.drop(index=['DE', 'DK', 'SE'])
    industry_demand = pd.concat([industry_demand, updated_germany_demand, updated_denmark_demand, updated_sweden_demand])

    return industry_demand

def write_incfile(filename, dataframe,prefix, suffix,path='incfiles'):
    """
    Writes an incfile.
    
    Parameters:
    filename (str): The name of the incfile to be created.
    dataframe (pd.DataFrame): The DataFrame to be written to the incfile.
    prefix (str): The prefix for the incfile.
    suffix (str): The suffix for the incfile.
    path (str): The path where the incfile will be saved.
    """
    incfile = IncFile(name=filename,
                        prefix=prefix,
                        suffix=suffix,
                        path=path)
    incfile.body = pd.DataFrame(index=dataframe.index, columns=dataframe.columns, data=dataframe.values)
    incfile.save()

    return None

if __name__ == "__main__":
    # Example usage of the functions
    input_path = os.path.join('Outputs')
    pd.options.display.float_format = '{:.2f}'.format
    df_all = read_country_files(input_path)
    initial_electricity_demand = pd.read_excel(os.path.join("data", 'demand_electricity.xlsx'), index_col=0)
    dict_data = extract_demands(df_all, model_years=[2030, 2040, 2050], initial_electricity_demand=initial_electricity_demand,
                                set_custom_aviation_RES=0.7, set_custom_shipping_RES=0,)

    aviation = df_all[(df_all["Sector"] == "Pass Aviation") & (df_all["Year"] == 2050) & (df_all["Country"] == "EU27") & (df_all["Demand"] > 0) & (df_all["FuelGroup"] != "Overall Demand")].copy()
    aviation["Share"] = aviation["Demand"] / aviation["Demand"].sum()

    maritime = df_all[(df_all["Sector"] == "Maritime") & (df_all["Year"] == 2050) & (df_all["Country"] == "EU27") & (df_all["Demand"] > 0) & (df_all["FuelGroup"] != "Overall Demand")].copy()
    maritime["Share"] = maritime["Demand"] / maritime["Demand"].sum()

    print("\nAviation demand shares for EU27 in 2050:")
    print(aviation)
    print("\nMaritime demand shares for EU27 in 2050:")
    print(maritime)
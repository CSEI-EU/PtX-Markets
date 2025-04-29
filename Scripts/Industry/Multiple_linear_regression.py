# Multiple linear Regression
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression
import os
from osgeo import ogr


# Based on Neuwirth et al (2024) 
sector_feedstock = ['Physical output (kt steel)', 'Integrated steelworks (kt steel)',
                    'Electric arc (kt steel)','Basic chemicals (kt ethylene eq.)']

# Based on TRL of UBA
sector_ind_heat = ['Iron and Steel ','Cement', 'Ceramics & other non metallic minerals', 'Glass production']


demand = pd.read_excel("Scripts\Overview_JRC-IDEES_EU27.xlsx", sheet_name = 'Input')

region = 'European Union - 27 countries (from 2020)'
#['European Union - 27 countries (from 2020)', 'Albania', 'Austria','Belgium', 'Bulgaria', 'Switzerland', 
# 'Cyprus', 'Czechia','Germany', 'Denmark', 'Spain', 'Estonia', 'Finland', 'France','Greece', 'Croatia', 
# 'Hungary', 'Ireland', 'Italy', 'Lithuania','Luxembourg', 'Latvia', 'North Macedonia', 'Malta', 'Montenegro',
# 'Netherlands', 'Norway', 'Poland', 'Portugal', 'Romania', 'Serbia','Slovakia', 'Slovenia', 'Sweden', 'Turkey']

demand = demand.T
demand.columns = demand.iloc[0]
demand.drop(['Subsector','Unit'], axis=0, inplace = True)
demand.index.name = 'Year'
demand.index= pd.to_datetime(demand.index, format='%Y')


ind_demand = demand[['Iron and Steel ', 'Alumina production', 'Aluminium production',
                    'Other non-ferrous metals', 'Basic chemicals', 'Other chemicals',
                    'Pharmaceutical products', 'Cement',
                    'Ceramics & other non metallic minerals', 'Glass production', 'Pulp',
                    'Paper', 'Printing', 'Food, beverages and tobacco', 'Transport ',
                    'Machinery', 'Textiles and leather', 'Wood and wood products',
                    'Other industrial sectors']]

ind_demand_kt = demand[['Physical output (kt steel)', 'Integrated steelworks (kt steel)',
                        'Electric arc (kt steel)', 'Alumina production (kt alumina)',
                        'Aluminium production (kt aluminium)',
                        'Aluminium - primary production (kt aluminium)',
                        'Aluminium - secondary production (kt aluminium)',
                        'Other non-ferrous metals (kt lead eq.)',
                        'Basic chemicals (kt ethylene eq.)',
                        'Pharmaceutical products etc. (kt ethylene eq.)', 'Cement (kt Cement)',
                        'Ceramics & other NMM (kt bricks eq.)', 'Glass production  (kt glass)',
                        'Pulp production (kt pulp)', 'Paper production  (kt paper)',
                        'Printing and media reproduction (kt paper eq.)']]
#ind_demand = ind_demand.reset_index()
#ind_demand_long = ind_demand.melt(id_vars='Year', var_name='Subsector', value_name='energy_demand')

pass_transport_demand = demand[['Powered two-wheelers', 'Passenger cars',
                                'Motor coaches, buses and trolley buses',
                                'Metro and tram, urban light rail', 'Conventional passenger trains',
                                'High speed passenger trains', 'Aviation-Domestic-pass',
                                'Aviation -International - Intra-EEAwUK - pass',
                                'Aviation-International - Extra-EEAwUK - pass']] 
#pass_transport_demand = pass_transport_demand.reset_index()
#pass_transport_demand_long = pass_transport_demand.melt(id_vars='Year', var_name='Subsector', value_name='energy_demand')

goods_transport_demand = demand[['Light commercial vehicles', 'Heavy goods vehicles', 'Rail transport',
                                'Aviation-Domestic-goods',
                                'Aviation-International - Intra-EEAwUK - goods',
                                'Aviation-International - Extra-EEAwUK - goods',
                                'Shipping-Domestic coastal shipping', 'Inland waterways',
                                'Maritime - Intra -EEA', 'Maritime - Extra -EEA']]
#goods_transport_demand = goods_transport_demand.reset_index()
#goods_transport_demand_long = goods_transport_demand.melt(id_vars='Year', var_name='Subsector', value_name='energy_demand')


gdp = pd.read_excel("..\Scripts\Projected_GDP.xlsx", index_col="Year")
gdp.index= pd.to_datetime(gdp.index, format='%Y')
gdp = gdp[[region]]
historic_gdp = gdp[gdp.index < '2022-01-01']
projected_gdp = gdp[gdp.index > '2021-01-01']



def linear_regression_visualisation(demand_sector_df, sectors="ind", plot=False, save=False):
    """
    Perform a linear regression on historical demand data and visualize the results.
    Save all sector results in a single Excel file with separate sheets.
    """

    results_dict = {}  # Store all results before saving

    for sector in demand_sector_df.columns:
        historical_data = demand_sector_df[[sector]].join(historic_gdp)

        # Standardize GDP for PCA
        scaler = StandardScaler()
        data_scaled = scaler.fit_transform(historic_gdp)

        # Apply PCA
        pca = PCA(n_components=1)
        principal_components = pca.fit_transform(data_scaled)

        # Add PCA component
        historical_data['PC1'] = principal_components

        # Define independent and dependent variables
        y = historical_data[sector]  # Energy demand
        X = historical_data[['PC1']]

        # Train Linear Regression
        model = LinearRegression()
        model.fit(X, y)

        # Predict future data
        future_data_scaled = scaler.transform(projected_gdp)
        future_pc1 = pca.transform(future_data_scaled)
        y_future = model.predict(future_pc1)
        y_future = np.maximum(y_future, 0)  # Set negative predictions to zero

        # Create results DataFrame
        results = pd.DataFrame({'Predicted Demand': y_future}, index=projected_gdp.index)

        # Store in dictionary for later saving
        results_dict[sector] = results

        if plot:
            # Assign units
            unit_mapping = {"ind": "ktoe", "pass": "pkm", "ind_kt": "kt"}
            unit = unit_mapping.get(sectors, "tkm")

            # Plot Results
            fig, ax1 = plt.subplots(figsize=(12, 6))
            million_gdp = gdp / 1_000_000
            million_projected_gdp = projected_gdp / 1_000_000

            ax1.plot(demand_sector_df.index, y, label='Historical Demand', color='darkblue')
            ax1.plot(results.index, results['Predicted Demand'], label='Projected Demand (2022-2050)', linestyle='--', color='blue')
            ax1.set_xlabel('Year')
            ax1.set_ylabel(f'Demand in {unit}')
            ax1.legend(loc='upper left')

            ax2 = ax1.twinx()
            ax2.plot(million_gdp.index, million_gdp[region], label='GDP', color='green')
            ax2.plot(million_projected_gdp.index, million_projected_gdp[region], label='Projected GDP (2022-2050)', linestyle='--', color='lightgreen')
            ax2.set_ylabel('GDP in MEUR')
            ax2.legend(loc='upper right')
            plt.axvline(x=demand_sector_df.index[-1], linestyle='--', color='grey', label='Forecast Start')
            plt.title(f'Demand Projection for {sector} with GDP (in Millions)')
            plt.grid(True)
            plt.xticks(rotation=45)
            plt.show()

    # Save all results in **one** Excel file with **different sheets**
    if save:
        file_path = f"..\Scripts\Results\{datetime.datetime.today().strftime('%Y_%m_%d_')}{sectors}_{region}.xlsx"
        with pd.ExcelWriter(file_path) as writer:
            for sector, result_df in results_dict.items():
                safe_sector = sector.replace(" ", "_").replace("/", "-")[:31]  # Ensure valid sheet names
                result_df.to_excel(writer, sheet_name=safe_sector)




linear_regression_visualisation(ind_demand, sectors = "ind", plot = False, save = False)
linear_regression_visualisation(ind_demand_kt, sectors = "ind_kt", plot = True, save = False)
linear_regression_visualisation(pass_transport_demand, sectors = "pass", plot = False, save = False)
linear_regression_visualisation(goods_transport_demand, sectors = "goods", plot = False,  save = False)
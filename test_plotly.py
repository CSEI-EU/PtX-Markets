import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# Random data to practice streamlit dashboard
np.random.seed(0)
years = [2025, 2030, 2035, 2040, 2045, 2050]
regions = ['Denmark', 'Sweden', 'Norway', 'Germany']
sectors = ['Industry', 'Transport', 'Heating', 'Power']
subsectors = ['Road', 'Rail', 'Aviation', 'Maritime']
scenarios = ['Hydrogen', 'Electrification', 'Ammonia', 'Methanol']

# Create the corresponding data frame
data_list = []
for scenario in scenarios:
    for region in regions:
        for sector in sectors:
            if sector == 'Transport': # only to be consistent with transport = sum of subsectors
                for subsector in subsectors:
                    for year in years:
                        value = np.random.randint(100, 500)
                        data_list.append({'Year': year, 'Region': region, 'Sector': sector, 'Subsector': subsector, 'Scenario': scenario, 'Value': value})
            else:
                for year in years:
                    value = np.random.randint(100, 500)
                    data_list.append({'Year': year, 'Region': region, 'Sector': sector, 'Subsector': None, 'Scenario': scenario, 'Value': value})
df = pd.DataFrame(data_list)


# Technology efficiency trends : introduce information on technology
efficiency_data = {
    'Year': years,
    'Hydrogen Energy Demand (%)': np.linspace(50, 75, len(years)),
    'Battery Energy Density (Wh/kg)': np.linspace(100, 300, len(years)),
    'Ammonia Production Efficiency (%)': np.linspace(40, 55, len(years)),
    'Methanol Production Efficiency (%)': np.linspace(35, 50, len(years))
}
efficiency_df = pd.DataFrame(efficiency_data)



# -------- Initiate the dashboard with title and graphs --------
st.set_page_config(layout='wide')
title_alignment = """
<style>
.centered-title {
text-align: center;
}
</style>
<h1 class="centered-title">Energy Demand Dashboard</h1>
"""
st.markdown(title_alignment, unsafe_allow_html=True)



# -------- First row : Global energy demand and key numbers --------

st.subheader("Global Energy Demand by Scenario")
graph_global, key_num = st.columns((6, 4))

global_demand = df.groupby(['Year', 'Scenario'])['Value'].sum().reset_index()

# First column : Line graph using Plotly
fig = px.line(global_demand, x='Year', y='Value', color='Scenario',
              labels={'Value': 'Total Energy Demand'})

with graph_global:
    st.plotly_chart(fig)


# Filter data for the year 2050 and 2025
demand_2050 = df[df['Year'] == 2050]
demand_2025 = df[df['Year'] == 2025]

# Find scenario with the highest prediction (hypotheticlly)
highest_scenario = global_demand.groupby("Scenario")["Value"].max().idxmax()
highest_value = global_demand.groupby("Scenario")["Value"].max().max()
highest_year = global_demand[global_demand["Value"] == highest_value]["Year"].values[0]  # Extract the year

avg_demand_2050 = demand_2050["Value"].mean()
avg_demand_2025 = demand_2025["Value"].mean()
percent_increase = ((avg_demand_2050 - avg_demand_2025) / avg_demand_2025) * 100

# Find the sector with the highest demand in 2050
sector_demand_2050 = demand_2050.groupby('Sector')['Value'].sum()
highest_sector_2050 = sector_demand_2050.idxmax()
highest_value_2050 = sector_demand_2050.max()

# Find the demand for the same sector in 2025
sector_value_2025 = demand_2025[demand_2025['Sector'] == highest_sector_2050]['Value'].sum()
percent_increase_sector = ((highest_value_2050 - sector_value_2025) / sector_value_2025) * 100


# Second column : Key numbers and info box
with key_num:
    st.metric(label="Predicted Energy Demand for 2050", value=f"{avg_demand_2050:.0f} GWh", delta=f"{percent_increase:.1f} %")
    st.info(f"**{highest_scenario}** scenario is predicted to have the highest energy pic demand of **{highest_value} GWh** in **{highest_year}**.")
    st.info(f"The **{highest_sector_2050}** sector is predicted to have the highest energy demand of **{highest_value_2050} GWh** in 2050, compared to **{sector_value_2025} GWh** in 2025, a **{percent_increase_sector:.1f}%** increase.")

st.markdown('''---''')



# -------- Second row : Bar chart for each scenario to show different sectors --------
st.subheader("Energy Demand by Sector")

tabs = st.tabs(scenarios)
custom_blues = ['#08306b', '#2171b5', '#6baed6', '#c6dbef', '#deebf7']
color_palette = custom_blues[:len(sectors)]  # Blue color palette

for tab, scenario in zip(tabs, scenarios):
    with tab:
        scenario_data = df[df['Scenario'] == scenario]
        pivot_data = scenario_data.pivot_table(index='Year', columns='Sector', values='Value', aggfunc='sum')

        fig = px.bar(
            pivot_data,
            x=pivot_data.index,
            y=pivot_data.columns,
            labels={'value': 'Energy Demand', 'Year': 'Year'},
            title=f"Evolution of sector proportion for {scenario} Scenario",
            color_discrete_sequence=color_palette,
        )
        fig.update_layout(yaxis=dict(range=[0, 11000]))
        st.plotly_chart(fig)


        # Pie chart for subsector distribution in Transport for 2025 and 2050
        transport_data_2025 = scenario_data[(scenario_data['Sector'] == 'Transport') & (scenario_data['Year'] == 2025)]
        transport_data_2050 = scenario_data[(scenario_data['Sector'] == 'Transport') & (scenario_data['Year'] == 2050)]

        transport_pivot_2025 = transport_data_2025.pivot_table(index='Year', columns='Subsector', values='Value', aggfunc='sum').fillna(0)
        transport_pivot_2050 = transport_data_2050.pivot_table(index='Year', columns='Subsector', values='Value', aggfunc='sum').fillna(0)

        pie_chart_2025 = px.pie(values=transport_pivot_2025.values[0], names=transport_pivot_2025.columns,
                                    title='Subsector Distribution in Transport for 2025')
        pie_chart_2050 = px.pie(values=transport_pivot_2050.values[0], names=transport_pivot_2050.columns,
                                    title='Subsector Distribution in Transport for 2050')

        # Display pie charts side by side
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(pie_chart_2025)
        with col2:
            st.plotly_chart(pie_chart_2050)
 
        if scenario == "Hydrogen":
            technology_options = ['SOEC', 'PEMEC', 'AEC']
            selected_technology = st.selectbox("Select Electrolysis Technology", technology_options)
            efficiency_mapping = {
                    'AEC': 57.7,
                    'PEMEC': 52.6,
                    'SOEC':61.5
                }       
            selected_efficiency = efficiency_mapping[selected_technology]
            st.info(f"Selected Technology: **{selected_technology}** with Efficiency: **{selected_efficiency}%**")
            fig_eff = px.line(efficiency_df, x='Year', y='Hydrogen Energy Demand (%)', markers=True)


        # Additional graph for technology efficiency trends
        fig_eff.update_layout(template='plotly_white', title=f"Efficiency Improvements for {scenario}")
        st.plotly_chart(fig_eff, use_container_width=True)

st.markdown('''---''')


# ---- Third row : map of the region with demand by country ----

regions_data = pd.DataFrame({
    'Region': ['Denmark', 'Sweden', 'Norway', 'Germany'],
    'lat': [56.2639, 59.0, 60.4720, 51.1657],
    'lon': [9.5018, 15.0, 8.4689, 10.4515],
    'Energy Demand (GWh)': [300, 400, 350, 500]  # Example to change afterwards
})

st.subheader("Energy Demand by Country in 2025")

# Select box for year selection
selected_year = st.selectbox("Select Year", years)

global_demand_2025 = df[df['Year'] == selected_year].groupby('Region')['Value'].sum().reset_index()
regions_data = regions_data.merge(global_demand_2025, on='Region')

# Create a plotly map
fig = px.scatter_geo(
    regions_data,
    lat='lat',
    lon='lon',
    size='Value',  # Adjust marker size to be visible on map
    size_max=20,
    color='Value',  # Color markers based on energy demand
    color_continuous_scale=px.colors.sequential.Reds,
    hover_name='Region',
    projection="natural earth",
)

# Update layout for better map visibility
fig.update_traces(
    marker=dict(line=dict(width=1, color='DarkSlateGrey')),
    textposition="top center",  # Position text above markers
    textfont=dict(size=10, color='black')
)

fig.update_layout(
    geo=dict(
        showland=True,
        landcolor="white",
        showocean=True,
        oceancolor="lightgrey",
        lakecolor="lightblue",
        lataxis_range=[50, 70],
        lonaxis_range=[5, 30],
        bgcolor='white'
    ),
    margin=dict(l=0, r=0, t=50, b=0)  # Margins for a better layout
)

st.plotly_chart(fig)

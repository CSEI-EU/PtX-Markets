import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns

# Random data to practice streamlit dashboard
np.random.seed(0)
years = [2025, 2030, 2035, 2040, 2045, 2050]
regions = ['Denmark', 'Sweden', 'Norway', 'Germany']
sectors = ['Transport', 'Industry', 'Agriculture', 'Power']
scenarios = ['Hydrogen', 'Electrification', 'Ammonia', 'Methanol']

# Create the data frame
data_list = []

for scenario in scenarios:
    for region in regions:
        for sector in sectors:
            for year in years:
                value = np.random.randint(100, 500)
                data_list.append({'Year': year, 'Region': region, 'Sector': sector, 'Scenario': scenario, 'Value': value})

df = pd.DataFrame(data_list)


# Initiate the dashboard with title and graphs 
st.title("Energy demand dashboard")


# Part 1 : Global Energy Demand Graph for all scenarios
st.subheader("Global Energy Demand for all scenarios")

global_demand = df.groupby(['Year', 'Scenario'])['Value'].sum().reset_index()

# Create a line plot using Plotly
fig = px.line(global_demand, x='Year', y='Value', color='Scenario', title="Global Energy Demand Over the Years",
              labels={'Year': 'Year', 'Value': 'Total Energy Demand'})
st.plotly_chart(fig)




# Part 2: Panel with 4 Bar charts for each scenario (1 bar per year, stacked by sector)
st.subheader("Energy Demand by Sector for Each Scenario")

# Define distinct colors for each sector
sector_colors = sns.color_palette("Blues", len(sectors))

for scenario in scenarios:
    scenario_data = df[df['Scenario'] == scenario]
    # Pivot the data to have years as index and sectors as columns
    pivot_data = scenario_data.pivot_table(index='Year', columns='Sector', values='Value', aggfunc='sum')
    
    # Stacked bar with plotly
    fig = go.Figure()

    for i, sector in enumerate(sectors):
        fig.add_trace(go.Bar(x=pivot_data.index, y=pivot_data[sector], name=sector,
                             marker_color=sector_colors[i]))

    fig.update_layout(
        barmode='stack',
        title=f"Energy Demand by Sector - {scenario}",
        xaxis_title="Year",
        yaxis_title="Energy Demand",
        legend_title="Sector"
    )
    
    st.plotly_chart(fig)

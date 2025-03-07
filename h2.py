# -*- coding: utf-8 -*-
"""
Created on Fri Mar  7 15:37:01 2025

@author: mar.eco
"""

import streamlit as st
import matplotlib.pyplot as plt

def show(df):
    st.title("Hydrogen Scenario")

    # Filter the data for the Hydrogen scenario
    hydrogen_data = df[df['Scenario'] == 'Hydrogen']

    # Evolution over the years
    st.subheader("Energy Demand Evolution")
    evolution_data = hydrogen_data.groupby('Year')['Value'].sum().reset_index()
    fig, ax = plt.subplots()
    ax.plot(evolution_data['Year'], evolution_data['Value'], marker='o')
    ax.set_ylabel("Total Energy Demand")
    ax.set_title("Energy Demand Over the Years")
    st.pyplot(fig)

    # Key numbers
    st.subheader("Key Numbers")
    demand_2050 = hydrogen_data[hydrogen_data['Year'] == 2050]['Value'].sum()
    demand_2025 = hydrogen_data[hydrogen_data['Year'] == 2025]['Value'].sum()
    increase = ((demand_2050 - demand_2025) / demand_2025) * 100
    st.metric(label="Energy Demand in 2050", value=f"{demand_2050:.0f} GWh", delta=f"{increase:.1f} %")

    # Pie charts by sector
    st.subheader("Energy Demand by Sector in 2050")
    sector_data_2050 = hydrogen_data[hydrogen_data['Year'] == 2050].groupby('Sector')['Value'].sum()
    fig, ax = plt.subplots()
    ax.pie(sector_data_2050, labels=sector_data_2050.index, autopct='%1.1f%%', startangle=90)
    ax.set_title("Sector Distribution in 2050")
    st.pyplot(fig)

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 16:01:17 2025

@author: mar.eco
"""

import streamlit as st 
import numpy as np
import pandas as pd

df = pd.DataFrame({'first column': [1,2,3,4], 'second column': [10,20,30,40]})


st.write("Here's our first attempt at using data to create a table:")
st.write(df)


data = {
    "Sector": ["Residential", "Industry", "Transport", "Agriculture", "Commercial & Services", "Other (Public sector, etc.)"],
    "Energy Demand (GWh)": [35000, 40000, 30000, 10000, 20000, 5000],
    "Share (%)": [25, 28, 21, 7, 14, 5]
}

df_energy = pd.DataFrame(data)

st.line_chart(df_energy)


map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

st.map(map_data)
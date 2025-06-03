import streamlit as st
import pandas as pd

from mappings import *
from process import *
from global_plots import * 
from transport_plots import *
from industry_plots import *


# Call important files
transport_file = r"C:\Users\mar.eco\OneDrive - CBS - Copenhagen Business School\Desktop\PtX-Markets\REMIND\Results_REMIND_JRC.csv"
industry_path = r"C:\Users\mar.eco\OneDrive - CBS - Copenhagen Business School\Desktop\PtX-Markets\Scripts\Industry\Results_per_Country"

transport_data = load_transport_data(transport_file)
industry_df = load_industry_data(industry_path)

fuel_transport = transport_data[transport_data['Category'].isin(transport_fuel_paths)].copy()
fuel_transport[["MainCategory", "Fuel"]] = fuel_transport["Category"].apply(
    lambda x: pd.Series(extract_main_and_fuel(x, categories))
)

transport_data['Country_full'] = transport_data['Country'].map(iso_to_country)
transport_data = transport_data[transport_data["Category"].isin(categories)]
transport_data["MainCategory"] = transport_data["Category"]


industry_df['Country_full'] = industry_df['Country'].map(iso_to_country)
transport_name = 'Transport'
industry_name = 'Industry'

# -------- Initiate the dashboard with title and graphs --------
st.set_page_config(layout='wide')
title_alignment = """
<style>
.centered-title {
text-align: center;
}
</style>
<h1 class="centered-title">Energy demand results</h1>
"""
st.markdown(title_alignment, unsafe_allow_html=True)


# Make a choice for country 
all_countries = sorted(transport_data['Country'].unique())
selected_country = st.selectbox("Select a country:", all_countries)

# -------- EU27 Global energy demand and key numbers --------
st.subheader(f"{selected_country} Global energy demand")

# Get EU27 data
country_transport, country_transport_demand = get_eu27_demand(transport_data, selected_country, transport_name)
country_industry, country_industry_demand = get_eu27_demand(industry_df, selected_country,industry_name)
combined_demand = pd.concat([country_transport_demand, country_industry_demand], ignore_index=True)

# Plot of both sectors
fig_combined = create_eu27_combined_plot(country_transport_demand, transport_name, country_industry_demand, industry_name)

# Key metrics
t_2025 = country_transport_demand[country_transport_demand['Year'] == 2025]['Value'].values[0]
t_2050 = country_transport_demand[country_transport_demand['Year'] == 2050]['Value'].values[0]
t_change, t_growth = calculate_growth(t_2025, 2025, t_2050, 2050)

i_2030 = country_industry_demand[country_industry_demand['Year'] == 2030]['Value'].values[0]
i_2050 = country_industry_demand[country_industry_demand['Year'] == 2050]['Value'].values[0]
i_change, i_growth = calculate_growth(i_2030, 2030, i_2050, 2050)

# Most demanding categories 
top_transport_2025 = highest_category_info(country_transport, 2025)[1]
top_transport_2050 = highest_category_info(country_transport, 2050)[1]
top_industry_2030 = highest_category_info(country_industry, 2030)[1]
top_industry_2050 = highest_category_info(country_industry, 2050)[1]

graph_eu27, key_num = st.columns((6, 4))
with graph_eu27:
    st.plotly_chart(fig_combined, use_container_width=True)

# Second column: Key numbers for global demand
with key_num:
    st.subheader(transport_name)
    st.metric("2050 demand", f"{t_2050:.2f} EJ", delta=f"{t_change:.1f} % vs 2025")
    st.info(f"""
            Average annual growth rate: {t_growth:.1f} % \\
            Top category in 2025: **{top_transport_2025}** \\
            Top category in 2050: **{top_transport_2050}**
            """)
    st.markdown('---')

    st.subheader(industry_name)
    st.metric("2050 demand", f"{i_2050:.4f} EJ", delta=f"{i_change:.1f} % vs 2030")
    st.info(f"""
            Average annual growth rate: {i_growth:.1f} % \\
            Top category in 2030: **{top_industry_2030}** \\
            Top category in 2050: **{top_industry_2050}**
            """) 
st.markdown('---')



# -------- Heatmaps of 2030 demand: Transport vs Industry --------
st.subheader("Country-level energy demand by year")

selected_year = st.selectbox("Select a year", [2030, 2040, 2050], index=0)
fig_maps = create_demand_heatmaps(transport_data, industry_df, selected_year)
st.plotly_chart(fig_maps)


# -------- Energy demand by most consuming countries --------
st.subheader("Most energy-demanding countries over time")

fig_transport, fig_industry = create_top_demanding_countries_figures(transport_data, industry_df)

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_transport)
with col2:
    st.plotly_chart(fig_industry)


# Color sclaes for pie charts
custom_blues = ['#08306b', '#2171b5', '#6baed6', '#c6dbef', '#deebf7', '#b3cde3', '#a6bddb', '#9ebcda', '#8c96c6']
custom_reds = ['#67000d', '#cb181d', "#f55c2d"]


# ---- Organize dashboard using TABS ----
tab1, tab2 = st.tabs(["Transport", "Industry"])

with tab1:
    st.subheader("Evolution of categories - Transport")

    # ----- Bar plot for main categories -----
    fig_main_transport = plot_main_transport_stack(country_transport, custom_blues)
    st.plotly_chart(fig_main_transport)

    # ----- Pie chars for categories -----
    plot_transport_pie_charts(country_transport, 2025)
    plot_transport_pie_charts(country_transport, 2050)

    available_cats = sorted(fuel_transport["MainCategory"].unique())
    selected_cat = st.selectbox("Select transport category:", available_cats)
    filtered_df = fuel_transport[fuel_transport["MainCategory"] == selected_cat]
    st.dataframe(filtered_df)

    years = sorted(fuel_transport['Year'].unique())
    selected_year = st.selectbox("Select year:", years)
    plot_transport_fuel_pie_charts(fuel_transport, selected_cat, selected_year)

    # ------ Heat maps for most consuming category --------
    target_category = highest_category_info(country_transport, 2050)[0]
    fig_cat_transport = plot_transport_heatmap(transport_data, target_category)
    st.plotly_chart(fig_cat_transport)


with tab2:
    st.subheader("Evolution of categories - Industry")

    # ----- Bar plot for main categories -----
    fig_main_industry = plot_main_industry_bar(country_industry, custom_reds)
    st.plotly_chart(fig_main_industry)

    # ----- Pie chars for categories -----
    plot_industry_pie(industry_df, 2030)
    plot_industry_pie(industry_df, 2050)

    # ------ Heat maps for most consuming category --------
    target_industry_category = top_industry_2050
    fig_cat_industry = plot_industry_choropleth(industry_df, target_industry_category)
    st.plotly_chart(fig_cat_industry)
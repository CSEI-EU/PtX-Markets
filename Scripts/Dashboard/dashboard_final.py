import streamlit as st
import pandas as pd
import os

# -------- Initiate the dashboard with title and graphs --------
st.set_page_config(layout='wide')

title_alignment = """
<style>
.centered-title {
text-align: center;
}
</style>
<h1 class="centered-title">Green Fuels and Energy demand Outlook</h1>
"""
st.markdown(title_alignment, unsafe_allow_html=True)

from mappings import *
from process import *
from global_plots import * 
from transport_plots import *
from industry_plots import *

# Call important files
transport_file = os.path.join('..', '..', 'REMIND', 'Results_REMIND_JRC.csv')
industry_path = os.path.join('..', 'Industry', 'Results_per_Country')
final_output_path = os.path.join('..', '..', 'Outputs')

transport_data = load_transport_data(transport_file)
industry_df = load_industry_data(industry_path)
final_df = load_combined_outputs(final_output_path)

fuel_transport = transport_data[transport_data['Category'].isin(transport_fuel_paths)].copy()
fuel_transport[["MainCategory", "Fuel"]] = fuel_transport["Category"].apply(lambda x: pd.Series(extract_main_and_fuel(x, categories)))

transport_data['Country_full'] = transport_data['Country'].map(iso_to_country)
transport_data = transport_data[transport_data["Category"].isin(categories)]
transport_data["MainCategory"] = transport_data["Category"]

industry_df['Country_full'] = industry_df['Country'].map(iso_to_country)
transport_name = 'Transport'
industry_name = 'Industry'

# -------- Side bar with relevant choices for the dashboard user --------
with st.sidebar:
    st.title("Filters")
    all_countries = sorted(transport_data['Country'].unique())

    # Set the default country to be EU27
    default_index = 0
    if 'EU27' in all_countries:
        default_index = all_countries.index('EU27')
    selected_country = st.selectbox("Select a country:", all_countries, index=default_index)

    selected_year = st.selectbox("Select a year", [2030, 2040, 2050], index=3)

    focus = st.radio("What is the focus of the analysis?",
    ["All energy carriers",
    "Green fuels only",
    # "Hydrogen only",
    "Hydrogen vs other Green fuels",
    "Green fuels vs Fossil fuels"],
    index=0)

st.markdown("""
This dashboard explores how final energy demand evolves across Europe and how 
electricity-based fuels (Power-to-X) progressively replace fossil energy in transport and industry.
It first provides a strategic overview of Power-to-X integration and total energy demand, and then dives into sector-specific insights for Transport and Industry.
""")

c1, c2, c3 = st.columns(3)
country_data = final_df[final_df['Country'] == selected_country]

# Calculate metrics for the chose year 
total = country_data[country_data['Year'] == selected_year]['Value'].sum()
ptx = country_data[(country_data['Year'] == selected_year) & (country_data['FuelGroup'].isin(ptx_carriers))]['Value'].sum()
penetration = (ptx / total * 100) if total > 0 else 0

if focus == "Hydrogen only":
    h2 = country_data[(country_data['Year'] == selected_year) & 
                      (country_data['FuelGroup'] == "Hydrogen")]['Value'].sum()
    h2_share = h2 / total * 100 if total > 0 else 0

    c1.metric(f"Total Demand ({selected_year})", f"{total:.2f} EJ")
    c2.metric(f"Hydrogen demand ({selected_year})", f"{h2:.3f} EJ")
    c3.metric("Hydrogen share of total", f"{h2_share:.1f}%")

elif focus == "Hydrogen vs other PtX":
    h2 = country_data[(country_data['Year'] == selected_year) & 
                      (country_data['FuelGroup'] == "Hydrogen")]['Value'].sum()
    other_ptx = country_data[(country_data['Year'] == selected_year) & 
                             (country_data['FuelGroup'].isin([x for x in ptx_carriers if x != "Hydrogen"]))]['Value'].sum()
    h2_share_ptx = h2 / (h2 + other_ptx) * 100 if (h2 + other_ptx) > 0 else 0

    c1.metric(f"Total Demand ({selected_year})", f"{total:.2f} EJ")
    c2.metric(f"Hydrogen in PtX ({selected_year})", f"{h2:.3f} EJ")
    c3.metric("Hydrogen share of PtX", f"{h2_share_ptx:.1f}%")

else:
    # Default PtX KPIs
    c1.metric(f"Total Demand ({selected_year})", f"{total:.2f} EJ")
    c2.metric(f"PtX Market size ({selected_year})", f"{ptx:.3f} EJ")
    c3.metric(f"PtX integration", f"{penetration:.1f}%")


# Charts for PtX integration 
st.subheader(f"Energy demand and fuel per sector in {selected_country}")
filtered_master = apply_focus_filter(
    final_df[final_df['Country'] == selected_country],
    focus
)

# st.write(sorted(filtered_master["FuelGroup"].unique()))
st.plotly_chart(plot_ptx_transition_wedge(filtered_master, selected_country),use_container_width=True)
st.plotly_chart(plot_sector_ptx_intensity(filtered_master, selected_country, selected_year))

# European aggregate 
eu_avg = final_df.groupby(["Year","FuelGroup"])["Value"].sum().reset_index()
eu_avg["Country"] = "EU27"

# -------- EU27 Global energy demand and key numbers --------
st.subheader(f"{selected_country} Global energy demand")

# Get EU27 data
country_transport, country_transport_demand = get_country_demand(transport_data, selected_country, transport_name)
country_industry, country_industry_demand = get_country_demand(industry_df, selected_country,industry_name)
combined_demand = pd.concat([country_transport_demand, country_industry_demand], ignore_index=True)

# Plot of both sectors
fig_combined = create_country_combined_plot(country_transport_demand, transport_name, country_industry_demand, industry_name)

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
fig_maps = create_demand_heatmaps(transport_data, industry_df, selected_year)
st.plotly_chart(fig_maps, use_container_width=True,config= {"scrollZoom": False,"displayModeBar": False})


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

    # ------ Heat maps for most consuming category --------
    target_category = highest_category_info(country_transport, 2050)[0]
    fig_cat_transport = plot_transport_heatmap(transport_data, target_category)
    st.plotly_chart(fig_cat_transport, use_container_width = True, config= {"scrollZoom": False,"displayModeBar": False})

    st.write("TEST TO SEE")
    st.write(final_df[final_df["Country"] == selected_country][["Year","FuelGroup","Value"]].head(20))

    st.subheader("Power-to-X in Transport")
    fig_ptx_simple = plot_transport_ptx_share_simple(final_df, selected_country)
    st.plotly_chart(fig_ptx_simple, use_container_width=True, config= {"scrollZoom": False,"displayModeBar": False})


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
    st.plotly_chart(fig_cat_industry, use_container_width=True,config= {"scrollZoom": False,"displayModeBar": False})
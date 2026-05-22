import streamlit as st
import pandas as pd
import os
from mappings import ptx_carriers, comparison_colors, ptx_fuel_colors
from process import *
from global_plots import * 
from transport_plots import *
from industry_plots import *

# For Streamlite Community Cloud, need to have path from the root folder
transport_file = os.path.join('REMIND', '.Results_REMIND_JRC.csv')
industry_path = os.path.join('Scripts', 'Industry', 'Results_per_Country')
final_output_path = os.path.join('Outputs')

transport_data, industry_df, final_df = load_all_data(transport_file, industry_path, final_output_path)
transport_data, industry_df, fuel_transport = prepare_data(transport_data, industry_df)

# -------- Initiate the dashboard with title and Key figures --------
st.set_page_config(layout='wide')
st.markdown(
    """
    <h1 style="text-align: center;">
        Green Fuels and Energy Demand Outlook
    </h1>
    """,
    unsafe_allow_html=True,
)

st.markdown("""
This dashboard explores how final energy demand evolves across Europe and how 
Green fuels progressively replace fossil energy in transport and industry.
It first provides a strategic overview of Green fuels integration and total energy demand, and then dives into sector-specific insights for Transport and Industry.
""")

# -------- Side bar with relevant choices for the dashboard user --------
with st.sidebar:
    st.title("Filters")
    all_countries = sorted(transport_data['Country'].unique())
    default_index = all_countries.index('EU27')
    
    selected_country = st.selectbox("Select a country:", all_countries, index=default_index, format_func=format_country_name)
    selected_year = st.selectbox("Select a year", [2030, 2040, 2050], index=2)
    focus = st.radio("What is the focus of the analysis?",
            ["All energy carriers", "Green fuels only", "Hydrogen vs other Green fuels", "Green fuels vs Fossil fuels"],index=0)


# -------- Calculate metrics for the chosen year --------
country_data = final_df[final_df['Country'] == selected_country]
eu_data = final_df[final_df['Country'] == "EU27"]

total_eu = eu_data[eu_data['Year'] == selected_year]['Value'].sum()
total = country_data[country_data['Year'] == selected_year]['Value'].sum()
ptx = country_data[(country_data['Year'] == selected_year) & (country_data['FuelGroup'].isin(ptx_carriers))]['Value'].sum()
share_ptx = (ptx / total * 100) if total > 0 else 0

metrics = [("Total Demand", total, "EJ"), ("Green fuels Demand", ptx, "EJ"), ("Green fuels market share", share_ptx, "%")]

if selected_country != "EU27":
    share_country = (total / total_eu * 100) if total_eu > 0 else 0
    metrics.insert(1, ("Share in EU27 Total demand", share_country, "%"))

cols = st.columns(len(metrics))
for col, (label, value, unit) in zip(cols, metrics):
    if "share" in label.lower():
        col.metric(label + f" ({selected_year})", f"{value:.2f}{unit}")
    else:
        col.metric(label + f" ({selected_year})", f"{value:.3f}{unit}")


# -------- Plots for energy carriers with focus filter --------
st.subheader(f"Energy demand and fuel per sector in {selected_country}")
filtered_master = apply_focus_filter(final_df[final_df['Country'] == selected_country], focus)
if focus in ["Hydrogen vs other Green fuels", "Green fuels vs Fossil fuels"]:
    color_map = comparison_colors
else:
    color_map = ptx_fuel_colors

st.plotly_chart(plot_ptx_transition_wedge(filtered_master, selected_country, color_map),use_container_width=True)
st.plotly_chart(plot_sector_ptx_intensity(filtered_master, selected_country, selected_year, color_map))



# -------- EU27 Global energy demand and key numbers --------
st.subheader(f"{selected_country} Global energy demand")

transport_name,  industry_name = 'Transport', 'Industry'
country_transport, country_transport_demand = get_country_demand(transport_data, selected_country, transport_name)
country_industry, country_industry_demand = get_country_demand(industry_df, selected_country,industry_name)
combined_demand = pd.concat([country_transport_demand, country_industry_demand], ignore_index=True)
fig_combined = create_country_combined_plot(country_transport_demand, transport_name, country_industry_demand, industry_name)

sectors = [("Transport", country_transport, country_transport_demand, 2025, 2050),
    ("Industry", country_industry, country_industry_demand, 2030, 2050)]

graph_col, key_col = st.columns((6, 4))
with graph_col:
    st.plotly_chart(fig_combined, use_container_width=True)

with key_col:
    for name, raw_df, df, year_start, year_end in sectors:
        start_val = df.loc[df['Year'] == year_start, 'Value'].values[0]
        end_val = df.loc[df['Year'] == year_end, 'Value'].values[0]
        change, growth = calculate_growth(start_val, year_start, end_val, year_end)
        
        # Top categories
        top_start = highest_category_info(raw_df, year_start)[1]
        top_end = highest_category_info(raw_df, year_end)[1]
        
        st.subheader(name)
        st.metric(f"{year_end} demand", f"{end_val:.2f} EJ", delta=f"{change:.1f}% vs {year_start}")
        st.info(f"""
                Average annual growth rate: {growth:.1f}% \\
                Top category in {year_start}: **{top_start}** \\
                Top category in {year_end}: **{top_end}**
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



# ---- Separate the dashboard into 2 tabs for Transport and Industry separated analysis ----
tabs_info = [
    {"name": "Transport", "data": country_transport, "full_data": transport_data,
    "bar_plot": plot_main_transport_stack, "pie_plot": plot_transport_pie_charts, "heatmap_plot": plot_transport_heatmap,
    "colors": ['#08306b', '#2171b5', '#6baed6', '#c6dbef', '#deebf7', '#b3cde3', '#a6bddb', '#9ebcda', '#8c96c6'],
    "pie_years": [2025, 2050],
    "heatmap_target": lambda: highest_category_info(country_transport, 2050)[0]
    },

    {"name": "Industry", "data": country_industry, "full_data": industry_df,
    "bar_plot": plot_main_industry_bar, "pie_plot": plot_industry_pie, "heatmap_plot": plot_industry_choropleth,
    "colors": ['#67000d', '#cb181d', "#f55c2d"], 
    "pie_years": [2030, 2050],
    "heatmap_target": lambda: highest_category_info(country_industry, 2050)[0]
    }
]

tab_objs = st.tabs([tab["name"] for tab in tabs_info])
for tab_obj, info in zip(tab_objs, tabs_info):
    with tab_obj:
        st.subheader(f"Evolution of categories - {info['name']}")
        fig_bar = info['bar_plot'](info["data"], info["colors"])
        st.plotly_chart(fig_bar)

        for year in info["pie_years"]:
            info["pie_plot"](info["data"], year)

        target = info["heatmap_target"]()
        fig_heatmap = info["heatmap_plot"](info["full_data"], target)
        st.plotly_chart(fig_heatmap, use_container_width=True, config={"scrollZoom": False, "displayModeBar": False})
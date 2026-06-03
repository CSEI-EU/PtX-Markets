from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

from mappings import *
from process import convert_to_alpha3

'''
This file contains functions to visualize global trends in Transport and Industry sectors.
It generates aggregated plots for country and EU-wide demand, and visualize Fuels transition and composition.
The functions are built using Plotly and can be supported by different sections of Streamlit dashboard.

Functions included: 

1. Aggregation utilities:
- get_country_demand: Filters and aggregates demand data for EU27 or a specified country.
- create_country_combined_plot: Plots Transport and Industry demand evolution over time side by side.
- calculate_growth: Computes total and annual growth percentages between two years.
- highest_category_info: Identifies the most energy-demanding category for a given year.

2. Global plots: 
- create_demand_heatmaps: Creates choropleth maps for transport and industry demand in Europe for a specific year.
- aggregate_country_demand: Aggregates yearly demand data by country and identifies top 5 consumers.
- plot_top_countries_over_time: Plots energy demand trends for top countries.
- create_top_demanding_countries_figures: Combines transport and industry plots for top-consuming countries.

3. Green fuels results specific plots:
- plot_ptx_transition_wedge: Plots evolution of fuels consumption between 2030 and 2050.
- plot_sector_ptx_intensity: Bar chart showing which sectors are the biggest PtX consumers.
- apply_focus_filter: Filter for the user to chose his focus on fuel or comparison between energy carriers.
'''

def get_country_demand(df, country_name, sector_name):
    df_eu27 = df[df['Country'] == country_name]
    df_grouped = df_eu27.groupby('Year')['Value'].sum().reset_index()
    df_grouped['Sector'] = sector_name
    return df_eu27, df_grouped


def create_country_combined_plot(first_sector_df, name_first_sector, second_sector_df, name_second_sector):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,subplot_titles=(name_first_sector, name_second_sector))

    fig.add_trace(go.Scatter(x=first_sector_df['Year'], y=first_sector_df['Value'], mode='lines', name=name_first_sector), row=1, col=1)
    fig.add_trace(go.Scatter(x=second_sector_df['Year'], y=second_sector_df['Value'], mode='lines', name=name_second_sector), row=2, col=1)

    fig.update_yaxes(title_text="Energy demand (EJ)", row=1, col=1)
    fig.update_yaxes(title_text="Energy demand (EJ)", row=2, col=1)
    fig.update_layout(height=600, width=800, showlegend=False)

    return fig


def calculate_growth(value_start, year_start, value_end, year_end):
    if value_start == 0:
        return 0, 0
    change = ((value_end - value_start) / value_start) * 100
    annual_growth = ((value_end / value_start) ** (1/(year_end-year_start)) - 1) * 100
    return change, annual_growth


def highest_category_info(data, year):
    top_cat_key = data[data['Year'] == year].groupby('Category')['Value'].sum().idxmax()
    return top_cat_key, corresponding_cat(top_cat_key)


@st.cache_data
def create_demand_heatmaps(first_sector_df, second_sector_df, selected_year):
    # Filter out EU27 and target year
    transport = first_sector_df[(first_sector_df['Year'] == selected_year) & (first_sector_df['Country'] != 'EU27')].copy()
    industry = second_sector_df[(second_sector_df['Year'] == selected_year) & (second_sector_df['Country'] != 'EU27')].copy()
    transport['iso_alpha'] = transport['Country'].apply(convert_to_alpha3)
    industry['iso_alpha'] = industry['Country'].apply(convert_to_alpha3)

    # Group by country
    t_map_data = transport.groupby('iso_alpha')['Value'].sum().reset_index()
    i_map_data = industry.groupby('iso_alpha')['Value'].sum().reset_index()
    transport_zmax = (first_sector_df[first_sector_df['Country'] != 'EU27'].groupby(['Year', 'Country'])['Value'].sum()).max()
    industry_zmax = (second_sector_df[second_sector_df['Country'] != 'EU27'].groupby(['Year', 'Country'])['Value'].sum()).max()

    fig_maps = make_subplots(
        rows=1, cols=2,
        subplot_titles=[f"Transport Demand ({selected_year})", f"Industry Demand ({selected_year})"],
        specs=[[{"type": "choropleth"}, {"type": "choropleth"}]],
        horizontal_spacing=0.05)

    fig_maps.add_trace(go.Choropleth(
        locations=t_map_data['iso_alpha'],
        z=t_map_data['Value'],
        colorscale="Reds",
        zmin=0,
        zmax=transport_zmax,
        colorbar=dict(
            title=dict(text="Demand (EJ)", font=dict(size=14)),
            tickfont=dict(size=12),
            len=0.55,         
            thickness=12,    
            x=0.47,          
            y=0.5),
        showscale=True,
        geo='geo1'), row=1, col=1)

    fig_maps.add_trace(go.Choropleth(
        locations=i_map_data['iso_alpha'],
        z=i_map_data['Value'],
        colorscale="Reds",
        zmin=0,
        zmax=industry_zmax,
        colorbar=dict(
            title="Demand (EJ)", 
            len=0.55,
            thickness=12,
            x=0.999,
            y=0.5),
        showscale=True,
        geo='geo2'), row=1, col=2)

    fig_maps.update_layout(
        height=800,
        width=1400,
        geo=dict(scope='europe', showland=True, landcolor="white", lataxis_range=[35, 70], lonaxis_range=[-15, 35]),
        geo2=dict(scope='europe', showland=True, landcolor="white", lataxis_range=[35, 70], lonaxis_range=[-15, 35]),
        margin=dict(t=50, l=20, r=20, b=10))

    # Fix the legend for years 
    for ann in fig_maps.layout.annotations:
        ann.y = 0.85
        ann.font.size = 18

    return fig_maps


def aggregate_country_demand(df):
    df = df[df['Country'] != 'EU27']
    agg_df = df.groupby(['Country', 'Year'], as_index=False)['Value'].sum()
    top_countries = agg_df.groupby('Country')['Value'].sum().nlargest(5).index.tolist()
    filtered = agg_df[agg_df['Country'].isin(top_countries)]
    
    return filtered, top_countries


def plot_top_countries_over_time(filtered_df, top_countries, title, color_map):
    fig = go.Figure()
    for country in top_countries:
        country_df = filtered_df[filtered_df['Country'] == country]
        fig.add_trace(go.Scatter(x=country_df['Year'], y=country_df['Value'], mode='lines', name=country, line=dict(color=color_map[country])))
        
    fig.update_layout(title=title, yaxis_title="Energy demand (EJ)", height=500, width=600)
    return fig


def create_top_demanding_countries_figures(first_sector_df, second_sector_df):
    transport_agg, top_transport = aggregate_country_demand(first_sector_df)
    industry_agg, top_industry = aggregate_country_demand(second_sector_df)

    # Combine all unique countries and assign colors
    combined_countries = list(set(top_transport + top_industry))
    colors = px.colors.qualitative.Safe
    color_map = {country: colors[i % len(colors)] for i, country in enumerate(combined_countries)}

    fig_transport = plot_top_countries_over_time(transport_agg, top_transport, "Transport", color_map)
    fig_industry = plot_top_countries_over_time(industry_agg, top_industry, "Industry", color_map)

    return fig_transport, fig_industry



def plot_ptx_transition_wedge(df, country_code, color_map):
    plot_df = df[df['Country'] == country_code].copy()
    plot_df.loc[plot_df['FuelGroup'] == 'Power', 'FuelGroup'] = 'Electricity'
    plot_df = plot_df.groupby(['Year', 'FuelGroup'])['Value'].sum().reset_index()
    
    fig = px.area(plot_df, x="Year", y="Value", color="FuelGroup",
                  color_discrete_map=color_map,
                  category_orders={"FuelGroup": fuel_order_full,"Year": [2030, 2040, 2050]},
                  labels={"Value": "Demand (EJ)", "FuelGroup": "Fuel type"})

    fig.update_traces(hovertemplate="Demand: %{y:.3f} EJ<extra></extra>")
    fig.update_layout(yaxis_title="Total Energy Demand (EJ)", hovermode="x unified", legend_title_text=" ")
    return fig



def plot_sector_ptx_intensity(df, country_code, year, color_map):
    plot_df = df[(df['Country'] == country_code) & (df['Year'] == year)].copy()
    plot_df.loc[plot_df['FuelGroup'] == 'Power', 'FuelGroup'] = 'Electricity'

    fig = px.bar(plot_df, x="Sector", y="Value", color="FuelGroup",
                 title=f"Sectoral Fuel Mix in {year} ({country_code})",
                 color_discrete_map=color_map,
                 category_orders={"FuelGroup": fuel_order_full}, 
                 labels={"Value": "Demand (EJ)", "FuelGroup": "Fuel type"})

    fig.update_traces(hovertemplate="Demand: %{y:.3f} EJ<extra></extra>")
    fig.update_layout(yaxis_title="Energy Demand (EJ)", hovermode="x unified", legend_title_text=" ")
    return fig




def apply_focus_filter(df, focus):
    df = df.copy()
    df.loc[df['FuelGroup'] == 'Power', 'FuelGroup'] = 'Electricity'
    
    if focus == "Green fuels only":
        return df[df["FuelGroup"].isin(ptx_carriers)]

    elif focus == "Hydrogen vs other Green fuels":
        d = df[df["FuelGroup"].isin(ptx_carriers)].copy()
        d["FuelGroup"] = d["FuelGroup"].apply(lambda x: "Hydrogen" if x == "Hydrogen" else "Other Green fuels")
        return d

    elif focus == "Green fuels vs Fossil fuels":
        d = df[df["FuelGroup"].isin(ptx_carriers + fossil_carriers)].copy()
        d["FuelGroup"] = d["FuelGroup"].apply(lambda x: "Green fuels" if x in ptx_carriers else "Fossil fuels")
        return d

    else:
        return df
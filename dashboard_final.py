import streamlit as st
import os 
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pycountry

# Transport data file 
output_transport_file = r"C:\Users\mar.eco\OneDrive - CBS - Copenhagen Business School\Desktop\PtX-Markets\REMIND\Results_REMIND_JRC.csv"
transport_data = pd.read_csv(output_transport_file)
transport_data['Year'] = transport_data['Year'].astype(int)

# Industry data files
output_industry_path = r"C:\Users\mar.eco\OneDrive - CBS - Copenhagen Business School\Desktop\PtX-Markets\Scripts\Industry\Results_per_Country"
industry_data = []
industry_files = [f for f in os.listdir(output_industry_path) if f.endswith(".xlsx")]

# Read each files and crete a final combined dataset
for file_name in industry_files:
    year, country = file_name.replace(".xlsx", "").split("_")
    file_path = os.path.join(output_industry_path, file_name)
    df = pd.read_excel(file_path, index_col=0)

    # Replace missing values by 0 
    # or indicate weither they are missing or not?
    df = df.apply(pd.to_numeric, errors='coerce').fillna(0)

    for material in df.index:
        for sector in df.columns:
            industry_data.append({
                "Year": int(year),
                "Country": country,
                "Category": sector,
                "Material": material.strip(),
                "Value": df.loc[material, sector] * 3.6 * 0.000001
            })

industry_df = pd.DataFrame(industry_data)


iso_to_country = {
    'AT': 'Austria', 'BE': 'Belgium', 'BG': 'Bulgaria', 'CY': 'Cyprus',
    'CZ': 'Czech Republic', 'DE': 'Germany', 'DK': 'Denmark', 'EE': 'Estonia',
    'EL': 'Greece', 'ES': 'Spain', 'FI': 'Finland', 'FR': 'France',
    'HR': 'Croatia', 'HU': 'Hungary', 'IE': 'Ireland', 'IT': 'Italy',
    'LT': 'Lithuania', 'LU': 'Luxembourg', 'LV': 'Latvia', 'MT': 'Malta',
    'NL': 'Netherlands', 'PL': 'Poland', 'PT': 'Portugal', 'RO': 'Romania',
    'SE': 'Sweden', 'SI': 'Slovenia', 'SK': 'Slovakia'
}
transport_data['Country_full'] = transport_data['Country'].map(iso_to_country)
industry_df['Country_full'] = industry_df['Country'].map(iso_to_country)

categories = [
    "FE|Transport|Freight|Road|Heavy",
    "FE|Transport|Freight|Road|Light",
    "FE|Transport|Pass|Road|Bus",
    "FE|Transport|Pass|Road|LDV|Four Wheelers",
    "FE|Transport|Pass|Road|LDV|Two Wheelers",
    "FE|Transport|Pass|Domestic Aviation",
    "FE|Transport|Pass|Aviation",
    "FE|Transport|Pass|Rail",
    "FE|Transport|Freight|Rail",
    "FE|Transport|Bunkers|Freight|International Shipping",
    "FE|Transport|Freight|Domestic Shipping"               
]

main_category_mapping = {
    "FE|Transport|Freight|Road|Heavy": "Road",
    "FE|Transport|Freight|Road|Light": "Road",
    "FE|Transport|Pass|Road|Bus": "Road",
    "FE|Transport|Pass|Road|LDV|Four Wheelers": "Road",
    "FE|Transport|Pass|Road|LDV|Two Wheelers": "Road",
    "FE|Transport|Pass|Domestic Aviation": "Aviation",
    "FE|Transport|Pass|Aviation": "Aviation",
    "FE|Transport|Pass|Rail": "Rail",
    "FE|Transport|Freight|Rail": "Rail",
    "FE|Transport|Bunkers|Freight|International Shipping": "Shipping",
    "FE|Transport|Freight|Domestic Shipping": "Shipping"
}

sub_category_mapping = {
    "FE|Transport|Freight|Road|Heavy": "Freight: Road (Heavy)",
    "FE|Transport|Freight|Road|Light": "Freight: Road (Light)",
    "FE|Transport|Freight|Rail": "Freight: Rail",
    "FE|Transport|Pass|Road|Bus": "Passenger: Road (Bus)",
    "FE|Transport|Pass|Road|LDV|Four Wheelers": "Passenger: Road (4W)",
    "FE|Transport|Pass|Road|LDV|Two Wheelers": "Passenger: Road (2W)",
    "FE|Transport|Pass|Rail": "Passenger: Rail",
    "FE|Transport|Pass|Aviation": "Passenger: Aviation (International)",
    "FE|Transport|Pass|Domestic Aviation": "Passenger: Aviation (Domestic)",
    "FE|Transport|Bunkers|Freight|International Shipping": "Freight: Shipping (International)",
    "FE|Transport|Freight|Domestic Shipping": "Freight: Shipping (Domestic)"
}

def corresponding_cat(category):
    if category == "FE|Transport|Freight|Road|Heavy":
        new_cat = "Goods road transport (Heavy)"
    elif category == "FE|Transport|Freight|Road|Light":
        new_cat = "Goods road transport (Light)"
        
    elif category == "FE|Transport|Pass|Road|Bus":
            new_cat = "Passenger car (Bus)"
    elif category == "FE|Transport|Pass|Road|LDV|Four Wheelers":
        new_cat = "Passenger car (Four wheelers)"
    elif category == "FE|Transport|Pass|Road|LDV|Two Wheelers":
        new_cat = "Passenger car (Two wheelers)"
        
    elif category == "FE|Transport|Pass|Domestic Aviation":
        new_cat = "Domestic Aviation"
    elif category == "FE|Transport|Pass|Aviation":
        new_cat = "Aviation"
        
    elif category == "FE|Transport|Pass|Rail":
        new_cat = "Passenger rail transport"
    elif category == "FE|Transport|Pass|Rail":
        new_cat = "Goods rail transport"

    elif category == "FE|Transport|Bunkers|Freight|International Shipping":
        new_cat = "International Shipping"
    elif category == "FE|Transport|Freight|Domestic Shipping":
        new_cat = "Domestic Shipping"

    else:
        return category
    
    return(new_cat)


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


# -------- First row : EU27 Global energy demand and key numbers --------
st.subheader("EU27 Global energy demand")

# Create a filtered dataset for EU27
eu27_transport = transport_data[transport_data['Country'] == 'EU27']
eu27_transport_demand = eu27_transport.groupby('Year')['Value'].sum().reset_index()
eu27_transport_demand['Sector'] = 'Transport'

eu27_industry = industry_df[industry_df['Country'] == 'EU27']
eu27_industry_demand = eu27_industry.groupby('Year')['Value'].sum().reset_index()
eu27_industry_demand['Sector'] = 'Industry'

combined_demand = pd.concat([eu27_transport_demand, eu27_industry_demand], ignore_index=True)

# Plot
fig_combined = make_subplots(rows=2, cols=1, shared_xaxes=True,subplot_titles=("Transport", "Industry"))
fig_combined.add_trace(go.Scatter(x=eu27_transport_demand['Year'], y=eu27_transport_demand['Value'],mode='lines', name='Transport'),
    row=1, col=1)
fig_combined.add_trace(go.Scatter(x=eu27_industry_demand['Year'], y=eu27_industry_demand['Value'],mode='lines', name='Industry'),
    row=2, col=1)

fig_combined.update_yaxes(title_text="Energy demand (EJ)", row=1, col=1)
fig_combined.update_yaxes(title_text="Energy demand (EJ)", row=2, col=1)
fig_combined.update_layout(height=600, width=800,showlegend=False)

# Key metrics
t_2025 = eu27_transport_demand[eu27_transport_demand['Year'] == 2025]['Value'].values[0]
t_2050 = eu27_transport_demand[eu27_transport_demand['Year'] == 2050]['Value'].values[0]
t_change = ((t_2050 - t_2025) / t_2025) * 100
t_growth = ((t_2050 - t_2025) / (2050 - 2025)) / t_2025 * 100

# For industry compare 2030 to 2050
i_2030 = eu27_industry_demand[eu27_industry_demand['Year'] == 2030]['Value'].values[0]
i_2050 = eu27_industry_demand[eu27_industry_demand['Year'] == 2050]['Value'].values[0]
i_change = ((i_2050 - i_2030) / i_2030) * 100
i_growth = ((i_2050 - i_2030) / (2050 - 2030)) / i_2030 * 100

# Most demanding categories 
def highest_category_info(data, year):
    top_cat_key = data[data['Year'] == year].groupby('Category')['Value'].sum().idxmax()
    return corresponding_cat(top_cat_key)

top_transport_2025 = highest_category_info(eu27_transport, 2025)
top_transport_2050 = highest_category_info(eu27_transport, 2050)
top_industry_2030 = highest_category_info(eu27_industry, 2030)
top_industry_2050 = highest_category_info(eu27_industry, 2050)

graph_eu27, key_num = st.columns((6, 4))
with graph_eu27:
    st.plotly_chart(fig_combined, use_container_width=True)

# Second column: Key numbers for EU27 global demand
with key_num:
    st.subheader("Transport")
    st.metric("2050 demand", f"{t_2050:.2f} EJ", delta=f"{t_change:.1f} % vs 2025")
    st.info(f"""
            Average annual growth rate: {t_growth:.1f} % \\
            Top category in 2025: **{top_transport_2025}** \\
            Top category in 2050: **{top_transport_2050}**
            """)
    st.markdown('---')

    st.subheader("Industry")
    st.metric("2050 demand", f"{i_2050:.2f} EJ", delta=f"{i_change:.1f} % vs 2030")
    st.info(f"""
            Average annual growth rate: {i_growth:.1f} % \\
            Top category in 2030: **{top_industry_2030}** \\
            Top category in 2050: **{top_industry_2050}**
            """)
    
st.markdown('---')

# -------- Heatmaps of 2030 demand: Transport vs Industry --------
st.subheader("Country-level energy demand by year")

# Need to convert iso2 to iso3 country codes for plotly 
def convert_to_alpha3(iso2):
    try:
        return pycountry.countries.get(alpha_2=iso2).alpha_3
    except:
        return None

# Filter data for selected year 
selected_year = st.selectbox("Select a year", [2030, 2040, 2050], index=0)
transport = transport_data[(transport_data['Year'] == selected_year) & (transport_data['Country'] != 'EU27')]
industry= industry_df[(industry_df['Year'] == selected_year) & (industry_df['Country'] != 'EU27')]

transport['iso_alpha'] = transport['Country'].apply(convert_to_alpha3)
industry['iso_alpha'] = industry['Country'].apply(convert_to_alpha3)

# Aggregate by country
t_map_data = transport.groupby('iso_alpha')['Value'].sum().reset_index()
i_map_data = industry.groupby('iso_alpha')['Value'].sum().reset_index()

transport_zmax = (transport_data[transport_data['Country'] != 'EU27'].groupby(['Year', 'Country'])['Value'].sum()).max()
industry_zmax = (industry_df[industry_df['Country'] != 'EU27'].groupby(['Year', 'Country'])['Value'].sum()).max()

# Side-by-side maps
fig_maps = make_subplots(
    rows=1, cols=2,
    subplot_titles=["Transport Demand (2030)", "Industry Demand (2030)"],
    specs=[[{"type": "choropleth"}, {"type": "choropleth"}]],
    horizontal_spacing=0.05
)

# Transport map
fig_maps.add_trace(go.Choropleth(
    locations=t_map_data['iso_alpha'],
    z=t_map_data['Value'],
    colorscale="Reds",
    zmin=0,
    zmax=transport_zmax,
    colorbar=dict(
        title="Energy demand (EJ)",
        titlefont=dict(size=14),
        tickfont=dict(size=12),
        x=0.43  
    ),
    showscale=True,
    geo='geo1'
), row=1, col=1)

# Industry map
fig_maps.add_trace(go.Choropleth(
    locations=i_map_data['iso_alpha'],
    z=i_map_data['Value'],
    colorscale="Reds",
    zmin=0,
    zmax=industry_zmax,
    colorbar=dict(title="Energy demand (EJ)"),
    showscale=True,
    geo='geo2'
), row=1, col=2)

fig_maps.update_layout(
    height=800,
    width=1400,
    geo=dict(scope='europe', showland=True, landcolor="white", lataxis_range=[35, 70], lonaxis_range=[-15, 35]),
    geo2=dict(scope='europe', showland=True, landcolor="white", lataxis_range=[35, 70], lonaxis_range=[-15, 35]),
    margin=dict(t=50, l=20, r=20, b=10)
)
st.plotly_chart(fig_maps)


# -------- Energy demand by most consuming countries --------
st.subheader("Most energy-demanding countries over time")

# Aggregate data per countries
data_without_eu27 = transport_data[transport_data['Country'] != 'EU27']
transport_agg = data_without_eu27.groupby(['Country', 'Year'], as_index=False)['Value'].sum()
industry_without_eu27 = industry_df[industry_df['Country'] != 'EU27']
industry_agg = industry_without_eu27.groupby(['Country', 'Year'], as_index=False)['Value'].sum()

# Get top 5 countries for each sector
top_transport_countries = transport_agg.groupby('Country')['Value'].sum().nlargest(5).index.tolist()
top_industry_countries = industry_agg.groupby('Country')['Value'].sum().nlargest(5).index.tolist()

# Combine unique countries and assign colors
combined_countries = list(set(top_transport_countries + top_industry_countries))
colors = px.colors.qualitative.Safe
color_map = {country: colors[i % len(colors)] for i, country in enumerate(combined_countries)}

# Filter datasets
filtered_transport = transport_agg[transport_agg['Country'].isin(top_transport_countries)]
filtered_industry = industry_agg[industry_agg['Country'].isin(top_industry_countries)]

# Create Transport figure
fig_transport = go.Figure()
for country in top_transport_countries:
    df = filtered_transport[filtered_transport['Country'] == country]
    fig_transport.add_trace(go.Scatter(
        x=df['Year'],
        y=df['Value'],
        mode='lines',
        name=country,
        line=dict(color=color_map[country])
    ))

fig_transport.update_layout(
    title="Transport Energy Demand",
    yaxis_title="Energy Demand (EJ)",
    height=500,
    width=600
)

# Create Industry figure
fig_industry = go.Figure()
for country in top_industry_countries:
    df = filtered_industry[filtered_industry['Country'] == country]
    fig_industry.add_trace(go.Scatter(
        x=df['Year'],
        y=df['Value'],
        mode='lines',
        name=country,
        line=dict(color=color_map[country])
    ))

fig_industry.update_layout(
    title="Industry Energy Demand",
    yaxis_title="Energy Demand (EJ)",
    height=500,
    width=600
)

# Show side-by-side in Streamlit
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_transport)
with col2:
    st.plotly_chart(fig_industry)



# -------- EU27 category breakdown over time --------
st.subheader("Evolution of categories in EU27")

custom_blues = ['#08306b', '#2171b5', '#6baed6', '#c6dbef', '#deebf7', '#b3cde3', '#a6bddb', '#9ebcda', '#8c96c6']
eu27_transport['MainCategory'] = eu27_transport['Category'].map(main_category_mapping)

# Group by year and main category
main_grouped = eu27_transport.groupby(['Year', 'MainCategory'])['Value'].sum().reset_index()
pivot_main = main_grouped.pivot(index='Year', columns='MainCategory', values='Value').fillna(0)

main_categories = ['Road', 'Aviation', 'Rail', 'Shipping']
available_main_categories = [cat for cat in ['Road', 'Aviation', 'Rail', 'Shipping'] if cat in pivot_main.columns]
colors_main = custom_blues[:len(available_main_categories)]

fig_main = px.bar(
    pivot_main,
    x=pivot_main.index,
    y=available_main_categories,
    labels={'value': 'Energy Demand (EJ)', 'Year': 'Year'},
    color_discrete_sequence=colors_main
)
fig_main.update_layout(barmode='stack', yaxis_title='Energy Demand (EJ)', legend_title='Transport Mode')
st.plotly_chart(fig_main)



industry_grouped = eu27_industry.groupby(['Year', 'Category'])['Value'].sum().reset_index()
pivot_industry = industry_grouped.pivot(index='Year', columns='Category', values='Value').fillna(0)

custom_reds = ['#67000d', '#a50f15', '#cb181d', '#ef3b2c', '#fb6a4a', '#fc9272', '#fcbba1', '#fee0d2']
available_industry_sectors = pivot_industry.columns.tolist()
colors_industry = custom_reds[:len(available_industry_sectors)]

# Plot
fig_industry = px.bar(
    pivot_industry,
    x=pivot_industry.index,
    y=available_industry_sectors,
    labels={'value': 'Energy Demand ()', 'Year': 'Year'},
    color_discrete_sequence=colors_industry
)
fig_industry.update_layout(
    barmode='stack',
    yaxis_title='Energy Demand ()',
    legend_title='Industry Sector'
)

st.plotly_chart(fig_industry)


# -------- Pie charts for category distribution in 2025 and 2050 --------
eu27_transport['SubCategory'] = eu27_transport['Category'].map(sub_category_mapping)
sub_data = eu27_transport.groupby(['Year', 'SubCategory'])['Value'].sum().reset_index()

def split_and_plot(year):
    year_data = sub_data[sub_data['Year'] == year]
    passenger = year_data[year_data['SubCategory'].str.contains('Passenger')]
    freight = year_data[year_data['SubCategory'].str.contains('Freight')]

    col1, col2 = st.columns(2)
    with col1:
        pie_pass = px.pie(passenger, names='SubCategory', values='Value',
                          title=f"Passenger Transport Breakdown ({year})")
        st.plotly_chart(pie_pass)

    with col2:
        pie_freight = px.pie(freight, names='SubCategory', values='Value',
                             title=f"Freight Transport Breakdown ({year})")
        st.plotly_chart(pie_freight)

st.subheader("Subcategory Distribution: Passenger vs Freight")
split_and_plot(2025)
split_and_plot(2050)

st.markdown("---")


# ---- Third row : map of the region with demand by country ----
target_category = "FE|Transport|Pass|Road|LDV|Four Wheelers"
filtered_data = transport_data[
    (transport_data['Category'] == target_category) &
    (transport_data['Country'] != 'EU27')  # Exclude total of eu27
]

filtered_data['iso_alpha'] = filtered_data['Country'].apply(convert_to_alpha3)
years_to_plot = [2020, 2050]
color_range = [0, filtered_data['Value'].max()]


# Prepare the subplot for final plot
fig = make_subplots(
    rows=1, cols=2,
    subplot_titles=[f"{year}" for year in years_to_plot],
    specs=[[{"type": "choropleth"}, {"type": "choropleth"}]],
    horizontal_spacing=0.05
)

for i, year in enumerate(years_to_plot):
    year_data = filtered_data[filtered_data['Year'] == year]
    demand_by_country = year_data.groupby('iso_alpha')['Value'].sum().reset_index()

    choropleth = go.Choropleth(
        locations=demand_by_country['iso_alpha'],
        z=demand_by_country['Value'],
        colorscale="RdBu_r",
        colorbar=dict(
            title="Energy Demand (EJ)" if i == 1 else None,
            titlefont=dict(size=18),
            tickfont=dict(size=16)
            ),
        zmin=color_range[0],
        zmax=color_range[1],
        showscale=(i == 1),
        geo=f'geo{i+1}'
        )

    fig.add_trace(choropleth, row=1, col=i+1)


fig.update_layout(
    title_text="Energy Demand for 4-wheelers in 2020 vs 2050",
    title_font=dict(size=26, family="Arial", color="black"),
    title_x=0.4,
    height=1000,
    width = 1400,
    margin=dict(l=20, r=20, t=50, b=10),
    geo=dict(
        scope='europe',
        showland=True, landcolor="white",
        lakecolor="lightblue", bgcolor='white',
        lataxis_range=[35, 70],
        lonaxis_range=[-15, 35]
    ),
    geo2=dict(  # second map geo layout
        scope='europe',
        showland=True, landcolor="white",
        lakecolor="lightblue", bgcolor='white',
        lataxis_range=[35, 70],
        lonaxis_range=[-15, 35]
    )
)

st.plotly_chart(fig, use_container_width=True)
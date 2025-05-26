import streamlit as st
import pandas as pd
import plotly.express as px


output_file = r"C:\Users\mar.eco\OneDrive - CBS - Copenhagen Business School\Desktop\PtX-Markets\REMIND\Results_REMIND_JRC.csv"
transport_data = pd.read_csv(output_file)
transport_data['Year'] = transport_data['Year'].astype(int)

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
st.subheader("EU27 Global energy demand (Transport)")

# Create a filtered dataset for the total EU27 data
eu27_data = transport_data[transport_data['Country'] == 'EU27']
eu27_global_demand = eu27_data.groupby('Year')['Value'].sum().reset_index()

# Calculate the values for 2025 and 2050 
demand_2025 = eu27_global_demand[eu27_global_demand['Year'] == 2025]['Value'].values[0]
demand_2050 = eu27_global_demand[eu27_global_demand['Year'] == 2050]['Value'].values[0]
percent_change = ((demand_2050 - demand_2025) / demand_2025) * 100

fig = px.line(eu27_global_demand, x='Year', y='Value',
              labels={'Value': 'Energy Demand (EJ)', 'Year': 'Year'})



graph_eu27, key_num = st.columns((6, 4))
with graph_eu27:
    st.plotly_chart(fig)

# Second column: Key numbers for EU27 global demand
with key_num:
    st.metric(label="Predicted energy demand in 2050", 
              value=f"{demand_2050:.2f} EJ", delta=f"{percent_change:.1f} decrease between 2025 and 2050")
    
    # Highlight the top energy-consuming subcategory in 2025 or 2050
    top_category_2025 = eu27_data[eu27_data['Year'] == 2025].groupby('Category')['Value'].sum().idxmax()
    top_category_2050 = eu27_data[eu27_data['Year'] == 2050].groupby('Category')['Value'].sum().idxmax()
    top_category_2025 = corresponding_cat(top_category_2025)
    top_category_2050 = corresponding_cat(top_category_2050)    
    st.info(f"**{top_category_2025}** category is predicted to be the highest energy consumer in 2025, "
            f"while in 2050, the highest demand is expected from **{top_category_2050}**.")
    
    
    # Average annual growth rate of energy demand
    avg_annual_growth_rate = ((demand_2050 - demand_2025) / (2050 - 2025)) / demand_2025 * 100
    st.info(f"The average annual growth rate of energy demand from 2025 to 2050 is "
            f"{avg_annual_growth_rate:.1f} % per year.")

st.markdown('---')




# -------- EU27 category breakdown over time --------
st.subheader("Evolution of Transport Categories in EU27")

custom_blues = ['#08306b', '#2171b5', '#6baed6', '#c6dbef', '#deebf7', '#b3cde3', '#a6bddb', '#9ebcda', '#8c96c6']
eu27_data['MainCategory'] = eu27_data['Category'].map(main_category_mapping)

# Group by year and main category
main_grouped = eu27_data.groupby(['Year', 'MainCategory'])['Value'].sum().reset_index()
pivot_main = main_grouped.pivot(index='Year', columns='MainCategory', values='Value').fillna(0)


main_categories = ['Road', 'Aviation', 'Rail', 'Shipping']
available_main_categories = [cat for cat in ['Road', 'Aviation', 'Rail', 'Shipping'] if cat in pivot_main.columns]
colors_main = custom_blues[:len(available_main_categories)]

fig_main = px.bar(
    pivot_main,
    x=pivot_main.index,
    y=available_main_categories,
    title="EU27 Energy Demand by Transport Mode (Road, Aviation, Rail, Maritime)",
    labels={'value': 'Energy Demand (EJ)', 'Year': 'Year'},
    color_discrete_sequence=colors_main
)
fig_main.update_layout(barmode='stack', yaxis_title='Energy Demand (EJ)', legend_title='Transport Mode')
st.plotly_chart(fig_main)




# -------- Pie charts for category distribution in 2025 and 2050 --------
eu27_data['SubCategory'] = eu27_data['Category'].map(sub_category_mapping)
sub_data = eu27_data.groupby(['Year', 'SubCategory'])['Value'].sum().reset_index()

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




# -------- Energy demand by most consuming countries --------
st.subheader("Energy Demand by country")

data_without_eu27 = transport_data[transport_data['Country'] != 'EU27']

# Sum over all categories for each countries and each year, get the top 5 consuming
aggregated_data = data_without_eu27.groupby(['Country', 'Year'], as_index=False)['Value'].sum()
top_countries = aggregated_data.groupby('Country')['Value'].sum().nlargest(5).index
filtered_data = aggregated_data[aggregated_data['Country'].isin(top_countries)]

fig = px.line(filtered_data,
              x='Year', y='Value', color='Country',
              title="Energy Demand for most consuming countries",
              labels={'Value': 'Energy Demand (EJ)', 'Year': 'Year'})

st.plotly_chart(fig)






# ---- Third row : map of the region with demand by country ----
target_category = "FE|Transport|Pass|Road|LDV|Four Wheelers"
filtered_data = transport_data[
    (transport_data['Category'] == target_category) &
    (transport_data['Country'] != 'EU27')  # Exclude total of eu27
]
import pycountry
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Need to convert iso2 to iso3 country codes for plotly 
def convert_to_alpha3(iso2):
    try:
        return pycountry.countries.get(alpha_2=iso2).alpha_3
    except:
        return None


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


'''
This file contains functions and mappings for clear definitions of categories and use of consistent colors.

Functions included: 
- extract_main_and_fuel: Gets the category and fuel from REMIND categories definition.
- corresponding_cat: Matches the REMIND categories with JRC ones by names.

Mappings: 
1. Clear categories and definitions
- iso_to_country: Maps alpha-2 country code to entire country name.
- categories: Main REMIND transport categories.
- main_category_mapping: Maps the above categories to global Road, Rail, Shipping and Aviation.
- transport_fuel_paths: Gives complete list of fuels per REMIND transport categories. 
- sub_category_mapping: Maps the sub-categories for Transport with specification (eg. Heavy or Light Road)
- fuel_order_full: Specifies order for energy carriers plots.
- ptx_carriers: Defines energy carriers considered as green.
- fossil_carriers: Defines energy carriers considered as fossil.

2. Colors specifications
- transport_sub_colors: Maps above sub-categories to colors for plots.
- industry_category_colors: Maps main Industry categories to specific colors.
- industry_fuel_colors: Maps industry fuels to specific colors.
- transport_fuel_colors: Maps transport fuels to specific colors.
- ptx_fuel_colors: Maps global energy carriers to speicific colors.
- comparison_colors: Defines colors for comparison plots.
'''


def extract_main_and_fuel(category_str, categories):
    # Sort categories by length descending to match longest prefix first
    categories_sorted = sorted(categories, key=len, reverse=True)
    
    for cat_prefix in categories_sorted:
        if category_str.startswith(cat_prefix):
            remainder = category_str[len(cat_prefix):]
            if remainder.startswith("|"):
                remainder = remainder[1:]  # remove leading '|'
            return cat_prefix, remainder
        
    # If no prefix matched, return None and full string as fuel
    return None, category_str


corresponding_categories = {
    "FE|Transport|Freight|Road|Heavy": "Goods road transport (Heavy)",
    "FE|Transport|Freight|Road|Light": "Goods road transport (Light)",
    "FE|Transport|Pass|Road|Bus": "Passenger car (Bus)",
    "FE|Transport|Pass|Road|LDV|Four Wheelers": "Passenger car (Four wheelers)",
    "FE|Transport|Pass|Road|LDV|Two Wheelers": "Passenger car (Two wheelers)",
    "FE|Transport|Pass|Domestic Aviation": "Domestic Aviation",
    "FE|Transport|Pass|Aviation": "Aviation",
    "FE|Transport|Pass|Rail": "Passenger rail transport",
    "FE|Transport|Freight|Rail": "Goods rail transport",
    "FE|Transport|Bunkers|Freight|International Shipping": "International Shipping",
    "FE|Transport|Freight|Domestic Shipping": "Domestic Shipping",
}
def corresponding_cat(category):
    return corresponding_categories.get(category, category)


iso_to_country = {
    'AT': 'Austria', 'BE': 'Belgium', 'BG': 'Bulgaria', 'CY': 'Cyprus',
    'CZ': 'Czech Republic', 'DE': 'Germany', 'DK': 'Denmark', 'EE': 'Estonia',
    'EL': 'Greece', 'ES': 'Spain', 'FI': 'Finland', 'FR': 'France',
    'HR': 'Croatia', 'HU': 'Hungary', 'IE': 'Ireland', 'IT': 'Italy',
    'LT': 'Lithuania', 'LU': 'Luxembourg', 'LV': 'Latvia', 'MT': 'Malta',
    'NL': 'Netherlands', 'PL': 'Poland', 'PT': 'Portugal', 'RO': 'Romania',
    'SE': 'Sweden', 'SI': 'Slovenia', 'SK': 'Slovakia'
}


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

transport_fuel_paths = [
    # Freight Road Heavy
    "FE|Transport|Freight|Road|Heavy|Electricity",
    "FE|Transport|Freight|Road|Heavy|Hydrogen",
    "FE|Transport|Freight|Road|Heavy|Gases",
    "FE|Transport|Freight|Road|Heavy|Gases|Biomass",
    "FE|Transport|Freight|Road|Heavy|Gases|Fossil",
    "FE|Transport|Freight|Road|Heavy|Gases|Hydrogen",
    "FE|Transport|Freight|Road|Heavy|Liquids",
    "FE|Transport|Freight|Road|Heavy|Liquids|Biomass",
    "FE|Transport|Freight|Road|Heavy|Liquids|Fossil",
    "FE|Transport|Freight|Road|Heavy|Liquids|Hydrogen",

    # Freight Road Light
    "FE|Transport|Freight|Road|Light|Electricity",
    "FE|Transport|Freight|Road|Light|Hydrogen",
    "FE|Transport|Freight|Road|Light|Gases",
    "FE|Transport|Freight|Road|Light|Gases|Biomass",
    "FE|Transport|Freight|Road|Light|Gases|Fossil",
    "FE|Transport|Freight|Road|Light|Gases|Hydrogen",
    "FE|Transport|Freight|Road|Light|Liquids",
    "FE|Transport|Freight|Road|Light|Liquids|Biomass",
    "FE|Transport|Freight|Road|Light|Liquids|Fossil",
    "FE|Transport|Freight|Road|Light|Liquids|Hydrogen",

    # Passenger Road Bus
    "FE|Transport|Pass|Road|Bus|Electricity",
    "FE|Transport|Pass|Road|Bus|Hydrogen",
    "FE|Transport|Pass|Road|Bus|Gases",
    "FE|Transport|Pass|Road|Bus|Gases|Biomass",
    "FE|Transport|Pass|Road|Bus|Gases|Fossil",
    "FE|Transport|Pass|Road|Bus|Gases|Hydrogen",
    "FE|Transport|Pass|Road|Bus|Liquids",
    "FE|Transport|Pass|Road|Bus|Liquids|Biomass",
    "FE|Transport|Pass|Road|Bus|Liquids|Fossil",
    "FE|Transport|Pass|Road|Bus|Liquids|Hydrogen",

    # Passenger Road LDV Four Wheelers
    "FE|Transport|Pass|Road|LDV|Four Wheelers|Electricity",
    "FE|Transport|Pass|Road|LDV|Four Wheelers|Hydrogen",
    "FE|Transport|Pass|Road|LDV|Four Wheelers|Gases",
    "FE|Transport|Pass|Road|LDV|Four Wheelers|Gases|Biomass",
    "FE|Transport|Pass|Road|LDV|Four Wheelers|Gases|Fossil",
    "FE|Transport|Pass|Road|LDV|Four Wheelers|Gases|Hydrogen",
    "FE|Transport|Pass|Road|LDV|Four Wheelers|Liquids",
    "FE|Transport|Pass|Road|LDV|Four Wheelers|Liquids|Biomass",
    "FE|Transport|Pass|Road|LDV|Four Wheelers|Liquids|Fossil",
    "FE|Transport|Pass|Road|LDV|Four Wheelers|Liquids|Hydrogen",

    # Passenger Road LDV Two Wheelers
    "FE|Transport|Pass|Road|LDV|Two Wheelers|Electricity",
    "FE|Transport|Pass|Road|LDV|Two Wheelers|Liquids",
    "FE|Transport|Pass|Road|LDV|Two Wheelers|Liquids|Biomass",
    "FE|Transport|Pass|Road|LDV|Two Wheelers|Liquids|Fossil",
    "FE|Transport|Pass|Road|LDV|Two Wheelers|Liquids|Hydrogen",

    # Bunkers Freight International Shipping
    "FE|Transport|Bunkers|Freight|International Shipping|Liquids",

    # Freight Domestic Shipping
    "FE|Transport|Freight|Domestic Shipping|Liquids",
    "FE|Transport|Freight|Domestic Shipping|Liquids|Biomass",
    "FE|Transport|Freight|Domestic Shipping|Liquids|Fossil",
    "FE|Transport|Freight|Domestic Shipping|Liquids|Hydrogen",

    # Bunkers Pass International Aviation
    "FE|Transport|Bunkers|Pass|International Aviation|Liquids",

    # Passenger Domestic Aviation
    "FE|Transport|Pass|Domestic Aviation|Electricity",
    "FE|Transport|Pass|Domestic Aviation|Hydrogen",
    "FE|Transport|Pass|Domestic Aviation|Liquids",
    "FE|Transport|Pass|Domestic Aviation|Liquids|Biomass",
    "FE|Transport|Pass|Domestic Aviation|Liquids|Fossil",
    "FE|Transport|Pass|Domestic Aviation|Liquids|Hydrogen",

    # Passenger Aviation
    "FE|Transport|Pass|Aviation|Electricity",
    "FE|Transport|Pass|Aviation|Hydrogen",
    "FE|Transport|Pass|Aviation|Liquids",
    "FE|Transport|Pass|Aviation|Liquids|Biomass",
    "FE|Transport|Pass|Aviation|Liquids|Fossil",
    "FE|Transport|Pass|Aviation|Liquids|Hydrogen",

    # Passenger Rail
    "FE|Transport|Pass|Rail|Electricity",
    "FE|Transport|Pass|Rail|Hydrogen",
    "FE|Transport|Pass|Rail|Liquids",
    "FE|Transport|Pass|Rail|Liquids|Biomass",
    "FE|Transport|Pass|Rail|Liquids|Fossil",
    "FE|Transport|Pass|Rail|Liquids|Hydrogen",

    # Freight Rail
    "FE|Transport|Freight|Rail|Electricity",
    "FE|Transport|Freight|Rail|Hydrogen",
    "FE|Transport|Freight|Rail|Liquids", 
    "FE|Transport|Freight|Rail|Liquids|Biomass",
    "FE|Transport|Freight|Rail|Liquids|Fossil",
    "FE|Transport|Freight|Rail|Liquids|Hydrogen",
]


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

fuel_order_full = [
    "Fossil Liquids",
    "Fossil Gases",
    "Biomass [Solid]",
    "Biogenic Liquids",
    "Biogenic Gases",
    "Synthetic Liquids",
    "Synthetic Gases",
    "Methanol",
    "Ammonia",
    "Hydrogen",
    "Electricity",
    "Renewable Energy Carrier"
]

ptx_carriers = ['Hydrogen', 'Ammonia', 'Methanol', 'Synthetic Gases', 'Synthetic Liquids', "Biogenic Gases", "Biogenic Liquids", "Biomass [Solid]",]
fossil_carriers = ["Fossil Gases", "Fossil Liquids"]

transport_sub_colors = {
    # Freight
    "Freight: Road (Heavy)": "#c95155",     
    "Freight: Road (Light)": "#dd878b",       
    "Freight: Rail": "#88a0a8",               
    "Freight: Shipping (International)": "#a3937f", 
    "Freight: Shipping (Domestic)": "#c2b280",       

    # Passenger
    "Passenger: Road (Bus)": "#729ece",     
    "Passenger: Road (4W)": "#91bfdb",      
    "Passenger: Road (2W)": "#a6d96a",       
    "Passenger: Rail": "#4575b4",            
    "Passenger: Aviation (International)": "#b8a9c9", 
    "Passenger: Aviation (Domestic)": "#8073ac"      
}

industry_category_colors = {"Iron & Steel": "#e41a1c", "Chemicals": "#377eb8", "Non-metallic minerals": "#4daf4a"}
industry_fuel_colors = {"Ammonia": "#e41a1c","Biomass": "#fb9a99", "Methanol": "#a6cee3", "Hydrogen": "#fdbf6f", "Biogas": "#ff7f00", "Overall demand": "#b2df8a", "Other": "#1f78b4"}
transport_fuel_colors = {"Electricity": "#a6cee3", "Hydrogen": "#fdbf6f", "Gases": "#fb9a99", "Liquids": "#1f78b4", "Other": "#e31a1c", }
ptx_fuel_colors = {
    "Fossil Liquids": "#1a237e",
    "Fossil Gases": "#6674be",
    "Biomass [Solid]": "#984e43",
    "Biogenic Liquids": "#7cb342",
    "Biogenic Gases": "#cddc39",
    "Synthetic Liquids": "#f9a825",
    "Synthetic Gases": "#ef6c00",
    "Methanol": "#009E73",
    "Ammonia": "#ab47bc",
    "Hydrogen": "#3fa5ff",
    "Electricity": "#17becf",
    "Renewable Energy Carrier": "#5A4A82"
}

comparison_colors = {"Hydrogen": "#1e88e5", "Other Green fuels": "#43a047", "Green fuels": "#43a047", "Fossil fuels": "#1a237e"}
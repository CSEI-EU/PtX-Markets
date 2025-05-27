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

transport_main_colors = {
    "Road": "#e41a1c",      
    "Aviation": "#377eb8",  
    "Rail": "#4daf4a",       
    "Shipping": "#984ea3"    
}

industry_category_colors = {
    "Iron & Steel": "#e41a1c",
    "Chemicals": "#377eb8",
    "Non-metallic minerals": "#4daf4a"
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

industry_fuel_colors = {
    "Ammonia": "#e41a1c",
    "Biomass": "#fb9a99",
    "Methanol": "#a6cee3",
    "Hydrogen": "#fdbf6f",
    "Biogas": "#ff7f00",
    "Overall demand": "#b2df8a",
    "Other": "#1f78b4"
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
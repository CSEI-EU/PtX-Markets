import os 
import pandas as pd
import pycountry


def load_transport_data(filepath):
    df = pd.read_csv(filepath)
    df['Year'] = df['Year'].astype(int)
    return df


def load_industry_data(filepath):
    industry_data = []
    industry_files = [f for f in os.listdir(filepath) if f.endswith(".xlsx")]

    for file_name in industry_files:
        year, country = file_name.replace(".xlsx", "").split("_")
        file_path = os.path.join(filepath, file_name)
        df = pd.read_excel(file_path, index_col=0)
        df = df.apply(pd.to_numeric, errors='coerce').fillna(0)

        for material in df.index:
            for sector in df.columns:
                industry_data.append({
                    "Year": int(year),
                    "Country": country,
                    "Category": sector,
                    "Material": material.strip(),
                    "Value": df.loc[material, sector] * 3.6 * 0.000001 # Convert to EJ 
                })

    return pd.DataFrame(industry_data)

def convert_to_alpha3(iso2):
    try:
        return pycountry.countries.get(alpha_2=iso2).alpha_3
    except:
        return None
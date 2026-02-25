# PtX-Markets Energy Demand project

This project visualises and analyes the evolution of energy demand in Europe with a focus on Green Fuels integration. It uses data from REMIND and JRC and produces a dynamic dashboard for interactive analysis.

Project structure
PtX-Markets/
├── Inputs/
│   └── JRC-IDEES (2021) raw data and Neuwirth (2024) for Industry
│
├── Outputs/
│   └── Green and fossil fuels demand results per country (EJ) for 2030, 2040 and 2050
│
├── REMIND/
│   └── REMIND Transport results (European aggregates) with JRC categories used as a proxy
│
├── Scripts/
│   ├── Industry/
│   │   │── Preparation of population and GDP projections based on SSP2 historic data
│   │   ├── Regression script for future scenario demand per country
│   │   └── Results folder for each country, per year 
│   │
│   ├── Transport/
│   │   └── Script to clean, sort, and analyze REMIND data per category
│   │
│   ├── Dashboard_dynamic/
│   │   │── Dashboard_dynamic script for final Streamlit Community Cloud deployment
│   │   └── Process Script for general loading of files
│   │   └── Global plots, Transport plots, Industry plots files to separate handling of categories in the main script
│   │   └── Mappings fore relevant categories and colors in the dashboard
│   │
│   └── Dashboard_static/
│       └── Index.html file for static version of the dashboard on very few data (DK and EU27)
│
└── README.md


Usage:
Install dependencies with "pip install -r Scripts/Dashboard_dynamic/requirements.txt"
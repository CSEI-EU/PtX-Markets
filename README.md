# PtX-Markets Energy Demand Dashboard

<img width="1839" height="832" alt="ptx_markets_dashboard" src="https://github.com/user-attachments/assets/e75d5978-f671-425f-820c-f403c92c1173" />

Explore the interactive dashboard of the **[Power-to-X Energy Demand Model](https://ptx-markets-results.streamlit.app/)**

The PtX-Markets Energy Demand Dashboard is developed by the Copenhagen School of Energy Infrastructure (CSEI). The project provides a framework for estimating and visualizing future demand for green fuels across Europe based on publicly available energy scenarios and sectoral demand data.

The dashboard combines data from REMIND, JRC-IDEES, and additional literature to derive country-level demand projections for the industry and transport sectors. The processed results are presented through an interactive dashboard for scenario exploration and analysis.

## Contents

- [Description](#description)
- [Dashboard Structure](#dashboard-structure)
- [Installation](#installation)
- [Contributing](#contributing)
- [Citing](#citing)
- [License](#license)

---

## Description

The PtX-Markets Energy Demand Dashboard estimates future demand for green fuels across Europe for the years 2030, 2040, and 2050. Rather than modelling energy markets, the project develops sector-specific demand projections by combining publicly available datasets with future scenario assumptions.

The dashboard focuses on two major demand sectors:

- **Industry**, where country-level demand projections are derived from JRC-IDEES data combined with population and GDP projections.
- **Transport**, where European REMIND scenario results are processed and allocated to detailed transport categories using JRC-IDEES as a proxy.

The workflow consists of three main components:

1. **Input data preparation**, including the processing of REMIND scenario outputs, JRC-IDEES statistics, and supporting datasets.
2. **Demand estimation**, where future country-level fuel demand is calculated using regression models and scenario assumptions.
3. **Visualization**, where the processed results are presented through an interactive Streamlit dashboard and a lightweight static dashboard.

The outputs include country-level demand projections for fossil and green fuels, enabling comparisons across sectors, countries, and future time horizons.

---

## Dashboard Structure

```text
PtX-Markets/
│
├── Inputs/
│   └── JRC-IDEES (2021) raw data and Neuwirth (2024) data for the industry sector.
│
├── Outputs/
│   └── Country-level demand projections for green and fossil fuels (EJ)
│       for 2030, 2040, and 2050.
│
├── REMIND/
│   └── REMIND transport scenario results (European aggregates)
│       mapped to JRC-IDEES transport categories.
│
├── Scripts/
│   │
│   ├── Industry/
│   │   ├── Preparation of population and GDP projections based on
│   │   │   historical SSP2 data.
│   │   ├── Regression scripts for estimating future country-level demand.
│   │   └── Country-specific results for each scenario year.
│   │
│   ├── Transport/
│   │   └── Scripts for cleaning, processing, and analysing REMIND
│   │       transport data by category.
│   │
│   ├── Dashboard_dynamic/
│   │   ├── Main Streamlit application.
│   │   ├── Data processing and loading routines.
│   │   ├── Plotting modules for global, transport, and industry analyses.
│   │   └── Category mappings and dashboard colour definitions.
│   │
│   └── Dashboard_static/
│       └── Static HTML dashboard for demonstration purposes
│           (Denmark and EU27 only).
│
└── README.md
```

---

## Installation

The dashboard can either be explored through the online dashboard or run locally for development, further analysis, and modification of the underlying assumptions.

### Using the Dashboard

The results can be explored directly through the online Streamlit dashboard without installing any software:

https://ptx-markets-results.streamlit.app/

### Running the Dashboard Locally

If you would like to reproduce the analysis, modify assumptions, or further develop the dashboard, we recommend using a dedicated Python virtual environment (e.g. Anaconda or `venv`).

Clone the repository:

```bash
git clone https://github.com/CSEI-EU/PtX-Markets.git
cd PtX-Markets
```

Install the required packages:

```bash
pip install -r Scripts/Dashboard_dynamic/requirements.txt
```

Launch the dashboard locally:

```bash
streamlit run Scripts/Dashboard_dynamic/dashboard_dynamic.py
```

---

## Contributing

The PtX-Markets Energy Demand Dashboard is developed by researchers at the Copenhagen School of Energy Infrastructure (CSEI).

| Person | Contribution |
| --- | --- |
| *Mathilde Roger Estrade* | Main Dashboard development, Data Processing and Scenario Development |
| *Flora v. Mikulicz-Radecki* | Data processing and Data Collection |
| *Johannes Giehl* | Conceptualization and Methodology |
| *Jens Weibezahn* | Conceptualization and Methodology |

---

## Citing

If you use the PtX-Markets Energy Demand Project in your research, please cite:

> Roger Estrade, Mathilde, v. Mikulicz-Radecki, Flora, Giehl, Johannes, Weibezahn, Jens. (2026), *PtX-Markets Energy Demand Dashboard*. Copenhagen School of Energy Infrastructure (CSEI). Copenhagen Business School. GitHub repository. https://github.com/CSEI-EU/PtX-Markets. Accessed YYYY-MM-DD.

If the project is accompanied by a scientific publication in the future, please cite the publication in addition to the repository.

---

## License

The PtX-Markets Energy Demand Project is distributed under the license specified in the `LICENSE` file.

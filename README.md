# Electric Vehicles and Charging Stations Dashboard

## App Deployment URL

https://gp84ldgpxiqzz92ttodcpw.streamlit.app

## Local Setup Instructions

```bash
git clone https://github.com/TharunDoma/vp1.git
cd vp1
pip install -r requirements.txt
streamlit run vaprijj.py
```

## Project Overview

This Streamlit web application provides:

- Overview of electric vehicles' growth over years
- Insights on mileage comparison between EV companies
- State-level EV infrastructure analysis
- Geospatial visualization of charging stations
- LLM-powered assistant for EV dataset analysis

## Dataset Sources

- EV_Stations_Combined_State_Level.csv: Combined charging station dataset.
- Electric_Vehicles_Population_Data.csv: Population data of electric vehicles.
- EV_stations.csv: Geolocation and type of charging stations.

## Features

- 📈 EV Growth and Mileage Analysis
- 📍 Interactive Geospatial Map
- 🏙️ State-wise Charging Infrastructure Breakdown
- 🤖 LLM-based EV Data Assistant (Groq API)

## Technologies Used

- Streamlit
- Pandas
- Altair
- Plotly
- OpenStreetMap
- Groq API (LLM Model Integration)

## How to Deploy

- Deploy on [Streamlit Community Cloud](https://streamlit.io/cloud) by connecting your GitHub repo.
- Ensure you have added your `GROQ_API_KEY` in Streamlit secrets.

## Note

- Large CSV files (> 25MB) might not be previewable on GitHub but are fully usable within the app.

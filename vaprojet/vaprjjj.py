import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import base64
import requests  

# ---------- Add background CSS ----------
def add_bg_from_local(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/gif;base64,{encoded_string}");
            background-attachment: fixed;
            background-size: cover;
            background-position: center;
        }}
        .block-container, .css-18e3th9 {{
            background-color: rgba(255, 255, 255, 0.8);
            padding: 20px;
            border-radius: 10px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Add background from local file


# Load Combined State-Level Dataset
@st.cache_data
def load_data():
    df = pd.read_csv("data/EV_Stations_Combined_State_Level.csv")
    ev_population = pd.read_csv("data/Electric_Vehicle_Population_Data.csv")
    return df, ev_population

df, ev_population = load_data()

# Sidebar Navigation
st.sidebar.title("EV & Charging Stations Dashboard")
page = st.sidebar.radio("Go to", ["Overview", "State-Level Insights", "Geospatial Analysis", "LLM Insights"])

# -------------------- Overview Page --------------------
if page == "Overview":
    st.title("Electric Vehicles and Charging Stations Overview")
    add_bg_from_local("images/LIGHTNING_G4.gif")
    # Clean EV population data: drop missing and remove 2024
    ev_population = ev_population.dropna(subset=['Make', 'Model', 'Model Year', 'Electric Range'])
    ev_population_filtered = ev_population[ev_population['Model Year'] < 2024]

    st.metric("Total States Analyzed", len(df))
    st.metric("Total Unique EV Makes", ev_population_filtered['Make'].nunique())
    st.metric("Total Unique EV Models", ev_population_filtered['Model'].nunique())

    selected_companies = st.multiselect("Select EV Companies", ev_population_filtered['Make'].dropna().unique())

    if selected_companies:
        filtered_data = ev_population_filtered[ev_population_filtered['Make'].isin(selected_companies)]
        st.subheader(f"EV Growth Over Years for {', '.join(selected_companies)}")
        growth_data = filtered_data.groupby(['Model Year', 'Make']).size().reset_index(name='EV Count')
        fig_company_growth = px.line(growth_data, x='Model Year', y='EV Count', color='Make', markers=True,
                                     title='EV Growth Over Years by Company')
        st.plotly_chart(fig_company_growth)

    st.subheader("Mileage Comparison Between Companies")
    mileage_data = ev_population_filtered.groupby('Make')['Electric Range'].mean().reset_index().dropna()
    fig_mileage = px.bar(mileage_data, x='Make', y='Electric Range', color='Make', title='Average Range by Company')
    st.plotly_chart(fig_mileage)

    st.subheader("All EVs vs Yearly Growth")
    total_growth_data = ev_population_filtered.groupby('Model Year').size().reset_index(name='Total EV Count')
    fig_total_growth = px.line(total_growth_data, x='Model Year', y='Total EV Count', markers=True, title='Total EV Growth Over Years')
    st.plotly_chart(fig_total_growth)
    st.caption("🔍 2024 data excluded from growth charts due to incomplete or ongoing reporting.")

    st.subheader("📥 Download Full Dataset")
    st.download_button("Download Combined State Dataset", data=df.to_csv(index=False), file_name='EV_Stations_Combined_State_Level.csv')


# -------------------- State-Level Insights --------------------
elif page == "State-Level Insights":
    st.title("State-Level Analysis")
    add_bg_from_local("images/tookki.gif")
    state_full_names = {
        'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California',
        'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia',
        'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa',
        'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
        'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri',
        'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey',
        'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio',
        'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
        'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont',
        'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'
    }

    full_state_list = [state_full_names.get(abbr, abbr) for abbr in df['State'].unique()]
    selected_state_full = st.selectbox("Select State", sorted(full_state_list))
    selected_state_abbr = [abbr for abbr, full in state_full_names.items() if full == selected_state_full]
    selected_state_abbr = selected_state_abbr[0] if selected_state_abbr else selected_state_full

    state_data = df[df['State'] == selected_state_abbr]

    st.subheader(f"Details for {selected_state_full}")
    st.write(state_data)

    st.subheader("Charging Infrastructure Overview")
    st.subheader(f"Charging Infrastructure Distribution in {selected_state_full}")

# Prepare data for the pie chart
    infra_data = state_data[['Total Level 1 Chargers', 'Total Level 2 Chargers', 'Total DC Fast Chargers']].sum().reset_index()
    infra_data.columns = ['Charger Type', 'Count']

    # Create a pie chart with custom styling
    infra_pie_fig = px.pie(
        infra_data,
        names='Charger Type',
        values='Count',
        title=f"Unique Charging Infrastructure Overview in {selected_state_full}",
        color_discrete_sequence=px.colors.qualitative.Pastel,  # Use a pastel color palette
        hole=0.3  # Create a semi-donut style pie chart
    )

    # Add advanced features like custom text positioning and labels
    infra_pie_fig.update_traces(
        textposition='outside',  # Position text outside the slices
        textinfo='percent+label',  # Show labels and percentages
        pull=[0.1, 0.2, 0.1]  # Pull slices outward for emphasis
    )

    st.plotly_chart(infra_pie_fig)

    st.subheader("Comparison of EV Companies Based on Average Electric Range")

    # Group data by EV companies (Make) and calculate metrics
    ev_comparison = ev_population.groupby('Make').agg({
        'Electric Range': 'mean',  # Average range per company
        'Model': 'count'  # Total number of models per company
    }).reset_index()
    ev_comparison.rename(columns={'Model': 'Total Models'}, inplace=True)

    # Create a bar chart comparing EV companies
    ev_comparison_fig = px.bar(ev_comparison, x='Make', y='Electric Range',
                            color='Electric Range',
                            hover_data=['Total Models'],
                            title="Comparison of EV Companies by Average Range",
                            labels={"Make": "EV Company", "Electric Range": "Average Electric Range (Miles)"},
                            height=600)
    st.plotly_chart(ev_comparison_fig)

# -------------------- Geospatial Analysis --------------------
elif page == "Geospatial Analysis":
    st.title("Geospatial Distribution of Charging Stations")
    add_bg_from_local("images/evvabgrnd.png")
    ev_stations = pd.read_csv("data/EV_stations.csv")
    map_data = ev_stations[['Latitude', 'Longitude', 'EV Level1 EVSE Num', 'EV Level2 EVSE Num', 'EV DC Fast Count']].dropna(subset=['Latitude', 'Longitude'])

    def station_type(row):
        if row['EV DC Fast Count'] > 0:
            return 'DC Fast'
        elif row['EV Level2 EVSE Num'] > 0:
            return 'Level 2'
        elif row['EV Level1 EVSE Num'] > 0:
            return 'Level 1'
        else:
            return 'Unknown'

    map_data['Station Type'] = map_data.apply(station_type, axis=1)

    fig_map = px.scatter_mapbox(map_data, lat='Latitude', lon='Longitude', color='Station Type',
                                color_discrete_map={'Level 1': 'blue', 'Level 2': 'green', 'DC Fast': 'red', 'Unknown': 'gray'},
                                zoom=3, height=600)
    fig_map.update_layout(mapbox_style='open-street-map')
    st.plotly_chart(fig_map)

    st.subheader("📥 Download Charging Stations Data")
    st.download_button("Download Charging Stations Data", data=ev_stations.to_csv(index=False), file_name='EV_Stations.csv')

# -------------------- LLM Insights Page using Groq --------------------
elif page == "LLM Insights":
    st.title("Ask the EV Assistant")
    add_bg_from_local("images/benz.webp")

    def ask_groq_llama(prompt):
        headers = {
            "Authorization": f"Bearer {st.secrets['GROQ_API_KEY']}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant for analyzing electric vehicle data."},
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    user_input = st.text_input("Ask something about EV data:")
    prompt=""
    if user_input:
        prompt = f"""You are an expert in electric vehicle data analysis.
EV population dataset columns: {', '.join(ev_population.columns)}
Charging station dataset columns: {', '.join(df.columns)}
User question: {user_input}"""

        try:
            answer = ask_groq_llama(prompt)
            st.markdown("### Answer")
            st.write(answer)
        except Exception as e:
            st.error(f"An error occurred: {e}")
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="CO2 Emissions Analysis", layout="wide")

# 1. Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("climate_data.csv")
    return df.dropna()

df = load_data()

# Sidebar
st.sidebar.title("🧭 Navigation")
section = st.sidebar.radio("Go to", [
    "Historical Trends",
    "Per Capita Impact",
    "Emissions vs Temperature",
    "Enhanced Temp Analysis",
    "Interactive Map",
    "Country Trends"
])

st.title("🌍 Climate Change Data Explorer")

# 2. Historical Trends & Turning Points
if section == "Historical Trends":
    st.header("📈 Historical Trends & Turning Points in Emissions")

    df_grouped = df.groupby('year').agg({
        'co2': 'sum',
        'cumulative_co2': 'sum'
    }).reset_index()

    fig1 = px.line(df_grouped, x='year', y='co2', title='Annual Total CO₂ Emissions (Mt)')
    fig2 = px.line(df_grouped, x='year', y='cumulative_co2', title='Cumulative CO₂ Emissions (Mt)')

    st.plotly_chart(fig1, use_container_width=True)
    st.plotly_chart(fig2, use_container_width=True)

# 3. Per Capita Impact and Equity Analysis
elif section == "Per Capita Impact":
    st.header("👤 Per Capita Impact and Equity Analysis")

    selected_year = st.slider("Select Year", int(df['year'].min()), int(df['year'].max()), 2020)

    top10 = df[df['year'] == selected_year].sort_values(by='co2_per_capita', ascending=False).head(10)

    fig = px.bar(top10, x='country', y='co2_per_capita', 
                 title=f"Top 10 Countries by CO₂ Per Capita in {selected_year}",
                 labels={'co2_per_capita': 'CO₂ per Capita (tonnes)'})
    st.plotly_chart(fig, use_container_width=True)

# 4. Emissions vs Temperature Change
elif section == "Emissions vs Temperature":
    st.header("🌡️ Connecting Emissions to Temperature Change")

    avg_df = df.groupby('country').agg({
        'co2': 'mean',
        'temperature_change_from_co2': 'mean'
    }).reset_index()

    fig = px.scatter(avg_df, x='co2', y='temperature_change_from_co2',
                     hover_name='country',
                     title="Avg Annual CO₂ vs. Temperature Change from CO₂",
                     labels={'co2': 'Avg CO₂ Emissions (Mt)', 'temperature_change_from_co2': 'Temp Change (°C)'})
    st.plotly_chart(fig, use_container_width=True)

# 5. Enhanced Temperature Change Analysis
elif section == "Enhanced Temp Analysis":
    st.header("🔥 Enhanced Temperature Change Analysis (GHG Inclusive)")

    enhanced_df = df.groupby('country').agg({
        'co2': 'mean',
        'temperature_change_from_co2': 'mean',
        'share_of_temperature_change_from_ghg': 'mean'
    }).reset_index()

    fig = px.scatter(
        enhanced_df,
        x='co2',
        y='temperature_change_from_co2',
        size='share_of_temperature_change_from_ghg',
        hover_name='country',
        title="CO₂ vs Temperature Change, Bubble Size = GHG Share",
        labels={
            'co2': 'Avg CO₂ Emissions (Mt)',
            'temperature_change_from_co2': 'Temp Change (°C)',
            'share_of_temperature_change_from_ghg': 'GHG Temp Share (%)'
        }
    )
    st.plotly_chart(fig, use_container_width=True)

# 6. Interactive Choropleth Map
elif section == "Interactive Map":
    st.header("🗺️ Interactive CO₂ per Capita Map")

    year = st.slider("Choose Year", int(df['year'].min()), int(df['year'].max()), 2020)

    map_data = df[df['year'] == year]

    fig = px.choropleth(
        map_data,
        locations="country",
        locationmode="country names",
        color="co2_per_capita",
        hover_name="country",
        color_continuous_scale="Viridis",
        title=f"CO₂ Emissions per Capita in {year}"
    )
    st.plotly_chart(fig, use_container_width=True)

# 7. Country-Level Time Series
elif section == "Country Trends":
    st.header("📊 Country-Level CO₂ & Temperature Trends")

    countries = st.multiselect("Select Countries", df['country'].unique(), default=["United States", "China", "India"])

    metric = st.selectbox("Metric", ["co2", "co2_per_capita", "temperature_change_from_co2"])

    fig = px.line(df[df['country'].isin(countries)], x='year', y=metric, color='country',
                  title=f"{metric.replace('_', ' ').title()} Over Time")

    st.plotly_chart(fig, use_container_width=True)

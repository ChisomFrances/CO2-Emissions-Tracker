import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="CO2 Emissions Analysis", layout="wide")

# 1. Load Data
@st.cache_data
def load_data():
    return pd.read_csv("climate_data.csv")

df = load_data()

# Sidebar
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", [
    "Historical Trends",
    "Per Capita Impact",
    "Emissions vs Temperature",
    "Interactive Map",
    "Country Trends"
])

st.sidebar.markdown("### Filter")
selected_year = st.sidebar.slider("Select Year", int(df['year'].min()), int(df['year'].max()), 2020)

st.title("🌍 Climate Change Data Explorer")

# 2. Historical Trends & Turning Points
if section == "Historical Trends":
    st.header("📈 Historical Trends & Turning Points in Emissions")

    world_df = df[df['country'] == 'World']

    metric = st.selectbox("Metric", ["co2", "co2_per_capita"])

# Plot CO2 vs Year
    st.subheader("World: CO₂ Emissions vs Year")
    fig_co2 = px.line(world_df, x='year', y=metric, title="World: CO₂ Emissions vs Year",
                  labels={'year': 'Year', 'co2': 'CO₂ Emissions (Mt)'})
    fig_co2.update_layout(xaxis=dict(showgrid=True), yaxis=dict(showgrid=True))
    st.plotly_chart(fig_co2, use_container_width=True)

# Plot Cumulative CO2 vs Year
    st.subheader("World: Cumulative CO₂ Emissions vs Year")
    fig_cumulative = px.line(world_df, x='year', y='cumulative_co2', title="World: Cumulative CO₂ Emissions vs Year",
                         labels={'year': 'Year', 'cumulative_co2': 'Cumulative CO₂ Emissions (Mt)'})
    fig_cumulative.update_layout(xaxis=dict(showgrid=True), yaxis=dict(showgrid=True))
    st.plotly_chart(fig_cumulative, use_container_width=True)


# 3. Per Capita Impact and Equity Analysis
elif section == "Per Capita Impact":
    st.header("👤 Per Capita Impact and Equity Analysis")

    top10 = df[df['year'] == selected_year].sort_values(by='co2_per_capita', ascending=False).head(10)

    fig = px.bar(top10, x='country', y='co2_per_capita',
                 title=f"Top 10 Countries by CO₂ Per Capita in {selected_year}",
                 labels={'co2_per_capita': 'CO₂ per Capita (tonnes)'})
    st.plotly_chart(fig, use_container_width=True)

# 4. Contributions to Global Warming 
elif section == "Emissions vs Temperature":
    st.header("🌡️ Connecting Emissions and Temperature Change")

    # Filter by year
    filtered_df = df[df['year'] == selected_year]

    # Multi-select countries
    countries = st.multiselect("Select Countries", df['country'].unique(), default=df['country'].unique())

    # Top and Bottom 20 countries
    top20 = filtered_df.sort_values(by="share_of_temperature_change_from_ghg", ascending=False).head(20)
    bottom20 = filtered_df.sort_values(by="share_of_temperature_change_from_ghg", ascending=True).head(20)

    st.subheader(f"Share of Global Temperature Change from GHGs by Country - {selected_year}")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🔺 Top 20 Countries")
        top20 = top20.sort_values(by="share_of_temperature_change_from_ghg", ascending=True)  # Reverse for bar orientation
        fig_col1 = px.bar(
            top20,
            x='share_of_temperature_change_from_ghg',
            y='country',
            orientation='h',
            title='Top 20 Countries',
            labels={'share_of_temperature_change_from_ghg': 'Share (%)', 'country': 'Country'}
        )

        fig_col1.update_layout(height=30 * len(top20), yaxis=dict(categoryorder='total ascending', automargin=True, showgrid=True),margin=dict(l=150, r=20, t=40, b=40),xaxis=dict(showgrid=True)
)

        st.plotly_chart(fig_col1, use_container_width=True)

    with col2:
        st.markdown("### 🔻 Bottom 20 Countries")
        bottom20 = bottom20.sort_values(by="share_of_temperature_change_from_ghg", ascending=True)
        fig_col2 = px.bar(
            bottom20,
            x='share_of_temperature_change_from_ghg',
            y='country',
            orientation='h',
            title='Bottom 20 Countries',
            labels={'share_of_temperature_change_from_ghg': 'Share (%)', 'country': 'Country'}
        )
        fig_col2.update_layout(height=30 * len(bottom20), yaxis=dict(categoryorder='total ascending', automargin=True,showgrid=True), margin=dict(l=150, r=20, t=40, b=40),xaxis=dict(showgrid=True))

        st.plotly_chart(fig_col2, use_container_width=True)


# 5. Interactive Choropleth Map
elif section == "Interactive Map":
    st.header("🗺️ Interactive CO₂ per Capita Map")

    map_data = df[df['year'] == selected_year]

    fig = px.choropleth(
        map_data,
        locations="country",
        locationmode="country names",
        color="co2_per_capita",
        hover_name="country",
        color_continuous_scale="Viridis",
        title=f"CO₂ Emissions per Capita in {selected_year}"
    )
    st.plotly_chart(fig, use_container_width=True)

# 6. Country-Level Time Series
elif section == "Country Trends":
    st.header("📊 Country-Level CO₂ & Temperature Trends")

    countries = st.multiselect("Select Countries", df['country'].unique(), default=["United States", "China", "India"])
    metric = st.selectbox("Metric", ["co2", "co2_per_capita", "temperature_change_from_co2"])

    fig = px.line(df[df['country'].isin(countries)], x='year', y=metric, color='country',
                  title=f"{metric.replace('_', ' ').title()} Over Time")
    st.plotly_chart(fig, use_container_width=True)

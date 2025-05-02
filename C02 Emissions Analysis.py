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

    world_df = df[df['country'] == 'World']

# Streamlit app title
st.title("World CO₂ Emissions Analysis")

# Plot CO2 vs Year
st.subheader("World: CO₂ Emissions vs Year")
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=world_df, x='year', y='co2', ax=ax)
ax.set(title="World: CO₂ Emissions vs Year", xlabel="Year", ylabel="CO₂ Emissions (Mt)")
ax.grid(True)
st.pyplot(fig)

# Plot Cumulative CO2 vs Year
st.subheader("World: Cumulative CO₂ Emissions vs Year")
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=world_df, x='year', y='cumulative_co2', ax=ax)
ax.set(title="World: Cumulative CO₂ Emissions vs Year", xlabel="Year", ylabel="Cumulative CO₂ Emissions (Mt)")
ax.grid(True)
st.pyplot(fig)

# 3. Per Capita Impact and Equity Analysis
elif section == "Per Capita Impact":
    st.header("👤 Per Capita Impact and Equity Analysis")

    selected_year = st.slider("Select Year", int(df['year'].min()), int(df['year'].max()), 2020)

    top10 = df[df['year'] == selected_year].sort_values(by='co2_per_capita', ascending=False).head(10)

    fig = px.bar(top10, x='country', y='co2_per_capita', 
                 title=f"Top 10 Countries by CO₂ Per Capita in {selected_year}",
                 labels={'co2_per_capita': 'CO₂ per Capita (tonnes)'})
    st.plotly_chart(fig, use_container_width=True)

# 4. Contributions to Global Warming
elif section == "Emissions and Temperature":
    st.header("🌡️ Connecting Emissions and Temperature Change")

# Sidebar filters
st.sidebar.title("Filter")
selected_year = st.sidebar.slider("Select Year", int(df['year'].min()), int(df['year'].max()), 2020)

# Filter by year
filtered_df = df[df['year'] == selected_year]

# Top 20 countries
top20 = filtered_df.sort_values(by="share_of_temperature_change_from_ghg", ascending=False).head(20)

# Bottom 20 countries
bottom20 = filtered_df.sort_values(by="share_of_temperature_change_from_ghg", ascending=True).head(20)

# Display
st.title("🌡️ Share of Global Temperature Change from GHGs by Country")
st.subheader(f"Year: {selected_year}")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🔺 Top 20 Countries")
    fig_top, ax_top = plt.subplots(figsize=(8, 6))
    sns.barplot(data=top20, y="country", x="share_of_temperature_change_from_ghg", palette="Reds_r", ax=ax_top)
    ax_top.set_title("Top 20 Countries")
    ax_top.set_xlabel("Share (%)")
    ax_top.set_ylabel("Country")
    st.pyplot(fig_top)

with col2:
    st.markdown("### 🔻 Bottom 20 Countries")
    fig_bottom, ax_bottom = plt.subplots(figsize=(8, 6))
    sns.barplot(data=bottom20, y="country", x="share_of_temperature_change_from_ghg", palette="Blues", ax=ax_bottom)
    ax_bottom.set_title("Bottom 20 Countries")
    ax_bottom.set_xlabel("Share (%)")
    ax_bottom.set_ylabel("Country")
    st.pyplot(fig_bottom)


# 5. Interactive Choropleth Map
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

#6. Country-Level Time Series
elif section == "Country Trends":
    st.header("📊 Country-Level CO₂ & Temperature Trends")

    countries = st.multiselect("Select Countries", df['country'].unique(), default=["United States", "China", "India"])

    metric = st.selectbox("Metric", ["co2", "co2_per_capita", "temperature_change_from_co2"])

    fig = px.line(df[df['country'].isin(countries)], x='year', y=metric, color='country',
                  title=f"{metric.replace('_', ' ').title()} Over Time")

    st.plotly_chart(fig, use_container_width=True)

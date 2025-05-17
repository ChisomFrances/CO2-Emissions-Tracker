import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Global Emissions Analysis", layout="wide")

# 1. Load Data
@st.cache_data
def load_data():
    return pd.read_csv("climate_data.csv")

df = load_data()

#st.title("Global Emissions Analysis")
st.markdown(
    "<h1 style='text-align:left; margin-top:0px ;'>Global Emissions Analysis</h1>",
    unsafe_allow_html=True
)

# Sidebar
st.sidebar.markdown("## Navigation")
section = st.sidebar.radio(
        label="### Go to",
        options=[
    "Global Historical Trends",
    "Country Trends",
    "Country Trends with Interactive Map",
    "Per Capita Impact",
    "Emissions and Temperature",
       
])


# Conditional year filter in sidebar for specific sections
year_sections = ["Country Trends with Interactive Map","Per Capita Impact", "Emissions and Temperature"]
if section in year_sections:
    st.sidebar.markdown("### Filter")
    selected_year = st.sidebar.slider(
        "Select Year",
        int(df['year'].min()),
        int(df['year'].max()),
        2020
    )

metric_sections = ["Global Historical Trends", "Country Trends","Country Trends with Interactive Map"]
if section in metric_sections:
    st.sidebar.markdown("### Metric")
    label_map = {
    "co2": "CO₂",
    "co2_per_capita": "CO₂ per Capita"
}

# Metric filter only for the two metric sections
def get_metric():
    labels = {
        "co2": "CO₂",
        "co2_per_capita": "CO₂ per Capita"
    }
    return st.sidebar.selectbox(
        "Select Metric",
        options=list(labels.keys()),
        format_func=lambda k: labels[k]
    )

if section in metric_sections:
    metric = get_metric()

PX_CONTINUOUS = [
    [0.0,  '#2E8B57'],  # olive green
    [0.2,  '#9CAF88'],  # sage green
    [0.5,  '#ADFF2F'],  # greenish yellow
    [0.8,  '#FFFF00'],  # yellow
    [1.0,  '#FF0000']   # red
]

# 2. Historical Trends & Turning Points
if section == "Global Historical Trends":
    st.subheader("Annual Global Emissions")

    world_df = df[df['country'] == 'World']


# Plot CO2 vs Year
    fig_co2 = px.line(world_df, x='year', y=metric,
                      color_discrete_sequence=['#738678'],
                  labels={'year': 'Year', 'co2': 'CO₂  (million tonnes)','co2_per_capita': 'CO₂ Per Capita (tonnes)'})
    fig_co2.update_layout(xaxis=dict(showgrid=True), yaxis=dict(showgrid=True))
    st.plotly_chart(fig_co2, use_container_width=True)


# 3. Country-Level Time Series
elif section == "Country Trends":
    

    countries = st.multiselect("Select Countries", df['country'].unique(), default=["United States", "China", "India"])
    
    st.subheader("Country-Level Emissions")
    
    palette = px.colors.sample_colorscale(PX_CONTINUOUS, len(countries))

    fig = px.line(
        df[df['country'].isin(countries)],
        x='year', y=metric,
        color='country',
        color_discrete_sequence=palette,
        labels={'year': 'Year',
                'co2': 'CO₂ (million tonnes)',
                'co2_per_capita': 'CO₂ Per Capita (tonnes)'},
        template='plotly_white'
    )
    st.plotly_chart(fig, use_container_width=True)

#4 Interactive Choropleth Map
elif section == "Country Trends with Interactive Map":
    st.subheader(f"Emissions in {selected_year}")
  
    map_data = df[df['year'] == selected_year]


    fig = px.choropleth(
        map_data,
        locations="country",
        locationmode="country names",
        color=metric,
        labels={'co2': 'CO₂  (million tonnes)', 'co2_per_capita': 'CO₂ Per Capita (tonnes)'},
        hover_name="country",
        color_continuous_scale=PX_CONTINUOUS,
        template='plotly_white'
        #title=f"Emissions in {selected_year}"
    )
    st.plotly_chart(fig, use_container_width=True)

#5 Per Capita Impact and Equity Analysis
elif section == "Per Capita Impact":
    st.subheader("Per Capita Impact and Equity Analysis")

    # List of excluded countries
    excluded_countries = [
        'Africa','Africa (GCP)', 'Asia', 'Asia (GCP)', 'Asia (excl. China and India)', 'Central America (GCP)', 'Europe',
        'Europe (GCP)', 'Europe (excl. EU-27)', 'Europe (excl. EU-28)', 'European Union (27)', 'European Union (28)',
        'High-income countries', 'International aviation', 'International shipping', 'International transport',
        'Kuwaiti Oil Fires', 'Kuwaiti Oil Fires (GCP)', 'Least developed countries (Jones et al.)', 'Low-income countries',
        'Lower-middle-income countries', 'Middle East (GCP)', 'Non-OECD (GCP)', 'North America', 'North America (GCP)',
        'North America (excl. USA)','South America', 'OECD (GCP)', 'OECD (Jones et al.)', 'Oceania (GCP)', 'Ryukyu Islands (GCP)',
        'South America (GCP)', 'Upper-middle-income countries', 'World'
    ]

        # Filter by year and exclude countries
    filtered_df = df[(df['year'] == selected_year) & (~df['country'].isin(excluded_countries))]

    # Top 10 by CO₂ per capita
    top10 = filtered_df.sort_values(by='co2_per_capita', ascending=False).head(10)

    # Bar chart
    fig = px.bar(
        top10,
        x='country',
        y='co2_per_capita',
        color_discrete_sequence=['#738678'],
        title=f"Top 10 Countries by CO₂ Per Capita in {selected_year}",
        labels={'co2_per_capita': 'CO₂ per Capita (tonnes)', 'country': 'Country'}
    )
    fig.update_layout(xaxis=dict(showgrid=True), yaxis=dict(showgrid=True))

    st.plotly_chart(fig, use_container_width=True)


# 5. Contributions to Global Warming 
elif section == "Emissions and Temperature":
    st.subheader(f"Share of Global Temperature Change from GHGs by Country - {selected_year}")


    # Excluded countries (aggregates and regions)
    excluded_countries = [
        'Africa','Africa (GCP)', 'Asia', 'Asia (GCP)', 'Asia (excl. China and India)', 'Central America (GCP)', 'Europe',
        'Europe (GCP)', 'Europe (excl. EU-27)', 'Europe (excl. EU-28)', 'European Union (27)', 'European Union (28)',
        'High-income countries', 'International aviation', 'International shipping', 'International transport',
        'Kuwaiti Oil Fires', 'Kuwaiti Oil Fires (GCP)', 'Least developed countries (Jones et al.)', 'Low-income countries',
        'Lower-middle-income countries', 'Middle East (GCP)', 'Non-OECD (GCP)', 'North America', 'North America (GCP)',
        'North America (excl. USA)', 'South America','OECD (GCP)', 'OECD (Jones et al.)', 'Oceania (GCP)', 'Ryukyu Islands (GCP)',
        'South America (GCP)', 'Upper-middle-income countries', 'World'
    ]

    # Filter by year and exclude selected countries
    filtered_df = df[
        (df['year'] == selected_year) & (~df['country'].isin(excluded_countries))
    ]

    # Top and Bottom 20 countries
    top20 = filtered_df.sort_values(by="share_of_temperature_change_from_ghg", ascending=False).head(20)
    bottom20 = filtered_df.sort_values(by="share_of_temperature_change_from_ghg", ascending=True).head(20)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<h3 style='text-align:left;margin-left: 150px'>Top 20 Countries</h3>",
        unsafe_allow_html=True)
        fig_col1 = px.bar(
            top20.sort_values(by="share_of_temperature_change_from_ghg"),
            x='share_of_temperature_change_from_ghg',
            y='country',
            color_discrete_sequence=['#738678'],
            orientation='h',
            labels={'share_of_temperature_change_from_ghg': 'Share (%)', 'country': 'Country'}
        )
        fig_col1.update_layout(
            height=600,
            xaxis=dict(title='Share (%)', showgrid=True),
            yaxis=dict(categoryorder='total ascending', automargin=True),
            margin=dict(l=150, r=20, t=40, b=40)
        )
        st.plotly_chart(fig_col1, use_container_width=True)

    with col2:
        st.markdown("<h3 style='text-align:right;margin-right: 70px'>Bottom 20 Countries</h3>",
        unsafe_allow_html=True)
        fig_col2 = px.bar(
            bottom20.sort_values(by="share_of_temperature_change_from_ghg"),
            x='share_of_temperature_change_from_ghg',
            y='country',
            color_discrete_sequence=['#738678'],
            orientation='h',
            labels={'share_of_temperature_change_from_ghg': 'Share (%)', 'country': 'Country'}
        )
        fig_col2.update_layout(
            height=600,
            xaxis=dict(title='Share (%)', showgrid=True),
            yaxis=dict(categoryorder='total ascending', automargin=True),
            margin=dict(l=150, r=20, t=40, b=40)
        )
        st.plotly_chart(fig_col2, use_container_width=True)

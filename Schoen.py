import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

# Replace this with your actual CSV file URL from GitHub (must be the *raw* link!)
CSV_URL = "https://raw.githubusercontent.com/groot023/Streamlit/main/exclusieve_schoenen_verkoop_met_locatie.csv"

# Load data
@st.cache_data
def load_data(url):
    return pd.read_csv(url)

df = load_data(CSV_URL)

# App Title
st.title("👟 Exclusieve Schoenen Dashboard")

# Tabs
tab1, tab2 = st.tabs(["📊 Bar Chart", "🥧 Land Distribution"])

# ---------------- TAB 1: Bar Chart ----------------
with tab1:
    st.subheader("Dataset Overview")
    st.write(df.head())

    st.sidebar.header("🔍 Filter Data")

    if 'prijs' in df.columns and 'merk' in df.columns:
        categories = df['merk'].unique()
        selected_categories = st.sidebar.multiselect("Select Merken", categories, default=categories)

        filtered_df = df[df['merk'].isin(selected_categories)]

        st.subheader("💸 Prijs per Merk")
        chart = alt.Chart(filtered_df).mark_bar().encode(
            x='merk:N',
            y='prijs:Q',
            tooltip=['merk', 'prijs']
        ).properties(width=700, height=400)

        st.altair_chart(chart, use_container_width=True)
    else:
        st.error("Dataset must contain 'merk' and 'prijs' columns to render the chart.")

# ---------------- TAB 2: Pie Chart ----------------
with tab2:
    st.subheader("🌍 distribution per country")

    if 'land' in df.columns:
        land_counts = df['land'].value_counts().reset_index()
        land_counts.columns = ['land', 'aantal']

        pie_chart = px.pie(
            land_counts,
            names='land',
            values='aantal',
            title="Aantal verkopen per land",
            color_discrete_sequence=px.colors.sequential.RdBu
        )

        st.plotly_chart(pie_chart, use_container_width=True)
    else:
        st.warning("De kolom 'land' bestaat niet in de dataset.")

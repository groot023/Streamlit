import streamlit as st
import pandas as pd
import altair as alt

# Load local CSV (you can change this to the raw GitHub link if needed)
@st.cache_data
def load_data():
    df = pd.read_csv('exclusieve_schoenen_verkoop_met_locatie.csv')
    df['aankoopdatum'] = pd.to_datetime(df['aankoopdatum'], errors='coerce')  # Ensure proper date format
    return df

df = load_data()

# App Title
st.title("📊 First Test App in Streamlit")

# Tabs
tab1, tab2 = st.tabs(["📦 Bar Chart", "📈 Line Chart Over Time"])

# ------------- TAB 1: Bar Chart -------------
with tab1:
    st.subheader("Dataset Overview")
    st.write(df.head())

    st.sidebar.header("🔍 Filter Data")

    if 'prijs' in df.columns and 'merk' in df.columns:
        categories = df['merk'].unique()
        selected_categories = st.sidebar.multiselect("Select Categories", categories, default=categories)

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

# ------------- TAB 2: Line Chart -------------
with tab2:
    st.subheader("📈 Prijsontwikkeling over Tijd")

    if {'aankoopdatum', 'prijs', 'merk'}.issubset(df.columns):
        df_line = df.dropna(subset=['aankoopdatum', 'prijs', 'merk'])

        line_chart = alt.Chart(df_line).mark_line().encode(
            x='aankoopdatum:T',
            y='prijs:Q',
            color='merk:N',
            tooltip=['aankoopdatum', 'merk', 'prijs']
        ).properties(width=800, height=400)

        st.altair_chart(line_chart, use_container_width=True)
    else:
        st.warning("De kolommen 'aankoopdatum', 'prijs' en 'merk' moeten aanwezig zijn in de dataset.")

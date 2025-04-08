import streamlit as st
import pandas as pd
import altair as alt

# Replace this with your actual CSV file URL from GitHub
CSV_URL = "https://github.com/groot023/Streamlit/blob/main/exclusieve_schoenen_verkoop_met_locatie.csv"

# Load data
@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    return df

df = load_data(CSV_URL)

# App Title
st.title("📊 Interactive Bar Chart App")

# Check if the dataset has expected columns
st.subheader("Dataset Overview")
st.write(df.head())

# Sidebar filter pane
st.sidebar.header("🔍 Filter Data")

# Example: Assume the dataset has 'Category' and 'Value' columns
if 'Category' in df.columns and 'Value' in df.columns:

    # Unique categories for filtering
    categories = df['Category'].unique()
    selected_categories = st.sidebar.multiselect("Select Categories", categories, default=categories)

    # Filter the data
    filtered_df = df[df['Category'].isin(selected_categories)]

    # Show bar chart
    st.subheader("Bar Chart")
    chart = alt.Chart(filtered_df).mark_bar().encode(
        x='Category:N',
        y='Value:Q',
        tooltip=['Category', 'Value']
    ).properties(width=700, height=400)

    st.altair_chart(chart, use_container_width=True)
else:
    st.error("Dataset must contain 'Category' and 'Value' columns to render the chart.")


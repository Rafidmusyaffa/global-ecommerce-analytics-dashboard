import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.title("Global E-Commerce 3D Analytics Dashboard")

# Load data
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "processed" / "cleaned_superstore.csv"
df = pd.read_csv(DATA_PATH)

# Sidebar filters
st.sidebar.header("Filters")

category = st.sidebar.selectbox(
    "Select Category",
    df["Category"].unique()
)

segment = st.sidebar.selectbox(
    "Select Segment",
    df["Segment"].unique()
)

# Filter data
filtered = df[
    (df["Category"] == category) &
    (df["Segment"] == segment)
]

# KPI FIRST
col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"${filtered['Sales'].sum():,.0f}")
col2.metric("Total Profit", f"${filtered['Profit'].sum():,.0f}")
col3.metric("Avg Discount", f"{filtered['Discount'].mean():.2%}")

# ⚠️ check if empty
if filtered.empty:
    st.warning("No data available for selected filters")
else:
    fig = px.scatter_3d(
        filtered,
        x="Discount",
        y="Sales",
        z="Profit",
        color="Ship Mode",
        size="Sales",
        title="3D Profit Analysis"
    )

    st.plotly_chart(fig, use_container_width=True)

# AI Insight
st.subheader("AI Insights")

best_category = df.groupby("Category")["Profit"].sum().idxmax()
worst_category = df.groupby("Category")["Profit"].sum().idxmin()

st.write(f"Highest Profit Category: {best_category}")
st.write(f"Lowest Profit Category: {worst_category}")
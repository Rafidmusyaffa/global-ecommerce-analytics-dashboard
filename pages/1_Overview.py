import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(layout="wide")

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "processed" / "cleaned_superstore.csv"

df = pd.read_csv(DATA_PATH)

st.title("📊 Executive Overview")

# Sidebar KPIs
st.sidebar.header("📌 Global KPIs")
st.sidebar.metric("💰 Total Sales", f"${df['Sales'].sum():,.0f}")
st.sidebar.metric("📈 Total Profit", f"${df['Profit'].sum():,.0f}")
st.sidebar.metric("📦 Orders", len(df))

# Main KPIs
col1, col2, col3, col4 = st.columns(4)

col1.metric("Revenue", f"${df['Sales'].sum():,.0f}")
col2.metric("Profit", f"${df['Profit'].sum():,.0f}")
col3.metric("Avg Discount", f"{df['Discount'].mean():.2%}")
col4.metric("Orders", len(df))

st.divider()

st.subheader("📈 Profit by Category")
st.bar_chart(df.groupby("Category")["Profit"].sum())

# Download button
csv = df.to_csv(index=False)

st.download_button(
    "⬇️ Download Dataset",
    csv,
    "ecommerce_data.csv",
    "text/csv"
)
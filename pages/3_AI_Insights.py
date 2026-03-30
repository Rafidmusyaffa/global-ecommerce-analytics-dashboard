import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(layout="wide")

st.title("🤖 AI Business Insights")

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "processed" / "cleaned_superstore.csv"

df = pd.read_csv(DATA_PATH)

best = df.groupby("Category")["Profit"].sum().idxmax()
worst = df.groupby("Category")["Profit"].sum().idxmin()

col1, col2 = st.columns(2)

col1.success(f"🏆 Best Category: {best}")
col2.error(f"⚠️ Worst Category: {worst}")

st.divider()

st.subheader("📊 Sales by Region")
st.bar_chart(df.groupby("Region")["Sales"].sum())

st.subheader("📉 Discount Impact")
st.line_chart(df.sort_values("Discount")["Profit"])
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(layout="wide")

st.title("🌐 3D Business Analytics")

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "processed" / "cleaned_superstore.csv"

df = pd.read_csv(DATA_PATH)

category = st.sidebar.selectbox("Category", df["Category"].unique())

filtered = df[df["Category"] == category]

fig = px.scatter_3d(
    filtered,
    x="Discount",
    y="Sales",
    z="Profit",
    color="Segment",
    size="Sales",
    animation_frame="Region"
)

fig.update_layout(
    margin=dict(l=0, r=0, t=40, b=0)
)

st.plotly_chart(fig, use_container_width=True)
import streamlit as st
import plotly.express as px
from app_ui import load_data, apply_theme, sidebar_snapshot, render_metric_card, section_header

st.set_page_config(page_title="Overview", page_icon="📊", layout="wide")
df = load_data()
dark = apply_theme()
sidebar_snapshot(df, "Overview Snapshot")

section_header(
    "📊 Executive Overview",
    "High-level business performance across revenue, profit, discount behavior, and category mix."
)

k1, k2, k3, k4 = st.columns(4)

with k1:
    render_metric_card("💰 Total Sales", f"${df['Sales'].sum():,.0f}")

with k2:
    render_metric_card("📈 Total Profit", f"${df['Profit'].sum():,.0f}")

with k3:
    render_metric_card("🏷️ Avg Discount", f"{df['Discount'].mean():.2%}")

with k4:
    render_metric_card("🧾 Orders", f"{len(df):,}")

st.write("")

left, right = st.columns(2)

with left:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Profit by Category</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Which product groups contribute the most profit.</div>', unsafe_allow_html=True)

    fig1 = px.bar(
        df.groupby("Category")["Profit"].sum().reset_index(),
        x="Category",
        y="Profit",
        color="Category",
        text_auto=True,
        template="plotly_dark" if dark else "plotly_white"
    )
    fig1.update_layout(height=430, margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Sales by Region</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Regional performance across the business.</div>', unsafe_allow_html=True)

    fig2 = px.bar(
        df.groupby("Region")["Sales"].sum().reset_index(),
        x="Region",
        y="Sales",
        color="Region",
        text_auto=True,
        template="plotly_dark" if dark else "plotly_white"
    )
    fig2.update_layout(height=430, margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.write("")

st.markdown('<div class="chart-card">', unsafe_allow_html=True)
st.markdown('<div class="section-heading">Download</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">Export the full cleaned dataset for reporting or analysis.</div>', unsafe_allow_html=True)

csv = df.to_csv(index=False)
st.download_button(
    "⬇️ Download Full Dataset",
    data=csv,
    file_name="cleaned_superstore_full.csv",
    mime="text/csv",
    use_container_width=True,
)

st.markdown('</div>', unsafe_allow_html=True)

st.write("")

st.markdown('<div class="chart-card">', unsafe_allow_html=True)
st.markdown('<div class="section-heading">Featured Visual</div>', unsafe_allow_html=True)
st.image("images/top-10-products-by-sales.png", caption="Top Products by Sales", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)
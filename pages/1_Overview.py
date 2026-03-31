import streamlit as st
import plotly.express as px
from app_ui import load_data, apply_theme, sidebar_snapshot, render_metric_card, section_header, IMG_DIR, render_image_card

st.set_page_config(page_title="Overview", page_icon="📊", layout="wide")

df = load_data()
dark = apply_theme()
sidebar_snapshot(df, "Overview Snapshot")

section_header(
    "📊 Executive Overview",
    "High-level business performance across revenue, profit, discount behavior, and category mix.",
)

st.markdown('<div class="floating-kpi">', unsafe_allow_html=True)
k1, k2, k3, k4 = st.columns(4)

with k1:
    render_metric_card("💰 Total Sales", f"${df['Sales'].sum():,.0f}" if "Sales" in df.columns else "N/A")
with k2:
    render_metric_card("📈 Total Profit", f"${df['Profit'].sum():,.0f}" if "Profit" in df.columns else "N/A")
with k3:
    render_metric_card("🏷️ Avg Discount", f"{df['Discount'].mean():.2%}" if "Discount" in df.columns else "N/A")
with k4:
    render_metric_card("🧾 Orders", f"{len(df):,}")

st.markdown('</div>', unsafe_allow_html=True)
st.write("")

left, right = st.columns(2)

with left:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Profit by Category</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Which product groups contribute the most profit.</div>', unsafe_allow_html=True)

    if "Category" in df.columns and "Profit" in df.columns:
        cat = df.groupby("Category", as_index=False)["Profit"].sum()
        fig1 = px.bar(
            cat,
            x="Category",
            y="Profit",
            color="Category",
            template="plotly_dark" if dark else "plotly_white",
        )
        fig1.update_layout(height=430, margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.info("Category or Profit column not found.")
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Sales by Region</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Regional performance across the business.</div>', unsafe_allow_html=True)

    if "Region" in df.columns and "Sales" in df.columns:
        reg = df.groupby("Region", as_index=False)["Sales"].sum()
        fig2 = px.bar(
            reg,
            x="Region",
            y="Sales",
            color="Region",
            template="plotly_dark" if dark else "plotly_white",
        )
        fig2.update_layout(height=430, margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Region or Sales column not found.")
    st.markdown('</div>', unsafe_allow_html=True)

st.write("")

st.markdown('<div class="chart-card">', unsafe_allow_html=True)
st.markdown('<div class="section-heading">Featured Visuals</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">A richer visual story for the overview page.</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

g1, g2 = st.columns(2)
g3, g4 = st.columns(2)
g5, g6 = st.columns(2)

with g1:
    render_image_card(
        IMG_DIR / "global-sales-distribution.png",
        "Global Sales Distribution",
        "A broad location view that helps you understand where the business is strongest.",
        "Great opening visual for executives.",
    )

with g2:
    render_image_card(
        IMG_DIR / "global-sales-trend-over-time.png",
        "Global Sales Trend Over Time",
        "This visual highlights the overall growth path and changes over time.",
        "Useful for story-driven presentations.",
    )

with g3:
    render_image_card(
        IMG_DIR / "monthly-sales-heatmap.png",
        "Monthly Sales Heatmap",
        "Makes seasonality patterns and monthly changes easy to scan.",
        "Very readable on mobile screens.",
    )

with g4:
    render_image_card(
        IMG_DIR / "sales-by-region.png",
        "Sales by Region",
        "A clear comparison across regions for fast executive review.",
        "Helpful for geographic targeting.",
    )

with g5:
    render_image_card(
        IMG_DIR / "top-10-products-by-sales.png",
        "Top 10 Products by Sales",
        "Shows the most important products in your revenue mix.",
        "Good for operational prioritization.",
    )

with g6:
    render_image_card(
        IMG_DIR / "product-profitability-analysis.png",
        "Product Profitability Analysis",
        "Compares product performance from a margin perspective.",
        "A strong visual for decision-making.",
    )

st.write("")

st.markdown('<div class="chart-card">', unsafe_allow_html=True)
st.markdown('<div class="section-heading">Download</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">Export the full cleaned dataset for reporting or analysis.</div>', unsafe_allow_html=True)

csv = df.to_csv(index=False).encode("utf-8")
st.download_button(
    "⬇️ Download Full Dataset",
    data=csv,
    file_name="cleaned_superstore_full.csv",
    mime="text/csv",
    use_container_width=True,
)

st.markdown('</div>', unsafe_allow_html=True)
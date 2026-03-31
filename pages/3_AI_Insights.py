import streamlit as st
import pandas as pd
import plotly.express as px
from app_ui import load_data, apply_theme, sidebar_snapshot, section_header

st.set_page_config(page_title="AI Insights", page_icon="🤖", layout="wide")
df = load_data()
dark = apply_theme()
sidebar_snapshot(df, "Insight Snapshot")

section_header(
    "🤖 AI Business Insights",
    "Automatically generated business takeaways from your dataset."
)

profit_by_category = df.groupby("Category")["Profit"].sum().sort_values(ascending=False)
sales_by_region = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)
sales_by_segment = df.groupby("Segment")["Sales"].sum().sort_values(ascending=False) if "Segment" in df.columns else None

best_category = profit_by_category.index[0]
worst_category = profit_by_category.index[-1]
best_region = sales_by_region.index[0]
best_segment = sales_by_segment.index[0] if sales_by_segment is not None else "N/A"

c1, c2, c3, c4 = st.columns(4)

from app_ui import render_metric_card

with c1:
    render_metric_card("🏆 Best Category", best_category)
with c2:
    render_metric_card("⚠️ Weakest Category", worst_category)
with c3:
    render_metric_card("🌍 Best Region", best_region)
with c4:
    render_metric_card("🧑‍💼 Best Segment", best_segment)

st.write("")

avg_discount = df["Discount"].mean()
profit_total = df["Profit"].sum()

insights = [
    f"Highest profit category: {best_category}.",
    f"Lowest profit category: {worst_category}.",
    f"Top region by sales: {best_region}.",
    f"Average discount level: {avg_discount:.2%}.",
]

if "Discount" in df.columns:
    high_discount = df[df["Discount"] >= df["Discount"].quantile(0.75)]
    if not high_discount.empty and high_discount["Profit"].mean() < df["Profit"].mean():
        insights.append("High-discount transactions appear to reduce average profitability.")

if sales_by_segment is not None:
    insights.append(f"Top segment by sales: {best_segment}.")

st.markdown('<div class="chart-card">', unsafe_allow_html=True)
st.subheader("AI Summary")
st.text_area("Copyable insight summary", "\n".join(f"- {x}" for x in insights), height=220)
st.markdown('</div>', unsafe_allow_html=True)

left, right = st.columns(2)

with left:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.subheader("Category Profit Ranking")
    fig1 = px.bar(
        profit_by_category.reset_index(),
        x="Category",
        y="Profit",
        color="Category",
        text_auto=True,
        template="plotly_dark" if dark else "plotly_white",
    )
    fig1.update_layout(height=420, margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.subheader("Region Sales Ranking")
    fig2 = px.bar(
        sales_by_region.reset_index(),
        x="Region",
        y="Sales",
        color="Region",
        text_auto=True,
        template="plotly_dark" if dark else "plotly_white",
    )
    fig2.update_layout(height=420, margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.write("")

if profit_total > 0:
    st.success("Overall business is profitable. Keep optimizing discount strategy and invest more in strong categories and regions.")
else:
    st.warning("Overall profit is negative. Review pricing, discounts, and category mix.")

st.markdown(
    """
    <div class="chart-card">
    <b>Next action ideas</b><br><br>
    1. Reduce deep discounts on low-margin categories.<br>
    2. Focus marketing spend on the strongest region.<br>
    3. Review shipping efficiency for low-profit segments.<br>
    4. Promote the best category with premium placement.
    </div>
    """,
    unsafe_allow_html=True,
)
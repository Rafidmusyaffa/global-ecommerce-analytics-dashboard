import streamlit as st
import pandas as pd
import plotly.express as px

from app_ui import (
    load_data,
    apply_theme,
    sidebar_snapshot,
    section_header,
    render_metric_card,
    render_image_card,
    IMG_DIR,
)

st.set_page_config(page_title="AI Insights", page_icon="🤖", layout="wide")

df = load_data()
dark = apply_theme()
sidebar_snapshot(df, "Insight Snapshot")

section_header(
    "🤖 AI Business Insights",
    "A data-driven executive summary with key learnings, risks, and next-step recommendations.",
)

required_cols = ["Category", "Region", "Sales", "Profit"]
for col in required_cols:
    if col not in df.columns:
        st.error(f"Missing required column: {col}")
        st.stop()

# Optional columns
has_segment = "Segment" in df.columns
has_discount = "Discount" in df.columns
has_product = "Product Name" in df.columns or "Product" in df.columns
has_customer = "Customer Name" in df.columns or "Customer" in df.columns
has_date = "Order Date" in df.columns

product_col = "Product Name" if "Product Name" in df.columns else ("Product" if "Product" in df.columns else None)
customer_col = "Customer Name" if "Customer Name" in df.columns else ("Customer" if "Customer" in df.columns else None)

# Core metrics
sales_total = float(df["Sales"].sum())
profit_total = float(df["Profit"].sum())
avg_discount = float(df["Discount"].mean()) if has_discount else None
profit_margin = (profit_total / sales_total) if sales_total != 0 else 0

profit_by_category = df.groupby("Category")["Profit"].sum().sort_values(ascending=False)
sales_by_region = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)
sales_by_segment = df.groupby("Segment")["Sales"].sum().sort_values(ascending=False) if has_segment else None

best_category = profit_by_category.index[0] if not profit_by_category.empty else "N/A"
worst_category = profit_by_category.index[-1] if not profit_by_category.empty else "N/A"
best_region = sales_by_region.index[0] if not sales_by_region.empty else "N/A"
best_segment = sales_by_segment.index[0] if sales_by_segment is not None and not sales_by_segment.empty else "N/A"

# Concentration analysis
top_category_share = 0
top_region_share = 0

if not profit_by_category.empty:
    top_category_share = float(profit_by_category.iloc[0] / profit_by_category.sum()) if profit_by_category.sum() != 0 else 0

if not sales_by_region.empty:
    top_region_share = float(sales_by_region.iloc[0] / sales_by_region.sum()) if sales_by_region.sum() != 0 else 0

# Discount impact
discount_note = "Discount column not available."
high_discount_profit = None
low_discount_profit = None

if has_discount:
    high_discount = df[df["Discount"] >= df["Discount"].quantile(0.75)]
    low_discount = df[df["Discount"] < df["Discount"].quantile(0.75)]

    if not high_discount.empty:
        high_discount_profit = float(high_discount["Profit"].mean())
    if not low_discount.empty:
        low_discount_profit = float(low_discount["Profit"].mean())

    if high_discount_profit is not None and low_discount_profit is not None:
        if high_discount_profit < low_discount_profit:
            discount_note = "Higher discounts are associated with lower average profit."
        else:
            discount_note = "Higher discounts do not appear to damage average profit in this dataset."

# Monthly trend if date exists
monthly_df = None
trend_note = "Order date column not available, so time trend analysis is limited."
trend_change = None

if has_date:
    temp = df.copy()
    temp["Order Date"] = pd.to_datetime(temp["Order Date"], errors="coerce")
    temp = temp.dropna(subset=["Order Date"])
    if not temp.empty:
        monthly_df = temp.assign(Month=temp["Order Date"].dt.to_period("M").dt.to_timestamp())
        monthly_sales = monthly_df.groupby("Month", as_index=False)["Sales"].sum().sort_values("Month")

        if len(monthly_sales) >= 6:
            recent_3 = monthly_sales.tail(3)["Sales"].mean()
            prev_3 = monthly_sales.iloc[-6:-3]["Sales"].mean()
            if prev_3 != 0:
                trend_change = (recent_3 - prev_3) / prev_3
                trend_note = (
                    "Recent sales momentum is stronger than the previous period."
                    if trend_change > 0
                    else "Recent sales momentum is weaker than the previous period."
                )
        elif len(monthly_sales) > 1:
            trend_note = "Time trend is available, but not enough data for a strong momentum comparison."

# Customer/product leaders if available
top_product = None
top_customer = None

if product_col:
    top_product_series = df.groupby(product_col)["Sales"].sum().sort_values(ascending=False)
    if not top_product_series.empty:
        top_product = top_product_series.index[0]

if customer_col:
    top_customer_series = df.groupby(customer_col)["Sales"].sum().sort_values(ascending=False)
    if not top_customer_series.empty:
        top_customer = top_customer_series.index[0]

# Insight generation
insights = []
recommendations = []
what_we_learned = []

insights.append(f"Best profit category: {best_category}.")
insights.append(f"Weakest profit category: {worst_category}.")
insights.append(f"Best sales region: {best_region}.")
if best_segment != "N/A":
    insights.append(f"Best sales segment: {best_segment}.")
if top_product:
    insights.append(f"Top product by sales: {top_product}.")
if top_customer:
    insights.append(f"Top customer by sales: {top_customer}.")
if avg_discount is not None:
    insights.append(f"Average discount level: {avg_discount:.2%}.")
insights.append(discount_note)
insights.append(trend_note)

what_we_learned.append(
    f"The business is generating total sales of ${sales_total:,.0f} with total profit of ${profit_total:,.0f}."
)
what_we_learned.append(
    f"Profit margin is about {profit_margin:.2%}, which helps show whether revenue is being converted into healthy earnings."
)
what_we_learned.append(
    f"The strongest category contributes {top_category_share:.2%} of total category profit, which shows how concentrated profit is."
)
what_we_learned.append(
    f"The strongest region contributes {top_region_share:.2%} of total regional sales, which shows where the market is strongest."
)

if has_discount and high_discount_profit is not None and low_discount_profit is not None:
    what_we_learned.append(
        f"High-discount orders average ${high_discount_profit:,.2f} profit, while lower-discount orders average ${low_discount_profit:,.2f} profit."
    )

if profit_margin < 0.10:
    recommendations.append("Improve margin control by reviewing pricing, shipping cost, and discount strategy.")
if has_discount and avg_discount is not None and avg_discount > 0.15:
    recommendations.append("Reduce deep discounting on low-margin products and focus promotions on healthier items.")
if top_category_share > 0.35:
    recommendations.append("Diversify profit generation so the business is not too dependent on one category.")
if top_region_share > 0.40:
    recommendations.append("Invest in the strongest region, but also build growth plans for weaker regions.")
if trend_change is not None and trend_change < 0:
    recommendations.append("Launch a recovery plan for recent sales slowdown through promotions or product mix updates.")
if best_segment != "N/A":
    recommendations.append("Use the best-performing segment as the primary target for marketing and upsell campaigns.")
if not recommendations:
    recommendations.append("Keep monitoring category mix, discount behavior, and regional performance to protect growth.")

# Executive summary paragraph
summary_lines = [
    f"The dataset shows total sales of ${sales_total:,.0f} and total profit of ${profit_total:,.0f}.",
    f"The best-performing category is {best_category}, while {worst_category} needs more attention.",
    f"The strongest region is {best_region}, and the business margin is {profit_margin:.2%}.",
]

if best_segment != "N/A":
    summary_lines.append(f"The top segment by sales is {best_segment}.")
if top_product:
    summary_lines.append(f"The top product by sales is {top_product}.")
if top_customer:
    summary_lines.append(f"The top customer by sales is {top_customer}.")
if has_discount and avg_discount is not None:
    summary_lines.append(f"Average discount is {avg_discount:.2%}, and {discount_note.lower()}")
if trend_change is not None:
    summary_lines.append(
        f"Recent momentum changed by {trend_change:.2%} compared with the previous comparable period."
    )

executive_summary = " ".join(summary_lines)

# KPI row
c1, c2, c3, c4 = st.columns(4)
with c1:
    render_metric_card("💰 Total Sales", f"${sales_total:,.0f}")
with c2:
    render_metric_card("📈 Total Profit", f"${profit_total:,.0f}")
with c3:
    render_metric_card("🧮 Profit Margin", f"{profit_margin:.2%}")
with c4:
    render_metric_card("🌍 Best Region", best_region)

st.write("")

# Executive summary card
st.markdown('<div class="chart-card">', unsafe_allow_html=True)
st.markdown('<div class="section-heading">Executive AI Summary</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-sub">A data-driven narrative you can copy into reports, presentations, or portfolio notes.</div>',
    unsafe_allow_html=True,
)
st.text_area("Copyable executive summary", executive_summary, height=180)
st.markdown('</div>', unsafe_allow_html=True)

st.write("")

# Learned / Next steps / Risks
left, right = st.columns(2)

with left:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("#### What we learned")
    for item in what_we_learned:
        st.write(f"• {item}")
    st.markdown('</div>', unsafe_allow_html=True)

    st.write("")
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("#### Business strengths")
    st.write(f"• Strongest category: {best_category}")
    st.write(f"• Strongest region: {best_region}")
    if best_segment != "N/A":
        st.write(f"• Strongest segment: {best_segment}")
    if top_product:
        st.write(f"• Top product: {top_product}")
    if top_customer:
        st.write(f"• Top customer: {top_customer}")
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("#### What the company should do next")
    for i, item in enumerate(recommendations, start=1):
        st.write(f"{i}. {item}")
    st.markdown('</div>', unsafe_allow_html=True)

    st.write("")
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("#### Risk signals")
    if profit_margin < 0.10:
        st.warning("Profit margin is relatively low, so cost and pricing control matter more.")
    else:
        st.success("Profitability is healthy overall.")
    if has_discount and avg_discount is not None and avg_discount > 0.15:
        st.warning("Discount level is fairly high, so pricing pressure may be reducing earnings.")
    if top_category_share > 0.35:
        st.info("Profit is concentrated in one category, so diversification would reduce risk.")
    if top_region_share > 0.40:
        st.info("Sales are concentrated in one region, so expansion in other regions could help.")
    if trend_change is not None and trend_change < 0:
        st.warning("Recent momentum is weakening compared with the previous period.")
    st.markdown('</div>', unsafe_allow_html=True)

st.write("")

# Visual evidence
st.markdown('<div class="chart-card">', unsafe_allow_html=True)
st.markdown('<div class="section-heading">Supporting Analysis</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">These visuals help support the insights above.</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

v1, v2 = st.columns(2)
v3, v4 = st.columns(2)
v5, v6 = st.columns(2)

with v1:
    fig1 = px.bar(
        profit_by_category.reset_index(),
        x="Category",
        y="Profit",
        color="Category",
        title="Category Profit Ranking",
        template="plotly_dark" if dark else "plotly_white",
    )
    fig1.update_layout(height=380, margin=dict(l=0, r=0, t=45, b=0))
    st.plotly_chart(fig1, use_container_width=True)

with v2:
    fig2 = px.bar(
        sales_by_region.reset_index(),
        x="Region",
        y="Sales",
        color="Region",
        title="Region Sales Ranking",
        template="plotly_dark" if dark else "plotly_white",
    )
    fig2.update_layout(height=380, margin=dict(l=0, r=0, t=45, b=0))
    st.plotly_chart(fig2, use_container_width=True)

with v3:
    if sales_by_segment is not None:
        fig3 = px.bar(
            sales_by_segment.reset_index(),
            x="Segment",
            y="Sales",
            color="Segment",
            title="Segment Sales Ranking",
            template="plotly_dark" if dark else "plotly_white",
        )
        fig3.update_layout(height=380, margin=dict(l=0, r=0, t=45, b=0))
        st.plotly_chart(fig3, use_container_width=True)
    else:
        render_image_card(
            IMG_DIR / "sales-by-customer-segment.png",
            "Sales by Customer Segment",
            "A supportive image that shows segment performance clearly.",
            "If your dataset has no segment column, this visual still helps the page feel complete.",
        )

with v4:
    if has_discount:
        clean_df = df.copy()
        clean_df = clean_df.dropna(subset=["Discount"])

        # Create numeric bins safely
        clean_df["Discount Band"] = pd.cut(
            clean_df["Discount"],
            bins=4,
            labels=["Low", "Medium", "High", "Very High"]
        )

        discount_profit_df = (
            clean_df.groupby("Discount Band")["Profit"]
            .mean()
            .reset_index()
        )

        fig4 = px.bar(
            discount_profit_df,
            x="Discount Band",
            y="Profit",
            title="Average Profit by Discount Band",
            template="plotly_dark" if dark else "plotly_white",
        )

        fig4.update_layout(height=380, margin=dict(l=0, r=0, t=45, b=0))
        st.plotly_chart(fig4, use_container_width=True)

    else:
        render_image_card(
            IMG_DIR / "profit-margin-by-category.png",
            "Profit Margin by Category",
            "A visual support card for margin-focused analysis.",
            "Useful when discount data is not available.",
        )

with v5:
    render_image_card(
        IMG_DIR / "top-10-products-by-profit.png",
        "Top 10 Products by Profit",
        "Shows which products generate the strongest profitability.",
        "Great for portfolio storytelling.",
    )

with v6:
    render_image_card(
        IMG_DIR / "sales-forecast-prediction.png",
        "Sales Forecast Prediction",
        "Adds a forward-looking view to the insights page.",
        "Makes the dashboard feel more advanced and executive-ready.",
    )

st.write("")

# Downloadable summary
download_text = (
    "AI BUSINESS INSIGHTS\n\n"
    f"Executive Summary:\n{executive_summary}\n\n"
    "What We Learned:\n"
    + "\n".join(f"- {item}" for item in what_we_learned)
    + "\n\nNext Steps:\n"
    + "\n".join(f"- {item}" for item in recommendations)
)

st.markdown('<div class="chart-card">', unsafe_allow_html=True)
st.markdown('<div class="section-heading">Export Insights</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">Download the summary for reports, slides, or portfolio notes.</div>', unsafe_allow_html=True)

st.download_button(
    "⬇️ Download AI Summary",
    data=download_text,
    file_name="ai_business_insights.txt",
    mime="text/plain",
    use_container_width=True,
)
st.markdown('</div>', unsafe_allow_html=True)

st.write("")

if profit_total > 0:
    st.success(
        "Overall business is profitable. Keep improving margin quality, protecting strong categories, and expanding winning regions."
    )
else:
    st.warning(
        "Overall profit is negative. Review pricing, discounts, shipping cost, and category mix."
    )
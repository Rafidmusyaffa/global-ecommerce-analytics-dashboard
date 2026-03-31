import streamlit as st
from app_ui import apply_theme, IMG_DIR

st.set_page_config(
    page_title="Global E-Commerce Intelligence Platform",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.sidebar.title("Global E-Commerce")
theme_choice = st.sidebar.radio("Theme", ["🌙 Dark", "☀️ Light"], index=0)
st.session_state["dark_mode"] = theme_choice.startswith("🌙")
apply_theme()

st.title("🌍 Global E-Commerce Intelligence Platform")
st.caption("AI-powered business intelligence dashboard for executive storytelling and portfolio presentation.")

st.markdown('<div class="accent-line"></div>', unsafe_allow_html=True)

left, right = st.columns([1.15, 0.95], vertical_alignment="center")

with left:
    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-title">A premium dashboard for revenue, profit, and growth analysis.</div>
            <div class="hero-subtitle">
                Built for laptop and mobile, with executive KPI cards, 3D analytics, AI insights,
                polished navigation, and download-ready reporting views.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    c1, c2, c3 = st.columns(3)
    c1.metric("Pages", "3")
    c2.metric("Visuals", "20+")
    c3.metric("Live link", "Active")

    st.write("")
    st.markdown(
        """
        <div class="section-card">
            <span class="pill">KPI Cards</span>
            <span class="pill">3D Analytics</span>
            <span class="pill">AI Insights</span>
            <span class="pill">Download Button</span>
            <span class="pill">Responsive Layout</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

with right:
    st.image(
        IMG_DIR / "global-sales-distribution.png",
        caption="Global Sales Distribution",
        use_container_width=True,
    )

st.write("")
tab1, tab2 = st.tabs(["Featured Visuals", "Project Highlights"])

with tab1:
    a, b = st.columns(2)
    a.image(IMG_DIR / "sales-by-region.png", caption="Sales by Region", use_container_width=True)
    b.image(IMG_DIR / "sales-forecast-prediction.png", caption="Sales Forecast Prediction", use_container_width=True)

    c, d = st.columns(2)
    c.image(IMG_DIR / "top-10-products-by-sales.png", caption="Top Products by Sales", use_container_width=True)
    d.image(IMG_DIR / "product-profitability-analysis.png", caption="Product Profitability Analysis", use_container_width=True)

with tab2:
    st.markdown(
        """
        <div class="section-card">
        <b>What this dashboard shows</b><br><br>
        • Executive overview of total sales, profit, and discount behavior.<br>
        • Interactive 3D analytics with filters for category, segment, region, and shipping mode.<br>
        • AI insights that summarize the strongest and weakest performance areas.<br>
        • Downloadable data for reporting and portfolio use.<br>
        • A polished layout designed to feel like a real business product.
        </div>
        """,
        unsafe_allow_html=True,
    )
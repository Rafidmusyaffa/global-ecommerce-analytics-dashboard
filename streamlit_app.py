import streamlit as st
from app_ui import apply_theme, IMG_DIR, render_image_card, section_header

st.set_page_config(
    page_title="Global E-Commerce Intelligence Platform",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.sidebar.title("Global E-Commerce")
theme_choice = st.sidebar.radio("Theme", ["🌙 Dark", "☀️ Light"], index=0)
st.session_state["dark_mode"] = theme_choice.startswith("🌙")
dark = apply_theme()

st.title("🌍 Global E-Commerce Intelligence Platform")
st.caption("AI-powered business intelligence dashboard for executive storytelling and portfolio presentation.")

st.markdown('<div class="accent-line"></div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="chart-card">
        <div class="section-heading">Welcome</div>
        <div class="section-sub">
            This dashboard is built for desktop and mobile, with executive KPI cards,
            3D analytics, AI insights, and downloadable reporting views.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Pages", "3")
c2.metric("Visuals", "20+")
c3.metric("Theme", "Dark / Light")
c4.metric("Device Ready", "Mobile + Desktop")

st.write("")

left, right = st.columns([1.15, 0.95], vertical_alignment="center")

with left:
    st.markdown(
        """
        <div class="chart-card">
            <div class="hero-title" style="font-size: clamp(1.8rem, 2.6vw, 3rem);">
                A premium dashboard for revenue, profit, and growth analysis.
            </div>
            <div class="hero-subtitle">
                Built for laptop and mobile, with executive KPI cards, 3D analytics, AI insights,
                polished navigation, and download-ready reporting views.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    st.markdown(
        """
        <div class="chart-card">
            <span class="mini-pill">KPI Cards</span>
            <span class="mini-pill">3D Analytics</span>
            <span class="mini-pill">AI Insights</span>
            <span class="mini-pill">Download Button</span>
            <span class="mini-pill">Responsive Layout</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

with right:
    hero_img = IMG_DIR / "global-sales-distribution.png"
    if hero_img.exists():
        st.image(hero_img, caption="Global Sales Distribution", use_container_width=True)
    else:
        st.info("Add `images/global-sales-distribution.png` to show the hero image.")

st.write("")

tab1, tab2, tab3 = st.tabs(["Featured Visuals", "More Insights", "Project Highlights"])

with tab1:
    r1c1, r1c2 = st.columns(2)
    r2c1, r2c2 = st.columns(2)
    r3c1, r3c2 = st.columns(2)

    render_image_card(
        IMG_DIR / "global-sales-trend-over-time.png",
        "Global Sales Trend Over Time",
        "Shows the direction of total sales across time and highlights stronger growth periods.",
        "Useful for executive trend storytelling.",
    )
    render_image_card(
        IMG_DIR / "sales-by-region.png",
        "Sales by Region",
        "A clear regional performance view that helps identify strong and weak markets.",
        "Great for geographic analysis.",
    )

    render_image_card(
        IMG_DIR / "sales-by-customer-segment.png",
        "Sales by Customer Segment",
        "Compares performance across customer groups so the business can prioritize the right audience.",
        "Good for marketing and segmentation.",
    )
    render_image_card(
        IMG_DIR / "top-10-products-by-sales.png",
        "Top 10 Products by Sales",
        "Highlights your biggest revenue drivers and the products that deserve more visibility.",
        "Helps with merchandising and promotions.",
    )

    render_image_card(
        IMG_DIR / "product-profitability-analysis.png",
        "Product Profitability Analysis",
        "Balances sales with margin so you can see which products are actually worth scaling.",
        "A strong portfolio visual.",
    )
    render_image_card(
        IMG_DIR / "profit-margin-by-category.png",
        "Profit Margin by Category",
        "Shows which categories deliver the healthiest margin and which ones need review.",
        "Excellent for margin strategy.",
    )

with tab2:
    section_header(
        "Visual Story Library",
        "More visuals for a larger, more attractive homepage experience.",
    )

    left, right = st.columns(2)

    with left:
        render_image_card(
            IMG_DIR / "monthly-sales-trend.png",
            "Monthly Sales Trend",
            "A month-by-month trend view that makes seasonal movement easy to spot.",
            "Useful for planning and forecasting.",
        )
        render_image_card(
            IMG_DIR / "sales-distribution-by-category.png",
            "Sales Distribution by Category",
            "Shows how sales are distributed across product categories at a glance.",
            "Great for quick category comparison.",
        )
        render_image_card(
            IMG_DIR / "top-10-countries-by-sales.png",
            "Top 10 Countries by Sales",
            "A market ranking view for international performance storytelling.",
            "Good for global expansion analysis.",
        )

    with right:
        render_image_card(
            IMG_DIR / "monthly-sales-heatmap.png",
            "Monthly Sales Heatmap",
            "A compact pattern view that makes strong and weak months stand out quickly.",
            "Very useful on mobile too.",
        )
        render_image_card(
            IMG_DIR / "top-10-customers-by-revenue.png",
            "Top 10 Customers by Revenue",
            "Shows your most valuable customers and where revenue concentration is highest.",
            "Great for customer strategy.",
        )
        render_image_card(
            IMG_DIR / "sales-forecast-prediction.png",
            "Sales Forecast Prediction",
            "A forward-looking visual for planning and executive discussion.",
            "Makes the page feel more advanced.",
        )

with tab3:
    st.markdown(
        """
        <div class="story-card">
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

    st.markdown(
        """
        <div class="story-card">
        <b>Design goal</b><br><br>
        Make the dashboard comfortable on phone and desktop, with larger image sections,
        cleaner spacing, and a premium analytics look.
        </div>
        """,
        unsafe_allow_html=True,
    )
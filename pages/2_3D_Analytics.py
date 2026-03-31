import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from app_ui import load_data, apply_theme, sidebar_snapshot, render_metric_card, section_header, IMG_DIR, render_image_card

st.set_page_config(page_title="3D Analytics", page_icon="🌐", layout="wide")

df = load_data()
dark = apply_theme()

section_header(
    "🌐 3D Analytics",
    "Interactive 3D exploration with category, segment, region, and ship-mode filters.",
)

st.sidebar.header("🎛️ Filters")

categories = sorted(df["Category"].dropna().unique().tolist()) if "Category" in df.columns else []
segments = sorted(df["Segment"].dropna().unique().tolist()) if "Segment" in df.columns else []
regions = sorted(df["Region"].dropna().unique().tolist()) if "Region" in df.columns else []
ship_modes = sorted(df["Ship Mode"].dropna().unique().tolist()) if "Ship Mode" in df.columns else []

with st.sidebar.expander("🎛️ Filters", expanded=False):
    selected_categories = st.multiselect("Category", categories, default=categories)
    selected_segments = st.multiselect("Segment", segments, default=segments)
    selected_regions = st.multiselect("Region", regions, default=regions)
    selected_ship_modes = st.multiselect("Ship Mode", ship_modes, default=ship_modes)

filtered = df.copy()

if selected_categories and "Category" in filtered.columns:
    filtered = filtered[filtered["Category"].isin(selected_categories)]
if selected_segments and "Segment" in filtered.columns:
    filtered = filtered[filtered["Segment"].isin(selected_segments)]
if selected_regions and "Region" in filtered.columns:
    filtered = filtered[filtered["Region"].isin(selected_regions)]
if selected_ship_modes and "Ship Mode" in filtered.columns:
    filtered = filtered[filtered["Ship Mode"].isin(selected_ship_modes)]

sidebar_snapshot(filtered, "Filtered Snapshot")

if filtered.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

c1, c2, c3, c4 = st.columns(4)
with c1:
    render_metric_card("Filtered Sales", f"${filtered['Sales'].sum():,.0f}" if "Sales" in filtered.columns else "N/A")
with c2:
    render_metric_card("Filtered Profit", f"${filtered['Profit'].sum():,.0f}" if "Profit" in filtered.columns else "N/A")
with c3:
    render_metric_card("Avg Discount", f"{filtered['Discount'].mean():.2%}" if "Discount" in filtered.columns else "N/A")
with c4:
    render_metric_card("Rows in View", f"{len(filtered):,}")

st.write("")

tab1, tab2, tab3 = st.tabs(["3D Scatter", "3D Surface", "Drilldown"])

with tab1:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)

    if all(col in filtered.columns for col in ["Discount", "Sales", "Profit"]):
        fig = px.scatter_3d(
            filtered,
            x="Discount",
            y="Sales",
            z="Profit",
            color="Segment" if "Segment" in filtered.columns else None,
            symbol="Category" if "Category" in filtered.columns else None,
            size="Sales",
            opacity=0.72,
            hover_data=[c for c in ["Category", "Segment", "Region", "Ship Mode"] if c in filtered.columns],
            title="3D Sales vs Profit vs Discount",
            template="plotly_dark" if dark else "plotly_white",
        )
        fig.update_layout(height=600, margin=dict(l=0, r=0, t=45, b=0))
        st.plotly_chart(fig, use_container_width=True, config={"responsive": True})
    else:
        st.info("Missing Discount, Sales, or Profit columns.")
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)

    if "Region" in filtered.columns and "Category" in filtered.columns and "Sales" in filtered.columns:
        pivot = filtered.pivot_table(
            values="Sales",
            index="Region",
            columns="Category",
            aggfunc="sum",
            fill_value=0,
        )

        if pivot.empty:
            st.info("Not enough data for the surface chart.")
        else:
            x_labels = list(pivot.columns)
            y_labels = list(pivot.index)

            surface = go.Figure(
                data=[
                    go.Surface(
                        z=pivot.values,
                        x=list(range(len(x_labels))),
                        y=list(range(len(y_labels))),
                        colorscale="Viridis",
                    )
                ]
            )

            surface.update_layout(
                template="plotly_dark" if dark else "plotly_white",
                title="3D Sales Surface: Region vs Category",
                height=600,
                margin=dict(l=0, r=0, t=45, b=0),
                scene=dict(
                    xaxis=dict(
                        title="Category",
                        tickmode="array",
                        tickvals=list(range(len(x_labels))),
                        ticktext=x_labels,
                    ),
                    yaxis=dict(
                        title="Region",
                        tickmode="array",
                        tickvals=list(range(len(y_labels))),
                        ticktext=y_labels,
                    ),
                    zaxis=dict(title="Sales"),
                ),
            )
            st.plotly_chart(surface, use_container_width=True, config={"responsive": True})
    else:
        st.info("Region, Category, or Sales column not found.")
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Drilldown Visual Story</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">This tab now shows images clearly on both desktop and mobile.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    d1, d2 = st.columns(2)
    d3, d4 = st.columns(2)
    d5, d6 = st.columns(2)

    with d1:
        render_image_card(
            IMG_DIR / "3d-sales-vs-profit-vs-discount-anaysis.png",
            "3D Sales vs Profit vs Discount",
            "Main 3D view for spotting trade-offs between discount, profit, and sales.",
            "This is the core drilldown visual.",
        )

    with d2:
        render_image_card(
            IMG_DIR / "3D-sales-surface-region-vs-category.png",
            "3D Sales Surface: Region vs Category",
            "A surface view that compares sales intensity across regions and categories.",
            "Great for pattern detection.",
        )

    with d3:
        render_image_card(
            IMG_DIR / "3D-sales-distribution-by-category-and-region.png",
            "3D Sales Distribution by Category and Region",
            "Shows how sales are distributed across major business dimensions.",
            "Good for strategic segmentation.",
        )

    with d4:
        render_image_card(
            IMG_DIR / "3D-monthly-category-performance.png",
            "3D Monthly Category Performance",
            "Combines time and category to reveal performance shifts during the year.",
            "Excellent for seasonal storytelling.",
        )

    with d5:
        render_image_card(
            IMG_DIR / "3D-discount-impact-on-profit.png",
            "3D Discount Impact on Profit",
            "Helps show how discounting affects profitability across the dataset.",
            "Very useful for pricing review.",
        )

    with d6:
        render_image_card(
            IMG_DIR / "category-vs-region-heatmap.png",
            "Category vs Region Heatmap",
            "A compact comparison map that is easy to read on mobile and desktop.",
            "Strong supporting drilldown view.",
        )

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Filter Summary</div>', unsafe_allow_html=True)
    st.write(f"Categories selected: {len(selected_categories)}")
    st.write(f"Segments selected: {len(selected_segments)}")
    st.write(f"Regions selected: {len(selected_regions)}")
    st.write(f"Ship modes selected: {len(selected_ship_modes)}")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Download Filtered Data</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Export the filtered slice for analysis or reporting.</div>', unsafe_allow_html=True)
    filtered_csv = filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download filtered slice",
        filtered_csv,
        file_name="filtered_3d_analytics.csv",
        mime="text/csv",
        use_container_width=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)
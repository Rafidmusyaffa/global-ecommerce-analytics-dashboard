import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from app_ui import load_data, apply_theme, sidebar_snapshot, render_metric_card, section_header

st.set_page_config(page_title="3D Analytics", page_icon="🌐", layout="wide")
df = load_data()
dark = apply_theme()

section_header(
    "🌐 3D Analytics",
    "Interactive 3D exploration with category, segment, region, and ship-mode filters."
)

st.sidebar.header("🎛️ Filters")

categories = sorted(df["Category"].dropna().unique().tolist()) if "Category" in df.columns else []
segments = sorted(df["Segment"].dropna().unique().tolist()) if "Segment" in df.columns else []
regions = sorted(df["Region"].dropna().unique().tolist()) if "Region" in df.columns else []
ship_modes = sorted(df["Ship Mode"].dropna().unique().tolist()) if "Ship Mode" in df.columns else []

selected_categories = st.sidebar.multiselect("Category", categories, default=categories)
selected_segments = st.sidebar.multiselect("Segment", segments, default=segments)
selected_regions = st.sidebar.multiselect("Region", regions, default=regions)
selected_ship_modes = st.sidebar.multiselect("Ship Mode", ship_modes, default=ship_modes)

filtered = df.copy()

if selected_categories:
    filtered = filtered[filtered["Category"].isin(selected_categories)]
if selected_segments:
    filtered = filtered[filtered["Segment"].isin(selected_segments)]
if selected_regions:
    filtered = filtered[filtered["Region"].isin(selected_regions)]
if selected_ship_modes:
    filtered = filtered[filtered["Ship Mode"].isin(selected_ship_modes)]

sidebar_snapshot(filtered, "Filtered Snapshot")

if filtered.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

c1, c2, c3, c4 = st.columns(4)
with c1:
    render_metric_card("Filtered Sales", f"${filtered['Sales'].sum():,.0f}")
with c2:
    render_metric_card("Filtered Profit", f"${filtered['Profit'].sum():,.0f}")
with c3:
    render_metric_card("Avg Discount", f"{filtered['Discount'].mean():.2%}")
with c4:
    render_metric_card("Rows in View", f"{len(filtered):,}")

st.write("")

tab1, tab2, tab3 = st.tabs(["3D Scatter", "3D Surface", "Drilldown"])

with tab1:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    fig = px.scatter_3d(
        filtered,
        x="Discount",
        y="Sales",
        z="Profit",
        color="Segment",
        symbol="Category",
        size="Sales",
        opacity=0.72,
        hover_data=["Category", "Segment", "Region", "Ship Mode"],
        title="3D Sales vs Profit vs Discount",
        template="plotly_dark" if dark else "plotly_white",
    )
    fig.update_layout(height=720, margin=dict(l=0, r=0, t=45, b=0))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    if "Region" in filtered.columns:
        pivot = filtered.pivot_table(
            values="Sales",
            index="Region",
            columns="Category",
            aggfunc="sum",
            fill_value=0,
        )

        surface = go.Figure(
            data=[
                go.Surface(
                    z=pivot.values,
                    x=list(range(len(pivot.columns))),
                    y=list(range(len(pivot.index))),
                    colorscale="Viridis",
                )
            ]
        )

        surface.update_layout(
            template="plotly_dark" if dark else "plotly_white",
            title="3D Sales Surface: Region vs Category",
            height=720,
            margin=dict(l=0, r=0, t=45, b=0),
        )
        st.plotly_chart(surface, use_container_width=True)
    else:
        st.info("Region column not found, so the 3D surface view is unavailable.")
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    left, right = st.columns(2)

    with left:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown("#### Filter summary")
        st.write(f"Categories selected: {len(selected_categories)}")
        st.write(f"Segments selected: {len(selected_segments)}")
        st.write(f"Regions selected: {len(selected_regions)}")
        st.write(f"Ship modes selected: {len(selected_ship_modes)}")
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown("#### Download filtered data")
        filtered_csv = filtered.to_csv(index=False)
        st.download_button(
            "⬇️ Download filtered slice",
            filtered_csv,
            file_name="filtered_3d_analytics.csv",
            mime="text/csv",
            use_container_width=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)
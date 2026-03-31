from pathlib import Path
import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "processed" / "cleaned_superstore.csv"
IMG_DIR = BASE_DIR / "images"


def load_data():
    df = pd.read_csv(DATA_PATH)

    for col in ["Sales", "Profit", "Discount"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def apply_theme():
    dark = st.session_state.get("dark_mode", True)

    if dark:
        bg = "#050816"
        text = "#E2E8F0"
        border = "rgba(148,163,184,0.16)"
    else:
        bg = "#F8FAFC"
        text = "#0F172A"
        border = "rgba(15,23,42,0.12)"

    st.markdown(
        f"""
        <style>
        html, body, [data-testid="stAppViewContainer"] {{
            background: linear-gradient(180deg, {bg} 0%, {bg} 100%);
            color: {text};
        }}

        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {bg}, {bg});
            border-right: 1px solid {border};
        }}

        [data-testid="stHeader"] {{
            background: transparent;
        }}

        #MainMenu, footer {{
            visibility: hidden;
        }}

        .block-container {{
            padding-top: 1rem;
            padding-bottom: 2rem;
            max-width: 1500px;
        }}

        .hero-title {{
            font-size: clamp(2rem, 3vw, 3.2rem);
            font-weight: 850;
            line-height: 1.02;
            letter-spacing: -0.03em;
            background: linear-gradient(90deg, #60A5FA, #22D3EE);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.25rem;
        }}

        .hero-subtitle {{
            color: rgba(226,232,240,0.78);
            font-size: 1.02rem;
            line-height: 1.6;
            max-width: 62rem;
        }}

        .accent-line {{
            height: 4px;
            width: 120px;
            border-radius: 999px;
            background: linear-gradient(90deg, #3B82F6, #22D3EE);
            margin: 0.8rem 0 1rem 0;
        }}

        .glass-card {{
            background: rgba(15,23,42,0.60);
            backdrop-filter: blur(14px);
            border: 1px solid {border};
            border-radius: 18px;
            padding: 1rem 1.05rem;
            box-shadow: 0 18px 50px rgba(0,0,0,0.22);
            transition: transform .20s ease, box-shadow .20s ease, border-color .20s ease;
        }}

        .glass-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 22px 60px rgba(59,130,246,0.16);
            border-color: rgba(96,165,250,0.45);
        }}

        .chart-card {{
            background: rgba(15,23,42,0.50);
            backdrop-filter: blur(14px);
            border-radius: 20px;
            padding: 1rem;
            border: 1px solid {border};
            box-shadow: 0 18px 50px rgba(0,0,0,0.18);
        }}

        .mini-pill {{
            display: inline-block;
            padding: 0.34rem 0.68rem;
            border-radius: 999px;
            border: 1px solid {border};
            margin: 0.15rem 0.18rem 0.15rem 0;
            font-size: 0.82rem;
            color: {text};
        }}

        .section-heading {{
            font-size: 1.15rem;
            font-weight: 750;
            margin-bottom: 0.2rem;
        }}

        .section-sub {{
            color: rgba(226,232,240,0.72);
            font-size: 0.95rem;
            margin-bottom: 0.75rem;
        }}

        .stDownloadButton > button {{
            border-radius: 14px;
            height: 3rem;
            font-weight: 700;
            background: linear-gradient(90deg,#3B82F6,#22D3EE);
            color: white;
            border: none;
        }}

        .stDownloadButton > button:hover {{
            box-shadow: 0 12px 28px rgba(59,130,246,0.28);
            transform: translateY(-1px);
        }}

        div[data-testid="metric-container"] {{
            border-radius: 16px;
            padding: 0.15rem 0.25rem;
        }}

        .metric-box {{
            background: rgba(15,23,42,0.58);
            border: 1px solid {border};
            border-radius: 18px;
            padding: 1rem 1.05rem;
            box-shadow: 0 18px 50px rgba(0,0,0,0.18);
        }}

        @media (max-width: 900px) {{
            .block-container {{
                padding-left: 1rem;
                padding-right: 1rem;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    return dark


def sidebar_snapshot(df, title="Live Snapshot"):
    st.sidebar.markdown(f"### 📊 {title}")
    st.sidebar.metric("Total Sales", f"${df['Sales'].sum():,.0f}")
    st.sidebar.metric("Total Profit", f"${df['Profit'].sum():,.0f}")
    st.sidebar.metric("Avg Discount", f"{df['Discount'].mean():.2%}")
    st.sidebar.metric("Rows", f"{len(df):,}")
    if "Category" in df.columns:
        top_category = df.groupby("Category")["Profit"].sum().idxmax()
        st.sidebar.info(f"Top Category: {top_category}")
    st.sidebar.divider()


def render_metric_card(label, value):
    st.markdown(
        f"""
        <div class="metric-box">
            <div style="font-size:0.95rem;font-weight:700;opacity:0.92;margin-bottom:0.35rem;">{label}</div>
            <div style="font-size:2rem;font-weight:800;line-height:1;">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(title, subtitle=""):
    st.markdown(f'<div class="hero-title">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="hero-subtitle">{subtitle}</div>', unsafe_allow_html=True)
    st.markdown('<div class="accent-line"></div>', unsafe_allow_html=True)
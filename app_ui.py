from pathlib import Path
import sqlite3
import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "processed" / "cleaned_superstore.csv"
DB_PATH = BASE_DIR / "notebooks" / "ecommerce.db"
IMG_DIR = BASE_DIR / "images"


def _load_from_sqlite(db_path: Path) -> pd.DataFrame:
    with sqlite3.connect(db_path) as conn:
        tables = pd.read_sql_query(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;",
            conn,
        )
        if tables.empty:
            raise FileNotFoundError("No tables found in the SQLite database.")

        table_name = tables.iloc[0]["name"]
        df = pd.read_sql_query(f'SELECT * FROM "{table_name}"', conn)

    return df


def load_data() -> pd.DataFrame:
    if DATA_PATH.exists():
        df = pd.read_csv(DATA_PATH)
    elif DB_PATH.exists():
        df = _load_from_sqlite(DB_PATH)
    else:
        raise FileNotFoundError(
            f"Could not find data file at {DATA_PATH} or database at {DB_PATH}"
        )

    for col in ["Sales", "Profit", "Discount"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    for col in ["Order Date", "Ship Date"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    return df


def apply_theme():
    dark = st.session_state.get("dark_mode", True)

    if dark:
        bg = "#050816"
        surface = "rgba(15,23,42,0.62)"
        surface_soft = "rgba(15,23,42,0.50)"
        text = "#E2E8F0"
        muted = "rgba(226,232,240,0.74)"
        border = "rgba(148,163,184,0.16)"
        btn_text = "#FFFFFF"
    else:
        bg = "#F8FAFC"
        surface = "rgba(255,255,255,0.94)"
        surface_soft = "rgba(255,255,255,0.90)"
        text = "#0F172A"
        muted = "rgba(15,23,42,0.68)"
        border = "rgba(15,23,42,0.12)"
        btn_text = "#0F172A"

    st.markdown(
        f"""
        <style>
        html, body, [data-testid="stAppViewContainer"] {{
            background: {bg};
            color: {text};
        }}

        [data-testid="stSidebar"] {{
            background: {bg};
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
            padding-bottom: 3rem;
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
            color: {muted};
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

        .chart-card {{
            background: {surface_soft};
            backdrop-filter: blur(14px);
            border-radius: 20px;
            padding: 1rem;
            border: 1px solid {border};
            box-shadow: 0 18px 50px rgba(0,0,0,0.18);
            margin-bottom: 1rem;
        }}

        .metric-box {{
            background: {surface};
            border: 1px solid {border};
            border-radius: 18px;
            padding: 1rem 1.05rem;
            box-shadow: 0 18px 50px rgba(0,0,0,0.18);
            min-height: 100%;
        }}

        .metric-label {{
            font-size: 0.88rem;
            font-weight: 700;
            opacity: 0.9;
            margin-bottom: 0.35rem;
            color: {text};
        }}

        .metric-value {{
            font-size: clamp(1.4rem, 2vw, 2rem);
            font-weight: 850;
            line-height: 1.05;
            color: {text};
        }}

        .section-heading {{
            font-size: 1.15rem;
            font-weight: 750;
            margin-bottom: 0.2rem;
            color: {text};
        }}

        .section-sub {{
            color: {muted};
            font-size: 0.95rem;
            margin-bottom: 0.75rem;
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

        .floating-kpi {{
            position: sticky;
            top: 0;
            z-index: 30;
            background: {surface_soft};
            backdrop-filter: blur(14px);
            border: 1px solid {border};
            border-radius: 18px;
            padding: 0.65rem;
            margin-bottom: 1rem;
        }}

        .image-card {{
            background: {surface};
            border: 1px solid {border};
            border-radius: 18px;
            padding: 0.8rem;
            box-shadow: 0 16px 44px rgba(0,0,0,0.16);
            margin-bottom: 1rem;
        }}

        .image-card-title {{
            font-size: 1rem;
            font-weight: 800;
            margin: 0.3rem 0 0.15rem 0;
            color: {text};
        }}

        .image-card-subtitle {{
            font-size: 0.9rem;
            color: {muted};
            margin-bottom: 0.55rem;
            line-height: 1.45;
        }}

        .image-card-caption {{
            font-size: 0.85rem;
            color: {muted};
            margin-top: 0.45rem;
        }}

        .story-card {{
            background: {surface_soft};
            border: 1px solid {border};
            border-radius: 18px;
            padding: 1rem 1.05rem;
            box-shadow: 0 18px 50px rgba(0,0,0,0.16);
            margin-bottom: 1rem;
        }}

        .stDownloadButton > button {{
            border-radius: 14px;
            height: 3rem;
            font-weight: 700;
            background: linear-gradient(90deg,#3B82F6,#22D3EE);
            color: {btn_text};
            border: none;
        }}

        .stDownloadButton > button:hover {{
            box-shadow: 0 12px 28px rgba(59,130,246,0.28);
            transform: translateY(-1px);
        }}

        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
            overflow-x: auto;
            scrollbar-width: none;
        }}

        .stTabs [data-baseweb="tab"] {{
            min-width: 120px;
        }}

        @media (max-width: 900px) {{
            .block-container {{
                padding-left: 0.8rem;
                padding-right: 0.8rem;
            }}

            .hero-subtitle {{
                font-size: 0.96rem;
            }}

            .floating-kpi {{
                position: sticky;
                top: 0;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    return dark


def sidebar_snapshot(df: pd.DataFrame, title="Live Snapshot"):
    st.sidebar.markdown(f"### 📊 {title}")
    if "Sales" in df.columns:
        st.sidebar.metric("Total Sales", f"${df['Sales'].sum():,.0f}")
    if "Profit" in df.columns:
        st.sidebar.metric("Total Profit", f"${df['Profit'].sum():,.0f}")
    if "Discount" in df.columns:
        st.sidebar.metric("Avg Discount", f"{df['Discount'].mean():.2%}")
    st.sidebar.metric("Rows", f"{len(df):,}")

    if "Category" in df.columns and "Profit" in df.columns and not df.empty:
        try:
            top_category = df.groupby("Category")["Profit"].sum().idxmax()
            st.sidebar.info(f"Top Category: {top_category}")
        except Exception:
            pass

    st.sidebar.divider()


def render_metric_card(label, value):
    st.markdown(
        f"""
        <div class="metric-box">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(title, subtitle=""):
    st.markdown(f'<div class="hero-title">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="hero-subtitle">{subtitle}</div>', unsafe_allow_html=True)
    st.markdown('<div class="accent-line"></div>', unsafe_allow_html=True)


def render_image_card(image_path, title, subtitle="", caption=""):
    st.markdown('<div class="image-card">', unsafe_allow_html=True)

    if image_path and Path(image_path).exists():
        st.image(image_path, use_container_width=True)
    else:
        st.info(f"Missing image: {Path(image_path).name if image_path else 'unknown file'}")

    st.markdown(f'<div class="image-card-title">{title}</div>', unsafe_allow_html=True)

    if subtitle:
        st.markdown(
            f'<div class="image-card-subtitle">{subtitle}</div>',
            unsafe_allow_html=True,
        )

    if caption:
        st.markdown(
            f'<div class="image-card-caption">{caption}</div>',
            unsafe_allow_html=True,
        )

    st.markdown('</div>', unsafe_allow_html=True)
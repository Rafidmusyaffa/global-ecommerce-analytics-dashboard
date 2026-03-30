import streamlit as st

st.set_page_config(
    page_title="Global E-Commerce Intelligence",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark mode toggle
dark_mode = st.sidebar.toggle("🌙 Dark Mode", value=True)

if dark_mode:
    st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🌍 Global E-Commerce Intelligence Platform")
st.caption("AI-Powered Business Intelligence Dashboard")

st.divider()

st.markdown("""
### 🚀 Features
- 📊 Executive KPI Dashboard  
- 🌐 Interactive 3D Analytics  
- 🤖 AI Business Insights  
- 📱 Responsive Mobile Layout  
- ⬇️ Downloadable Data  
""")

st.info("Use the sidebar to navigate")
import streamlit as st
from utils import load_css

st.set_page_config(
    page_title="ClearLens AI: 20/20 Vision for Your Health",
    page_icon="🧬",
    layout="centered"
)

load_css()

# Hero Section
st.markdown("""
<div class="hero-container">
    <h1 style="font-size: 4rem; margin-bottom: 0;">🧬 ClearLens AI</h1>
    <p style="font-size: 1.4rem; color: #94a3b8; font-family: 'Outfit';">20/20 Vision for Your Health.</p>
</div>
""", unsafe_allow_html=True)

# Hero Image (Local high-quality asset)
st.image("d:/LeedsHack2026/Bio Filter 2.0/frontend/bio_guide_hero.png", use_column_width=True)

st.markdown("""
<div class="glass-panel" style="margin-bottom: 2rem;">
    <h2 style="font-size: 1.8rem; margin-top: 0;">🧞 Meet ClearLens</h2>
    <p>ClearLens AI is your autonomous health advocate. We decode the back-of-package "chemical reality" and match it to your personal DNA goals.</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="glass-panel" style="text-align: center; padding: 1rem !important;">
        <h3 style="font-size: 1.2rem;">🔍 Decode</h3>
        <p style="font-size: 0.9rem;">Translate chemicals to "Community English".</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="glass-panel" style="text-align: center; padding: 1rem !important;">
        <h3 style="font-size: 1.2rem;">👨‍🍳 Bio-Chef</h3>
        <p style="font-size: 0.9rem;">Pantry-aware recipe suggestions.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="glass-panel" style="text-align: center; padding: 1rem !important;">
        <h3 style="font-size: 1.2rem;">🗣️ Log</h3>
        <p style="font-size: 0.9rem;">Autonomous bio-logging with AI.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

c1, c2 = st.columns(2)

if "user" not in st.session_state:
    with c1:
        if st.button("🔐 Sign In to ClearLens", type="primary", use_container_width=True):
            st.switch_page("pages/00_Login.py")
else:
    with c1:
        if st.button("🚀 Configure Bio-Profile", use_container_width=True):
            st.switch_page("pages/01_Profile.py")
    
    with c2:
        if st.button("📷 Launch Scanner", type="primary", use_container_width=True):
            st.switch_page("pages/02_Scanner.py")

st.markdown("<p style='text-align: center; opacity: 0.5;'>Built with 💚 for LeedsHack 2026 by <strong>The Illuminators (Sapna & Sandeep)</strong></p>", unsafe_allow_html=True)

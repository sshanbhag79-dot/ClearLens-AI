import streamlit as st
import time
from utils import load_user_history, api_get_profile, load_css
load_css()

# Mock Login Logic
def login(username):
    if not username:
        st.warning("Please enter a username.")
        return

    with st.spinner("🧬 Synchronizing Bio-Identity..."):
        time.sleep(0.8)
        st.session_state.user = {
            "name": username,
            "email": f"{username.lower().replace(' ', '')}@example.com",
            "picture": f"https://ui-avatars.com/api/?name={username}&background=random"
        }
        
        # Load User History
        history = load_user_history(username)
        st.session_state.scan_history = history
        
        # Load User Profile (Persistent)
        remote_profile = api_get_profile(username)
        if remote_profile:
             st.session_state.profile = remote_profile
             st.toast("🧬 Bio-Profile Loaded!")
        else:
             if "profile" in st.session_state:
                 del st.session_state.profile
        
        st.success(f"Identity Verified: Welcome, {username}!")
        time.sleep(0.5)
        st.switch_page("pages/01_Profile.py")

# Page Layout
st.markdown("""
<div class="hero-container">
    <h1 style="font-size: 4rem; margin-bottom: 0;">🔐</h1>
    <h2 style="font-size: 2.2rem; margin-top: 10px;">Verify Identity</h2>
    <p style="font-size: 1.1rem; color: #94a3b8;">Enter the portal to access your biological guardrails.</p>
</div>
""", unsafe_allow_html=True)

# Login Form
st.markdown('<div class="glass-panel" style="max-width: 400px; margin: 0 auto;">', unsafe_allow_html=True)
with st.form("login_form", border=False):
    username = st.text_input("Gamer Tag / Username", placeholder="e.g. BioWarrior", label_visibility="collapsed")
    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.form_submit_button("UNLEASH BIO-GUIDE", type="primary", use_container_width=True)
    
    if submitted:
        login(username)
st.markdown('</div>', unsafe_allow_html=True)

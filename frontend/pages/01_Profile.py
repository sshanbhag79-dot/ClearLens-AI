import streamlit as st
from utils import get_user_profile, load_css, require_login, api_update_profile

st.set_page_config(page_title="ClearLens Profile", page_icon="🧬")
load_css()

if not require_login():
    st.stop()

st.markdown("""
<div class="hero-container" style="padding: 2rem 1rem;">
    <h1 style="font-size: 3rem;">👤 Bio-Profile</h1>
    <p style="font-size: 1.1rem; color: #94a3b8;">Precision-tune your biological filters.</p>
</div>
""", unsafe_allow_html=True)

# Load current settings
current_profile = get_user_profile()

with st.container():
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    with st.form("profile_form", border=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🧬 Allergies")
            allergies = st.multiselect(
                "Filter out these ingredients:",
                ["Peanuts", "Tree Nuts", "Dairy", "Gluten", "Soy", "Shellfish", "Eggs"],
                default=current_profile["allergies"]
            )
        
        with col2:
            st.markdown("### 🏆 Dietary Goals")
            diets = st.multiselect(
                "Match my profile with:",
                ["Vegan", "Vegetarian", "Keto", "Paleo", "Low-Sugar", "Low-Sodium", "High-Protein", "Non-GMO"],
                default=current_profile["diets"]
            )
        
        st.divider()
        
        st.markdown("### 🛡️ Guardrail Strictness")
        strictness = st.select_slider(
            "How aggressive should the AI be?",
            options=["Flexible", "Moderate", "Strict"],
            value=current_profile["strictness"]
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("🚀 LOCK IN PROFILE", use_container_width=True)
        
        if submitted:
            new_profile = {
                "allergies": allergies,
                "diets": diets,
                "strictness": strictness
            }
            st.session_state.profile = new_profile
            
            # Save to Backend
            if "user" in st.session_state:
                 if api_update_profile(st.session_state.user["name"], new_profile):
                     st.toast("🧬 Bio-Profile Cloud-Synced!")
                 else:
                     st.error("Failed to sync profile (local only).")
                     
            st.success("✅ Profile Updated! Your filters are now active.")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.info("💡 **Pro-Tip:** BioFilter uses these parameters to calculate your 'Trust Verdict' and 'Bio-Quality Index' in real-time.")

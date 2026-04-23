import streamlit as st
from utils import get_user_profile, scan_product, load_css, decode_image, decode_cv2_frame, require_login, generate_audio
from community_api import get_community_data
from utils import save_user_history
import time

st.set_page_config(page_title="ClearLens Scanner", page_icon="📷")
load_css()

if not require_login():
    st.stop()

st.title("📷 ClearLens Scanner")
# Check if profile is active
profile = get_user_profile()
if not profile["allergies"] and not profile["diets"]:
    st.warning("⚠️ You haven't set up your profile yet. The AI needs to know your needs.")
    if st.button("Go to Profile"):
        st.switch_page("pages/01_Profile.py")

st.markdown("""
<div class="hero-container" style="padding: 2rem 1rem;">
    <h1 style="font-size: 3rem;">📷 ClearLens Scanner</h1>
    <p style="font-size: 1.1rem; color: #94a3b8;">Instant biological verification of any barcode.</p>
</div>
""", unsafe_allow_html=True)

# Tab Reset Logic
def reset_scanner():
    keys_to_clear = ["scan_result", "last_scan", "last_community_barcode", "community_data", "last_latency", "audio_played", "last_barcode_audio"]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]

# CSS for video container (Already in styles.css, but keeping for directness if needed)
st.markdown("""
<style>
    div[data-testid="stVideo"] {
        border-radius: var(--radius-md);
        overflow: hidden;
        border: 1px solid var(--border-glass);
    }
</style>
""", unsafe_allow_html=True)

# Initialize chat state
if "chat_active" not in st.session_state:
    st.session_state.chat_active = False

# Input Mode Selector
st.markdown('<div class="glass-panel" style="padding: 10px !important; margin-bottom: 20px;">', unsafe_allow_html=True)
input_mode = st.radio(
    "Select Input Mode:",
    ["📷 Camera", "📤 Upload", "#️⃣ Manual"],
    horizontal=True,
    on_change=reset_scanner,
    key="input_mode",
    label_visibility="collapsed"
)
st.markdown('</div>', unsafe_allow_html=True)

decoded_barcode = None

if input_mode == "📷 Camera":
    if st.session_state.chat_active:
        st.info("🧞 **ClearLens is active.** Camera is paused to save power.")
        if st.button("📷 Resume Camera"):
            st.session_state.chat_active = False
            st.rerun()
    else:
        camera_image = st.camera_input("Take a picture")
        if camera_image:
            with st.spinner("Decoding DNA..."):
                decoded = decode_image(camera_image)
                if decoded:
                    decoded_barcode = decoded
                    st.session_state.last_scan = decoded
                    st.toast(f"✅ Barcode Detected: {decoded_barcode}")
                else:
                    st.warning("No barcode detected. Try again or switch to Manual.")

elif input_mode == "📤 Upload":
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"], label_visibility="collapsed")
    if uploaded_file:
        with st.spinner("Decoding..."):
            decoded = decode_image(uploaded_file)
            if decoded:
                decoded_barcode = decoded
                st.session_state.last_scan = decoded
                st.toast(f"✅ Barcode Detected: {decoded_barcode}")
            else:
                st.warning("No barcode detected.")

elif input_mode == "#️⃣ Manual":
    manual_input = st.text_input("Barcode Number", placeholder="e.g. 5449000000996", label_visibility="collapsed")
    if manual_input:
        decoded_barcode = manual_input
        st.session_state.last_scan = manual_input

# Use persisted scan if available and no new one
if not decoded_barcode and "last_scan" in st.session_state:
    decoded_barcode = st.session_state.last_scan

# Prepare for analysis
barcode = decoded_barcode 
col_btn1, col_btn2 = st.columns([2, 1])
with col_btn1:
    scan_btn = st.button("🔍 ANALYZE PRODUCT", type="primary", use_container_width=True, disabled=not barcode)
with col_btn2:
    refresh_btn = st.button("🔄 REFRESH", use_container_width=True)

if (scan_btn or refresh_btn) and barcode:
    # Clear old state to force refresh
    if "scan_result" in st.session_state:
        del st.session_state.scan_result
        
    with st.spinner("🧬 ClearLens is analyzing ingredients..."):
        # Make API Call
        start_time = time.time()
        result = scan_product(barcode, st.session_state.user["name"])
        latency = time.time() - start_time
        
        if result:
            # Save to History (Persistent & Session)
            save_user_history(st.session_state.user["name"], barcode, result)
            
            # Force refresh community data for new scan
            if "last_community_barcode" in st.session_state:
                del st.session_state.last_community_barcode

            # Persist in session
            st.session_state.scan_result = result
            st.session_state.last_latency = latency
            st.rerun()
        else:
            st.error("Failed to analyze product. Please try again.")
# Results Display
if "scan_result" in st.session_state:
    result = st.session_state.scan_result
    latency = st.session_state.get("last_latency", 0)
    
    if "error" in result:
        st.error(f"⚠️ Analysis Error: {result['error']}")
        if st.button("Try Another Barcode"):
            del st.session_state.scan_result
            st.rerun()
    else:
        product = result.get("product", {})
        status = result.get("status", "Yellow")
        reason = result.get("reason", "No reason provided.")
        alternative = result.get("alternative")
        
        # Dynamic styling
        status_map = {
            "Green": {"color": "#10b981", "icon": "🟢", "bg": "rgba(16, 185, 129, 0.1)"},
            "Yellow": {"color": "#f59e0b", "icon": "🟡", "bg": "rgba(245, 158, 11, 0.1)"},
            "Red": {"color": "#ef4444", "icon": "🔴", "bg": "rgba(239, 68, 68, 0.1)"}
        }
        config = status_map.get(status, status_map["Yellow"])
        card_color = config["color"]

        # Community Trust Shield (Top Banner)
        if "community_data" in st.session_state and st.session_state.community_data:
            c_data = st.session_state.community_data
            total_reviews = c_data.get('total_reviews', 0)
            avg_rating = c_data.get('average_rating', 0.0)
            
            st.markdown(f"""
            <div class="glass-panel" style="padding: 10px !important; margin-bottom: 15px; display: flex; align-items: center; justify-content: space-between; border: 1px solid rgba(255,255,255,0.2);">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 1.5rem;">🛡️</span>
                    <div>
                        <strong style="color: #f8fafc; font-size: 0.9rem;">Community Trust Shield</strong>
                        <div style="font-size: 0.8rem; color: #94a3b8;">{total_reviews} Vouches • {avg_rating}⭐ Avg</div>
                    </div>
                </div>
                <div style="background: rgba(255,255,255,0.1); padding: 5px 10px; border-radius: 20px; font-weight: bold; font-size: 0.8rem;">
                    VERIFIED
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="result-card" style="border-top: 4px solid {card_color}; background: {config['bg']} !important; margin-top: 5px;">
        <h1 style="color: {card_color}; font-size: 2.2rem; margin: 0;">{config['icon']} {status.upper()}</h1>
        <h3 style="margin-top: 5px; color: white !important; opacity: 1;">{product.get('product_name', 'Unknown Product')}</h3>
        <p style="font-family: 'Outfit'; font-weight: 700; color: {card_color}; margin-top: 15px; text-transform: uppercase; letter-spacing: 1px;">🔍 Decoding the Truth:</p>
        <p style="font-size: 1.1rem; line-height: 1.6; color: white !important;">{result.get('marketing_vs_reality', reason)}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Audio
    if "audio_played" not in st.session_state or st.session_state.last_barcode_audio != barcode:
        spoken_text = result.get('community_takeaway', reason)
        audio_text = f"Result is {status}. {spoken_text}"
        audio_bytes = generate_audio(audio_text)
        if audio_bytes:
            st.audio(audio_bytes, format="audio/mp3")
            st.session_state.last_barcode_audio = barcode
            st.session_state.audio_played = True
    
    # Sub-metrics
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Trust Verdict", f"{result.get('trust_score', 5)}/10")
    with m2:
        st.metric("Latency", f"{latency:.2f}s")
    with m3:
        if status == "Green":
             st.markdown('<p class="text-green" style="font-weight:bold; margin-top:35px;">✨ Leeds Approved</p>', unsafe_allow_html=True)
        else:
             st.markdown(f'<p class="text-yellow" style="font-weight:bold; margin-top:35px;">🌱 Reboot Suggested</p>', unsafe_allow_html=True)

    if alternative and status != "Green":
         st.success(f"🌱 **System Reboot:** {alternative}")
    
    # --- PROS & CONS & RED FLAGS ---
    st.markdown('<div class="glass-panel" style="margin-top: 20px;">', unsafe_allow_html=True)
    col_pros, col_cons = st.columns(2)
    
    if "pros" in result and result["pros"]:
        with col_pros:
            st.markdown("### ✅ Pros")
            for pro in result["pros"]:
                st.markdown(f"- {pro}")
    
    with col_cons:
        if "bio_red_flags" in result and result["bio_red_flags"]:
            st.markdown("### 🚩 Bio Red Flags")
            for flag in result["bio_red_flags"]:
                st.markdown(f'<span class="text-red">- {flag}</span>', unsafe_allow_html=True)
        elif "cons" in result and result["cons"]:
            st.markdown("### ❌ Cons")
            for con in result["cons"]:
                st.markdown(f"- {con}")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- COMMUNITY INSIGHTS ---
    if not barcode and result.get('barcode'):
        barcode = result['barcode']

    if "community_data" not in st.session_state or st.session_state.get("last_community_barcode") != barcode:
         with st.spinner("Fetching community consensus..."):
            from community_api import get_community_data
            comm_data = get_community_data(barcode)
            st.session_state.community_data = comm_data
            st.session_state.last_community_barcode = barcode
    
    comm_data = st.session_state.community_data

    if comm_data:
        st.divider()
        st.markdown("### 👥 Community Insights")
        
        c1, c2 = st.columns([1, 2])
        with c1:
            avg_rating = comm_data.get('average_rating', 0.0)
            total_reviews = comm_data.get('total_reviews', 0)
            st.metric("Average Rating", f"⭐ {avg_rating}/5", help=f"Based on {total_reviews} reviews")
        
        with c2:
            summary = comm_data.get('community_summary', 'No summary available.')
            st.info(f"**Consensus:** {summary}")

            # Recent Reviews
            if comm_data.get('recent_reviews'):
                with st.expander(f"View Recent Reviews ({comm_data.get('total_reviews', 0)})", expanded=True):
                    for item in comm_data['recent_reviews']:
                        rating_val = item.get('rating', 0)
                        stars = "⭐" * rating_val
                        user_display = item.get('username', 'Anonymous')
                        
                        # Highlight own votes
                        if "user" in st.session_state and st.session_state.user.get("name") == user_display:
                            user_display += " (You)"
                            
                        st.markdown(f"**{stars}** {item['comment']}")
                        st.caption(f"_{user_display} • {item['timestamp']}_")

        # Ingredients Analysis
        st.divider()
        st.subheader("🧬 Ingredients Breakdown")
        # DEBUG: Check what the AI returned
        # st.write("Debug - Raw Ingredients Data:", result.get("ingredients_analysis"))
        
        if result.get("ingredients_analysis"):
            try:
                for ing in result["ingredients_analysis"]:
                    status_color = "#2ecc71" if ing.get('status') == "Safe" else "#f59e0b" if ing.get('status') == "Caution" else "#ef4444"
                    status_icon = "✅" if ing.get('status') == "Safe" else "⚠️" if ing.get('status') == "Caution" else "🚫"
                    
                    sig = ing.get('significance', 'Medium')
                    sig_color = "#94a3b8"
                    if sig == "High": sig_color = "#f87171"
                    elif sig == "Medium": sig_color = "#fbbf24"
                    elif sig == "Low": sig_color = "#34d399"
                    
                    st.markdown(f"""
                    <div class="result-card" style="border-left: 4px solid {status_color}; padding: 16px !important; margin-bottom: 12px; border-radius: 12px; background: rgba(255,255,255,0.03);">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <strong style="font-size: 1.05rem; color: #f8fafc;">{status_icon} {ing.get('name', 'Unknown')}</strong>
                                <span style="margin-left: 8px; font-size: 0.7rem; background: {sig_color}22; color: {sig_color}; padding: 2px 6px; border-radius: 4px; border: 1px solid {sig_color}44; text-transform: uppercase; font-weight: bold;">{sig}</span>
                            </div>
                        </div>
                        <p style="margin: 8px 0 0 0; font-size: 0.9rem; color: #cbd5e1; line-height: 1.5;">{ing.get('reason', '')}</p>
                    </div>
                    """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error rendering ingredients: {e}")
                st.write(result.get("ingredients_analysis"))
        else:
             # Fallback if AI didn't return list
             with st.expander("View Raw Ingredients List"):
                st.write(product.get("ingredients_text", "No ingredients listed."))

        # --- REVIEW FORM (Moved to End) ---
        st.divider()
        st.subheader("🗣️ Add Your Review")
        if "user" in st.session_state:
            with st.form("community_review"):
                st.write("Rate this product:")
                # Star Rating Input
                rating_opts = ["1", "2", "3", "4", "5"]
                # Display simply as numbers to avoid clutter, label handles 'Stars'
                review_rating = st.radio("Stars", rating_opts, index=None, horizontal=True, format_func=lambda x: f"{x}⭐")
                
                review_comment = st.text_input("Community Note", placeholder="e.g. Delicious but high sugar...")
                
                submitted = st.form_submit_button("Submit Review")
                if submitted:
                    if not review_rating:
                        st.warning("Please select a star rating.")
                    elif not review_comment:
                        st.warning("Please add a note.")
                    else:
                        rating_int = int(review_rating)
                        from community_api import submit_vote
                        success = submit_vote(barcode, rating_int, review_comment, st.session_state.user["name"])
                        if success:
                            st.success("Review submitted! It will appear next time you scan.")
                            # Force Refresh
                            if "last_community_barcode" in st.session_state:
                                del st.session_state.last_community_barcode
                            st.rerun()
        else:
            st.info("Sign in to leave a review.")

if scan_btn and not barcode:
    st.warning("Please enter a barcode.")

# --- CLEARLENS ADVOCATE CHATBOT ---
st.divider()
if not st.session_state.chat_active:
    if st.button("🧞 Talk to ClearLens", use_container_width=True, type="secondary"):
        st.session_state.chat_active = True
        st.rerun()
else:
    with st.container(border=True):
        col1, col2 = st.columns([5, 1])
        with col1:
             st.markdown("### 🧞 ClearLens Advocate")
        with col2:
            if st.button("❌", help="Close Chat", key="close_chat_btn"):
                st.session_state.chat_active = False
                st.rerun()

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Chat UI Container - History Scrolls
    chat_container = st.container(height=400) # Fixed height for styling

    # Input comes AFTER the history container in code, but renders at bottom
    if prompt := st.chat_input("Ask ClearLens anything...", key="global_chat"):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        # Context pre-fetch
        current_barcode = st.session_state.get("last_scan")
        profile = get_user_profile()
        
        try:
            import requests
            from utils import API_URL
            
            chat_payload = {
                "message": prompt,
                "username": st.session_state.user["name"],
                "barcode": current_barcode,
                "user_profile": profile
            }
            
            with st.spinner("🧞 ClearLens thinking..."):
                resp = requests.post(f"{API_URL}/chat/bio-guide", json=chat_payload)
                if resp.status_code == 200:
                    data = resp.json()
                    reply = data["reply"]
                    st.session_state.chat_history.append({"role": "assistant", "content": reply})
                    
                    # Handle Log Intent
                    intent = data.get("intent")
                    log_params = data.get("log_params")
                    if intent == "LOG_MEAL" and log_params:
                        from log_api import log_meal
                        
                        # Safe conversion helper
                        def safe_float(val, default):
                            try:
                                return float(val) if val is not None else default
                            except:
                                return default
                            
                        cals = safe_float(log_params.get("calories"), 0.0)
                        qty = safe_float(log_params.get("quantity"), 1.0)
                        
                        log_success = log_meal(
                            username=st.session_state.user["name"],
                            barcode=current_barcode or "MANUAL",
                            product_name=log_params.get("product_name", "Unknown Product"),
                            calories=cals,
                            quantity=qty,
                            status=log_params.get("status", "Yellow"),
                            total_calories=cals * qty
                        )
                        if log_success:
                            st.toast(f"✅ Logged! Your Bio-Quality Index is now updated.")
                        
                        st.rerun()
                else:
                    st.error("ClearLens is offline.")
        except Exception as e:
            st.error(f"Chat error: {e}")

    # Render history inside the container
    with chat_container:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                with st.chat_message("user"):
                    st.markdown(msg["content"])
            else:
                with st.chat_message("assistant", avatar="🧞"):
                    st.markdown(msg["content"])

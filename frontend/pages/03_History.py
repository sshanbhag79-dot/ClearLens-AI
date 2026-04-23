import streamlit as st
from utils import require_login, load_css
import time

st.set_page_config(page_title="ClearLens History", page_icon="📜")
load_css()

if not require_login():
    st.stop()

st.markdown("""
<div class="hero-container" style="padding: 2rem 1rem;">
    <h1 style="font-size: 3rem;">📜 Scan History</h1>
    <p style="font-size: 1.1rem; color: #94a3b8;">Your past decodes and biological verifications.</p>
</div>
""", unsafe_allow_html=True)

if "scan_history" not in st.session_state or not st.session_state.scan_history:
    st.markdown('<div class="glass-panel" style="text-align:center;">', unsafe_allow_html=True)
    st.info("No scans yet. Go to the Scanner to reboot your food choices!")
    if st.button("📷 START LOGGING", type="primary", use_container_width=True):
        st.switch_page("pages/02_Scanner.py")
    st.markdown('</div>', unsafe_allow_html=True)
else:
    col_clear, _ = st.columns([1, 2])
    with col_clear:
        if st.button("🗑️ WIPE LOGS", use_container_width=True):
            st.session_state.scan_history = []
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    
    for item in st.session_state.scan_history:
        status = item.get('status', 'Yellow')
        product = item.get('product', {})
        
        # Robust name extraction: check product dict first, then top-level, then fallback
        name = product.get('product_name') or item.get('product_name') or 'Unknown Product'
        
        # Safe timestamp handling
        ts = item.get('timestamp', time.time())
        t_str = time.strftime('%d %b • %H:%M', time.localtime(ts))
        
        barcode = item.get('barcode', 'MANUAL')
        
        status_map = {
            "Green": {"color": "#10b981", "icon": "🟢"},
            "Yellow": {"color": "#f59e0b", "icon": "🟡"},
            "Red": {"color": "#ef4444", "icon": "🔴"}
        }
        config = status_map.get(status, status_map["Yellow"])
        card_color = config["color"]

        st.markdown(f"""
        <div class="result-card" style="border-right: 4px solid {card_color}; margin-bottom: 12px; padding: 15px !important;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="flex-grow: 1;">
                    <h3>{name}</h3>
                    <p>{t_str} • {barcode}</p>
                </div>
                <div style="text-align: right; min-width: 100px;">
                    <span style="color: {card_color}; font-weight: 800; font-size: 0.8rem; letter-spacing:1px; background: rgba(0,0,0,0.2); padding: 4px 8px; border-radius: 6px;">
                        {config['icon']} {status.upper()}
                    </span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

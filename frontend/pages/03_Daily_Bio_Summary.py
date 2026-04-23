import streamlit as st
import pandas as pd
from utils import load_css, require_login
from log_api import get_daily_summary, get_daily_history

st.set_page_config(page_title="ClearLens Dashboard", page_icon="📅")
load_css()

if not require_login():
    st.stop()

st.title("📅 Daily Bio-Summary")

if "user" in st.session_state:
    username = st.session_state.user["name"]
    
    # Fetch Data
    summary = get_daily_summary(username)
    history = get_daily_history(username)
    
    # 1. Dashboard Metrics
    if summary:
        st.subheader("Your Day at a Glance")
        d1, d2, d3, d4 = st.columns(4)
        with d1:
            st.metric("Total kcal", f"{summary.get('total_calories', 0)}")
        with d2:
            st.metric("Clean kcal", f"{summary.get('clean_calories', 0)}", delta_color="normal")
        with d3:
            st.metric("Red kcal", f"{summary.get('red_calories', 0)}", delta_color="inverse")
        with d4:
            upf = summary.get('upf_ratio', 0)
            st.metric("UPF %", f"{upf}%", delta=f"{upf}%", delta_color="inverse")
        st.divider()
        
    # 2. Detailed History
    st.subheader("🍽️ Detailed Meal Log")
    
    if history:
        # Import delete function
        from log_api import delete_meal_log
        
        for log in history:
            log_id = log.get('id')
            grade = log.get('grade', 'Yellow')
            emoji = "🔴" if grade == "Red" else "🟡" if grade == "Yellow" else "🟢"
            name = log.get('name', 'Unknown')
            calories = log.get('calories', 0)
            
            # Render each meal in a small card with a delete button
            with st.container():
                col_info, col_del = st.columns([5, 1])
                
                with col_info:
                    st.markdown(f"**{emoji} {name}** | {calories} kcal")
                
                with col_del:
                    if st.button("🗑️", key=f"del_{log_id}", help="Delete this record"):
                        if delete_meal_log(log_id):
                            st.toast(f"Deleted {name}")
                            st.rerun()
                        else:
                            st.error("Delete failed.")
                st.divider()
    else:
        st.info("No meals logged for today yet. Go to the Scanner to add some!")
else:
    st.warning("Please sign in to view your summary.")

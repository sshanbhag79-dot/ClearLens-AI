import streamlit as st

st.title("Tab Test")
# In 1.32.2, does key work for tabs?
tabs = st.tabs(["Tab 1", "Tab 2"], key="my_tabs")

st.write("Session State:", st.session_state)

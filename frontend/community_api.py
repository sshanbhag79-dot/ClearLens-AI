
import requests
import streamlit as st
import os

# Base URL for the backend
API_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

def get_community_data(barcode):
    """
    Fetches community data (trust score, summary, votes) for a barcode.
    """
    try:
        response = requests.get(f"{API_URL}/community/{barcode}")
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return None
        else:
            st.error(f"Error fetching community data: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Connection error: {e}")
        return None

def submit_vote(barcode, rating, comment, username):
    """
    Submits a new community review with rating.
    """
    payload = {
        "barcode": barcode,
        "rating": rating,
        "comment": comment,
        "username": username
    }
    
    try:
        response = requests.post(f"{API_URL}/community/vote", json=payload)
        if response.status_code == 200:
            return True
        else:
            st.error(f"Error submitting vote: {response.text}")
            return False
    except Exception as e:
        st.error(f"Connection error: {e}")
        return False

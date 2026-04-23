import requests
import streamlit as st
import os
import cv2
import numpy as np
import io
from gtts import gTTS
import json

HISTORY_FILE = "user_history.json"

def load_user_history(username):
    """Loads scan history for a specific user from JSON file."""
    if not os.path.exists(HISTORY_FILE):
        return []
    
    try:
        with open(HISTORY_FILE, "r") as f:
            all_history = json.load(f)
        return all_history.get(username, [])
    except Exception as e:
        print(f"Error loading history: {e}")
        return []

def save_user_history(username, barcode, result):
    """Saves a scan result to the user's history."""
    all_history = {}
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                all_history = json.load(f)
        except:
            all_history = {}
    
    if username not in all_history:
        all_history[username] = []
    
    # Enrich result with metadata for history display
    history_item = result.copy()
    history_item["barcode"] = barcode
    import time
    history_item["timestamp"] = time.time()
    
    # Prepend new item
    all_history[username].insert(0, history_item)
    
    try:
        with open(HISTORY_FILE, "w") as f:
            json.dump(all_history, f, indent=4)
        
        # Also update session state history if active
        if "scan_history" in st.session_state:
             st.session_state.scan_history.insert(0, history_item)
    except Exception as e:
        print(f"Error saving history: {e}")

def generate_audio(text: str):
    """
    Converts text to speech using gTTS.
    Returns bytes of the audio file.
    """
    try:
        tts = gTTS(text=text, lang='en')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        return fp.getvalue()
    except Exception as e:
        print(f"Audio generation error: {e}")
        return None

API_URL = "http://localhost:8000"

def decode_cv2_frame(image):
    """
    Decodes barcode from a cv2 image (numpy array).
    Returns the first decoded barcode string, or None.
    """
    if image is None:
        return None

    # Detect barcode
    # Available in OpenCV 4.7+
    if hasattr(cv2, 'barcode'):
        barcode_detector = cv2.barcode.BarcodeDetector()
        result = barcode_detector.detectAndDecode(image)
        
        decoded_info = None
        
        # Handle different return signatures (3 or 4 values)
        if len(result) == 4:
            retval, decoded_info, decoded_type, points = result
        elif len(result) == 3:
            decoded_info, decoded_type, points = result
        else:
            return None
        
        if decoded_info:
            # decoded_info can be a list/tuple if multiple barcodes, or a single string
            if isinstance(decoded_info, (list, tuple)):
                valid_files = [s for s in decoded_info if s]
                if valid_files:
                    return valid_files[0]
            elif isinstance(decoded_info, str) and decoded_info:
                return decoded_info
    
    return None

def decode_image(image_file):
    """
    Decodes barcode from an uploaded image file or camera buffer using OpenCV.
    Returns the first decoded barcode string, or None.
    """
    try:
        # Convert file-like object to numpy array
        # Check if it's a Streamlit UploadedFile or BytesIO
        if hasattr(image_file, "getvalue"):
            file_bytes = np.frombuffer(image_file.getvalue(), np.uint8)
        elif hasattr(image_file, "read"):
            file_bytes = np.frombuffer(image_file.read(), np.uint8)
        else:
            return None

        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        return decode_cv2_frame(image)
    except Exception as e:
        st.error(f"Error processing image: {e}")
        return None

def get_user_profile():
    if "profile" not in st.session_state:
        st.session_state.profile = {
            "allergies": [],
            "diets": [],
            "strictness": "Strict"
        }
    return st.session_state.profile

def require_login():
    """
    Redirects to the Login page if the user is not authenticated.
    Returns True if authenticated, False (and stops execution) if not.
    """
    if "user" not in st.session_state:
        st.warning("⚠️ Please sign in to continue.")
        st.switch_page("pages/00_Login.py")
        return False
    return True

def scan_product(barcode: str, username: str = ""):
    profile = get_user_profile()
    payload = {
        "barcode": barcode,
        "user_profile": profile
    }
    
    try:
        response = requests.post(f"{API_URL}/scan", json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return {"error": "Product not found"}
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": str(e)}

def api_get_profile(username):
    """Fetches user profile from backend."""
    try:
        response = requests.get(f"{API_URL}/user/{username}")
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error fetching profile: {e}")
    return None

def api_update_profile(username, profile_data):
    """Updates user profile in backend."""
    try:
        response = requests.post(f"{API_URL}/user/{username}", json=profile_data)
        return response.status_code == 200
    except Exception as e:
        print(f"Error updating profile: {e}")
        return False

def load_css():
    with open("frontend/styles.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    render_sidebar_dashboard()

def render_sidebar_dashboard():
    """
    Renders the Calorie & Bio-Quality Tracker in the sidebar.
    """
    if "user" in st.session_state:
        username = st.session_state.user["name"]
        
        try:
            resp = requests.get(f"{API_URL}/log/summary/{username}", timeout=5)
            if resp.status_code == 200:
                summary = resp.json()
                total_cals = summary.get("total_calories", 0)
                upf_ratio = summary.get("upf_ratio", 0) # Percentage of Red cals
                clean_cals = summary.get("clean_calories", 0)
                red_cals = summary.get("red_calories", 0)
                
                with st.sidebar:
                    st.markdown("## 📊 Daily Tracker")
                    
                    # 1. Total Calories (Big Number)
                    st.metric("Total Calories", f"{total_cals} kcal")
                    
                    # Sub-metrics
                    c1, c2 = st.columns(2)
                    c1.caption(f"🍏 Clean: {clean_cals}")
                    c2.caption(f"🚨 Red: {red_cals}")
                    
                    # 2. Bio-Quality Bar (Progress Bar Green -> Red)
                    # Mapping 0-100% UPF Ratio to a progress bar
                    # Higher UPF Ratio = More Red
                    st.markdown("**Bio-Quality Index**")
                    
                    # Normalize ratio for progress bar (0.0 to 1.0)
                    progress = min(max(upf_ratio / 100.0, 0.0), 1.0)
                    
                    # Display Progress Bar with color context
                    # Streamlit progress bars don't support direct colors easily, 
                    # but we can use st.markdown or just the progress value.
                    st.progress(progress)
                    
                    if upf_ratio < 10:
                        st.caption("🟢 Clean day! Keep it up.")
                    elif upf_ratio < 30:
                        st.caption("🟡 Moderate bio-quality.")
                    else:
                        st.caption("🔴 High UPF intake detected.")
                    
                    st.markdown("<br><p style='text-align: center; font-size: 0.8rem; opacity: 0.7;'>Built with 💚 by <strong>The Illuminators</strong><br>(Sapna & Sandeep)</p>", unsafe_allow_html=True)
        except Exception:
             pass

import requests
import streamlit as st
from utils import API_URL

def log_meal(username, barcode, product_name, calories, quantity, status, total_calories=None):
    """
    Logs a meal to the backend.
    """
    payload = {
        "username": username,
        "barcode": barcode,
        "product_name": product_name,
        "calories": calories, # per 100g
        "quantity": quantity, # units or 100g servings
        "status": status,
        "total_calories": total_calories # Explicit total
    }
    
    try:
        response = requests.post(f"{API_URL}/log/meal", json=payload)
        return response.status_code == 200
    except Exception as e:
        print(f"Error logging meal: {e}")
        return False

def get_daily_summary(username):
    """
    Retrieves daily summary for the user.
    """
    try:
        response = requests.get(f"{API_URL}/log/summary/{username}")
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error fetching summary: {e}")
    return None

def get_daily_history(username):
    """
    Retrieves detailed daily history for the user.
    """
    try:
        response = requests.get(f"{API_URL}/log/history/{username}")
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error fetching history: {e}")
    return []

def delete_meal_log(log_id):
    """
    Deletes a specific meal log via the API.
    """
    try:
        response = requests.delete(f"{API_URL}/log/{log_id}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error deleting log: {e}")
        return False

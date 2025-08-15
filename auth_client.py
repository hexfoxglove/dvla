import streamlit as st
import requests
import json
from firebase_admin import firestore
from firebase_config import db  # Firestore client from firebase_config.py

# -------------------------------
# Load Firebase API key from secrets
# -------------------------------
API_KEY = st.secrets["firebase_client"]["apiKey"]

# -------------------------------
# AUTH FUNCTIONS USING REST API
# -------------------------------

def sign_in(email: str, password: str):
    """
    Sign in a user with email/password via Firebase REST API.
    Returns: idToken, refreshToken, localId or None, None, None on failure.
    """
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    r = requests.post(url, data=json.dumps(payload))
    if r.status_code == 200:
        data = r.json()
        return data["idToken"], data.get("refreshToken"), data["localId"]
    else:
        print("Sign-in error:", r.json())
        return None, None, None

def sign_up(email: str, password: str):
    """
    Sign up a user with email/password via Firebase REST API.
    Returns: idToken, refreshToken, localId or None, None, None on failure.
    """
    # Check password length before sending request
    if len(password) < 6:
        print("Sign-up error: Password must be at least 6 characters")
        return None, None, None

    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    r = requests.post(url, data=json.dumps(payload))
    if r.status_code == 200:
        data = r.json()
        return data["idToken"], data.get("refreshToken"), data["localId"]
    else:
        # Print the Firebase error for debugging
        print("Sign-up error:", r.json())
        return None, None, None

# -------------------------------
# OPTIONAL: Firestore helper example
# -------------------------------

def create_user_document(local_id: str, email: str):
    """
    Create a user document in Firestore after signup.
    """
    doc_ref = db.collection("users").document(local_id)
    doc_ref.set({"email": email})

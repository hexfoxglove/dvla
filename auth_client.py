import streamlit as st
import requests
import json
from firebase_config import db  # Firestore client

API_KEY = st.secrets["firebase_client"]["apiKey"]

# -------------------------------
# AUTH FUNCTIONS USING REST API
# -------------------------------

def sign_in(email: str, password: str):
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
    if len(password) < 6:
        print("Sign-up error: Password must be at least 6 characters")
        return None, None, None

    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    r = requests.post(url, data=json.dumps(payload))
    if r.status_code == 200:
        data = r.json()
        # Optional: create a Firestore user document
        local_id = data["localId"]
        db.collection("users").document(local_id).set({"email": email})
        return data["idToken"], data.get("refreshToken"), local_id
    else:
        print("Sign-up error:", r.json())
        return None, None, None

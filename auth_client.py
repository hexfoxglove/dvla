import requests
import json
import firebase_admin
from firebase_admin import credentials, firestore

# Load Firebase API key (from firebase_client_config.json)
with open("firebase_client_config.json") as f:
    firebase_config = json.load(f)
API_KEY = firebase_config["apiKey"]

# Initialize Firebase Admin SDK for Firestore
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_key.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# -------------------------------
# AUTH FUNCTIONS USING REST API
# -------------------------------
def sign_in(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    r = requests.post(url, data=json.dumps(payload))
    if r.status_code == 200:
        data = r.json()
        return data["idToken"], data["refreshToken"], data["localId"]
    else:
        print("Sign-in error:", r.json())
        return None, None, None

def sign_up(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={API_KEY}"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    r = requests.post(url, data=json.dumps(payload))
    if r.status_code == 200:
        data = r.json()
        return data["idToken"], data["refreshToken"], data["localId"]
    else:
        print("Sign-up error:", r.json())
        return None, None, None

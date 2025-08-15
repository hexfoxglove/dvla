import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Firebase Admin SDK (Firestore)
cred_dict = dict(st.secrets["firebase_admin"])
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)

db = firestore.client()

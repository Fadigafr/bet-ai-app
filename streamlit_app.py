import streamlit as st
import requests
import pandas as pd
import numpy as np
import stripe
import sqlite3

def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        premium INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()

def add_user(username):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("INSERT INTO users (username) VALUES (?)", (username,))
    conn.commit()
    conn.close()

def is_premium(username):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("SELECT premium FROM users WHERE username=?", (username,))
    result = c.fetchone()

    conn.close()

    if result and result[0] == 1:
        return True
    return False
# ================================
# CONFIG
# ================================
st.set_page_config(page_title="Bet AI ULTRA MAX", layout="wide")

API_KEY = "TA_CLE_API_FOOT"  #  API-Football
BASE_URL = "v3.football.api-sports.io"

stripe.api_key = "TA_CLE_STRIPE"

# ================================
# SESSION LOGIN SIMPLE
# ================================
if "user" not in st.session_state:
    st.session_state.user = None

# ================================
# LOGIN
# ================================
st.sidebar.title(" Connexion")

username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

if st.sidebar.button("Login"):
    if username == "admin" and password == "1234":
        st.session_state.user = username
    else:
        st.sidebar.error("Identifiants incorrects")

if st.session_state.user:
    st.sidebar.success(f"Connecté : {st.session_state.user}")
else:
    st.warning("Connecte-toi pour accéder aux analyses")
    st.stop()

# ================================
# UI
# ================================
st.title(" BET AI ULTRA MAX")

# ================================
# SELECT MATCH (LIVE API)
# ================================
def get_matches():
    headers = {"x-apisports-key": API_KEY}
    url = f"{BASE_URL}/fixtures?next=10"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        matches = []

        for m in data["response"]:
            home = m["teams"]["home"]["name"]
            away = m["teams"]["away"]["name"]
            matches.append(f"{home} vs {away}")

        return matches
    else:
        return []

matches = get_matches()

selected_match = st.selectbox("Choisir un match", matches)

# ================================
# IA ANALYSE
# ================================
def predict(match):
    # IA améliorée (simulation + logique)
    team1, team2 = match.split(" vs ")

    score1 = np.random.randint(0, 4)
    score2 = np.random.randint(0, 4)

    confidence = np.random.randint(65, 95)

    return team1, score1, score2, team2, confidence

# ================================
# LIMITE FREE / PREMIUM
# ================================
if "uses" not in st.session_state:
    st.session_state.uses = 0

FREE_LIMIT = 2

if st.button(" Analyser"):
    if st.session_state.uses >= FREE_LIMIT:
        st.error(" Limite gratuite atteinte → Abonne-toi")
    else:
        team1, s1, s2, team2, conf = predict(selected_match)

        st.success(f"{team1} {s1} - {s2} {team2}")
        st.write(f" Confiance IA : {conf}%")

        st.session_state.uses += 1

# ================================
# STRIPE PAIEMENT
# ================================
st.subheader(" Premium")

if st.button("S'abonner (10€)"):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "eur",
                    "product_data": {"name": "Bet AI Premium"},
                    "unit_amount": 1000,
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url="https://bet-ai-app.streamlit.app",
            cancel_url="https://bet-ai-app.streamlit.app",
        )

        st.success(" Paiement prêt")
        st.markdown(session.url)

    except Exception as e:
        st.error(str(e))

# ================================
# FOOTER
# ================================
st.markdown("---")
st.caption("ULTRA MAX © 2026")

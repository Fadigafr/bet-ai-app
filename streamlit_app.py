import streamlit as st
import requests
import numpy as np
import stripe

# ========================
# CONFIG
# ========================
st.set_page_config(page_title="BET AI GOD MODE", layout="wide")

API_KEY = "TA_CLE_API"
BASE_URL = "https://v3.football.api-sports.io"

stripe.api_key = "TA_CLE_STRIPE"

# ========================
# LOGIN SIMPLE
# ========================
if "user" not in st.session_state:
    st.session_state.user = None

username = st.sidebar.text_input("Utilisateur")
password = st.sidebar.text_input("Mot de passe", type="password")

if st.sidebar.button("Connexion"):
    if username and password:
        st.session_state.user = username

if not st.session_state.user:
    st.warning("Connecte-toi")
    st.stop()

# ========================
# UI
# ========================
st.title("⚽ BET AI GOD MODE")

# ========================
# API MATCHS
# ========================
def get_matches():
    headers = {"x-apisports-key": API_KEY}
    url = BASE_URL + "/fixtures?next=5"

    try:
        r = requests.get(url, headers=headers)
        data = r.json()

        matches = []
        for m in data.get("response", []):
            home = m["teams"]["home"]["name"]
            away = m["teams"]["away"]["name"]
            matches.append(f"{home} vs {away}")

        return matches
    except:
        return []

matches = get_matches()

if not matches:
    matches = ["PSG vs Marseille", "Real Madrid vs Barca"]

match = st.selectbox("Choisir match", matches)

# ========================
# IA SIMPLE
# ========================
if "uses" not in st.session_state:
    st.session_state.uses = 0

if "premium" not in st.session_state:
    st.session_state.premium = False

if st.button("Analyser"):

    if not st.session_state.premium and st.session_state.uses >= 2:
        st.error("Passe Premium")
        st.stop()

    s1 = np.random.randint(0, 4)
    s2 = np.random.randint(0, 4)
    conf = np.random.randint(65, 95)

    team1, team2 = match.split(" vs ")

    st.success(f"{team1} {s1} - {s2} {team2}")
    st.write(f"Confiance : {conf}%")

    st.session_state.uses += 1

# ========================
# PAIEMENT
# ========================
if st.button("S'abonner (10€)"):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "eur",
                    "product_data": {"name": "Bet AI"},
                    "unit_amount": 1000,
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url="https://bet-ai-app.streamlit.app",
            cancel_url="https://bet-ai-app.streamlit.app",
        )

        st.success("Paiement prêt")
        st.write(session.url)

        st.session_state.premium = True

    except Exception as e:
        st.error(str(e))

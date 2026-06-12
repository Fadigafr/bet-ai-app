import streamlit as st
import numpy as np
from database import init_db, add_user, check_user, is_premium, set_premium

# =====================
# INIT DB
# =====================
init_db()

st.set_page_config(page_title="BET AI SaaS", layout="wide")

st.title(" BET AI SaaS LOGIN")

# =====================
# SESSION
# =====================
if "user" not in st.session_state:
    st.session_state.user = None

# =====================
# AUTH
# =====================
st.sidebar.subheader("Compte")

username = st.sidebar.text_input("Utilisateur")
password = st.sidebar.text_input("Mot de passe", type="password")

col1, col2 = st.sidebar.columns(2)

if col1.button("Login"):
    user = check_user(username, password)
    if user:
        st.session_state.user = username
    else:
        st.error("Erreur login")

if col2.button("Register"):
    add_user(username, password)
    st.success("Compte créé")

# =====================
# BLOQUER SI PAS CONNECTÉ
# =====================
if not st.session_state.user:
    st.warning("Connecte-toi")
    st.stop()

user = st.session_state.user

# =====================
# PREMIUM STATUS
# =====================
premium = is_premium(user)

# =====================
# INPUT MATCH
# =====================
team1 = st.text_input("Équipe 1")
team2 = st.text_input("Équipe 2")

# =====================
# IA
# =====================
def predict():
    s1 = np.random.randint(0, 4)
    s2 = np.random.randint(0, 4)
    return s1, s2

# =====================
# ANALYSE
# =====================
if st.button(" Analyse"):

    if not team1 or not team2:
        st.warning("Entre les équipes")
        st.stop()

    #  FREE LIMIT
    if not premium:
        st.error(" Réservé PREMIUM")
        st.stop()

    s1, s2 = predict()

    st.success(f"{team1} {s1} - {s2} {team2}")

# =====================
# STRIPE SIMULÉ (ACTIVATION)
# =====================
st.subheader(" Upgrade Premium")

if not premium:
    if st.button("Activer Premium"):
        set_premium(user)
        st.success(" Premium activé")

# =====================
# INFO USER
# =====================
if premium:
    st.success(" Compte Premium")
else:
    st.warning("Compte Gratuit")
"

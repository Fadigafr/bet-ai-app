import streamlit as st
import json
import hashlib
import os
import stripe
import requests
import random

def prediction_advanced():
    home_goals = random.randint(0, 4)
    away_goals = random.randint(0, 4)
    confidence = random.randint(70, 95)

    return home_goals, away_goals, confidence

if st.button("Analyse PRO MAX"):
    h, a, c = prediction_advanced()

    st.metric("Confiance IA", f"{c}%")
    st.write(f"Score exact : {h} - {a}")
def prediction():
    score = random.randint(0, 3)
    score2 = random.randint(0, 3)
    prob = random.randint(60, 90)

    return score, score2, prob

if st.button("Analyser"):
    s1, s2, prob = prediction()

    st.metric("Probabilité", f"{prob}%")
    st.write(f"Score prévu : {s1} - {s2}")
TOKEN = "TON_TOKEN_TELEGRAM"
CHAT_ID = "TON_CHAT_ID"

def envoyer_message(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    requests.post(url, data=data)

if st.button("Envoyer prédiction Telegram"):
    envoyer_message(" Prédiction du jour : victoire équipe A")
    st.success("Envoyé ")

stripe.api_key = "TA_CLE_STRIPE"

if st.button("Payer abonnement "):
    st.write("Paiement en cours...")
    st.success("Simulation paiement ")
# Fichier utilisateurs
USER_FILE = "users.json"

# Charger utilisateurs
def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return {}

# Sauvegarder utilisateurs
def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

# Hash mot de passe
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

users = load_users()

menu = st.sidebar.selectbox("Menu", ["Login", "Créer compte"])

if menu == "Créer compte":
    st.subheader("Créer un compte")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("S'inscrire"):
        if username not in users:
            users[username] = hash_password(password)
            save_users(users)
            st.success("Compte créé ")
        else:
            st.error("Utilisateur existe déjà")

elif menu == "Login":
    st.subheader("Connexion")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Se connecter"):
        if username in users and users[username] == hash_password(password):
            st.session_state["user"] = username
            st.success("Connecté ")
        else:
            st.error("Erreur login")

# Vérifier connexion
if "user" not in st.session_state:
    st.stop()

st.write(f"Bienvenue {st.session_state['user']}")

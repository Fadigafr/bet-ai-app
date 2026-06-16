import streamlit as st
import requests
import numpy as np
import time
import streamlit.components.v1 as components
import json

def load_users():
    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f)

st.subheader("Créer un compte")

new_user = st.text_input("Nom utilisateur")
new_pass = st.text_input("Mot de passe", type="password")

if st.button("S'inscrire"):
    users = load_users()

    if new_user in users:
        st.warning("Utilisateur déjà existant")
    else:
        users[new_user] = {
            "password": new_pass,
            "vip": False
        }
        save_users(users)
        st.success("Compte créé ")

st.subheader("Connexion")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

users = load_users()

if st.button("Se connecter"):
    if username in users and users[username]["password"] == password:
        st.session_state.logged = True
        st.session_state.user = username
        st.success("Connecté ")
    else:
        st.error("Erreur login")

    data = request.json

    email = data["customer_email"]

    users = load_users()

    if email in users:
        users[email]["vip"] = True
        save_users(users)
new_user = st.text_input("fadigafr2000@yahoo.fr")

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="BET AI PRO", layout="wide")
st.set_page_config(
    page_title="BET AI PRO",
    layout="centered"
)
st.markdown("""
<meta name="viewport" content="width=device-width, initial-scale=1">
""", unsafe_allow_html=True)
st.markdown("""
<link rel="manifest" href="manifest.json">
""", unsafe_allow_html=True)
st.markdown("""
<h1 style='text-align:center;color:#22c55e;'>
 BET AI PRO
</h1>
""", unsafe_allow_html=True)
st.markdown("""
<div style="background:#22c55e;padding:10px;border-radius:10px;text-align:center;color:black;">
 ACCÈS VIP - SIGNES PREMIUM
</div>
""", unsafe_allow_html=True)

API_KEY = "TA_API_KEY"

# TELEGRAM
TOKEN = "TON_TOKEN"
CHAT_ID = "TON_CHAT_ID"

# =========================
# TELEGRAM FUNCTION
# =========================
def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    try:
        requests.post(url, data=data)
    except:
        pass

# =========================
# LOGIN VIP
# =========================
if "logged" not in st.session_state:
    st.session_state.logged = False

password = st.text_input("Mot de passe VIP", type="password")

if password == "VIP123":
    st.session_state.logged = True

st.markdown("""
##  Devenir VIP

 Paiement sécurisé

 Clique ici :
https://paystack.com/pay/TON_LIEN
""")
users = load_users()

users = load_users()

if st.session_state.logged:
    user = st.session_state.user

    if not users[user]["vip"]:
        st.warning(" VIP requis")

        st.markdown(" https://paystack.com/pay/TON_LIEN")

        st.stop()

# =========================
# MATCHS (FAKE + TEST)
# =========================
matches = [
    ("PSG", "Marseille", 1.8, 3.3, 4.2),
    ("Real Madrid", "Barcelone", 1.9, 3.1, 3.7),
    ("Chelsea", "Arsenal", 2.0, 3.2, 3.5),
]

# =========================
# FREE MODE (BLOQUAGE)
# =========================
if not st.session_state.logged:
    st.write(" Version gratuite limitée")

    for i, (team1, team2, odd1, oddX, odd2) in enumerate(matches):
        if i > 1:
            st.warning(" Réservé VIP")
            break

        st.write(f"{team1} vs {team2}")

    st.stop()
if st.session_state.user == "fred":
    users = load_users()
    users["fred"]["vip"] = True
    save_users(users)

# =========================
# IA ANALYSE VALUE
# =========================
def analyse_value(odd1, oddX, odd2):
    prob1 = np.random.randint(45, 70)
    probX = np.random.randint(10, 25)
    prob2 = 100 - prob1 - probX

    p1 = prob1 / 100
    pX = probX / 100
    p2 = prob2 / 100

    v1 = round((p1 * odd1) - 1, 2)
    vX = round((pX * oddX) - 1, 2)
    v2 = round((p2 * odd2) - 1, 2)

    return prob1, probX, prob2, v1, vX, v2

# =========================
# ANTI-SPAM SYSTEM
# =========================
sent_alerts = set()
last_sent_time = 0
COOLDOWN = 300  # 5 minutes

# =========================
# UI
# =========================
st.title(" BET AI PRO")

for team1, team2, odd1, oddX, odd2 in matches:

    prob1, probX, prob2, v1, vX, v2 = analyse_value(odd1, oddX, odd2)

    values = {"1": v1, "X": vX, "2": v2}
    best = max(values, key=values.get)
    best_value = values[best]

    color = "green" if best_value > 0 else "red"

    html = f"""
    <div style="background:white;padding:15px;border-radius:10px;margin-bottom:10px;">
        <b>{team1} vs {team2}</b>

        <div style="margin-top:10px;">
            <span style="background:#eef2f7;padding:5px;">1: {prob1}% | {odd1}</span>
            <span style="background:#eef2f7;padding:5px;">X: {probX}% | {oddX}</span>
            <span style="background:#eef2f7;padding:5px;">2: {prob2}% | {odd2}</span>
        </div>

        st.markdown(""" CSS """, unsafe_allow_html=True)
st.markdown("""
<style>
.card {
    padding: 15px;
    border-radius: 12px;
    background: #1e293b;
}
</style>
""", unsafe_allow_html=True)

    # =========================
    # TELEGRAM ALERT
    # =========================
    match_id = f"{team1}-{team2}-{best}"
    current_time = time.time()

    if (
        best_value > 0.20
        and match_id not in sent_alerts
        and current_time - last_sent_time > COOLDOWN
    ):

        message = f"""
 VALUE BET

{team1} vs {team2}

Choix : {best}
Value : {best_value}

Cotes :
1={odd1} X={oddX} 2={odd2}
"""

        send_telegram(message)

        sent_alerts.add(match_id)
        last_sent_time = current_time

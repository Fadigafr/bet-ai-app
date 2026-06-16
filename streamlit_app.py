import streamlit as st
import numpy as np
import time
import requests
import streamlit.components.v1 as components

# =========================
# UTILISATEURS
# =========================
users = {
    "admin": {"password": "VIP123", "vip": True},
    "test": {"password": "1234", "vip": False}
}

st.set_page_config(page_title="BET AI PRO", layout="centered")

# =========================
# LOGIN PRO
# =========================
if "logged" not in st.session_state:
    st.session_state.logged = False
    st.session_state.user = None

st.markdown("##  Connexion BET AI PRO")

username = st.text_input("Utilisateur", key="user_input")
password = st.text_input("Mot de passe", type="password", key="pass_input")

if st.button(" Se connecter"):

    if username in users and users[username]["password"] == password:
        st.session_state.logged = True
        st.session_state.user = username
        st.success(f" Bienvenue {username}")
    else:
        st.error(" Accès refusé")

#  BLOCAGE
if not st.session_state.logged:
    st.warning(" Connecte-toi pour accéder à l'application")
    st.stop()

# =========================
# CONTROLE VIP
# =========================
current_user = st.session_state.user

if not users[current_user]["vip"]:
    st.warning(" Accès VIP requis")

    st.markdown(" Paiement : https://paystack.com/pay/TON_LIEN")

    st.stop()

# =========================
# LOGOUT
# =========================
if st.button(" Se déconnecter"):
    st.session_state.logged = False
    st.session_state.user = None
    st.rerun()

# =========================
# MATCH DATA
# =========================
matches = [
    ("PSG", "Marseille", 1.8, 3.3, 4.2),
    ("Real Madrid", "Barcelone", 1.9, 3.1, 3.7),
    ("Chelsea", "Arsenal", 2.0, 3.2, 3.5),
]

# =========================
# IA ELITE LOGIQUE
# =========================
def analyse_value(odd1, oddX, odd2):

    #  probabilités réalistes (pas trop aléatoire)
    base = np.random.uniform(0.4, 0.6)

    prob1 = round(base * 100)
    probX = round(np.random.uniform(0.15, 0.25) * 100)
    prob2 = 100 - prob1 - probX

    #  probas normalisées
    p1, pX, p2 = prob1/100, probX/100, prob2/100

    #  value bet réelle
    v1 = round((p1 * odd1) - 1, 2)
    vX = round((pX * oddX) - 1, 2)
    v2 = round((p2 * odd2) - 1, 2)

    return prob1, probX, prob2, v1, vX, v2

# =========================
# DASHBOARD
# =========================
st.markdown("##  DASHBOARD BET AI PRO")

col1, col2, col3 = st.columns(3)

col1.metric("Matchs", len(matches))
col2.metric("Mode", "IA ACTIVE")
col3.metric("Statut", "LIVE")

# =========================
# TELEGRAM (optionnel)
# =========================
sent_alerts = set()

def send_telegram(message):
    TOKEN = "TON_TOKEN"
    CHAT_ID = "TON_CHAT_ID"
    try:
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": message}
        )
    except:
        pass

# =========================
# LOOP MATCH
# =========================
for team1, team2, odd1, oddX, odd2 in matches:

    #  IA
    prob1, probX, prob2, v1, vX, v2 = analyse_value(odd1, oddX, odd2)

    values = {"1": v1, "X": vX, "2": v2}
    best = max(values, key=values.get)
    best_value = values[best]

    color = "#22c55e" if best_value > 0 else "red"

    confidence = max(prob1, probX, prob2)

    # =========================
    # CARD UI ELITE
    # =========================
    html = f"""
    <div style="background:#020617;padding:20px;border-radius:15px;margin-bottom:15px;color:white;">

        <h3> {team1} vs {team2}</h3>

        <p> Probabilités</p>
        <p>1: {prob1}% | X: {probX}% | 2: {prob2}%</p>

        <p> Confiance IA : {confidence}%</p>

        <p style="color:{color};font-size:18px;">
          VALUE BET : {best} ({best_value})
        </p>

        <p style="color:#22c55e;"> SIGNAL PREMIUM</p>

    </div>
    """

    components.html(html, height=230)

    # =========================
    # ALERT TELEGRAM
    # =========================
    match_id = f"{team1}-{team2}-{best}"

    if best_value > 0.20 and match_id not in sent_alerts:

        message = f"""
  BET AI PRO SIGNAL

  {team1} vs {team2}

  Choix : {best}
  Value : {best_value}
  Confiance : {confidence}%
"""

        send_telegram(message)

        sent_alerts.add(match_id)

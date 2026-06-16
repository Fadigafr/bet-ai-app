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
def analyse_advanced(team1, team2):def analyse_advanced(team1 goals_home > 0 and goals_away > 0 else "NON "

    #  score exact
    score = f"{goals_home} - {goals_away}"

    #  buteur simulé
    scorers = ["Mbappé", "Haaland", "Benzema", "Vinicius", "Salah"]
    scorer = np.random.choice(scorers)

    return over25, btts, score, scorer

    #  simulation buts
    goals_home = np.random.randint(0, 4)
    goals_away = np.random.randint(0, 4)

    total_goals = goals_home + goals_away

    #  OVER / UNDER
    over25 = "OVER 2.5 " if total_goals >= 3 else "UNDER 2.5 "

    #  BTTS


    return prob1, probX, prob2, v1, vX, v2
    def analyse_advanced(team1, team2):

    #  simulation buts
    goals_home = np.random.randint(0, 4)
    goals_away = np.random.randint(0, 4)

    total_goals = goals_home + goals_away

    #  OVER / UNDER
    over25 = "OVER 2.5 " if total_goals >= 3 else "UNDER 2.5 "

    #  BTTS
    btts = "OUI " if goals_home > 0 and goals_away > 0 else "NON "

    #  score exact
    score = f"{goals_home} - {goals_away}"

    #  buteur simple (simulation)
    scorers = ["Mbappé", "Haaland", "Benzema", "Vinicius", "Salah"]
    scorer = np.random.choice(scorers)

    return over25, btts, score, scorer
    if "OVER" in over25:
    over_count += 1

if "OUI" in btts:
    btts_count += 1

st.markdown("##  STATISTIQUES IA")

c1, c2, c3 = st.columns(3)

c1.metric("Matchs", total_matches)
c2.metric("Over 2.5", over_count)
c3.metric("BTTS Oui", btts_count)
``

# =========================
# DASHBOARD
# =========================
st.markdown("##  DASHBOARD BET AI PRO")

total_matches = len(matches)
over_count = 0
btts_count = 0
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
    over25, btts, score, scorer = analyse_advanced(team1, team

    # =========================
    # CARD UI ELITE
    # =========================
    html = f"""
<div style="background:#020617;padding:20px;border-radius:15px;margin-bottom:15px;color:white;">

    <h3> {team1} vs {team2}</h3>

    <p> Probabilités</p>
    <p>1: {prob1}% | X: {probX}% | 2: {prob2}%</p>

    <p> Confiance IA : {max(prob1, probX, prob2)}%</p>

    <p style="color:{color};font-size:18px;">
         VALUE BET : {best} ({best_value})
    </p>

    <hr>

    <p> <b>Score Exact :</b> {score}</p>
    <p> <b>Over/Under :</b> {over25}</p>
    <p> <b>BTTS :</b> {btts}</p>
    <p> <b>Buteur probable :</b> {scorer}</p>

    <p style="color:#22c55e;"> SIGNAL IA PREMIUM</p>

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

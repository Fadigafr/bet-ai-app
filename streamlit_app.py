import streamlit as st
import numpy as np
import requests
import streamlit.components.v1 as components

#  INIT SESSION STATE (OBLIGATOIRE)#  INIT SESSION STATE (OBLlogged" not in st.session_state:
    st.session_state.logged = False

if "user" not in st.session_state:
    st.session_state.user = None


st.set_page_config(page_title="BET AI PRO", layout="centered")

# =========================
# USERS
# =========================
users = {
    "admin": {"password": "VIP123", "vip": True},
    "user": {"password": "1234", "vip": False}
}

# =========================
# LOGIN
# =========================
if "logged" not in st.session_state:
    st.session_state.logged = False
    st.session_state.user = None

st.markdown("##  BET AI PRO LOGIN")

username = st.text_input("Utilisateur", key="input_user")
password = st.text_input("Mot de passe", type="password", key="input_pass")

if st.button("Se connecter"):
    if username in users and users[username]["password"] == password:
        st.session_state.logged = True
        st.session_state.user = username
        st.success(" Connexion réussie")
    else:
        st.error(" Accès refusé")

if not st.session_state.logged:
    st.stop()

# =========================
# VIP CONTROL
# =========================
current_user = st.session_state.get("user", None)

if current_user is None:
    st.stop()

if not users[current_user]["vip"]:
    st.warning(" Accès VIP requis")
    st.markdown(" https://paystack.com/pay/TON-LIEN")
    st.stop()

# =========================
# SELECT LEAGUE
# =========================
league_dict = {
    "Premier League": 39,
    "La Liga": 140,
    "Ligue 1": 61
}

league_name = st.selectbox(
    "Choisir une ligue",
    list(league_dict.keys()),
    key="league_main"
)

league = league_dict[league_name]

# =========================
# SAFE MATCH DATA
# =========================
def get_matches():
    return [
        ("PSG", "Marseille", 1.8, 3.3, 4.2),
        ("Real Madrid", "Barcelone", 1.9, 3.1, 3.7),
        ("Chelsea", "Arsenal", 2.0, 3.2, 3.5),
    ]

matches = get_matches()

# =========================
# IA PRO
# =========================
def analyse_super_pro(odd1, oddX, odd2):

    p1 = 1 / odd1
    pX = 1 / oddX
    p2 = 1 / odd2

    total = p1 + pX + p2

    prob1 = round((p1 / total) * 100)
    probX = round((pX / total) * 100)
    prob2 = 100 - prob1 - probX

    # SCORE
    if prob1 > 55:
        score = "2-0"
    elif prob2 > 55:
        score = "0-2"
    elif probX > 35:
        score = "1-1"
    else:
        score = "2-1"

    # MARKETS
    over25 = "OVER 2.5 " if (prob1 + prob2) > 60 else "UNDER 2.5 "
    btts = "OUI " if prob1 > 40 and prob2 > 40 else "NON "

    # VALUE
    v1 = round((prob1/100 * odd1) - 1, 2)
    vX = round((probX/100 * oddX) - 1, 2)
    v2 = round((prob2/100 * odd2) - 1, 2)

    return prob1, probX, prob2, v1, vX, v2, score, over25, btts

# =========================
# TELEGRAM
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
# DASHBOARD
# =========================
st.markdown("##  BET AI PRO DASHBOARD")

total_matches = len(matches)

# =========================
# PERFORMANCE
# =========================
if "history" not in st.session_state:
    st.session_state.history = []

# =========================
# LOOP MATCHES
# =========================
for team1, team2, odd1, oddX, odd2 in matches:

    prob1, probX, prob2, v1, vX, v2, score, over25, btts = analyse_super_pro(
        odd1, oddX, odd2
    )

    values = {"1": v1, "X": vX, "2": v2}
    best = max(values, key=values.get)
    best_value = values[best]

    st.session_state.history.append(best_value)

    color = "#22c55e" if best_value > 0 else "red"

    html = f"""
    <div style="
    background: linear-gradient(135deg,#020617,#0f172a);
    padding:20px;
    border-radius:15px;
    margin-bottom:15px;
    color:white">

    <h3> {team1} vs {team2}</h3>

    <p> Probabilités : {prob1}% | {probX}% | {prob2}%</p>

    <p style="color:{color};font-size:18px;">
     VALUE BET : {best} ({best_value})
    </p>

    <hr>

    <p> Score : <b>{score}</b></p>
    <p> {over25}</p>
    <p> {btts}</p>

    </div>
    """

    components.html(html, height=260)

    # TELEGRAM ALERT
    match_id = f"{team1}-{team2}-{best}"

    if best_value > 0.20 and match_id not in sent_alerts:

        message = f"""
  BET AI PRO

  {team1} vs {team2}
  Choix : {best}
  Value : {best_value}
"""

        send_telegram(message)
        sent_alerts.add(match_id)

# =========================
# STATS
# =========================
st.markdown("##  ANALYTICS")

col1, col2 = st.columns(2)

col1.metric("Matchs", total_matches)
col2.metric("Signaux", len(st.session_state.history))

if len(st.session_state.history) > 2:
    st.line_chart(st.session_state.history)

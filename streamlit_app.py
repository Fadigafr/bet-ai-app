import streamlit as st
import requests
import numpy as np
import time
import streamlit.components.v1 as components

st.text_input(" Mot de passe VIP", type="password")
password = st.text_input(" Mot de passe VIP", type="password", key="vip_password")
username = st.text_input("Utilisateur", key="username")

email = st.text_input("Email", key="email")
if "logged" not in st.session_state:
    st.session_state.logged = False

if password == "VIP123":
    st.session_state.logged = True

# =========================
# MATCH DATA (test)
# =========================
def get_team_stats(team_id):
    url = "https://v3.football.api-sports.io/teams/statistics"
    
    headers = {"x-apisports-key": API_KEY}

    params = {
        "team": team_id,
        "season": 2023,
        "league": 39
    }

    res = requests.get(url, headers=headers, params=params)
    return res.json()
matches = [
    ("PSG", "Marseille", 1.8, 3.3, 4.2),
    ("Real Madrid", "Barcelone", 1.9, 3.1, 3.7),
    ("Chelsea", "Arsenal", 2.0, 3.2, 3.5),
]

# =========================
# FREE MODE
# =========================
if not st.session_state.logged:
    st.warning(" Version gratuite limitée")

    for i, (team1, team2, odd1, oddX, odd2) in enumerate(matches):
        if i > 1:
            st.error(" Réservé VIP")
            break

        st.write(f"{team1} vs {team2}")

    st.stop()

# =========================
# IA ANALYSE
# =========================
def analyse_real(team1_stats, team2_stats):

    win_rate1 = team1_stats["wins"]["total"]
    win_rate2 = team2_stats["wins"]["total"]

    if win_rate1 > win_rate2:
        return "1"
    else:
        return "2"

# =========================
# ANTI-SPAM
# =========================
sent_alerts = set()
last_sent_time = 0
COOLDOWN = 300

# =========================
# UI HEADER
# =========================
st.markdown("##  BET AI PRO")
st.markdown("""
<link rel="manifest" href="manifest.json">
<meta name="theme-color" content="#0f172a">
""", unsafe_allow_html=True)


# =========================
# LOOP MATCH
# =========================
for team1, team2, odd1, oddX, odd2 in matches:

    prob1, probX, prob2, v1, vX, v2 = analyse_value(odd1, oddX, odd2)

    values = {"1": v1, "X": vX, "2": v2}
    best = max(values, key=values.get)
    best_value = values[best]

    color = "green" if best_value > 0 else "red"

    #  HTML PRO PROPRE
    html = f"""
    <div style="background:#1e293b;padding:15px;border-radius:10px;margin-bottom:10px;color:white;">
        <b>{team1} vs {team2}</b>

        <div style="margin-top:10px;">
            <span style="background:#334155;padding:5px;">1: {prob1}% | {odd1}</span><br>
            <span style="background:#334155;padding:5px;">X: {probX}% | {oddX}</span><br>
            <span style="background:#334155;padding:5px;">2: {prob2}% | {odd2}</span>
        </div>

        <br>

        <b>VALUE BET :</b>
        <span style="color:{color};font-weight:bold;">
            {best} ({best_value})
        </span>
    </div>
    """

    components.html(html, height=200)

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

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="BET AI PRO", layout="centered")

# TELEGRAM (remplace par tes vraies infos)
TOKEN = "TON_TOKEN"
CHAT_ID = "TON_CHAT_ID"

# =========================
# TELEGRAM FUNCTION
# =========================
def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
    except:
        pass

# =========================
# LOGIN VIP PRO
# =========================
if "logged" not in st.session_state:
    st.session_state.logged = False

st.markdown("###  Connexion VIP")

password = st.text_input(
    "Mot de passe VIP",
    type="password",
    key="vip_password"
)

#  bouton connexion
if st.button("Se connecter"):

    if password == "VIP123":
        st.session_state.logged = True
        st.success(" Connexion réussie")
    else:
        st.error(" Mot de passe incorrect")
        if not st.session_state.logged:
    st.warning(" Connecte-toi pour accéder à l'application")
    st.stop()
    if st.session_state.logged:
    if st.button("Se déconnecter"):
        st.session_state.logged = False
        st.experimental_rerun()
    



import streamlit as st
import requests
import numpy as np
import time
import streamlit.components.v1 as components
import matplotlib.pyplot as plt

#  1. DÉFINIR MATCHES AVANT TOUT
matches = [
    ("PSG", "Marseille", 1.8, 3.3, 4.2),
    ("Real Madrid", "Barcelone", 1.9, 3.1, 3.7),
    ("Chelsea", "Arsenal", 2.0, 3.2, 3.5),
]

#  2. DASHBOARD
st.markdown("##  Dashboard BET AI PRO")

col1, col2, col3 = st.columns(3)

col1.metric("Matchs analysés", len(matches))
col2.metric("Top Value", "0.25")
col3.metric("Signal", "1")
history = np.random.randint(-10, 20, 10)

fig, ax = plt.subplots()
ax.plot(history)
ax.set_title("Historique performance AI")

st.pyplot(fig)

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
for team1, team2, odd1, oddX, odd2 in matches:

    #  calcul IA
    prob1, probX, prob2, v1, vX, v2 = analyse_value(odd1, oddX, odd2)

    #  calcul value
    values = {"1": v1, "X": vX, "2": v2}

    best = max(values, key=values.get)
    best_value = values[best]

    color = "#22c55e" if best_value > 0 else "red"


html = f"""
<div style="background:#020617;padding:20px;border-radius:15px;margin-bottom:15px;color:white;">

    <h3> {team1} vs {team2}</h3>

    <p> Probabilités</p>
    <p>1: {prob1}% | X: {probX}% | 2: {prob2}%</p>

    <p> Value :</p>
    <p style="color:{color};font-size:18px;">
        {best} ({best_value})
    </p>

    <p style="color:#22c55e;"> SIGNAL IA PREMIUM</p>

</div>
"""

components.html(html, height=200)

st.markdown("""
<style>

body {
    background: linear-gradient(135deg, #020617, #0f172a);
    color: white;}

/* TITRE */
.title {
    text-align: center;
    font-size: 32px;
    font-weight: bold;
    color: #22c55e;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #94a3b8;
    margin-bottom: 30px;
}

/* CARD */
.card {
    background: #0f172a;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 15px;
    border: 1px solid rgba(34, 197, 94, 0.2);
    box-shadow: 0px 0px 15px rgba(34, 197, 94, 0.1);
}

/* MATCH TITLE */
.match {
    font-size: 20px;
    font-weight: bold;
}

/* BADGE */
.badge {
    background: #22c55e;
    color: black;
    padding: 5px 10px;
    border-radius: 8px;
    font-weight: bold;
}

/* VALUE */
.value-positive {
    color: #22c55e;
    font-weight: bold;
}

.value-negative {
    color: red;
    font-weight: bold;
}

/* INPUT */
.stTextInput > div > div > input {
    background-color: #1e293b;
    color: white;
    border-radius: 8px;
}

/* BUTTON */
.stButton button {
    background: linear-gradient(90deg, #22c55e, #4ade80);
    color: black;
    border-radius: 10px;
    font-weight: bold;
    width: 100%;
}

</style>
""", unsafe_allow_html=True)
st.markdown('<div class="title">⚽ BET AI PRO</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Prédiction intelligente & Value Bet</div>', unsafe_allow_html=True)


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

st.markdown("##  Dashboard BET AI PRO")

col1, col2, col3 = st.columns(3)

col1.metric("Matchs analysés", len(matches))
col2.metric("Top Value", "0.25")
col3.metric("Signal", "1")

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
confidence = max(prob1, probX, prob2)

st.progress(confidence / 100)

st.write(f" Confiance IA : {confidence}%")       

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

    color_class = "value-positive" if best_value > 0 else "value-negative"

html = f"""
<div class="card">

    <div class="match"> {team1} vs {team2}</div>

    <br>

    <div>
        <b>Probabilités :</b><br>
        1️ {prob1}% | {odd1}<br>
          {probX}% | {oddX}<br>
        2️ {prob2}% | {odd2}
    </div>

    <br>

    <div class="{color_class}">
          VALUE BET : {best} ({best_value})
    </div>

    <br>

    <span class="badge"> SIGNAL IA</span>

</div>
"""

components.html(html, height=230)


    # =========================
    # TELEGRAM ALERT
    # =========================
def plot_probs(prob1, probX, prob2, team1, team2):

    labels = [f"{team1}", "DRAW", f"{team2}"]
    values = [prob1, probX, prob2]

    fig, ax = plt.subplots()

    ax.bar(labels, values)
    ax.set_ylim(0, 100)
    ax.set_title("Probabilités (%)")

    st.pyplot(fig)

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
st.set_page_config(
    page_title="BET AI PRO",
    layout="centered"
)
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
# LOGIN DESIGN PREMIUM
# =========================
st.markdown("###  Connexion VIP")

password = st.text_input("Mot de passe", type="password", key="vip_password")

if st.button(" Accéder à BET AI PRO"):
    if password == "VIP123":
        st.session_state.logged = True
        st.success(" Connexion réussie")
    else:
        st.error(" Accès refusé")
if "logged" not in st.session_state:
    st.session_state.logged = False

#  STYLE PREMIUM
st.markdown("""
<style>
.main-box {
    background: #0f172a;
    padding: 30px;
    border-radius: 15px;
    text-align: center;
    color: white;
}

.title {
    font-size: 26px;
    color: #22c55e;
    font-weight: bold;
    margin-bottom: 10px;
}

.subtitle {
    color: #94a3b8;
    margin-bottom: 20px;
}

.stTextInput > div > div > input {
    background-color: #1e293b;
    color: white;
    border-radius: 8px;
}

.stButton button {
    background-color: #22c55e;
    color: black;
    border-radius: 10px;
    font-weight: bold;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

#  UI BOX
st.markdown('<div class="main-box">', unsafe_allow_html=True)

st.markdown('<div class="title"> BET AI PRO</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Connexion VIP</div>', unsafe_allow_html=True)

password = st.text_input(
    "Mot de passe",
    type="password",
    key="vip_password"
)

if st.button(" Se connecter"):
    if password == "VIP123":
        st.session_state.logged = True
        st.success(" Bienvenue VIP")
    else:
        st.error(" Mot de passe incorrect")

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# BLOQUAGE
# =========================
if not st.session_state.logged:
    st.stop()

# =========================
# LOGOUT BUTTON
# =========================
if st.session_state.logged:
    if st.button(" Se déconnecter"):
        st.session_state.logged = False
        st.rerun()
    



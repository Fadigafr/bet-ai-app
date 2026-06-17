import streamlit as st
import numpy as np
import requests
import streamlit.components.v1 as components

st.set_page_config(page_title="BET AI PRO", layout="centered")

# =========================
# INIT SESSION (OBLIGATOIRE)
# =========================
if "logged" not in st.session_state:
    st.session_state.logged = False

if "user" not in st.session_state:
    st.session_state.user = None

if "history" not in st.session_state:
    st.session_state.history = []

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

current_user = st.session_state.user

# =========================
# VIP ACCESS
# =========================
if not users[current_user]["vip"]:
    st.warning(" Accès VIP requis")
    st.markdown(" https://paystack.com/pay/TON-LIEN")
    st.stop()

# =========================
# COMPETITIONS
# =========================
competitions = {
    "🏴 Premier League": 39,
    "🇪🇸 La Liga": 140,
    "🇫🇷 Ligue 1": 61,
    "🇩🇪 Bundesliga": 78,
    "🇮🇹 Serie A": 135,
    "🏆 Ligue des Champions": 2,
    "🏆 Ligue Europa": 3
}

competition_name = st.selectbox(
    " Choisir une compétition",
    list(competitions.keys()),
    key="competition_select"
)

# =========================
# MATCH DATA (SAFE)
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
def analyse_ultra_pro(odd1, oddX, odd2):

    # =========================
    #  PROBABILITÉS BOOKMAKER
    # =========================
    p1 = 1 / odd1
    pX = 1 / oddX
    p2 = 1 / odd2

    total = p1 + pX + p2

    prob1 = p1 / total
    probX = pX / total
    prob2 = p2 / total

    # =========================
    #  FORME ÉQUIPE (SIMULATION)
    # =========================
    form_home = np.random.uniform(0.8, 1.2)
    form_away = np.random.uniform(0.8, 1.2)

    # =========================
    #  xG (EXPECTED GOALS)
    # =========================
    xg_home = (prob1 * 2.2) * form_home
    xg_away = (prob2 * 2.0) * form_away

    # =========================
    #  BUTS RÉALISTES
    # =========================
    goals_home = int(np.random.poisson(xg_home))
    goals_away = int(np.random.poisson(xg_away))

    # sécurité (pas de négatif)
    goals_home = max(0, goals_home)
    goals_away = max(0, goals_away)

    # score final
    score = f"{goals_home}-{goals_away}"

    # =========================
    #  BTTS (CORRIGÉ)
    # =========================
    if goals_home > 0 and goals_away > 0:
        btts = "OUI "
    else:
        btts = "NON "

    # =========================
    #  OVER / UNDER 2.5
    # =========================
    total_goals = goals_home + goals_away

    if total_goals >= 3:
        over25 = "OVER 2.5 "
    else:
        over25 = "UNDER 2.5 "

    # =========================
    #  CONVERSION EN %
    # =========================
    prob1 = int(prob1 * 100)
    probX = int(probX * 100)
    prob2 = 100 - prob1 - probX

    # =========================
    #  VALUE BET
    # =========================
    v1 = round((prob1 / 100 * odd1) - 1, 2)


    # =========================
    #  PROBABILITÉS BOOKMAKER
    # =========================
    p1 = 1 / odd1
    pX = 1 / oddX
    p2 = 1 / odd2

    total = p1 + pX + p2

    prob1 = p1 / total

# =========================
# TELEGRAM
# =========================
sent_alerts = set()

def send_telegram(message):
    TOKEN = "TON_TOKEN"
    CHAT_ID = "TON_CHAT_ID"
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": message})
    except:
        pass

# =========================
# DASHBOARD
# =========================
st.markdown(f"##  {competition_name}")

# =========================
# LOOP MATCHES
# =========================
for team1, team2, odd1, oddX, odd2 in matches:

    prob1, probX, prob2, v1, vX, v2, score, over25, btts = analyse_real_pro(
        odd1, oddX, odd2
    )

    values = {"1": v1, "X": vX, "2": v2}
    best = max(values, key=values.get)
    best_value = values[best]

    st.session_state.history.append(best_value)

    color = "#22c55e" if best_value > 0 else "red"

    html = f"""
    <div style="
    background:#020617;
    padding:20px;
    border-radius:15px;
    margin-bottom:15px;
    color:white">

    <h3> {team1} vs {team2}</h3>

    <p> {prob1}% | {probX}% | {prob2}%</p>

    <p style="color:{color};font-size:18px;">
      VALUE BET : {best} ({best_value})
    </p>

    <p> Score : {score}</p>
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
# ANALYTICS
# =========================
st.markdown("##  ANALYTICS")

col1, col2 = st.columns(2)

col1.metric("Matchs", len(matches))
col2.metric("Signals", len(st.session_state.history))

if len(st.session_state.history) > 2:
    st.line_chart(st.session_state.history)

# SCORE
if prob1 > 55:
    score = "2-0"
elif prob2 > 55:
    score = "0-2"
elif probX > 35:
    score = "1-1"
else:
    score = "2-1"

#  BTTS CORRIGÉ
goals_home = int(score.split("-")[0])
goals_away = int(score.split("-")[1])

if goals_home > 0 and goals_away > 0:
    btts = "OUI "
else:
    btts = "NON "

def analyse_real_pro(odd1, oddX, odd2):

    p1 = 1 / odd1
    pX = 1 / oddX
    p2 = 1 / odd2

    total = p1 + pX + p2

    prob1 = round((p1 / total) * 100)
    probX = round((pX / total) * 100)
    prob2 = 100 - prob1 - probX

    #  SCORE
    if prob1 > 55:
        score = "2-0"
    elif prob2 > 55:
        score = "0-2"
    elif probX > 35:
        score = "1-1"
    else:
        score = "2-1"

    #  BTTS basé sur le score (CORRECT)
    goals_home = int(score.split("-")[0])
    goals_away = int(score.split("-")[1])

    if goals_home > 0 and goals_away > 0:
        btts = "OUI "
    else:
        btts = "NON "

    #  OVER / UNDER
    over25 = "OVER 2.5 " if (prob1 + prob2) > 60 else "UNDER 2.5 "

    #  VALUE
    v1 = round((prob1/100 * odd1) - 1, 2)
    vX = round((probX/100 * oddX) - 1, 2)
    v2 = round((prob2/100 * odd2) - 1, 2)

    return prob1, probX, prob2, v1, vX, v2, score, over25, btts

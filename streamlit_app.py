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

if "results" not in st.session_state:
    st.session_state.results = []

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

    p1 = 1 / odd1
    pX = 1 / oddX
    p2 = 1 / odd2

    total = p1 + pX + p2

    prob1 = p1 / total
    probX = pX / total
    prob2 = p2 / total

    #  xG
    xg_home = prob1 * 2.2
    xg_away = prob2 * 2.0

    #  buts
    goals_home = int(np.random.poisson(xg_home))
    goals_away = int(np.random.poisson(xg_away))

    goals_home = max(0, goals_home)
    goals_away = max(0, goals_away)

    score = f"{goals_home}-{goals_away}"

    #  BTTS
    btts = "OUI " if goals_home > 0 and goals_away > 0 else "NON "

    #  OVER / UNDER
    total_goals = goals_home + goals_away
    over25 = "OVER 2.5 " if total_goals >= 3 else "UNDER 2.5 "

    #  %
    prob1 = int(prob1 * 100)
    probX = int(probX * 100)
    prob2 = 100 - prob1 - probX

    #  value
    v1 = round((prob1/100 * odd1) - 1, 2)
    vX = round((probX/100 * oddX) - 1, 2)
    v2 = round((prob2/100 * odd2) - 1, 2)

    #  RETOUR COMPLET (TRÈS IMPORTANT)
    return prob1, probX, prob2, v1, vX, v2, score, over25, btts

    values = {"1": v1, "X": vX, "2": v2}

#  d'abord calculer best
    best = max(values, key=values.get)
    best_value = values[best]

#  ensuite utiliser best
    match_id = f"{team1}-{team2}-{best}"

if "combo" not in st.session_state:
    st.session_state.combo = []

#  ajouter uniquement les bons value bets
if best_value > 0.20:
    st.session_state.combo.append((team1, team2, best))

st.markdown("##  COMBINÉ DU JOUR")

combo = st.session_state.combo[:5]  # max 5 matchs

if len(combo) == 0:
    st.info("Pas de combiné disponible")
else:
    for match in combo:
        team1, team2, bet = match
        st.write(f" {team1} vs {team2} → {bet}")

    st.success(" Ticket combiné prêt à jouer !")

#  simulation résultat (placeholder)
result = np.random.choice(["WIN", "LOSS"])

st.session_state.results.append(result)

st.markdown("##  PERFORMANCE IA")

wins = st.session_state.results.count("WIN")
losses = st.session_state.results.count("LOSS")

total = len(st.session_state.results)

if total > 0:
    winrate = round((wins / total) * 100)

    col1, col2, col3 = st.columns(3)
    col1.metric(" Gagnés", wins)
    col2.metric(" Perdus", losses)
    col3.metric(" Winrate", f"{winrate}%")

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
for match in matches:

    #  sécurité
    if len(match) != 5:
        continue

    team1, team2, odd1, oddX, odd2 = match

    prob1, probX, prob2, v1, vX, v2, score, over25, btts = analyse_ultra_pro(
        odd1, oddX, odd2
    )

    html = f"""
    <div>
        <h3>{team1} vs {team2}</h3>
        <p>{score} | {over25} | {btts}</p>
    </div>
    """

    components.html(html, height=200)

    values = {"1": v1, "X": vX, "2": v2}

#  d'abord calculer best
    best = max(values, key=values.get)
    best_value = values[best]

#  ensuite utiliser best
    match_id = f"{team1}-{team2}-{best}"

for team1, team2, odd1, oddX, odd2 in matches:

    prob1, probX, prob2, v1, vX, v2, score, over25, btts = analyse_ultra_pro(
        odd1, oddX, odd2
    )

    values = {"1": v1, "X": vX, "2": v2}

    best = max(values, key=values.get)
    best_value = values[best]

    match_id = f"{team1}-{team2}-{best}"

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

numeric = [1 if r == "WIN" else 0 for r in st.session_state.results]

if len(numeric) > 2:
   

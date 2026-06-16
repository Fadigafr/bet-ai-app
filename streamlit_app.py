import streamlit as st
import numpy as np
import streamlit.components.v1 as components
import requests

st.set_page_config(page_title="BET AI PRO", layout="centered")

# =========================
# LOGIN
# =========================
if "logged" not in st.session_state:
    st.session_state.logged = False

st.markdown("##  Connexion BET AI PRO")

password = st.text_input("Mot de passe", type="password", key="vip")

if st.button("Se connecter"):
    if password == "VIP123":
        st.session_state.logged = True
        st.success(" Connexion réussie")
    else:
        st.error(" Mot de passe incorrect")

if not st.session_state.logged:
    st.warning(" Connecte-toi pour accéder à l'application")
    st.stop()

if not users[current_user]["vip"]:
    st.warning(" Accès VIP requis")
    st.stop()

# =========================
# MATCH DATA
# =========================
def get_matches():

    url = "https://v3.football.api-sports.io/fixtures"

    headers = {
        "x-apisports-key": "TA_CLE_API"
    }

    params = {
        "league": 39,
        "season": 2023,
        "next": 5
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    matches = []

    for match in data["response"]:
        team1 = match["teams"]["home"]["name"]
        team2 = match["teams"]["away"]["name"]

        # simulation odds
        odd1 = round(np.random.uniform(1.5, 2.5), 2)
        oddX = round(np.random.uniform(2.5, 3.5), 2)
        odd2 = round(np.random.uniform(2.0, 4.0), 2)

        matches.append((team1, team2, odd1, oddX, odd2))

    return matches

matches = get_matches()

def get_team_stats(team_id):

    url = "https://v3.football.api-sports.io/teams/statistics"

    headers = {
        "x-apisports-key": "TA_CLE_API"
    }

    params = {
        "team": team_id,
        "season": 2023,
        "league": 39
    }

    return requests.get(url, headers=headers, params=params).json()
    
def get_matches():

    url = "https://v3.football.api-sports.io/fixtures"

    headers = {
        "x-apisports-key": "TA_CLE_API"
    }

    params = {
        "league": 39,   # Premier League
        "season": 2023,
        "next": 5       # prochains matchs
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    matches = []

    for match in data["response"]:
        team1 = match["teams"]["home"]["name"]
        team2 = match["teams"]["away"]["name"]

        #  cotes non incluses ici → on simule
        odd1 = round(np.random.uniform(1.5, 2.5), 2)
        oddX = round(np.random.uniform(2.5, 3.5), 2)
        odd2 = round(np.random.uniform(2.0, 4.0), 2)

        matches.append((team1, team2, odd1, oddX, odd2))

    return matches
# =========================
# IA VALUE
# =========================
def analyse_pro(odd1, oddX, odd2):

    #  convertir cotes en probabilités implicites
    p1 = 1 / odd1
    pX = 1 / oddX
    p2 = 1 / odd2

    total = p1 + pX + p2

    prob1 = int(p1 / total * 100)
    probX = int(pX / total * 100)
    prob2 = 100 - prob1 - probX

    #  calcul value
    v1 = round((prob1/100 * odd1) - 1, 2)
    vX = round((probX/100 * oddX) - 1, 2)
    v2 = round((prob2/100 * odd2) - 1, 2)

    return prob1, probX, prob2, v1, vX, v2

def predict_score(prob1, probX, prob2):

    if prob1 > 50:
        return "2-0"
    elif prob2 > 50:
        return "0-2"
    elif probX > 35:
        return "1-1"
    else:
        return "2-1"

def analyse_market(prob1, probX, prob2):

    goals_expect = (prob1 + prob2) / 2

    over25 = "OVER 2.5 " if goals_expect > 50 else "UNDER 2.5 "
    btts = "OUI " if prob1 > 40 and prob2 > 40 else "NON "

    return over25, btts

def predict_scorer(team1):

    scorers_db = {
        "PSG": ["Mbappé"],
        "Real Madrid": ["Vinicius"],
        "Chelsea": ["Jackson"],
        "Arsenal": ["Saka"]
    }

    return np.random.choice(scorers_db.get(team1, ["Top Player"]))

def analyse_real(odd1, oddX, odd2):

    #  base logique réelle
    prob1 = int(100 / odd1)
    probX = int(100 / oddX)
    prob2 = int(100 / odd2)

    total = prob1 + probX + prob2

    prob1 = int(prob1 / total * 100)
    probX = int(probX / total * 100)
    prob2 = 100 - prob1 - probX

    v1 = round((prob1/100 * odd1) - 1, 2)
    vX = round((probX/100 * oddX) - 1, 2)
    v2 = round((prob2/100 * odd2) - 1, 2)

    return prob1, probX, prob2, v1, vX, v2

league_dict = {
    "Premier League": 39,
    "La Liga": 140,
    "Ligue 1": 61
}

league_name = st.selectbox(
    "Choisir une ligue",
    list(league_dict.keys()),
    key="league_select_1"
)

market_type = st.selectbox(
    "Type de pari",
    ["1X2", "Over/Under", "BTTS"],
    key="market_select"
)

league = st.selectbox("Choisir une ligue", {...}, key="league")

team = st.selectbox("Choisir équipe", [...], key="team")

market = st.selectbox("Type pari", [...], key="market")

params = {
    "league": league,
    "season": 2023,
    "next": 5
}

def get_live_matches(api_key, league_id):

    url = "https://v3.football.api-sports.io/fixtures"

    headers = {
        "x-apisports-key": api_key
    }

    params = {
        "league": league_id,
        "live": "all"
    }

    res = requests.get(url, headers=headers, params=params)
    data = res.json()

    live_matches = []

    for match in data["response"]:
        team1 = match["teams"]["home"]["name"]
        team2 = match["teams"]["away"]["name"]

        score1 = match["goals"]["home"]
        score2 = match["goals"]["away"]

        minute = match["fixture"]["status"]["elapsed"]

        live_matches.append((team1, team2, score1, score2, minute))

    return live_matches

    url = "https://v3.football.api-sports.io/fixtures"

    headers = {"x-apisports-key": api_key}

    params = {
        "league": league_id,
        "live": "all"
}
    
st.markdown("##  MATCHS LIVE")

live_data = get_live_matches("TA_CLE_API", league)

for team1, team2, s1, s2, minute in live_data:

    st.markdown(f"""
     {team1} vs {team2}  
     Score : {s1} - {s2}  
     {minute}'
    """)

def get_standings_safe():

    return [
        {"position": 1, "team": "Manchester City", "points": 89},
        {"position": 2, "team": "Arsenal", "points": 84},
        {"position": 3, "team": "Liverpool", "points": 80},
        {"position": 4, "team": "Chelsea", "points": 70},
    ]

st.markdown("##  CLASSEMENT")

standings = get_standings_safe()

for team in standings[:10]:
    st.write(f"{team['position']} - {team['team']} ({team['points']} pts)")

st.markdown("""
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body {
    zoom: 0.9;
}
</style>
""", unsafe_allow_html=True)


# =========================
# IA ADVANCED
# =========================
def analyse_advanced(team1, team2):
    goals_home = np.random.randint(0, 4)
    goals_away = np.random.randint(0, 4)

    total_goals = goals_home + goals_away

    over25 = "OVER 2.5 " if total_goals >= 3 else "UNDER 2.5 "
    btts = "OUI " if goals_home > 0 and goals_away > 0 else "NON "
    score = f"{goals_home} - {goals_away}"

    scorers = ["Mbappé", "Haaland", "Benzema", "Vinicius", "Salah"]
    scorer = np.random.choice(scorers)

    return over25, btts, score, scorer

def analyse_super_pro(odd1, oddX, odd2):

    #  probabilités implicites
    p1 = 1 / odd1
    pX = 1 / oddX
    p2 = 1 / odd2

    total = p1 + pX + p2

    prob1 = round((p1 / total) * 100)
    probX = round((pX / total) * 100)
    prob2 = 100 - prob1 - probX

    #  score
    if prob1 > 55:
        score = "2-0"
    elif prob2 > 55:
        score = "0-2"
    elif probX > 35:
        score = "1-1"
    else:
        score = "2-1"

    #  over / under
    expected_goals = (prob1 + prob2) / 2
    over25 = "OVER 2.5 " if expected_goals > 50 else "UNDER 2.5 "

    #  BTTS
    btts = "OUI " if prob1 > 40 and prob2 > 40 else "NON "

    #  value
    v1 = round((prob1/100 * odd1) - 1, 2)
    vX = round((probX/100 * oddX) - 1, 2)
    v2 = round((prob2/100 * odd2) - 1, 2)

    return prob1, probX, prob2, v1, vX, v2, score, over25, btts

for match in matches:

    if len(match) == 5:
        team1, team2, odd1, oddX, odd2 = match
    else:
        continue

    prob1, probX, prob2, v1, vX, v2, score, over25, btts = analyse_super_pro(
        odd1, oddX, odd2
    )

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
st.markdown("##  DASHBOARD BET AI PRO")

total_matches = len(matches)
over_count = 0
btts_count = 0

# =========================
# LOOP MATCH
# =========================

def analyse_super_pro(odd1, oddX, odd2):

    p1 = 1 / odd1
    pX = 1 / oddX
    p2 = 1 / odd2

    total = p1 + pX + p2

    prob1 = round((p1 / total) * 100)
    probX = round((pX / total) * 100)
    prob2 = 100 - prob1 - probX

    #  score intelligent
    if prob1 > 55:
        score = "2-0"
    elif prob2 > 55:
        score = "0-2"
    elif probX > 35:
        score = "1-1"
    else:
        score = "2-1"

    #  markets
    expected_goals = (prob1 + prob2) / 2
    over25 = "OVER 2.5 " if expected_goals > 50 else "UNDER 2.5 "
    btts = "OUI " if prob1 > 40 and prob2 > 40 else "NON "

    #  value
    v1 = round((prob1/100 * odd1) - 1, 2)
    vX = round((probX/100 * oddX) - 1, 2)
    v2 = round((prob2/100 * odd2) - 1, 2)

    return prob1, probX, prob2, v1, vX, v2, score, over25, btts
for team1, team2, odd1, oddX, odd2 in matches:

    prob1, probX, prob2, v1, vX, v2 = analyse_pro(odd1, oddX, odd2)

    values = {"1": v1, "X": vX, "2": v2}
    best = max(values, key=values.get)
    best_value = values[best]

    #  BON ALIGNEMENT
    match_id = f"{team1}-{team2}-{best}"

    #  MEME NIVEAU
    if best_value > 0.20:

        message = f"{team1} vs {team2} → {best} ({best_value})"

        send_telegram(message)

        sent_alerts.add(match_id)

    # SCORE
    score = predict_score(prob1, probX, prob2)

    # OVER / BTTS
    over25, btts = analyse_market(prob1, probX, prob2)

    # BUTEUR
    scorer = predict_scorer(team1)

    # UI

for team1, team2, odd1, oddX, odd2 in matches:

    prob1, probX, prob2, v1, vX, v2, score, over25, btts = analyse_super_pro(
        odd1, oddX, odd2
    )

    #  dictionnaire valeurs correct
    values = {
        "1": v1,
        "X": vX,
        "2": v2
    }

    best = max(values, key=values.get)
    best_value = values[best]

    html = f"""
    <div style="background:#020617;padding:20px;border-radius:15px;margin-bottom:15px;color:white;">
        <h3 {team1} vs {team2}</h3>
        <p> {prob1}% | {probX}% | {prob2}%</p>
        <p> Score : <b>{score}</b></p>
        <p> {over25}</p>
        <p> {btts}</p>
    </div>
    """

    components.html(html, height=240)

    #  indentation obligatoire
    prob1, probX, prob2, v1, vX, v2, score, over25, btts = analyse_super_pro(
        odd1, oddX, odd2
    )

    # TELEGRAM
 
for team1, team2, odd1, oddX, odd2 in matches:

    prob1, probX, prob2, v1, vX, v2 = analyse_pro(odd1, oddX, odd2)

    values = {"1": v1, "X": vX, "2": v2}
    best = max(values, key=values.get)
    best_value = values[best]

    match_id = f"{team1}-{team2}-{best}"

    if best_value > 0.20:
        st.write(match_id)

        message = f"""
  BET AI PRO

  {team1} vs {team2}
  Choix : {best}
  Value : {best_value}
"""

        send_telegram(message)
        sent_alerts.add(match_id)

    prob1, probX, prob2, v1, vX, v2 = analyse_pro(odd1, oddX, odd2)

    values = {"1": v1, "X": vX, "2": v2}
    best = max(values, key=values.get)
    best_value = values[best]

# =========================
# STATS
# =========================
st.markdown("##  STATISTIQUES")

c1, c2, c3 = st.columns(3)

c1.metric("Matchs", total_matches)
c2.metric("Over 2.5", over_count)
c3.metric("BTTS", btts_count)

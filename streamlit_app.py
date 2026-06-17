import streamlit as st
import numpy as np
import requests
import streamlit.components.v1 as components

def get_teams(api_key, competition_id):

    url = "https://v3.football.api-sports.io/teams"

    headers = {
        "x-apisports-key": api_key
    }

    params = {
        "league": competition_id,
        "season": 2024
    }

    res = requests.get(url, headers=headers, params=params)
    data = res.json()

    teams = []

    if "response" in data:
        for t in data["response"]:
            teams.append(t["team"]["name"])

    return teams

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

if "bankroll" not in st.session_state:
    st.session_state.bankroll = 100  #  capital initial

if "history_gain" not in st.session_state:
    st.session_state.history_gain = []

# =========================
# USERS
# =========================
users = {
    "admin": {"password": "VIP123", "vip": True},
    "user": {"password": "1234", "vip": False}

}

stake = st.number_input("💸 Mise (€)", min_value=1, max_value=100, value=10)


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
    # Ligues
    "🏴 Premier League": 39,
    "🇪🇸 La Liga": 140,
    "🇫🇷 Ligue 1": 61,

    # Coupes internationales
    "🌍 Coupe du Monde": 1,
    "🌍 Coupe du Monde 2026": 1,
    "🏆 CAN (Afrique)": 6,
    "🏆 Copa America": 9,
    "🏆 Euro": 4,
}
competition_name = st.selectbox(
    "🏆 Choisir une compétition",
    list(competitions.keys())
)

competition_id = competitions[competition_name]

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

for team1, team2, odd1, oddX, odd2 in matches:

    prob1, probX, prob2, v1, vX, v2, score, over25, btts = analyse_ultra_pro(
        odd1, oddX, odd2
    )

    values = {"1": v1, "X": vX, "2": v2}

    best = max(values, key=values.get)
    best_value = values[best]

    # ✅ ICI uniquement
    if best_value > 0.20:
        st.write(f"🔥 VALUE BET: {team1} vs {team2} → {best}")
    
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

st.markdown("##  BANKROLL")

col1, col2 = st.columns(2)

col1.metric(" Capital actuel", f"{round(st.session_state.bankroll,2)} €")
col2.metric(" Profit", f"{round(st.session_state.bankroll - 100,2)} €")

st.markdown("## 💰 DASHBOARD FINANCIER")

profit = st.session_state.bankroll - 100

col1, col2, col3 = st.columns(3)

col1.metric("💳 Bankroll", f"{round(st.session_state.bankroll,2)} €")
col2.metric("📈 Profit", f"{round(profit,2)} €")
col3.metric("🎯 ROI", f"{round((profit/100)*100,1)} %")


# =========================
# LOOP MATCHES
# =========================
def get_teams(api_key, competition_id):

    import requests

    url = "https://v3.football.api-sports.io/teams"

    headers = {
        "x-apisports-key": api_key
    }

    params = {
        "league": competition_id,
        "season": 2024
    }

    try:
        res = requests.get(url, headers=headers, params=params)
        data = res.json()

        teams = []

        if "response" in data and len(data["response"]) > 0:
            for t in data["response"]:
                teams.append(t["team"]["name"])

        return teams

    except:
        return []

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

def calculate_stake(bankroll, value):

    if value < 0.10:
        return 0

    elif value < 0.20:
        return bankroll * 0.05

    elif value < 0.40:
        return bankroll * 0.10

    else:
        return bankroll * 0.15

for team1, team2, odd1, oddX, odd2 in matches:

    # ✅ IA
    prob1, probX, prob2, v1, vX, v2, score, over25, btts = analyse_ultra_pro(
        odd1, oddX, odd2
    )

    # ✅ VALUE BET
    values = {"1": v1, "X": vX, "2": v2}
    best = max(values, key=values.get)
    best_value = values[best]

    # ✅ BANKROLL (mise intelligente)
    stake = calculate_stake(st.session_state.bankroll, best_value)

    # ✅ IGNORER mauvais bets
    if stake == 0:
        continue

    # ✅ simulation cote
    odd_simulated = round(np.random.uniform(1.5, 2.2), 2)

    # ✅ simulation résultat intelligent
    win_prob = 0.60 if best_value > 0.25 else 0.45
    result = np.random.choice(["WIN", "LOSS"], p=[win_prob, 1 - win_prob])

    # ✅ calcul gain/perte
    if result == "WIN":
        gain = stake * (odd_simulated - 1)
    else:
        gain = -stake

    # ✅ mise à jour bankroll
    st.session_state.bankroll += gain
    st.session_state.history_gain.append(st.session_state.bankroll)

    # ✅ affichage
    st.write(f"⚽ {team1} vs {team2}")
    st.write(f"✅ Choix: {best} | 💰 Value: {round(best_value,2)}")
    st.write(f"💸 Mise: {round(stake,2)}€ | 🎯 Résultat: {result}")
    st.write(f"📊 Gain: {round(gain,2)}€")
    st.write("---")

st.markdown("## 💰 BANKROLL")

profit = st.session_state.bankroll - 100

col1, col2 = st.columns(2)

col1.metric("💳 Capital", f"{round(st.session_state.bankroll,2)} €")
col2.metric("📈 Profit", f"{round(profit,2)} €")

if len(st.session_state.history_gain) > 2:
    st.line_chart(st.session_state.history_gain)

teams = get_teams(API_KEY, competition_id)

st.markdown("## ⚽ ÉQUIPES")

for team in teams:
    st.write(f"✅ {team}")

season = st.selectbox(
    "📅 Choisir une année",
    [2024, 2025, 2026, 2027]
)

calendar = get_calendar(API_KEY, competition_id, season)

st.markdown(f"## 📅 CALENDRIER {season}")

if len(calendar) == 0:
    st.warning("Pas de données disponibles")
else:
    for date, t1, t2 in calendar[:20]:
        st.write(f"📆 {date} → {t1} vs {t2}")

def get_teams(api_key, competition_id):

    url = "https://v3.football.api-sports.io/teams"

    headers = {"x-apisports-key": api_key}

    params = {
        "league": competition_id,
        "season": 2024
    }

    res = requests.get(url, headers=headers, params=params)
    data = res.json()

    teams = []

    if "response" in data:
        for t in data["response"]:
            teams.append(t["team"]["name"])

    return teams

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

def calculate_stake(bankroll, value):

    if value < 0.10:
        return 0

    elif value < 0.20:
        return bankroll * 0.05

    elif value < 0.40:
        return bankroll * 0.10

    else:
        return bankroll * 0.15

    message = f"""
  BET AI PRO

  {team1} vs {team2}
  Choix : {best}
  Value : {best_value}
"""

    send_telegram(message)
    st.session_state.combo.append((team1, team2, best))

if len(st.session_state.history_gain) > 2:
    st.line_chart(st.session_state.history_gain)

st.markdown("## 🔗 COMBINÉ PRO")

combo = st.session_state.combo[:5]

total_odds = 1

for team1, team2, bet in combo:
    odd = round(np.random.uniform(1.3, 2.2), 2)
    total_odds *= odd
    st.write(f"✅ {team1} vs {team2} → {bet} ({odd})")

if len(combo) > 0:
    potential_gain = stake * total_odds
    st.success(f"💰 Gain potentiel: {round(potential_gain,2)} €")

# ✅ probabilité de gagner basée sur value
win_prob = 0.55 if best_value > 0.20 else 0.45

result = np.random.choice(["WIN", "LOSS"], p=[win_prob, 1 - win_prob])

# ✅ cote réelle simulée
odd = round(np.random.uniform(1.5, 2.2), 2)

if result == "WIN":
    gain = stake * (odd - 1)
else:
    gain = -stake

# ✅ mise à jour bankroll
st.session_state.bankroll += gain
st.session_state.history_gain.append(st.session_state.bankroll)

if st.session_state.bankroll <= 0:
    st.error("💀 Bankroll détruite ! Recharge nécessaire")
    st.stop

total_odds = 1

for match in combo:
    total_odds *= match[3]

potential_gain = total_odds * stake

if len(st.session_state.history_gain) > 2:
    st.line_chart(st.session_state.history_gain)

   

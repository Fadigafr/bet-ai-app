import streamlit as st
import numpy as np
import requests

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="BET AI PRO", layout="centered")

# =========================
# SESSION STATE
# =========================
if "logged" not in st.session_state:
    st.session_state.logged = False

if "user" not in st.session_state:
    st.session_state.user = None

if "bankroll" not in st.session_state:
    st.session_state.bankroll = 100.0

if "history_gain" not in st.session_state:
    st.session_state.history_gain = [100.0]

# =========================
# USERS
# =========================
users = {
    "admin": {"password": "VIP123", "vip": True},
    "user": {"password": "1234", "vip": False},
}

# =========================
# API KEY
# =========================
API_KEY = st.sidebar.text_input(
    "Clé API-Football",
    type="password",
    key="api_key_input"
)

# =========================
# LOGIN
# =========================
st.title("⚽ BET AI PRO")

if not st.session_state.logged:
    st.markdown("### 🔐 Connexion")

    username = st.text_input("Utilisateur", key="login_username")
    password = st.text_input("Mot de passe", type="password", key="login_password")

    if st.button("Se connecter", key="login_button"):
        if username in users and users[username]["password"] == password:
            st.session_state.logged = True
            st.session_state.user = username
            st.success("Connexion réussie")
            st.rerun()
        else:
            st.error("Accès refusé")

    st.stop()

current_user = st.session_state.user

if not users[current_user]["vip"]:
    st.warning("Accès VIP requis")
    st.markdown("Lien Paystack : https://paystack.com/pay/TON-LIEN")
    st.stop()

if st.sidebar.button("Se déconnecter", key="logout_button"):
    st.session_state.logged = False
    st.session_state.user = None
    st.rerun()

# =========================
# COMPÉTITIONS PAR PAYS
# =========================
countries = {
    "🌍 Tous": None,
    "🇬🇧 Angleterre": "England",
    "🇪🇸 Espagne": "Spain",
    "🇫🇷 France": "France",
    "🇩🇪 Allemagne": "Germany",
    "🇮🇹 Italie": "Italy",
    "🌍 International": "World",
    "🌍 Afrique": "Africa",
    "🌎 Amérique du Sud": "South America",
}

competitions = {
    "England": {
        "🏴 Premier League": 39,
        "🏴 FA Cup": 45,
    },
    "Spain": {
        "🇪🇸 La Liga": 140,
        "🇪🇸 Copa del Rey": 143,
    },
    "France": {
        "🇫🇷 Ligue 1": 61,
        "🇫🇷 Coupe de France": 66,
    },
    "Germany": {
        "🇩🇪 Bundesliga": 78,
    },
    "Italy": {
        "🇮🇹 Serie A": 135,
        "🇮🇹 Coppa Italia": 137,
    },
    "World": {
        "🌍 Coupe du Monde": 1,
        "🌍 Coupe du Monde 2026": 1,
        "🏆 Euro": 4,
    },
    "Africa": {
        "🏆 CAN": 6,
    },
    "South America": {
        "🏆 Copa America": 9,
    },
}

country_name = st.selectbox(
    "🌍 Choisir un pays / zone",
    list(countries.keys()),
    key="country_filter"
)

selected_country = countries[country_name]

if selected_country is None:
    filtered_competitions = {}

    for comp_group in competitions.values():
        filtered_competitions.update(comp_group)
else:
    filtered_competitions = competitions.get(selected_country, {})

if not filtered_competitions:
    st.warning("Aucune compétition disponible pour ce choix.")
    st.stop()

competition_name = st.selectbox(
    "🏆 Choisir une compétition",
    list(filtered_competitions.keys()),
    key="competition_filter"
)

competition_id = filtered_competitions[competition_name]

season = st.selectbox(
    "📅 Choisir une saison",
    [2024, 2025, 2026, 2027],
    index=2,
    key="season_filter"
)

st.markdown(f"## {competition_name} - Saison {season}")

# =========================
# API FUNCTIONS
# =========================
def api_get(url, params):
    if not API_KEY:
        return {}

    headers = {
        "x-apisports-key": API_KEY
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        return response.json()
    except Exception:
        return {}


def get_teams(competition_id, season):
    url = "https://v3.football.api-sports.io/teams"

    params = {
        "league": competition_id,
        "season": season
    }

    data = api_get(url, params)

    teams = []

    for item in data.get("response", []):
        team_name = item.get("team", {}).get("name")
        if team_name:
            teams.append(team_name)

    return teams


def get_calendar(competition_id, season):
    url = "https://v3.football.api-sports.io/fixtures"

    params = {
        "league": competition_id,
        "season": season,
        "next": 20
    }

    data = api_get(url, params)

    calendar = []

    for match in data.get("response", []):
        date = match.get("fixture", {}).get("date", "")[:10]
        home = match.get("teams", {}).get("home", {}).get("name", "")
        away = match.get("teams", {}).get("away", {}).get("name", "")

        if home and away:
            calendar.append((date, home, away))

    return calendar


def get_matches(competition_id, season):
    calendar = get_calendar(competition_id, season)

    matches = []

    for _, home, away in calendar[:10]:
        odd1 = round(np.random.uniform(1.5, 2.6), 2)
        oddX = round(np.random.uniform(2.7, 3.8), 2)
        odd2 = round(np.random.uniform(1.8, 4.5), 2)

        matches.append((home, away, odd1, oddX, odd2))

    if not matches:
        matches = [
            ("PSG", "Marseille", 1.80, 3.30, 4.20),
            ("Real Madrid", "Barcelone", 1.90, 3.10, 3.70),
            ("Chelsea", "Arsenal", 2.00, 3.20, 3.50),
        ]

    return matches

# =========================
# IA FUNCTIONS
# =========================
def analyse_ultra_pro(odd1, oddX, odd2):
    p1 = 1 / odd1
    pX = 1 / oddX
    p2 = 1 / odd2

    total = p1 + pX + p2

    prob1_float = p1 / total
    probX_float = pX / total
    prob2_float = p2 / total

    xg_home = prob1_float * 2.2
    xg_away = prob2_float * 2.0

    goals_home = int(np.random.poisson(xg_home))
    goals_away = int(np.random.poisson(xg_away))

    score = f"{goals_home}-{goals_away}"

    if goals_home > 0 and goals_away > 0:
        btts = "OUI"
    else:
        btts = "NON"

    total_goals = goals_home + goals_away

    if total_goals >= 3:
        over25 = "OVER 2.5"
    else:
        over25 = "UNDER 2.5"

    prob1 = int(prob1_float * 100)
    probX = int(probX_float * 100)
    prob2 = 100 - prob1 - probX

    v1 = round((prob1 / 100 * odd1) - 1, 2)
    vX = round((probX / 100 * oddX) - 1, 2)
    v2 = round((prob2 / 100 * odd2) - 1, 2)

    return prob1, probX, prob2, v1, vX, v2, score, over25, btts


def calculate_stake(bankroll, value):
    if value < 0.10:
        return 0

    if value < 0.20:
        return bankroll * 0.05

    if value < 0.40:
        return bankroll * 0.10

    return bankroll * 0.15

# =========================
# ÉQUIPES
# =========================
with st.expander("⚽ Liste des équipes"):
    teams = get_teams(competition_id, season)

    if teams:
        for team in teams:
            st.write(f"✅ {team}")
    else:
        st.info("Aucune équipe disponible via API pour cette compétition/saison.")

# =========================
# CALENDRIER
# =========================
with st.expander("📅 Calendrier des matchs"):
    calendar = get_calendar(competition_id, season)

    if calendar:
        for date, home, away in calendar:
            st.write(f"📆 {date} → {home} vs {away}")
    else:
        st.info("Calendrier indisponible via API. Des matchs de démonstration seront utilisés.")

# =========================
# MATCHES
# =========================
matches = get_matches(competition_id, season)

st.markdown("## 📊 Dashboard prédictions")

combo = []
signals = 0

for team1, team2, odd1, oddX, odd2 in matches:
    prob1, probX, prob2, v1, vX, v2, score, over25, btts = analyse_ultra_pro(
        odd1, oddX, odd2
    )

    values = {
        "1": v1,
        "X": vX,
        "2": v2
    }

    best = max(values, key=values.get)
    best_value = values[best]

    stake = calculate_stake(st.session_state.bankroll, best_value)

    if best_value > 0.20:
        combo.append((team1, team2, best, odd1 if best == "1" else oddX if best == "X" else odd2))
        signals += 1

    st.markdown("---")
    st.subheader(f"⚽ {team1} vs {team2}")

    col1, col2, col3 = st.columns(3)

    col1.metric("1", f"{prob1}%")
    col2.metric("X", f"{probX}%")
    col3.metric("2", f"{prob2}%")

    st.write(f"💰 Cotes : 1={odd1} | X={oddX} | 2={odd2}")
    st.write(f"✅ Meilleur choix : {best}")
    st.write(f"🔥 Value : {best_value}")
    st.write(f"⚽ Score exact probable : {score}")
    st.write(f"📈 Over/Under : {over25}")
    st.write(f"🤝 Les deux équipes marquent : {btts}")
    st.write(f"💸 Mise conseillée : {round(stake, 2)} €")

# =========================
# COMBINÉ
# =========================
st.markdown("## 🔗 Combiné automatique")

if not combo:
    st.info("Aucun combiné disponible pour le moment.")
else:
    total_odds = 1

    for team1, team2, bet, odd in combo[:5]:
        total_odds *= odd
        st.write(f"✅ {team1} vs {team2} → {bet} @ {odd}")

    potential_gain = total_odds * 10

    st.success(f"Cote totale estimée : {round(total_odds, 2)}")
    st.success(f"Gain potentiel pour 10€ : {round(potential_gain, 2)} €")

# =========================
# BANKROLL
# =========================
st.markdown("## 💳 Bankroll")

profit = st.session_state.bankroll - 100

col1, col2, col3 = st.columns(3)

col1.metric("Capital", f"{round(st.session_state.bankroll, 2)} €")
col2.metric("Profit", f"{round(profit, 2)} €")
col3.metric("Signaux", signals)

if len(st.session_state.history_gain) > 2:
    st.line_chart(st.session_state.history_gain)

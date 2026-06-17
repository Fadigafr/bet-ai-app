import streamlit as st
import numpy as np
import requests

# =========================
# RAPIDAPI FOOTBALL
# =========================
RAPIDAPI_KEY = st.secrets.get("RAPIDAPI_KEY", "")
RAPIDAPI_HOST = "free-api-live-football-data.p.rapidapi.com"


def rapidapi_get(endpoint, params):
    url = f"https://free-api-live-football-data.p.rapidapi.com/{endpoint}"

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST,
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=15
        )

        if response.status_code != 200:
            st.error(f"Erreur API : {response.status_code}")
            st.write(response.text)
            return []

        return response.json()

    except Exception as e:
        st.error(f"Erreur connexion API : {e}")
        return []


def search_players(search_text):
    return rapidapi_get(
        "football-players-search",
        {"search": search_text}
    )


def search_teams(search_text):
    return rapidapi_get(
        "football-teams-search",
        {"search": search_text}
    )


# =========================
# CONFIG
# =========================
st.set_page_config(page_title="BET AI PRO", layout="centered")

# =========================
# STYLE API FOOTBALL
# =========================
st.markdown("""
<style>
.api-card {
    background: linear-gradient(135deg, #020617, #0f172a);
    padding: 18px;
    border-radius: 16px;
    margin-bottom: 14px;
    color: white;
    border: 1px solid rgba(34, 197, 94, 0.25);
    box-shadow: 0 0 18px rgba(34, 197, 94, 0.12);
}

.api-title {
    font-size: 20px;
    font-weight: 800;
    color: #22c55e;
    margin-bottom: 8px;
}

.api-info {
    font-size: 14px;
    color: #cbd5e1;
    margin-bottom: 4px;
}

.api-badge {
    display: inline-block;
    background: #22c55e;
    color: #020617;
    padding: 4px 10px;
    border-radius: 999px;
    font-weight: 700;
    font-size: 12px;
    margin-top: 8px;
}
</style>
""", unsafe_allow_html=True)


def display_card(item, card_type="joueur"):
    if not isinstance(item, dict):
        st.markdown(f"""
        <div class="api-card">
            <div class="api-title">{item}</div>
            <span class="api-badge">{card_type.upper()}</span>
        </div>
        """, unsafe_allow_html=True)
        return

    name = (
        item.get("name")
        or item.get("player_name")
        or item.get("team_name")
        or item.get("title")
        or item.get("full_name")
        or "Nom indisponible"
    )

    team = (
        item.get("team")
        or item.get("club")
        or item.get("team_name")
        or item.get("current_team")
        or "Non disponible"
    )

    country = (
        item.get("country")
        or item.get("nationality")
        or item.get("country_name")
        or "Non disponible"
    )

    league = (
        item.get("league")
        or item.get("competition")
        or item.get("league_name")
        or "Non disponible"
    )

    st.markdown(f"""
    <div class="api-card">
        <div class="api-title">⚽ {name}</div>
        <div class="api-info">🏟️ Équipe / Club : {team}</div>
        <div class="api-info">🌍 Pays : {country}</div>
        <div class="api-info">🏆 Compétition : {league}</div>
        <span class="api-badge">{card_type.upper()}</span>
    </div>
    """, unsafe_allow_html=True)

# =========================
# RAPIDAPI FOOTBALL
# =========================
RAPIDAPI_KEY = st.secrets.get("RAPIDAPI_KEY", "")
RAPIDAPI_HOST = "free-api-live-football-data.p.rapidapi.com"


def rapidapi_get(endpoint, params):
    url = f"https://free-api-live-football-data.p.rapidapi.com/{endpoint}"

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST,
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=15
        )

        if response.status_code != 200:
            st.error(f"Erreur API : {response.status_code}")
            st.code(response.text)
            return []

        return response.json()

    except Exception as e:
        st.error(f"Erreur connexion API : {e}")
        return []


def search_players(search_text):
    return rapidapi_get(
        "football-players-search",
        {"search": search_text}
    )


def search_teams(search_text):
    return rapidapi_get(
        "football-teams-search",
        {"search": search_text}
    )


def extract_results(api_data):
    if isinstance(api_data, dict):
        if "response" in api_data:
            return api_data["response"]
        if "data" in api_data:
            return api_data["data"]
        if "results" in api_data:
            return api_data["results"]
        return [api_data]

    if isinstance(api_data, list):
        return api_data

    return []


def display_card(item, card_type="player"):
    if not isinstance(item, dict):
        st.markdown(f"""
        <div class="api-card">
            <div class="api-title">{item}</div>
            <span class="api-badge">{card_type.upper()}</span>
        </div>
        """, unsafe_allow_html=True)
        return

    name = (
        item.get("name")
        or item.get("player_name")
        or item.get("team_name")
        or item.get("title")
        or item.get("full_name")
        or "Nom indisponible"
    )

    team = (
        item.get("team")
        or item.get("club")
        or item.get("team_name")
        or item.get("current_team")
        or "Non disponible"
    )

    country = (
        item.get("country")
        or item.get("nationality")
        or item.get("country_name")
        or "Non disponible"
    )

    league = (
        item.get("league")
        or item.get("competition")
        or item.get("league_name")
        or "Non disponible"
    )

    st.markdown(f"""
    <div class="api-card">
        <div class="api-title">⚽ {name}</div>
        <div class="api-info">🏟️ Équipe / Club : {team}</div>


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
# FILTRE PAYS + COMPÉTITIONS
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
    "🌎 Amérique du Sud": "South America"
}

competitions_by_country = {
    "England": {
        "🏴 Premier League": 39,
        "🏴 FA Cup": 45
    },
    "Spain": {
        "🇪🇸 La Liga": 140,
        "🇪🇸 Copa del Rey": 143
    },
    "France": {
        "🇫🇷 Ligue 1": 61,
        "🇫🇷 Coupe de France": 66
    },
    "Germany": {
        "🇩🇪 Bundesliga": 78
    },
    "Italy": {
        "🇮🇹 Serie A": 135,
        "🇮🇹 Coppa Italia": 137
    },
    "World": {
        "🌍 Coupe du Monde": 1,
        "🏆 Euro": 4
    },
    "Africa": {
        "🏆 CAN": 6
    },
    "South America": {
        "🏆 Copa America": 9
    }
}

country_name = st.selectbox(
    "🌍 Choisir un pays",
    list(countries.keys()),
    key="country_select"
)

selected_country = countries[country_name]

if selected_country is None:
    filtered_competitions = {}

    for comp_group in competitions_by_country.values():
        filtered_competitions.update(comp_group)
else:
    filtered_competitions = competitions_by_country.get(selected_country, {})

if not filtered_competitions:
    st.warning("Aucune compétition disponible.")
    st.stop()

competition_name = st.selectbox(
    "🏆 Choisir une compétition",
    list(filtered_competitions.keys()),
    key="competition_select"
)

competition_id = filtered_competitions[competition_name]
        
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

st.markdown("## 🔎 Recherche équipe football")

team_search = st.text_input(
    "Entrer le nom de l'équipe",
    value="chelsea",
    key="team_search_input"
)

if st.button("Rechercher équipe", key="search_team_button"):
    teams_data = search_teams(team_search)

    st.markdown("### Résultats équipes")
    st.write(teams_data)

# =========================
# RECHERCHE API FOOTBALL
# =========================
st.markdown("## 🔎 Recherche Football Pro")

tab_players, tab_teams = st.tabs(["👤 Joueurs", "🏟️ Équipes"])


with tab_players:
    st.markdown("### 👤 Recherche joueur")

    player_search = st.text_input(
        "Nom du joueur",
        value="messi",
        key="player_search_input"
    )

    if st.button("🔍 Rechercher joueur", key="search_player_button"):
        if not RAPIDAPI_KEY:
            st.warning("Ajoute ta clé RAPIDAPI_KEY dans les secrets Streamlit.")
        else:
            players_data = search_players(player_search)
            players = extract_results(players_data)

            if not players:
                st.warning("Aucun joueur trouvé.")
            else:
                for player in players[:10]:
                    display_card(player, card_type="joueur")


with tab_teams:
    st.markdown("### 🏟️ Recherche équipe")

    team_search = st.text_input(
        "Nom de l'équipe",
        value="chelsea",
        key="team_search_input"
    )

    if st.button("🔍 Rechercher équipe", key="search_team_button"):
        if not RAPIDAPI_KEY:
            st.warning("Ajoute ta clé RAPIDAPI_KEY dans les secrets Streamlit.")
        else:
            teams_data = search_teams(team_search)
            teams = extract_results(teams_data)

            if not teams:
                st.warning("Aucune équipe trouvée.")
            else:
                for team in teams[:10]:
                    display_card(team, card_type="équipe")
    
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

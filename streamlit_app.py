import base64
from pathlib import Path
import numpy as np
import requests
import streamlit as st

# =====================================================
# CONFIGURATION APP
# =====================================================
st.set_page_config(page_title="BET AI PRO", layout="wide", page_icon="⚽")

DEFAULT_BANKROLL = 100.0
PAYSTACK_LINK = "https://paystack.com/pay/TON-LIEN"
RAPIDAPI_HOST = "free-api-live-football-data.p.rapidapi.com"

BACKGROUND_FILES = ["background.jpg", "fond.jpg", "2026-06-17 23.18.44.jpg"]
LOGO_FILES = ["logo.jpg", "banner.jpg", "2026-06-17 23.19.12.jpg"]

st.info(
    "BET AI PRO est un outil d’analyse et de prédiction football. "
    "Les résultats proposés sont des estimations statistiques et ne garantissent aucun gain. "
    "Les paris sportifs comportent un risque. "

    MAX_STAKE_PERCENT = 0.10  # maximum 10% de la bankroll par pari
STOP_LOSS_PERCENT = 0.30  # stop si perte de 30%

initial_bankroll = 100

if st.session_state.bankroll <= initial_bankroll * (1 - STOP_LOSS_PERCENT):
    st.error("⛔ Stop-loss atteint : arrête les paris aujourd’hui.")
    st.stop()
    
    USERS = {
    "admin": {"password": "VIP123", "vip": True},
    "user": {"password": "1234", "vip": False},
}

COUNTRIES = {
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

COMPETITIONS_BY_COUNTRY = {
    "England": {"🏴 Premier League": 39, "🏴 FA Cup": 45},
    "Spain": {"🇪🇸 La Liga": 140, "🇪🇸 Copa del Rey": 143},
    "France": {"🇫🇷 Ligue 1": 61, "🇫🇷 Coupe de France": 66},
    "Germany": {"🇩🇪 Bundesliga": 78},
    "Italy": {"🇮🇹 Serie A": 135, "🇮🇹 Coppa Italia": 137},
    "World": {"🌍 Coupe du Monde": 1, "🌍 Coupe du Monde 2026": 1, "🏆 Euro": 4},
    "Africa": {"🏆 CAN": 6},
    "South America": {"🏆 Copa America": 9},
}

DEMO_MATCHES = [
    ("PSG", "Marseille", 1.80, 3.30, 4.20),
    ("Real Madrid", "Barcelone", 1.90, 3.10, 3.70),
    ("Chelsea", "Arsenal", 2.00, 3.20, 3.50),
    ("Côte d'Ivoire", "Nigeria", 2.10, 3.00, 3.40),
]

# =====================================================
# UTILITAIRES IMAGE / STYLE
# =====================================================
def find_existing_file(file_names):
    for file_name in file_names:
        if Path(file_name).exists():
            return file_name
    return None


def image_to_base64(file_path):
    try:
        with open(file_path, "rb") as file:
            return base64.b64encode(file.read()).decode("utf-8")
    except Exception:
        return ""


def apply_style():
    background_file = find_existing_file(BACKGROUND_FILES)
    background_css = ""

    if background_file:
        encoded_background = image_to_base64(background_file)
        if encoded_background:
            background_css = f"""
            .stApp {{
                background-image:
                    linear-gradient(rgba(2, 6, 23, 0.80), rgba(2, 6, 23, 0.92)),
                    url('data:image/jpg;base64,{encoded_background}');
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            """

    css = """
    <style>
    __BACKGROUND_CSS__

    .block-container {
        max-width: 1150px;
        padding-top: 1.2rem;
    }

    .main-card {
        background: rgba(2, 6, 23, 0.82);
        border: 1px solid rgba(56, 189, 248, 0.25);
        box-shadow: 0 0 30px rgba(14, 165, 233, 0.16);
        border-radius: 22px;
        padding: 22px;
        margin-bottom: 18px;
        color: #e5e7eb;
        backdrop-filter: blur(8px);
    }

    .bet-title {
        font-size: 2.5rem;
        font-weight: 900;
        letter-spacing: 1px;
        color: #38bdf8;
        text-align: center;
        margin-bottom: 0.25rem;
        text-shadow: 0 0 18px rgba(56, 189, 248, 0.45);
    }

    .bet-subtitle {
        text-align: center;
        color: #cbd5e1;
        margin-bottom: 1rem;
    }

    .signal-good {
        color: #22c55e;
        font-size: 1.15rem;
        font-weight: 800;
    }

    .signal-low {
        color: #f97316;
        font-size: 1.15rem;
        font-weight: 800;
    }

    .mini-badge {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 999px;
        background: rgba(34, 197, 94, 0.15);
        color: #86efac;
        border: 1px solid rgba(34, 197, 94, 0.35);
        margin-right: 6px;
        margin-bottom: 6px;
        font-size: 0.88rem;
        font-weight: 700;
    }

    .stButton button {
        border-radius: 12px;
        font-weight: 800;
        border: 1px solid rgba(56, 189, 248, 0.45);
        background: linear-gradient(90deg, #0284c7, #22c55e);
        color: white;
    }
    </style>
    """.replace("__BACKGROUND_CSS__", background_css)

    st.markdown(css, unsafe_allow_html=True)


def show_logo():
    logo_file = find_existing_file(LOGO_FILES)

    if logo_file:
        st.image(logo_file, use_container_width=True)
    else:
        st.markdown('<div class="bet-title">⚽ BET AI PRO</div>', unsafe_allow_html=True)
        st.markdown('<div class="bet-subtitle">Prédictions football • Value Bet • Bankroll</div>', unsafe_allow_html=True)

# =====================================================
# SESSION STATE
# =====================================================
def init_session():
    defaults = {
        "logged": False,
        "user": None,
        "bankroll": DEFAULT_BANKROLL,
        "history_gain": [DEFAULT_BANKROLL],
        "manual_results": [],
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# =====================================================
# API RAPIDAPI
# =====================================================
def read_secret(name, default=""):
    try:
        return st.secrets.get(name, default)
    except Exception:
        return default


def get_rapidapi_key():
    secret_key = read_secret("RAPIDAPI_KEY", "")
    sidebar_key = st.sidebar.text_input("Clé RapidAPI", type="password", key="rapidapi_key_input")
    return sidebar_key or secret_key


def rapidapi_get(endpoint, params, api_key):
    if not api_key:
        return {}

    url = f"https://{RAPIDAPI_HOST}/{endpoint}"
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": RAPIDAPI_HOST,
        "Content-Type": "application/json",
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        if response.status_code != 200:
            return {"error": response.text, "status_code": response.status_code}
        return response.json()
    except Exception as exc:
        return {"error": str(exc), "status_code": 0}


def extract_results(api_data):
    if isinstance(api_data, dict):
        if "response" in api_data:
            return api_data.get("response", [])
        if "data" in api_data:
            return api_data.get("data", [])
        if "results" in api_data:
            return api_data.get("results", [])
        if api_data.get("error"):
            return []
        return [api_data]

    if isinstance(api_data, list):
        return api_data

    return []


def search_players(search_text, api_key):
    return rapidapi_get("football-players-search", {"search": search_text}, api_key)


def search_teams(search_text, api_key):
    return rapidapi_get("football-teams-search", {"search": search_text}, api_key)

# =====================================================
# DONNÉES APP
# =====================================================
def get_filtered_competitions(selected_country):
    if selected_country is None:
        filtered_competitions = {}
        for competition_group in COMPETITIONS_BY_COUNTRY.values():
            filtered_competitions.update(competition_group)
        return filtered_competitions

    return COMPETITIONS_BY_COUNTRY.get(selected_country, {})


def get_demo_matches():
    return DEMO_MATCHES

# =====================================================
# IA / BETTING
# =====================================================
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
    btts = "OUI" if goals_home > 0 and goals_away > 0 else "NON"
    over25 = "OVER 2.5" if goals_home + goals_away >= 3 else "UNDER 2.5"

    prob1 = int(prob1_float * 100)
    probX = int(probX_float * 100)
    prob2 = 100 - prob1 - probX

    v1 = round((prob1 / 100 * odd1) - 1, 2)
    vX = round((probX / 100 * oddX) - 1, 2)
    v2 = round((prob2 / 100 * odd2) - 1, 2)

    return prob1, probX, prob2, v1, vX, v2, score, over25, btts


def calculate_stake(bankroll, value):
    if value < 0.10:
        return 0.0
    if value < 0.20:
        return bankroll * 0.05
    if value < 0.40:
        return bankroll * 0.10
    return bankroll * 0.15


def selected_odd(best, odd1, oddX, odd2):
    if best == "1":
        return odd1
    if best == "X":
        return oddX
    return odd2

# =====================================================
# UI COMPONENTS
# =====================================================
def display_api_card(item, card_type="élément"):
    if not isinstance(item, dict):
        st.markdown(f"""
        <div class="main-card">
            <h3>{item}</h3>
            <span class="mini-badge">{card_type.upper()}</span>
        </div>
        """, unsafe_allow_html=True)
        return

    name = item.get("name") or item.get("player_name") or item.get("team_name") or item.get("title") or "Nom indisponible"
    team = item.get("team") or item.get("club") or item.get("current_team") or item.get("team_name") or "Non disponible"
    country = item.get("country") or item.get("nationality") or item.get("country_name") or "Non disponible"
    league = item.get("league") or item.get("competition") or item.get("league_name") or "Non disponible"

    st.markdown(f"""
    <div class="main-card">
        <h3>⚽ {name}</h3>
        <p>🏟️ Équipe / Club : {team}</p>
        <p>🌍 Pays : {country}</p>
        <p>🏆 Compétition : {league}</p>
        <span class="mini-badge">{card_type.upper()}</span>
    </div>
    """, unsafe_allow_html=True)


def display_match_card(team1, team2, prob1, probX, prob2, best, best_value, score, over25, btts, stake, odd1, oddX, odd2):
    color_class = "signal-good" if best_value > 0 else "signal-low"
    st.markdown(f"""
    <div class="main-card">
        <h2>⚽ {team1} vs {team2}</h2>
        <span class="mini-badge">1 : {prob1}% @ {odd1}</span>
        <span class="mini-badge">X : {probX}% @ {oddX}</span>
        <span class="mini-badge">2 : {prob2}% @ {odd2}</span>
        <p class="{color_class}">💰 Value Bet : {best} ({best_value})</p>
        <p>⚽ Score exact probable : <b>{score}</b></p>
        <p>📈 Over/Under : <b>{over25}</b></p>
        <p>🤝 Les deux équipes marquent : <b>{btts}</b></p>
        <p>💸 Mise conseillée : <b>{round(stake, 2)} €</b></p>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# MAIN APP
# =====================================================
def main():
    init_session()
    apply_style()
    show_logo()

    api_key = get_rapidapi_key()

    # -------------------------
    # LOGIN
    # -------------------------
    if not st.session_state.logged:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown("### 🔐 Connexion BET AI PRO")
        username = st.text_input("Utilisateur", key="login_user")
        password = st.text_input("Mot de passe", type="password", key="login_pass")

        if st.button("Se connecter", key="login_btn"):
            if username in USERS and USERS[username]["password"] == password:
                st.session_state.logged = True
                st.session_state.user = username
                st.success("Connexion réussie")
                st.rerun()
            else:
                st.error("Accès refusé")

        st.markdown('</div>', unsafe_allow_html=True)
        st.stop()

    current_user = st.session_state.user

    if not USERS[current_user]["vip"]:
        st.warning("Accès VIP requis")
        st.markdown(f"Paiement Paystack : {PAYSTACK_LINK}")
        st.stop()

    if st.sidebar.button("Se déconnecter", key="logout_btn"):
        st.session_state.logged = False
        st.session_state.user = None
        st.rerun()

    # -------------------------
    # SIDEBAR FILTERS
    # -------------------------
    st.sidebar.markdown("## ⚙️ Filtres")

    country_name = st.sidebar.selectbox("🌍 Pays / Zone", list(COUNTRIES.keys()), key="country_select")
    selected_country = COUNTRIES[country_name]
    filtered_competitions = get_filtered_competitions(selected_country)

    if not filtered_competitions:
        st.warning("Aucune compétition disponible.")
        st.stop()

    competition_name = st.sidebar.selectbox("🏆 Compétition", list(filtered_competitions.keys()), key="competition_select")
    season = st.sidebar.selectbox("📅 Saison", [2024, 2025, 2026, 2027], index=2, key="season_select")

    st.markdown(f"## 📊 Dashboard — {competition_name} ({season})")

    # -------------------------
    # SEARCH API
    # -------------------------
    with st.expander("🔎 Recherche API Football : joueurs et équipes"):
        tab_players, tab_teams = st.tabs(["👤 Joueurs", "🏟️ Équipes"])

        with tab_players:
            player_search = st.text_input("Nom du joueur", value="messi", key="player_search")
            if st.button("Rechercher joueur", key="player_btn"):
                if not api_key:
                    st.warning("Ajoute RAPIDAPI_KEY dans les secrets ou dans la sidebar.")
                else:
                    data = search_players(player_search, api_key)
                    results = extract_results(data)
                    if not results:
                        st.warning("Aucun joueur trouvé.")
                    for item in results[:10]:
                        display_api_card(item, "joueur")

        with tab_teams:
            team_search = st.text_input("Nom de l'équipe", value="chelsea", key="team_search")
            if st.button("Rechercher équipe", key="team_btn"):
                if not api_key:
                    st.warning("Ajoute RAPIDAPI_KEY dans les secrets ou dans la sidebar.")
                else:
                    data = search_teams(team_search, api_key)
                    results = extract_results(data)
                    if not results:
                        st.warning("Aucune équipe trouvée.")
                    for item in results[:10]:
                        display_api_card(item, "équipe")

    # -------------------------
    # MATCHES / PREDICTIONS
    # -------------------------
    matches = get_demo_matches()
    combo = []
    signals = 0

    for team1, team2, odd1, oddX, odd2 in matches:
        prob1, probX, prob2, v1, vX, v2, score, over25, btts = analyse_ultra_pro(odd1, oddX, odd2)

        values = {"1": v1, "X": vX, "2": v2}
        best = max(values, key=values.get)
        best_value = values[best]
        stake = calculate_stake(st.session_state.bankroll, best_value)

        if best_value > 0.20:
            combo.append((team1, team2, best, selected_odd(best, odd1, oddX, odd2)))
            signals += 1

        display_match_card(team1, team2, prob1, probX, prob2, best, best_value, score, over25, btts, stake, odd1, oddX, odd2)

if best_value < 0.10:
    risk_level = "ÉLEVÉ"
elif best_value < 0.25:
    risk_level = "MOYEN"
else:
    risk_level = "CONTRÔLÉ"

st.write(f"⚠️ Niveau de risque : {risk_level}")

    # -------------------------
    # COMBO
    # -------------------------
    st.markdown("## 🔗 Combiné automatique")

    if not combo:
        st.info("Aucun combiné disponible pour le moment.")
    else:
        total_odds = 1.0
        for team1, team2, bet, odd in combo[:5]:
            total_odds *= odd
            st.write(f"✅ {team1} vs {team2} → {bet} @ {odd}")

        st.success(f"Cote totale estimée : {round(total_odds, 2)}")
        st.success(f"Gain potentiel pour 10€ : {round(total_odds * 10, 2)} €")

    # -------------------------
    # BANKROLL
    # -------------------------
    st.markdown("## 💳 Bankroll")
    profit = st.session_state.bankroll - DEFAULT_BANKROLL

    col1, col2, col3 = st.columns(3)
    col1.metric("Capital", f"{round(st.session_state.bankroll, 2)} €")
    col2.metric("Profit", f"{round(profit, 2)} €")
    col3.metric("Signaux", signals)

    if len(st.session_state.history_gain) > 2:
        st.line_chart(st.session_state.history_gain)

if __name__ == "__main__":
    main()

MAX_STAKE_PERCENT = 0.10  # maximum 10% de la bankroll par pari
STOP_LOSS_PERCENT = 0.30  # stop si perte de 30%

initial_bankroll = 100

if st.session_state.bankroll <= initial_bankroll * (1 - STOP_LOSS_PERCENT):
    st.error("⛔ Stop-loss atteint : arrête les paris aujourd’hui.")
    st.stop()

    

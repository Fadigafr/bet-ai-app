import base64
from pathlib import Path

import numpy as np
import requests
import streamlit as st

# ==========================================
# CONFIG
# ==========================================
st.set_page_config(page_title="BET AI PRO", layout="wide", page_icon="⚽")

DEFAULT_BANKROLL = 100.0
MAX_STAKE_PERCENT = 0.10
STOP_LOSS_PERCENT = 0.30

RAPIDAPI_HOST = "free-api-live-football-data.p.rapidapi.com"

# ==========================================
# SESSION
# ==========================================
def init_session():
    if "bankroll" not in st.session_state:
        st.session_state.bankroll = DEFAULT_BANKROLL

# ==========================================
# STYLE + IMAGES
# ==========================================
def set_bg():
    if Path("background.jpg").exists():
        with open("background.jpg", "rb") as f:
            bg = base64.b64encode(f.read()).decode()

        st.markdown(f"""
        <style>
        .stApp {{
            background-image:
            linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.9)),
            url("data:image/jpg;base64,{bg}");
            background-size: cover;
        }}
        </style>
        """, unsafe_allow_html=True)

def show_logo():
    if Path("logo.jpg").exists():
        st.image("logo.jpg", use_container_width=True)
    else:
        st.title("⚽ BET AI PRO")

# ==========================================
# API
# ==========================================
def get_api_key():
    secret = ""
    try:
        secret = st.secrets.get("RAPIDAPI_KEY", "")
    except:
        pass

    sidebar = st.sidebar.text_input("Clé API", type="password")
    return sidebar or secret

def api_call(endpoint, params, api_key):
    if not api_key:
        return []

    url = f"https://{RAPIDAPI_HOST}/{endpoint}"

    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": RAPIDAPI_HOST
    }

    try:
        r = requests.get(url, headers=headers, params=params)
        return r.json()
    except:
        return []

# ==========================================
# IA PREDICTIONS
# ==========================================
def analyse_match(odd1, oddX, odd2):
    p1 = 1 / odd1
    pX = 1 / oddX
    p2 = 1 / odd2

    total = p1 + pX + p2

    prob1 = p1 / total
    probX = pX / total
    prob2 = p2 / total

    # Score simulé
    goals_home = np.random.poisson(prob1 * 2.2)
    goals_away = np.random.poisson(prob2 * 2.0)

    score = f"{goals_home}-{goals_away}"

    # Marchés
    btts = "OUI" if goals_home > 0 and goals_away > 0 else "NON"
    over25 = "OVER 2.5" if (goals_home + goals_away) >= 3 else "UNDER 2.5"

    # Value
    v1 = (prob1 * odd1) - 1
    vX = (probX * oddX) - 1
    v2 = (prob2 * odd2) - 1

    return (
        int(prob1*100),
        int(probX*100),
        int(prob2*100),
        round(v1,2),
        round(vX,2),
        round(v2,2),
        score,
        over25,
        btts
    )

def calculate_stake(bankroll, value):
    max_stake = bankroll * MAX_STAKE_PERCENT

    if value < 0.10:
        return 0
    elif value < 0.20:
        return min(bankroll * 0.05, max_stake)
    else:
        return min(bankroll * 0.1, max_stake)

# ==========================================
# MATCH DEMO
# ==========================================
matches = [
    ("PSG", "Marseille", 1.8, 3.3, 4.2),
    ("Real Madrid", "Barcelone", 1.9, 3.2, 3.5),
    ("Chelsea", "Arsenal", 2.0, 3.2, 3.3),
]

# ==========================================
# MAIN
# ==========================================
def main():
    init_session()
    set_bg()
    show_logo()

    st.info("⚠️ Outil d'analyse : aucun gain garanti. Risque de perte.")

    api_key = get_api_key()

    st.sidebar.title("⚙️ Options")

    # STOP LOSS
    if st.session_state.bankroll <= DEFAULT_BANKROLL * (1 - STOP_LOSS_PERCENT):
        st.error("⛔ Stop-loss atteint")
        st.stop()

    combo = []
    total_signals = 0

    for team1, team2, odd1, oddX, odd2 in matches:

        prob1, probX, prob2, v1, vX, v2, score, over25, btts = analyse_match(odd1, oddX, odd2)

        values = {"1": v1, "X": vX, "2": v2}
        best = max(values, key=values.get)
        best_value = values[best]

        stake = calculate_stake(st.session_state.bankroll, best_value)

        if best_value > 0.2:
            combo.append((team1, team2, best))
            total_signals += 1

        st.markdown(f"""
        ### ⚽ {team1} vs {team2}
        Probabilités : {prob1}% / {probX}% / {prob2}%
        
        ✅ Value Bet : {best} ({best_value})

        🎯 Score : {score}  
        📈 {over25}  
        🤝 BTTS : {btts}

        💰 Mise : {round(stake,2)}€
        """)

    # COMBO
    st.markdown("## 🔗 Combiné automatique")

    if combo:
        for c in combo:
            st.write(f"{c[0]} vs {c[1]} → {c[2]}")
    else:
        st.info("Aucun bon combiné")

    # BANKROLL
    st.markdown("## 💳 Bankroll")
    st.metric("Capital", f"{st.session_state.bankroll}€")
    st.metric("Signaux", total_signals)

# ==========================================
if __name__ == "__main__":
    main()

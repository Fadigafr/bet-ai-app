import base64
from pathlib import Path

import numpy as np
import requests
 CONFIGimport streamlit as st
# ==========================================
st.set_page_config(page_title="BET AI PRO+", layout="wide")

DEFAULT_BANKROLL = 100.0
MAX_STAKE = 0.10
STOP_LOSS = 0.30

# ==========================================
# SESSION
# ==========================================
if "bankroll" not in st.session_state:
    st.session_state.bankroll = DEFAULT_BANKROLL

# ==========================================
# UI DESIGN PRO
# ==========================================
def load_background():
    if Path("background.jpg").exists():
        with open("background.jpg", "rb") as f:
            bg = base64.b64encode(f.read()).decode()

        st.markdown(f"""
        <style>
        .stApp {{
            background-image:
            linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.95)),
            url("data:image/jpg;base64,{bg}");
            background-size: cover;
        }}

        .card {{
            background: rgba(15,23,42,0.85);
            padding: 18px;
            border-radius: 18px;
            margin-bottom: 15px;
            border: 1px solid rgba(56,189,248,0.25);
        }}

        .value {{
            color:#22c55e;
            font-weight:bold;
        }}

        .risk-high {{color:#ef4444;}}
        .risk-mid {{color:#f59e0b;}}
        .risk-low {{color:#22c55e;}}
        </style>
        """, unsafe_allow_html=True)

# ==========================================
# IA ENGINE
# ==========================================
def compute_probs(o1, oX, o2):
    p1, pX, p2 = 1/o1, 1/oX, 1/o2
    total = p1+pX+p2
    return p1/total, pX/total, p2/total

def poisson(p1, p2):
    return np.random.poisson(p1*2.3), np.random.poisson(p2*2.0)

def value(prob, odd):
    return prob*odd - 1

def kelly(bankroll, prob, odd):
    edge = prob*odd - 1
    if edge <= 0:
        return 0
    k = edge/(odd-1)
    return min(bankroll*k, bankroll*MAX_STAKE)

def confidence(v, p):
    score = (v*100)+(p*100)
    return max(0, min(100, round(score,1)))

def risk_level(conf):
    if conf < 40:
        return "🔴 ÉLEVÉ", "risk-high"
    elif conf < 65:
        return "🟠 MOYEN", "risk-mid"
    return "🟢 FAIBLE", "risk-low"

# ==========================================
# API ODDS (BOOKMAKERS)
# ==========================================
def fetch_odds(api_key):
    if not api_key:
        return []

    url = "https://api.odds-api.io/v3/odds"

    params = {
        "apiKey": api_key,
        "sport": "football",
        "league": "england-premier-league",
        "bookmakers": "Bet365,Betfair"
    }

    try:
        res = requests.get(url, params=params, timeout=10)
        data = res.json()

        matches = []

        for game in data.get("data", []):
            home = game["home"]
            away = game["away"]

            book = list(game["bookmakers"].values())[0]
            odds_data = book[0]["odds"][0]

            o1 = float(odds_data["home"])
            o2 = float(odds_data["away"])
            oX = 3.2

            matches.append((home, away, o1, oX, o2))

        return matches

    except:
        return []

# ==========================================
# FALLBACK
# ==========================================
def fallback_matches():
    return [
        ("PSG","Marseille",1.8,3.3,4.2),
        ("Real Madrid","Barcelone",1.9,3.2,3.6),
        ("Chelsea","Arsenal",2.1,3.1,3.3),
    ]

# ==========================================
# MAIN
# ==========================================
def main():
    load_background()

    st.title("⚽ BET AI PRO+ 🔥")
    st.warning("⚠️ Analyse IA – pas de garantie de gain")

    api_key = st.sidebar.text_input("Clé API Odds", type="password")

    bankroll = st.session_state.bankroll

    # STOP LOSS
    if bankroll <= DEFAULT_BANKROLL*(1-STOP_LOSS):
        st.error("⛔ Stop-loss atteint")
        st.stop()

    matches = fetch_odds(api_key)

    if not matches:
        st.info("Mode simulation activé")
        matches = fallback_matches()
    else:
        st.success("Cotes bookmakers chargées ✅")

    results = []
    combo = []

    # ======================================
    # LOOP MATCHES
    # ======================================
    for team1, team2, o1, oX, o2 in matches:

        p1, pX, p2 = compute_probs(o1,oX,o2)
        gh, ga = poisson(p1,p2)

        v1, vX, v2 = value(p1,o1), value(pX,oX), value(p2,o2)

        values = {"1":v1,"X":vX,"2":v2}
        best = max(values, key=values.get)
        best_value = values[best]

        probs = {"1":p1,"X":pX,"2":p2}
        prob = probs[best]

        conf = confidence(best_value, prob)
        stake = kelly(bankroll, prob, {"1":o1,"X":oX,"2":o2}[best])

        risk_text, risk_class = risk_level(conf)

        if conf > 65:
            combo.append((team1, team2, best))

        st.markdown(f"""
        <div class="card">
        <h3>⚽ {team1} vs {team2}</h3>

        📊 Prob : {int(p1*100)} / {int(pX*100)} / {int(p2*100)}<br>

        💸 Cotes :
        {o1} | {oX} | {o2}<br><br>

        💰 <span class="value">Value Bet : {best} ({round(best_value,2)})</span><br>

        🧠 Confiance : {conf}%<br>
        ⚠️ <span class="{risk_class}">Risque : {risk_text}</span><br>

        🎯 Score : {gh}-{ga}<br>
        📈 {'OVER 2.5' if gh+ga>=3 else 'UNDER 2.5'}<br>
        🤝 {'OUI' if gh>0 and ga>0 else 'NON'}<br>

        💸 Mise Kelly : {round(stake,2)}€
        </div>
        """, unsafe_allow_html=True)

        results.append((team1, team2, conf, best))

    # ======================================
    # TOP BETS
    # ======================================
    st.markdown("## 🧠 TOP PARIS")

    for r in sorted(results, key=lambda x:x[2], reverse=True):
        st.write(f"✅ {r[0]} vs {r[1]} → {r[3]} ({r[2]}%)")

    # ======================================
    # COMBO
    # ======================================
    st.markdown("## 🔗 COMBINÉ IA")

    if combo:
        for c in combo:
            st.write(f"{c[0]} vs {c[1]} → {c[2]}")
    else:
        st.info("Aucun combiné fiable")

    # ======================================
    # BANKROLL
    # ======================================
    st.markdown("## 💳 BANKROLL")

    st.metric("Capital", f"{round(bankroll,2)} €")

# ==========================================
if __name__ == "__main__":
    main()

# ==========================================

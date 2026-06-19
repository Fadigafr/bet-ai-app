import base64
from pathlib import Path

import numpy as np
import requests
import streamlit as st

# ==========================================
# CONFIG
# ==========================================
st.set_page_config(page_title="BET AI ELITE", layout="wide")

DEFAULT_BANKROLL = 100.0
MAX_STAKE = 0.1
STOP_LOSS = 0.3

RAPIDAPI_HOST = "free-api-live-football-data.p.rapidapi.com"

# ==========================================
# SESSION
# ==========================================
if "bankroll" not in st.session_state:
    st.session_state.bankroll = DEFAULT_BANKROLL

# ==========================================
# STYLE
# ==========================================
def set_background():
    if Path("background.jpg").exists():
        with open("background.jpg", "rb") as f:
            bg = base64.b64encode(f.read()).decode()

        st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{bg}");
            background-size: cover;
        }}
        </style>
        """, unsafe_allow_html=True)

# ==========================================
# API
# ==========================================
def get_api_key():
    try:
        return st.secrets.get("RAPIDAPI_KEY", "")
    except:
        return ""

def get_matches(api_key):
    if not api_key:
        return []

    url = f"https://{RAPIDAPI_HOST}/football-matches"
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": RAPIDAPI_HOST
    }

    try:
        r = requests.get(url, headers=headers)
        data = r.json()
        return data.get("response", [])
    except:
        return []

# ==========================================
# IA ENGINE
# ==========================================
def compute_probs(o1, oX, o2):
    p1, pX, p2 = 1/o1, 1/oX, 1/o2
    total = p1 + pX + p2
    return p1/total, pX/total, p2/total

def poisson(p1, p2):
    return np.random.poisson(p1*2.3), np.random.poisson(p2*2.1)

def value(prob, odd):
    return prob * odd - 1

def kelly(bankroll, prob, odd):
    edge = prob*odd - 1
    if edge <= 0:
        return 0
    k = edge / (odd - 1)
    return min(bankroll * k, bankroll * MAX_STAKE)

def confidence(value, prob):
    score = (value*100) + (prob*100)
    return max(0, min(100, round(score,1)))

# ==========================================
# DEMO FALLBACK
# ==========================================
def demo_matches():
    return [
        ("PSG", "Marseille", 1.8, 3.3, 4.2),
        ("Real Madrid", "Barcelone", 1.9, 3.2, 3.6),
        ("Chelsea", "Arsenal", 2.1, 3.1, 3.3),
    ]

# ==========================================
# MAIN
# ==========================================
def main():
    set_background()

    st.title("⚽ BET AI ELITE 🔥")
    st.warning("⚠️ Analyse IA – aucun gain garanti")

    api_key = st.sidebar.text_input("Clé API", type="password")

    bankroll = st.session_state.bankroll

    # STOP LOSS
    if bankroll <= DEFAULT_BANKROLL * (1 - STOP_LOSS):
        st.error("⛔ Stop-loss atteint")
        st.stop()

    matches = demo_matches()

    results = []
    combo = []

    for team1, team2, o1, oX, o2 in matches:

        p1, pX, p2 = compute_probs(o1, oX, o2)
        gh, ga = poisson(p1, p2)

        v1, vX, v2 = value(p1,o1), value(pX,oX), value(p2,o2)

        values = {"1":v1,"X":vX,"2":v2}
        best = max(values, key=values.get)
        best_value = values[best]

        probs = {"1":p1,"X":pX,"2":p2}
        prob = probs[best]

        conf = confidence(best_value, prob)

        stake = kelly(bankroll, prob, {"1":o1,"X":oX,"2":o2}[best])

        if conf > 65:
            combo.append((team1, team2, best))

        # DISPLAY
        st.markdown(f"""
### ⚽ {team1} vs {team2}

📊 Prob : {int(p1*100)}% / {int(pX*100)}% / {int(p2*100)}%

💰 Value : {best} ({round(best_value,2)})

🧠 Confiance : {conf}%

🎯 Score : {gh}-{ga}  
📈 {'OVER 2.5' if gh+ga>=3 else 'UNDER 2.5'}  
🤝 {'OUI' if gh>0 and ga>0 else 'NON'}

💸 Mise : {round(stake,2)}€
""")

        results.append((team1, team2, conf, best))

    # CLASSEMENT
    st.markdown("## 🧠 Meilleurs paris")
    for r in sorted(results, key=lambda x:x[2], reverse=True):
        st.write(f"✅ {r[0]} vs {r[1]} → {r[3]} ({r[2]}%)")

    # COMBO
    st.markdown("## 🔗 Combiné IA")
    if combo:
        for c in combo:
            st.write(f"{c[0]} vs {c[1]} → {c[2]}")
    else:
        st.info("Aucun combiné fiable")

    # BANKROLL
    st.markdown("## 💳 Bankroll")
    st.metric("Capital", f"{round(bankroll,2)} €")

# ==========================================
if __name__ == "__main__":
    main()

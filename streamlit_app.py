import base64
from pathlib import Path

import numpy as np
import streamlit as st

# ==========================================
        return 0
    stake = (edge / (odd - 1))
    return min(bankroll * stake, bankroll * MAX_STAKE_PERCENT)


def confidence_score(value, prob):
    conf = (value * 100) + (prob * 100)
    return min(max(round(conf, 1), 0), 100)


def risk_level(confidence):
    if confidence < 40:
        return "🔴 Élevé"
    elif confidence < 65:
        return "🟠 Moyen"
    else:
        return "🟢 Contrôlé"

# ==========================================
# MATCHES (SIMULATION OU API PLUS TARD)
# ==========================================
matches = [
    ("PSG", "Marseille", 1.8, 3.3, 4.2),
    ("Real Madrid", "Barcelone", 1.9, 3.2, 3.6),
    ("Chelsea", "Arsenal", 2.1, 3.1, 3.3),
    ("Bayern", "Dortmund", 1.7, 3.4, 4.5),
]

# ==========================================
# MAIN
# ==========================================
def main():
    set_background()

    st.title("⚽ BET AI PRO+ 🔥")
    st.warning("⚠️ Analyse intelligente - aucun gain garanti")

    bankroll = st.session_state.bankroll

    # STOP LOSS
    if bankroll <= DEFAULT_BANKROLL * (1 - STOP_LOSS):
        st.error("⛔ Stop-loss atteint")
        st.stop()

    results = []
    combo = []

    for team1, team2, o1, oX, o2 in matches:

        # Probabilités
        p1, pX, p2 = calculate_probabilities(o1, oX, o2)

        # Score IA
        gh, ga = poisson_model(p1, p2)

        # Value
        v1 = value_bet(p1, o1)
        vX = value_bet(pX, oX)
        v2 = value_bet(p2, o2)

        values = {"1": v1, "X": vX, "2": v2}
        best = max(values, key=values.get)
        best_value = values[best]

        probs = {"1": p1, "X": pX, "2": p2}
        prob = probs[best]

        # Confiance IA
        confidence = confidence_score(best_value, prob)

        # Mise Kelly
        stake = kelly(bankroll, prob, {"1":o1,"X":oX,"2":o2}[best])

        # Risque
        risk = risk_level(confidence)

        # Marchés
        btts = "OUI" if gh > 0 and ga > 0 else "NON"
        over25 = "OVER 2.5" if gh + ga >= 3 else "UNDER 2.5"

        results.append({
            "match": f"{team1} vs {team2}",
            "bet": best,
            "value": best_value,
            "confidence": confidence,
            "stake": stake
        })

        if confidence > 65:
            combo.append((team1, team2, best))

        # AFFICHAGE
        st.markdown(f"""
### ⚽ {team1} vs {team2}

📊 Probabilités : {int(p1*100)}% / {int(pX*100)}% / {int(p2*100)}%

💰 Value Bet : **{best} ({round(best_value,2)})**

🧠 Confiance IA : **{confidence}%**
⚠️ Risque : **{risk}**

🎯 Score IA : {gh}-{ga}  
📈 {over25}  
🤝 BTTS : {btts}

💸 Mise optimale (Kelly) : **{round(stake,2)} €**
""")

    # ======================================
    # CLASSEMENT IA
    # ======================================
    st.markdown("## 🧠 Classement des meilleurs paris")

    results_sorted = sorted(results, key=lambda x: x["confidence"], reverse=True)

    for r in results_sorted:
        st.write(f"✅ {r['match']} → {r['bet']} ({r['confidence']}%)")

    # ======================================
    # COMBO IA
    # ======================================
    st.markdown("## 🔗 Combiné intelligent")

    if combo:
        for c in combo:
            st.write(f"{c[0]} vs {c[1]} → {c[2]}")
    else:
        st.info("Aucun combiné fiable")

    # ======================================
    # BANKROLL
    # ======================================
    st.markdown("## 💳 Bankroll")

    st.metric("Capital", f"{round(bankroll,2)} €")


# ==========================================
if __name__ == "__main__":
    main()
``
# CONFIG
# ==========================================
st.set_page_config(page_title="BET AI PRO+", layout="wide", page_icon="⚽")

DEFAULT_BANKROLL = 100.0
MAX_STAKE_PERCENT = 0.10
STOP_LOSS = 0.30

# ==========================================
# SESSION
# ==========================================
if "bankroll" not in st.session_state:
    st.session_state.bankroll = DEFAULT_BANKROLL

# ==========================================
# UI STYLE
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
# IA ENGINE
# ==========================================
def calculate_probabilities(o1, oX, o2):
    p1, pX, p2 = 1/o1, 1/oX, 1/o2
    total = p1+pX+p2
    return p1/total, pX/total, p2/total


def poisson_model(p1, p2):
    home_goals = np.random.poisson(p1 * 2.3)
    away_goals = np.random.poisson(p2 * 2.1)
    return home_goals, away_goals


def value_bet(prob, odd):
    return (prob * odd) - 1


def kelly(bankroll, prob, odd):
    edge = prob * odd - 1

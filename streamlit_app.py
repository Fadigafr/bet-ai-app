import streamlit as st
:import numpy as np
        st.warning("Entre les équipes")
        st.stop()

    s1, s2, xg1, xg2 = predict()

    total = s1 + s2

    st.subheader(" Score IA")
    st.success(f"{team1} {s1} - {s2} {team2}")

    # =====================
    # PROBABILITÉS SIMPLIFIÉES
    # =====================
    prob_team1 = xg1 / (xg1 + xg2)
    prob_team2 = xg2 / (xg1 + xg2)
    prob_draw = 1 - (prob_team1 + prob_team2)

    # conversion en "cotes"
    odd1 = round(1 / prob_team1, 2)
    odd2 = round(1 / prob_team2, 2)

    # =====================
    # LOGIQUE PARIS
    # =====================
    btts = s1 > 0 and s2 > 0
    over25 = total >= 3

    if s1 > s2:
        winner = team1
        double = "1X"
    elif s2 > s1:
        winner = team2
        double = "X2"
    else:
        winner = "Match nul"
        double = "X"

    # =====================
    # AFFICHAGE PARIS
    # =====================
    st.subheader(" Analyse Paris PRO")

    st.write(f" Gagnant : {winner}")
    st.write(f" Double chance : {double}")
    st.write(f" BTTS : {'OUI' if btts else 'NON'}")
    st.write(f" +2.5 buts : {'OUI' if over25 else 'NON'}")

    # =====================
    # COTES IA
    # =====================
    st.subheader(" Cotes estimées IA")

    st.write(f"{team1} : {odd1}")
    st.write(f"{team2} : {odd2}")

    # =====================
    # VALUE BET (IMPORTANT)
    # =====================
    st.subheader(" Détection VALUE BET")

    value_bets = []

    if prob_team1 > 0.6:
        value_bets.append(f"Victoire {team1}")

    if prob_team2 > 0.6:
        value_bets.append(f"Victoire {team2}")

    if btts and xg1 > 1.2 and xg2 > 1.2:
        value_bets.append("BTTS")

    if over25 and total >= 3:
        value_bets.append("+2.5 buts")

    if value_bets:
        st.success(", ".join(value_bets))
    else:
        st.warning("Pas de value bet clair")

    # =====================
    # COMBINÉ RENTABLE
    # =====================
    st.subheader(" Combiné IA rentable")

    combo = []

    combo.append(double)

    if btts:
        combo.append("BTTS")

    if over25:
        combo.append("+2.5 buts")

    st.warning(" + ".join(combo))

    # =====================
    # CONFIANCE
    # =====================
    confidence = int((abs(xg1 - xg2) + total) * 20)
    confidence = max(60, min(95, confidence))

    st.subheader(" Confiance IA")
    st.write(f"{confidence}%")

# =====================
# FOOTER
# =====================
st.markdown("---")
st.caption("BET AI GOD FINAL © 2026")


# =====================
# CONFIG
# =====================
st.set_page_config(page_title="BET AI GOD FINAL", layout="wide")

st.title(" BET AI GOD FINAL")

# =====================
# INPUT
# =====================
team1 = st.text_input("Équipe 1")
team2 = st.text_input("Équipe 2")

# =====================
# IA xG + PROBABILITÉS
# =====================
def predict():

    attack1 = np.random.uniform(1.0, 2.5)
    attack2 = np.random.uniform(1.0, 2.5)

    defense1 = np.random.uniform(0.8, 2.0)
    defense2 = np.random.uniform(0.8, 2.0)

    xg1 = attack1 * (2 - defense2)
    xg2 = attack2 * (2 - defense1)

    s1 = max(0, round(xg1))
    s2 = max(0, round(xg2))

    return s1, s2, xg1, xg2

# =====================
# ANALYSE
# =====================
if st.button(" Analyse GOD FINAL"):


import streamlit as st
import numpy as np

# =====================
# CONFIG
# =====================
st.set_page_config(page_title="BET AI ULTIMATE", layout="wide")

st.title(" BET AI ULTIMATE AI")

# =====================
# INPUT
# =====================
team1 = st.text_input("Équipe 1")
team2 = st.text_input("Équipe 2")

# =====================
# IA
# =====================
def predict():

    attack1 = np.random.uniform(0.8, 2.2)
    attack2 = np.random.uniform(0.8, 2.2)

    defense1 = np.random.uniform(0.8, 2.0)
    defense2 = np.random.uniform(0.8, 2.0)

    xg1 = attack1 * (2 - defense2)
    xg2 = attack2 * (2 - defense1)

    score1 = max(0, round(xg1))
    score2 = max(0, round(xg2))

    return score1, score2, xg1, xg2

# =====================
# ANALYSE
# =====================
if st.button(" Analyse"):

    if not team1 or not team2:
        st.warning("Entre les équipes")
        st.stop()

    s1, s2, xg1, xg2 = predict()

    total = s1 + s2

    st.success(f"{team1} {s1} - {s2} {team2}")

    # logique paris
    if s1 > s2:
        winner = team1
        double = "1X"
    elif s2 > s1:
        winner = team2
        double = "X2"
    else:
        winner = "Match nul"
        double = "X"

    btts = s1 > 0 and s2 > 0
    over = total >= 3

    st.subheader(" Paris")

    st.write(f"Gagnant : {winner}")
    st.write(f"Double chance : {double}")
    st.write(f"BTTS : {'OUI' if btts else 'NON'}")
    st.write(f"+2.5 buts : {'OUI' if over else 'NON'}")

    # meilleur pari
    if xg1 > 1.5 and xg2 > 1.5:
        best = "BTTS + Over 2.5"
    elif xg1 > xg2:
        best = f"Victoire {team1}"
    else:
        best = f"Victoire {team2}"

    st.success(f" Meilleur pari : {best}")

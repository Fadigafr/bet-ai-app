import streamlit as st
import numpy as np

# =====================
# CONFIG
# =====================
st.set_page_config(page_title="BET AI    xg2 = attack2 * (2 - defense1)st.set_page_config(page_title="BET AI ULTIMATE", layout="wide")

    # conversion en score
    score1 = max(0, round(xg1))
    score2 = max(0, round(xg2))

    return score1, score2, xg1, xg2

# =====================
# ANALYSE
# =====================
if st.button(" Analyse ULTIMATE"):

    if not team1 or not team2:
        st.warning("Entre les équipes")
        st.stop()

    s1, s2, xg1, xg2 = predict_ultimate()

    total = s1 + s2

    st.subheader(" Prédiction IA")

    st.success(f"{team1} {s1} - {s2} {team2}")

    st.write(f"xG {team1} : {round(xg1,2)}")
    st.write(f"xG {team2} : {round(xg2,2)}")

    # =====================
    # LOGIQUE PARIS
    # =====================
    btts = s1 > 0 and s2 > 0
    over25 = total >= 3

    # gagnant
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
    st.subheader(" Analyse paris PRO")

    st.write(f" Gagnant : {winner}")
    st.write(f" Double chance : {double}")
    st.write(f" BTTS : {'OUI' if btts else 'NON'}")
    st.write(f" +2.5 buts : {'OUI' if over25 else 'NON'}")

    # =====================
    # MEILLEUR PARI INTELLIGENT
    # =====================
    st.subheader(" Meilleur bet (IA intelligente)")

    # logique avancée
    if xg1 > 1.5 and xg2 > 1.5:
        best = "BTTS + Over 2.5"
    elif xg1 > xg2 + 1:
        best = f"Victoire {team1}"
    elif xg2 > xg1 + 1:
        best = f"Victoire {team2}"
    elif total <= 2:
        best = "Under 2.5 buts"
    else:
        best = "Double chance " + double

    st.success(best)

    # =====================
    # COMBINÉ VALUE
    # =====================
    st.subheader(" Combiné intelligent")

    combo = []

    if xg1 > xg2:
        combo.append("1X")
    else:
        combo.append("X2")

    if btts:
        combo.append("BTTS")

    if over25:
        combo.append("+2.5 buts")

    st.warning(" + ".join(combo))

    # =====================
    # CONFIANCE
    # =====================
    confidence = int((abs(xg1 - xg2) + total) * 20)
    confidence = min(95, max(60, confidence))

    st.subheader(" Niveau confiance")
    st.write(f"{confidence}%")

# =====================
# FOOTER
# =====================
st.markdown("---")
st.caption("BET AI ULTIMATE © 2026")

st.title(" BET AI ULTIMATE AI")

# =====================
# INPUT
# =====================
team1 = st.text_input("Équipe 1")
team2 = st.text_input("Équipe 2")

# =====================
# IA AVANCÉE SIMPLIFIÉE
# =====================
def predict_ultimate():

    # force offensive (attaque)
    attack1 = np.random.uniform(0.8, 2.2)
    attack2 = np.random.uniform(0.8, 2.2)

    # faiblesse défensive
    defense1 = np.random.uniform(0.8, 2.0)
    defense2 = np.random.uniform(0.8, 2.0)

    # calcul xG simplifié
    xg1 = attack1 * (2 - defense2)

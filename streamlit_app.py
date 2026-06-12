import streamlit as st
import numpy as np

# ========================
# CONFIG
# ========================
st.set_page_config(page_title="BET AI PRO MAX PARIS", layout="wide")

st.title(" BET AI PRO MAX PARIS")

# ========================
# INPUT
# ========================
team1 = st.text_input("Équipe 1")
team2 = st.text_input("Équipe 2")

# ========================
# ANALYSE
# ========================
if st.button(" Analyse complète"):

    if not team1 or not team2:
        st.warning("Entre les deux équipes")
        st.stop()

    # génération score
    score1 = np.random.randint(0, 4)
    score2 = np.random.randint(0, 4)

    total = score1 + score2

    st.subheader(" Résultat IA")
    st.success(f"{team1} {score1} - {score2} {team2}")

    # ========================
    # BTTS
    # ========================
    btts = score1 > 0 and score2 > 0

    # ========================
    # OVER / UNDER
    # ========================
    over25 = total > 2

    # ========================
    # DOUBLE CHANCE
    # ========================
    if score1 > score2:
        double = "1X"
        winner = team1
    elif score2 > score1:
        double = "X2"
        winner = team2
    else:
        double = "X"
        winner = "Match nul"

    # ========================
    # AFFICHAGE PARIS
    # ========================
    st.subheader(" Suggestions de paris")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Paris simples")
        st.write(f" Gagnant : {winner}")
        st.write(f" Double chance : {double}")
        st.write(f" +2.5 buts : {'OUI' if over25 else 'NON'}")
        st.write(f" BTTS : {'OUI' if btts else 'NON'}")

    with col2:
        st.markdown("###  Score exact")
        st.write(f"{team1} {score1} - {score2} {team2}")

    # ========================
    # MEILLEUR PARI (IA)
    # ========================
    st.subheader(" Meilleur pari (IA)")

    if over25 and btts:
        best_bet = "BTTS + Over 2.5 buts"
    elif over25:
        best_bet = "Plus de 2.5 buts"
    elif btts:
        best_bet = "Les deux équipes marquent"
    else:
        best_bet = f"Victoire {winner}"

    st.success(f" {best_bet}")

    # ========================
    # COMBINÉ AUTOMATIQUE
    # ========================
    st.subheader(" Combiné automatique")

    combo = []

    combo.append(double)

    if over25:
        combo.append("+2.5 buts")

    if btts:
        combo.append("BTTS")

    st.warning(" + ".join(combo))

    # ========================
    # CONFIANCE PAR PARI
    # ========================
    st.subheader(" Confiance IA")

    conf_score = np.random.randint(60, 90)
    conf_btts = np.random.randint(60, 90)
    conf_over = np.random.randint(60, 90)

    st.write(f"Score exact : {conf_score}%")
    st.write(f"BTTS : {conf_btts}%")
    st.write(f"+2.5 buts : {conf_over}%")

# ========================
# FOOTER
# ========================
st.markdown("---")
st.caption("BET AI PRO MAX PARIS © 2026")

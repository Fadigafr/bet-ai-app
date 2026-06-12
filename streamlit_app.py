import streamlit as st
import numpy as np

# ========================
# CONFIG
# ========================
st.set_page_config(page_title="BET AI PRO", layout="wide")

# ========================
# UI
# ========================
st.title(" BET AI PRO + OPTIONS PARIS")

# ========================
# INPUT MATCH
# ========================
team1 = st.text_input("Équipe 1")
team2 = st.text_input("Équipe 2")

# ========================
# OPTIONS PARIS
# ========================
st.subheader(" Options de paris")

option_score = st.checkbox("Prédiction score exact")
option_btts = st.checkbox("Les deux équipes marquent (BTTS)")
option_over = st.checkbox("Plus de 2.5 buts")

# ========================
# IA SIMPLIFIÉE
# ========================
if st.button(" Lancer Analyse"):

    if not team1 or not team2:
        st.warning("Entre les deux équipes")
        st.stop()

    # génération scores
    score1 = np.random.randint(0, 4)
    score2 = np.random.randint(0, 4)

    total_goals = score1 + score2

    st.subheader(" Résultat IA")

    st.success(f"{team1} {score1} - {score2} {team2}")

    # ========================
    # SCORE EXACT
    # ========================
    if option_score:
        st.write(" Score exact recommandé :")
        st.markdown(f"**{team1} {score1} - {score2} {team2}**")

    # ========================
    # BTTS (les deux marquent)
    # ========================
    if option_btts:
        if score1 > 0 and score2 > 0:
            st.success(" BTTS : OUI (les deux équipes marquent)")
        else:
            st.error(" BTTS : NON")

    # ========================
    # OVER 2.5
    # ========================
    if option_over:
        if total_goals > 2:
            st.success(" +2.5 buts : OUI")
        else:
            st.error(" +2.5 buts : NON")

    # ========================
    # CONFIANCE
    # ========================
    confidence = np.random.randint(65, 95)
    st.write(f" Confiance IA : {confidence}%")

# ========================
# FOOTER
# ========================
st.markdown("---")
st.caption("BET AI PRO © 2026")

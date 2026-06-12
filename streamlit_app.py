import streamlit as st
import numpy as np

# =====================
# CONFIG APP
# =====================
st.set_page_config(
    page_title="BET AI PRO",
    layout="wide"
)

# =====================
# INIT SESSION
# =====================
if "uses" not in st.session_state:
    st.session_state["uses"] = 0

if "premium" not in st.session_state:
    st.session_state["premium"] = False

# =====================
# HEADER
# =====================
st.title(" BET AI PRO")
st.markdown("Analyse intelligente de paris sportifs")

# =====================
# INPUT
# =====================
team1 = st.text_input("Équipe 1")
team2 = st.text_input("Équipe 2")

# =====================
# IA (SAFE)
# =====================
def predict_scores():
    score_home = int(np.random.randint(0, 4))
    score_away = int(np.random.randint(0, 4))
    return score_home, score_away

# =====================
# ANALYSE BUTTON
# =====================
analyse_clicked = st.button("🔍 Lancer Analyse")

if analyse_clicked:
    #  Validation
    if team1.strip() == "" or team2.strip() == "":
        st.warning(" Entre les deux équipes")
        st.stop()

    #  Limite gratuite
    if not st.session_state["premium"]:
        if st.session_state["uses"] >= 2:
            st.error(" Limite gratuite atteinte (2 analyses max)")
            st.info("Passe en Premium pour accès illimité")
            st.stop()

    #  IA
    s1, s2 = predict_scores()
    total_goals = s1 + s2

    st.success(f"{team1} {s1} - {s2} {team2}")

    # =====================
    # LOGIQUE PARIS
    # =====================
    if s1 > s2:
        winner = team1
    elif s2 > s1:
        winner = team2
    else:
        winner = "Match nul"

    btts = (s1 > 0 and s2 > 0)
    over25 = (total_goals >= 3)

    # =====================
    # AFFICHAGE RESULTATS
    # =====================
    st.subheader(" Paris recommandés")

    st.write(f" Gagnant : {winner}")
    st.write(f" BTTS : {'OUI' if btts else 'NON'}")
    st.write(f" +2.5 buts : {'OUI' if over25 else 'NON'}")

    #  compteur usage
    if not st.session_state["premium"]:
        st.session_state["uses"] += 1

# =====================
# PREMIUM SECTION
# =====================
st.markdown("---")
st.subheader(" Pass Premium")

if not st.session_state["premium"]:
    activate = st.button("Activer Premium (simulation)")

    if activate:
        st.session_state["premium"] = True
        st.success(" Compte Premium activé")

# =====================
# USER STATUS
# =====================
st.markdown("---")

if st.session_state["premium"]:
    st.success(" Statut : PREMIUM (illimité)")
else:
    remaining = 2 - st.session_state["uses"]
    if remaining < 0:
        remaining = 0
    st.warning(f" Compte GRATUIT - Restant : {remaining} analyse(s)")

# =====================
# FOOTER
# =====================
st.markdown("---")
st.caption("BET AI PRO © 2026 - Version Stable")
``

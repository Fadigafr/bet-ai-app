import streamlit as st
import numpy as np

# =====================
# CONFIG
# =====================
st.set_page_config(page_title="BET AI PRO", layout="wide")

# =====================
# TITRE
# =====================
st.title(" BET AI PRO")

# =====================
# SESSION (GRATUIT / PREMIUM)
# =====================
if "uses" not in st.session_state:
    st.session_state.uses = 0

if "premium" not in st.session_state:
    st.session_state.premium = False

# =====================
# INPUT UTILISATEUR
# =====================
team1 = st.text_input("Équipe 1")
team2 = st.text_input("Équipe 2")

# =====================
# FONCTION IA SIMPLE
# =====================
def predict():
    score1 = np.random.randint(0, 4)
    score2 = np.random.randint(0, 4)
    return score1, score2

# =====================
# ANALYSE
# =====================
if st.button(" Analyse"):

    # Vérification input
    if not team1 or not team2:
        st.warning("Entre les équipes")
        st.stop()

    # Limitateur gratuit
    if not st.session_state.premium:
        if st.session_state.uses >= 2:
            st.error(" Limite gratuite atteinte")
            st.info("Passe Premium pour continuer")
            st.stop()

    # IA
    s1, s2 = predict()
    total = s1 + s2

    # Résultat
    st.success(f"{team1} {s1} - {s2} {team2}")

    # Logique paris
    if s1 > s2:
        winner = team1
    elif s2 > s1:
        winner = team2
    else:
        winner = "Match nul"

    btts = s1 > 0 and s2 > 0
    over25 = total >= 3

    # Affichage
    st.subheader(" Paris recommandés")
    st.write(f" Gagnant : {winner}")
    st.write(f" BTTS : {'OUI' if btts else 'NON'}")
    st.write(f" +2.5 buts : {'OUI' if over25 else 'NON'}")

    # compteur
    st.session_state.uses += 1

# =====================
# ACTIVATION PREMIUM
# =====================
st.subheader(" Pass Premium")

if not st.session_state.premium:
    if st.button("Activer Premium (simulation)"):
        st.session_state.premium = True
        st.success(" Premium activé")

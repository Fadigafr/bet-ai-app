import streamlit as st
import numpy as np

# =====================
# CONFIG
# =====================
st.set_page_config(page_title="BET AI PRO MAX", layout="wide")

# =====================
# SESSION
# =====================
if "uses" not in st.session_state:
    st.session_state["uses"] = 0

if "premium" not in st.session_state:
    st.session_state["premium"] = False

# =====================
# HEADER
# =====================
st.title(" BET AI PRO MAX")
st.markdown(" Prédictions IA - Paris intelligents - Gains optimisés")

# =====================
# INPUT
# =====================
team1 = st.text_input("Équipe 1")
team2 = st.text_input("Équipe 2")

# =====================
# IA PREDICTION
# =====================
def predict():
    s1 = np.random.randint(0, 4)
    s2 = np.random.randint(0, 4)
    return s1, s2

# =====================
# ANALYSE
# =====================
if st.button(" ANALYSE PRO"):

    if team1.strip() == "" or team2.strip() == "":
        st.warning("Entre les équipes")
        st.stop()

    # LIMITATION FREE
    if not st.session_state["premium"]:
        if st.session_state["uses"] >= 2:
            st.error(" Limite gratuite atteinte")
            st.info("Passe Premium ")
            st.stop()

    s1, s2 = predict()
    total = s1 + s2

    st.success(f"{team1} {s1} - {s2} {team2}")

    # LOGIQUE PARIS
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
    over25 = total >= 3

    # AFFICHAGE
    st.subheader(" PRONOS IA")

    st.write(f" Gagnant : {winner}")
    st.write(f" Double chance : {double}")
    st.write(f" BTTS : {'OUI' if btts else 'NON'}")
    st.write(f" +2.5 buts : {'OUI' if over25 else 'NON'}")

    # MEILLEUR PARI
    if btts and over25:
        best = "BTTS + Over 2.5"
    elif over25:
        best = "Over 2.5"
    elif btts:
        best = "BTTS"
    else:
        best = f"Victoire {winner}"

    st.success(f" Meilleur pari : {best}")

    # COMBINÉ
    combo = [double]
    if btts:
        combo.append("BTTS")
    if over25:
        combo.append("+2.5")

    st.warning(" Combiné : " + " + ".join(combo))

    # compteur
    if not st.session_state["premium"]:
        st.session_state["uses"] += 1

# =====================
# PREMIUM
# =====================
st.markdown("---")
st.subheader(" PASS PREMIUM")

if not st.session_state["premium"]:
    if st.button("Activer Premium"):
        st.session_state["premium"] = True
        st.success(" Premium activé")

# =====================
# STATUS
# =====================
if st.session_state["premium"]:
    st.success(" Compte PREMIUM (illimité)")
else:
    restant = 2 - st.session_state["uses"]
    if restant < 0:
        restant = 0
    st.warning(f" Gratuit - {restant} essais restants")

# =====================
# FOOTER
# =====================
st.markdown("---")
st.caption("BET AI PRO MAX © 2026")

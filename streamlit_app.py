import streamlit as st
import numpy as np

st.set_page_config(page_title="BET AI PRO", layout="wide")

st.title(" BET AI PRO MAX")

# =====================
# MATCHS EXEMPLE
# =====================
matches = [
    ("Atletico GO", "CRB"),
    ("SalPa", "KUPS Akatemia"),
    ("Dinamo Batumi", "Dila"),
]

# =====================
# IA ANALYSE
# =====================
def analyse_match(team1, team2):

    prob1 = np.random.randint(45, 75)
    probX = np.random.randint(5, 25)
    prob2 = 100 - prob1 - probX

    if prob1 > prob2:
        tip = "1"
        odd = round(1.3 + (100 - prob1)/100, 2)
    elif prob2 > prob1:
        tip = "2"
        odd = round(1.3 + (100 - prob2)/100, 2)
    else:
        tip = "X"
        odd = 3.00

    return prob1, probX, prob2, odd, tip

# =====================
# TABLE
# =====================
st.subheader(" Match Predictions")

for team1, team2 in matches:

    prob1, probX, prob2, odd, tip = analyse_match(team1, team2)

    with st.container():
        col1, col2, col3, col4 = st.columns([3,2,1,1])

        with col1:
            st.write(f"**{team1} vs {team2}**")
            st.caption("Match du jour")

        with col2:
            st.write(f"{prob1}% | {probX}% | {prob2}%")

        with col3:
            st.write(f"{odd}")

        with col4:
            st.success(tip)

# =====================
# DETAIL MATCH
# =====================
st.markdown("---")
st.subheader(" Analyse détaillée")

team1 = st.text_input("Équipe 1")
team2 = st.text_input("Équipe 2")

if st.button("Analyser (version PRO)"):
    
    if not team1 or not team2:
        st.warning("Entre les équipes")
        st.stop()

    prob1, probX, prob2, odd, tip = analyse_match(team1, team2)

    st.write("### 1. Contexte")
    st.write("Match de championnat, enjeu modéré")

    st.write("### 2. Forme récente")
    st.write("Équipe 1 plus régulière")

    st.write("### 3. Match-up")
    st.write("Match ouvert avec potentiel offensif")

    st.write("### 4. Absences")
    st.write("Effectif complet")

    st.write("### 5. Statistiques")
    st.write("Bonne production offensive")

    st.write("### 6. Value")
    st.write("La cote semble légèrement sous-évaluée")

    st.write("### 7. Paris recommandés")
    st.success(f" {tip} @ {odd}")

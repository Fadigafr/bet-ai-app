import streamlit as st
import numpy as np

st.set_page_config(page_title="BET AI PREMIUM", layout="wide")

# =====================
# HEADER STYLE APP
# =====================
st.markdown("""
<style>
.header {
    background-color: #1f8c96;
    padding: 15px;
    color: white;
    font-size: 22px;
    font-weight: bold;
}
.card {
    background-color: #f0f2f6;
    padding: 15px;
    margin-bottom: 10px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header"> BET AI PREMIUM</div>', unsafe_allow_html=True)

# =====================
# FAKE MATCHS (REMPLACE PAR API)
# =====================
matches = [
    ("Atletico GO", "CRB"),
    ("SalPa", "KUPS Akatemia"),
    ("Dinamo Batumi", "Dila"),
]

# =====================
# IA PRO (STRUCTURE)
# =====================
def analyse(team1, team2):

    prob1 = np.random.randint(45, 75)
    probX = np.random.randint(10, 25)
    prob2 = 100 - prob1 - probX

    if prob1 > prob2:
        tip = "1"
        odd = round(1.3 + (100 - prob1)/100, 2)
    else:
        tip = "2"
        odd = round(1.3 + (100 - prob2)/100, 2)

    return prob1, probX, prob2, odd, tip

# =====================
# LISTE MATCHS
# =====================
st.subheader(" Matchs du jour")

for team1, team2 in matches:

    prob1, probX, prob2, odd, tip = analyse(team1, team2)

    st.markdown(f"""
    <div class="card">
        <b>{team1} vs {team2}</b><br><br>

        <b>Probabilité :</b> {prob1}% | {probX}% | {prob2}%<br>
        <b>Cote :</b> {odd}<br>
        <b>Tip :</b> <span style="color:green; font-weight:bold">{tip}</span>
    </div>
    """, unsafe_allow_html=True)

# =====================
# ANALYSE DETAIL
# =====================
st.markdown("---")
st.subheader(" Analyse avancée")

team1 = st.text_input("Équipe 1")
team2 = st.text_input("Équipe 2")

if st.button("Analyser PRO"):

    if not team1 or not team2:
        st.warning("Entre les équipes")
        st.stop()

    st.write("### 1. Contexte")
    st.write("Match avec enjeu réel, motivation normale")

    st.write("### 2. Forme")
    st.write("Dynamique récente positive")

    st.write("### 3. Match-up")
    st.write("Match ouvert")

    st.write("### 4. Absences")
    st.write("Effectif complet")

    st.write("### 5. Stats")
    st.write("Bonne production offensive")

    st.write("### 6. Value")
    st.write("Cote intéressante")

    st.write("### 7. Meilleur pari")
    st.success(" 1X / Over 2.5")

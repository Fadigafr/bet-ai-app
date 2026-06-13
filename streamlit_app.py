import streamlit as st
import numpy as np

# =====================
# CONFIG (TOUJOURS EN HAUT)
# =====================
st.set_page_config(page_title="BET AI PRO", layout="wide")

# =====================
# STYLE (CSS PROPRE)
# =====================
st.markdown("""
<style>
.header {
    background-color: #1f8c96;
    padding: 15px;
    color: white;
    font-size: 22px;
    font-weight: bold;
    text-align: center;
    border-radius: 12px;
}
.card {
    background-color: white;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 10px;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
}
.prob {
    display: inline-block;
    background: #eef2f7;
    padding: 5px 10px;
    border-radius: 6px;
    margin-right: 5px;
}
.tip {
    color: green;
    font-weight: bold;
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

# =====================
# HEADER
# =====================
st.markdown('<div class="header">⚽ BET AI PRO MAX</div>', unsafe_allow_html=True)

st.markdown("---")

# =====================
# MATCHS (EXEMPLE)
# =====================
matches = [
    ("PSG", "Marseille"),
    ("Real Madrid", "Barcelone"),
    ("Chelsea", "Arsenal"),
]

# =====================
# IA ANALYSE SIMPLE
# =====================
def analyse(team1, team2):
    prob1 = np.random.randint(40, 70)
    probX = np.random.randint(10, 25)
    prob2 = 100 - prob1 - probX

    if prob1 > prob2:
        tip = "1"
        odd = round(1.4 + (100 - prob1)/100, 2)
    elif prob2 > prob1:
        tip = "2"
        odd = round(1.4 + (100 - prob2)/100, 2)
    else:
        tip = "X"
        odd = 3.0

    return prob1, probX, prob2, odd, tip

# =====================
# AFFICHAGE MATCHS
# =====================
st.subheader("📊 Matchs du jour")

for team1, team2 in matches:

    prob1, probX, prob2, odd, tip = analyse(team1, team2)

    st.markdown(f"""
    <div class="card">
        <b>{team1} vs {team2}</b><br><br>

        <span class="prob">{prob1}%</span>
        <span class="prob">{probX}%</span>
        <span class="prob">{prob2}%</span><br><br>

        <b>Cote :</b> {odd}<br><br>

        Tip : <span class="tip">{tip}</span>
    </div>
    """, unsafe_allow_html=True)

# =====================
# ANALYSE PERSONNALISÉE
# =====================
st.markdown("---")
st.subheader(" Analyse avancée")

team1_input = st.text_input("Équipe 1")
team2_input = st.text_input("Équipe 2")

if st.button(" Analyse PRO"):

    if not team1_input or not team2_input:
        st.warning(" Entre les équipes")
        st.stop()

    prob1, probX, prob2, odd, tip = analyse(team1_input, team2_input)

    st.markdown("### Résultat IA")

    st.success(f"{team1_input} vs {team2_input}")

    st.write(f" Prob : {prob1}% / {probX}% / {prob2}%")
    st.write(f" Cote estimée : {odd}")
    st.write(f" Tip : {tip}")

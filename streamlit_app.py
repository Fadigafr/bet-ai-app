import streamlit as st
import requests
import numpy as np
import html

st.set_page_config(page_title="BET AI LIVE", layout="wide")
API_KEY = "TA_CLE_API"
BASE_URL = "https://v3.football.api-sports.io"

# =====================
# STYLE
# =====================
st.markdown("""
<style>
body {
    background-color: #f5f7fb;
}
.header {
    background-color: #1f8c96;
    padding: 15px;
    color: white;
    text-align: center;
    font-size: 22px;
    border-radius: 10px;
}
.card {
    background-color: white;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 10px;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
}
.prob {
    background: #eef2f7;
    padding: 5px 10px;
    border-radius: 6px;
    margin-right: 5px;
}
.tip {
    color: green;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown('<div class="header">BET AI LIVE</div>', unsafe_allow_html=True)

# =====================
# API MATCHS
# =====================
def get_matches():
    headers = {"x-apisports-key": API_KEY}
    url = BASE_URL + "/fixtures?next=5"

    try:
        r = requests.get(url, headers=headers)
        data = r.json()

        matches = []

        for m in data.get("response", []):
            team1 = m["teams"]["home"]["name"]
            team2 = m["teams"]["away"]["name"]
            matches.append((team1, team2))

        return matches

    except:
        return []

# =====================
# IA ANALYSE
# =====================
def analyse(team1, team2):
    prob1 = np.random.randint(45, 70)
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
# MATCHS
# =====================
matches = get_matches()

if not matches:
    matches = [
        ("PSG", "Marseille"),
        ("Real Madrid", "Barcelone"),
        ("Chelsea", "Arsenal"),
    ]

# =====================
# AFFICHAGE
# =====================
st.subheader("Matchs LIVE")

html_content = f"""
<div class="card">
    <b>{team1} vs {team2}</b>

    <div style="margin-top:10px;">
        <span class="prob">1: {prob1}%</span>
        <span class="prob">X: {probX}%</span>
        <span class="prob">2: {prob2}%</span>
    </div>

    <br>

    <b>Cote estimée :</b> {odd}

    <br><br>

    <span class="tip">Tip : {tip}</span>
</div>
"""

#  DÉCODE ICI
st.markdown(html.unescape(html_content), unsafe_allow_html=True)

# =====================
# ANALYSE MANUELLE
# =====================
st.markdown("---")
st.subheader("Analyse personnalisée")

team1_input = st.text_input("Équipe 1")
team2_input = st.text_input("Équipe 2")

if st.button("Analyser"):
    if team1_input and team2_input:
        prob1, probX, prob2, odd, tip = analyse(team1_input, team2_input)

        st.markdown(f"""
        <div class="card">
            <b>{team1_input} vs {team2_input}</b>

            <div style="margin-top:10px;">
                <span class="prob">1: {prob1}%</span>
                <span class="prob">X: {probX}%</span>
                <span class="prob">2: {prob2}%</span>
            </div>

            <br>

            <b>Cote estimée :</b> {odd}

            <br><br>

            <span class="tip">Tip : {tip}</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("Entre les deux équipes")

st.markdown("<span style='color:red'>TEST OK</span>", unsafe_allow_html=True)
# =====================
# CONFIG
# =====================

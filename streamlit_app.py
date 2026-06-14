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

def get_matches_and_odds():
    headers = {"x-apisports-key": API_KEY}

    url = BASE_URL + "/odds?league=61&season=2023"

    try:
        r = requests.get(url, headers=headers)
        data = r.json()

        matches = []

        for m in data.get("response", [])[:5]:

            teams = m["teams"]
            team1 = teams["home"]["name"]
            team2 = teams["away"]["name"]

            # récupération des cotes
            odds = m["bookmakers"][0]["bets"][0]["values"]

            odd1 = float(odds[0]["odd"])
            oddX = float(odds[1]["odd"])
            odd2 = float(odds[2]["odd"])

            matches.append((team1, team2, odd1, oddX, odd2))

        return matches

    except:
        return []

def analyse_value(team1, team2, odd1, oddX, odd2):

    prob1 = np.random.randint(45, 70)
    probX = np.random.randint(10, 25)
    prob2 = 100 - prob1 - probX

    p1 = prob1 / 100
    pX = probX / 100
    p2 = prob2 / 100

    value1 = round((p1 * odd1) - 1, 2)
    valueX = round((pX * oddX) - 1, 2)
    value2 = round((p2 * odd2) - 1, 2)

    return prob1, probX, prob2, value1, valueX, value2
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

import streamlit.components.v1 as components

for team1, team2 in matches:

    prob1, probX, prob2, odd, tip = analyse(team1, team2)

    html = f"""
    <div style="background:white;padding:15px;border-radius:10px;margin-bottom:10px;">
        <b>{team1} vs {team2}</b>

        <div style="margin-top:10px;">
            <span style="background:#eef2f7;padding:5px;border-radius:5px;">1: {prob1}%</span>
            <span style="background:#eef2f7;padding:5px;border-radius:5px;">X: {probX}%</span>
            <span style="background:#eef2f7;padding:5px;border-radius:5px;">2: {prob2}%</span>
        </div>

        <br>

        <b>Cote estimée :</b> {odd}

        <br><br>

        <span style="color:green;font-weight:bold;">Tip : {tip}</span>
    </div>
    """

    components.html(html, height=170)
    
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

components.html("<span style='color:red'>TEST</span>", height=50)

# =====================
# CONFIG
# =====================

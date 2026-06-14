import streamlit as st
import requests
import numpy as np

# =====================
# CONFIG
# =====================
st.set_page_config(page_title="BET AI LIVE", layout="wide")

API_KEY = "TA_CLE_API"
BASE_URL = "https://v3.football.api-sports.io"

# =====================
# STYLE
# =====================
st.markdown("""
<style>
.card {
    background-color: white;
    padding: 15px;
    border-radius: 12px;
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

st.markdown("""
<style>
.card {
    background-color: white;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 10px;
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

st.markdown('<div class="header"> BET AI LIVE</div>', unsafe_allow_html=True)

# =====================
# API MATCHS
# =====================
def get_matches():
    headers = {"x-apisports-key": API_KEY}
    url = BASE_URL + "/fixtures?next=10"

    try:
        r = requests.get(url, headers=headers)
        data = r.json()

        matches = []

        for m in data["response"]:
            home = m["teams"]["home"]["name"]
            away = m["teams"]["away"]["name"]

            matches.append((home, away))

        return matches

    except:
        return []

# =====================
# IA + PROBA
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
# RÉCUP MATCHS
# =====================
matches = get_matches()

if not matches:
    matches = [
        ("PSG", "Marseille"),
        ("Real Madrid", "Barca"),
        ("Chelsea", "Arsenal"),
    ]

# =====================
# AFFICHAGE
# =====================
st.subheader(" Matchs LIVE")

for team1, team2 in matches:

    prob1, probX, prob2, odd, tip = analyse(team1, team2)

    st.markdown(f"""
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
    """, unsafe_allow_html=True)

# =====================
# ANALYSE MANUELLE
# =====================
st.markdown("---")
st.subheader(" Analyse personnalisée")

t1 = st.text_input("Équipe 1")
t2 = st.text_input("Équipe 2")

if st.button(" Analyse PRO"):
    if not t1 or not t2:
        st.warning("Entre les équipes")
        st.stop()

    prob1, probX, prob2, odd, tip = analyse(t1, t2)

    st.success(f"{t1} vs {t2}")
    st.markdown(f"Probabilités : {prob1}% / {probX}% / {prob2}%")
    st.mardown(f"Cote estimée : {odd}")
    st.markdown(f"Meilleur pari : {tip}")

st.markdown(html, unsafe_allow_html=True)

st.markdown("""
<span style="color:red">TEST</span>
""", unsafe_allow_html=True)

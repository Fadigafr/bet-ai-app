import streamlit as stimportimport random

API_KEY = "TA_CLE_API"

st.set_page_config(page_title="BET AI PRO", layout="wide")

st.title("BET AI PRO")

password = st.text_input("Accès VIP", type="password")

if password != "VIP2026":
    st.warning("Accès réservé")
    st.stop()

team1 = st.text_input("Equipe 1")
team2 = st.text_input("Equipe 2")

if st.button("Analyser"):
    if team1 and team2:

        url = f"https://api-football-v1.p.rapidapi.com/v3/teams?search={team1}"

        headers = {
            "X-RapidAPI-Key": API_KEY,
            "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            st.success(f"{team1} vs {team2}")

            prob = random.randint(60, 90)  # temporaire

            st.metric("Prédiction IA", f"{prob}%")
        else:
            st.error("Erreur API")

    else:
        st.warning("Entre les équipes")
``
import requests

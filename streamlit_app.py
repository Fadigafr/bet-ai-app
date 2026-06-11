import streamlit as stimport streamlit requests

API_KEY = "TA_CLE_API"  # tu vas la créer

st.title("BET AI PRO")

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
            st.success("Analyse IA en cours...")
            st.write("Match :", team1, "vs", team2)

            # Simulation améliorée (en attendant vrai modèle)
            import random
            prob = random.randint(55, 85)

            st.metric("Prédiction IA", f"{prob}%")
        else:
            st.error("Erreur API")

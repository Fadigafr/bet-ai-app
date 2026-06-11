password = st.text_input("Accès VIP", type="password")

if password != "VIP2026":
    st.warning("Accès réservé aux abonnés")
    st.stop()
import streamlit as stimport streamlit requests

API_KEY = "package main

import (
	"fmt"
	"net/http"
	"io"
)

func main() {

	url := "https://free-api-live-football-data.p.rapidapi.com/football-players-search?search=m"

	req, _ := http.NewRequest("GET", url, nil)

	req.Header.Add("x-rapidapi-key", "acddc25c4amsh1b5de20e73be716p1933dfjsn4e554c3a6bf4")
	req.Header.Add("x-rapidapi-host", "free-api-live-football-data.p.rapidapi.com")
	req.Header.Add("Content-Type", "application/json")

	res, _ := http.DefaultClient.Do(req)

	defer res.Body.Close()
	body, _ := io.ReadAll(res.Body)

	fmt.Println(res)
	fmt.Println(string(body))

}"  # tu vas la créer

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

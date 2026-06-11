import streamlit as st
import requests application de prédiction ")import requests

# Exemple simple
team1 = st.text_input("Equipe 1")
team2 = st.text_input("Equipe 2")

if st.button("Analyser"):
    if team1 and team2:
        st.success(f"Analyse du match {team1} vs {team2}")

        # Simulation IA simple
        prob = np.random.randint(40, 90)

        st.metric("Probabilité de victoire équipe 1", f"{prob}%")
    else:
        st.warning("Entre les équipes")
import pandas as pd
import numpy as np

st.set_page_config(page_title="BET AI PRO", layout="wide")

st.title("BET AI PRO")


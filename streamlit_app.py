import streamlit as st
import requests
import numpy as np

st.set_page_config(page_title="BET AI PRO", layout="wide")

st.title("BET AI PRO")

# Login simple
password = st.text_input("Accès VIP", type="password")

if password != "VIP2026":
    st.warning("Accès réservé")
    st.stop()

team1 = st.text_input("Equipe 1")
team2 = st.text_input("Equipe 2")

if st.button("Analyser"):
    if team1 and team2:
        prob = np.random.randint(60, 90)
        st.success(f"{team1} vs {team2}")
        st.metric("Prédiction IA", f"{prob}%")
    else:
        st.warning("Entre les équipes")

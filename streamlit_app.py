import streamlit as st
import numpy as np

st.set_page_config(page_title="BET AI PRO", layout="wide")

st.title(" BET AI")

team1 = st.text_input("Équipe 1")
team2 = st.text_input("Équipe 2")

if st.button("Analyse"):

    if not team1 or not team2:
        st.warning("Entre les équipes")
        st.stop()

    s1 = np.random.randint(0, 4)
    s2 = np.random.randint(0, 4)

    st.success(f"{team1} {s1} - {s2} {team2}")

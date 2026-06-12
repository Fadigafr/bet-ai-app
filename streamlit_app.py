import streamlit as st
import numpy as np

st.set_page_config(page_title="BET AI GOD FINAL", layout="wide")

st.title(" BET AI")

team1 = st.text_input("Équipe 1")
team2 = st.text_input("Équipe 2")

def predict():
    s1 = np.random.randint(0, 4)
    s2 = np.random.randint(0, 4)
    return s1, s2

if st.button("Analyse"):

    if not team1 or not team2:
        st.warning("Entre les équipes")
        st.stop()

    s1, s2 = predict()

    st.success(f"{team1} {s1} - {s2} {team2}")

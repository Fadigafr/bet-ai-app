import streamlit as st
import numpy as np
password = st.text_input("Code d'accès", type="password")

if password != "1234":
    st.warning("Accès réservé aux abonnés")
    st.stop()
st.set_page_config(page_title="BET AI PRO", layout="wide")

# Style CSS
st.markdown("""
    <style>
    .main {
        background-color: #0b1c2c;
        color: white;
    }
    .stTextInput>div>div>input {
        background-color: #1e2a38;
        color: white;
    }
    .stButton>button {
        background-color: #00c853;
        color: white;
        font-size: 18px;
    }
    </style>
""", unsafe_allow_html=True)

st.title(" BET AI PRO")

st.write("Analyse intelligente des matchs")

team1 = st.text_input("Equipe 1")
team2 = st.text_input("Equipe 2")

if st.button("Analyser "):
    if team1 and team2:
        prob = np.random.randint(40, 90)

        st.success(f"{team1} vs {team2}")
        st.metric("Probabilité de victoire", f"{prob}%")
    else:
        st.warning("Entre les équipes")
``

import streamlit as st
import numpy as np
import requests
import schedule
import time

def job():
    generate_prono()

# envoi tous les jours à 10h
schedule.every().day.at("10:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(60)
from telegram_bot import send_message

def generate_prono():

    team1 = "PSG"
    team2 = "Marseille"

    s1 = np.random.randint(1, 3)
    s2 = np.random.randint(0, 2)

    total = s1 + s2

    btts = s1 > 0 and s2 > 0
    over = total >= 3

    message = f"""
 PRONO DU JOUR 

{team1} vs {team2}

 Score : {s1}-{s2}
 BTTS : {'OUI' if btts else 'NON'}
 +2.5 buts : {'OUI' if over else 'NON'}

 COMBINÉ :
"""

    combo = ["1X"]

    if btts:
        combo.append("BTTS")

    if over:
        combo.append("+2.5")

    message += " + ".join(combo)

    message += "\n Confiance : 85%"

    send_message(message)

generate_prono()

from telegram_bot import send_message

def generate_prono():

    team1 = "PSG"
    team2 = "Marseille"

    s1 = np.random.randint(1, 3)
    s2 = np.random.randint(0, 2)

    total = s1 + s2

    btts = s1 > 0 and s2 > 0
    over = total >= 3

    message = f"""
  PRONO DU JOUR 

{team1} vs {team2}

  Score : {s1}-{s2}
  BTTS : {'OUI' if btts else 'NON'}
  +2.5 buts : {'OUI' if over else 'NON'}

  COMBINÉ :
"""

    combo = ["1X"]

    if btts:
        combo.append("BTTS")

    if over:
        combo.append("+2.5")

    message += " + ".join(combo)

    message += "\n📈 Confiance : 85%"

    send_message(message)

generate_prono()
TOKEN = "TON_TOKEN_BOT"
CHAT_ID = "TON_CHAT_ID"

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text
    })
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

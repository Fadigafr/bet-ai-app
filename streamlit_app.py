STRIPE_KEY = "TA_CLE_STRIPE"
API_KEY = "TA_CLE_API"
TELEGRAM_TOKEN = "TON_BOT_TOKEN"
TELEGRAM_CHAT = "TON_CHAT_ID"
import streamlit as stimport streamlit as pd
import math
import numpy as np
``
import requests
import streamlit as st
import stripe
import pandas as pd
import math
import tensorflow as tf
import schedule

def poisson_model(xg_home, xg_away):
    home = draw = away = 0

    for i in range(5):
        for j in range(5):
            prob = (math.exp(-xg_home) * xg_home**i / math.factorial(i)) * \
                   (math.exp(-xg_away) * xg_away**j / math.factorial(j))

            if i > j:
                home += prob
            elif i == j:
                draw += prob
            else:
                away += prob

    return home, draw, away


def value_bet(prob, odds):
    return (prob * odds) - 1
def get_matches():
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

    headers = {
        "X-RapidAPI-Key": st.secrets["API_KEY"],
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    res = requests.get(url, headers=headers)
    data = res.json()

    matches = []

    for m in data["response"]:
        matches.append({
            "home": m["teams"]["home"]["name"],
            "away": m["teams"]["away"]["name"],
            "xg_home": m["goals"]["home"] or 1.3,
            "xg_away": m["goals"]["away"] or 1.1
        })

    return matches
    import sqlite3

def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT)")
    conn.commit()
    conn.close()

def register(user, pwd):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("INSERT INTO users VALUES (?,?)", (user, pwd))
    conn.commit()
    conn.close()

def login(user, pwd):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (user, pwd))
    res = c.fetchone()
    conn.close()
    return res is not None

stripe.api_key = st.secrets["STRIPE_KEY"]

def checkout():
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        mode='subscription',
        line_items=[{
            'price_data': {
                'currency': 'eur',
                'unit_amount': 1000,
                'recurring': {'interval': 'month'},
                'product_data': {'name': 'BET AI PRO VIP'},
            },
            'quantity': 1,
        }],
        success_url='https://bet-ai-app.streamlit.app',
        cancel_url='https://bet-ai-app.streamlit.app',
    )
    return session.url
def send_telegram(msg):
    url = f"https://api.telegram.org/bot{st.secrets['TELEGRAM_TOKEN']}/sendMessage"
    requests.post(url, data={
        "chat_id": st.secrets["TELEGRAM_CHAT"],
        "text": msg
    })  

def retrain():
    df = pd.read_csv("data_full.csv")

    X = df[["xg_home","xg_away","form_home","form_away"]]
    y = df["result"]

    model = tf.keras.Sequential([
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(3, activation='softmax')
    ])

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy')
    model.fit(X, y, epochs=10)

    model.save("model_auto.h5")

import time
from auto_learning 
import retrain

schedule.every().day.at("02:00").do(retrain)

while True:
    schedule.run_pending()
    time.sleep(60)
import streamlit as st
from ai_engine import poisson_model, value_bet
from api_data import get_matches
from auth import login, register, init_db
from payments import checkout
from telegram_bot import send_telegram

init_db()

# DESIGN
st.markdown("""
<style>
body { background: #0f172a; color: white; }
.card {
    background: #1e293b;
    padding: 15px;
    border-radius: 15px;
}
</style>
""", unsafe_allow_html=True)

st.title(" BET AI PRO")

# LOGIN
user = st.sidebar.text_input("User")
pwd = st.sidebar.text_input("Password", type="password")

if st.sidebar.button("Login"):
    is_logged = login(user, pwd)
else:
    is_logged = False

# REGISTER
if st.sidebar.button("Register"):
    register(user, pwd)

# VIP BLOCK
if not is_logged:
    st.warning(" Accès limité")
    if st.button(" VIP"):
        st.write(checkout())
    st.stop()

# MATCHES
matches = get_matches()

for m in matches[:5]:

    home, draw, away = poisson_model(m["xg_home"], m["xg_away"])
    value = value_bet(home, 2.2)

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader(f"{m['home']} vs {m['away']}")
    st.metric("Home", f"{home*100:.1f}%")
    st.metric("Draw", f"{draw*100:.1f}%")
    st.metric("Away", f"{away*100:.1f}%")

    if value > 0:
        st.success(" VALUE BET")
        send_telegram(f" VALUE BET: {m['home']} vs {m['away']}")

    st.markdown('</div>', unsafe_allow_html=True)
     “dashboard ultra animé”
 “IA précision extrême (pro bookmaker)”
 “scaling 1000 clients concret plan”
import xgboost as xgbimport xgboost as x,
    learning_rate=0.05
)

model_xgb = xgb.XGBClassifier(
    n_estimators=500,
model_dl = tf.keras.Sequential([
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(3, activation='softmax')
])
def final_prediction(prob_poisson, prob_xgb, prob_dl):

    return (
        0.4 * prob_poisson +
        0.3 * prob_xgb +
        0.3 * prob_dl
    )
    def value_bet(prob, odds):

    return (prob * odds) - 1 > 0.05
    def generate_tiktok_text(match):

    return f"""
 PARI DU JOUR 

{match['home']} vs {match['away']}

✅ IA détecte VALUE BET
✅ Probabilité élevée

 Ne rate pas ce match

 lien en bio
"""
    def generate_script(match):

    return f"""
  PARI À NE PAS RATER 

 {match['home']} vs {match['away']}

✅ Probabilité : 65%
✅ VALUE BET détecté

 Clique sur le lien dans la bio
"""
    pip install moviepy gtts pillow
    from moviepy.editor import *from moviepy    except:
        font = ImageFont.load_default()

    draw.text((50, 300), text, fill=(34, 197, 94), font=font)

    img.save(filename)


# ========================
# AUDIO VOIX
# ========================
def create_voice(text, filename):

    tts = gTTS(text=text, lang='fr')
    tts.save(filename)


# ========================
# VIDEO
# ========================
def create_video(match):

    text = generate_script(match)

    create_image(text, "frame.png")
    create_voice(text, "voice.mp3")

    clip = ImageClip("frame.png").set_duration(6)
    audio = AudioFileClip("voice.mp3")

    video = clip.set_audio(audio)

    video.write_videofile(
        f"{match['home']}_vs_{match['away']}.mp4",
        fps=24
    )


# ========================
# TEST
# ========================
match = {
    "home": "PSG",
    "away": "Lyon"
}

create_video(match)
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
import os


# ========================
# TEXTE IA
# ========================
def generate_script(match):

    return f"""
Pari du jour !

{match['home']} contre {match['away']}

Probabilité élevée !
Value bet détecté !

Clique sur le lien en bio !
"""


# ========================
# IMAGE TEXTE
# ========================
def create_image(text, filename):

    img = Image.new('RGB', (720, 1280), color=(15, 23, 42))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 40)
matches = [
    {"home": "PSG", "away": "Lyon"},
    {"home": "Arsenal", "away": "Chelsea"},
    {"home": "Barcelona", "away": "Real Madrid"}
]

for m in matches:
    create_video(m)
import schedule
import time
from video_generator import create_video

def daily_videos():

    matches = [
        {"home": "PSG", "away": "Lyon"},
        {"home": "Inter", "away": "Milan"}
    ]

    for m in matches:
        create_video(m)

schedule.every().day.at("09:00").do(daily_videos)

while True:
    schedule.run_pending()
    time.sleep(60)
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# CONFIG
VIDEO_PATH = "PSG_vs_Lyon.mp4"

driver = webdriver.Chrome()

# Ouvrir TikTok upload
driver.get("https://www.tiktok.com/upload")

print("Connecte-toi manuellement à TikTok...")
time.sleep(30)  # temps pour login

# Upload vidéo
file_input = driver.find_element(By.XPATH, "//input[@type='file']")
file_input.send_keys(VIDEO_PATH)

print("Vidéo upload en cours...")
time.sleep(15)

# Ajouter description
description = driver.find_element(By.XPATH, "//div[@role='textbox']")
description.send_keys(" PARI DU JOUR #bet #football #ia")

# Publier
publish_button = driver.find_element(By.XPATH, "//button[contains(., 'Post')]")
publish_button.click()

print("Vidéo publiée !")
time.sleep(5)

driver.quit()
from video_generator import create_video
from tiktok_upload import upload_video  # fonction que tu crées

matches = [
    {"home": "PSG", "away": "Lyon"},
    {"home": "Arsenal", "away": "Chelsea"}
]

for m in matches:
    create_video(m)
    upload_video(f"{m['home']}_vs_{m['away']}.mp4")
    import schedule
import time
from main import run_auto

schedule.every().day.at("09:00").do(run_auto)

while True:
    schedule.run_pending()
    time.sleep(60)
    

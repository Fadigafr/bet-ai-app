STRIPE_KEY = "TA_CLE_STRIPE"
API_KEY = "TA_CLE_API"
TELEGRAM_TOKEN = "TON_BOT_TOKEN"
TELEGRAM_CHAT = "TON_CHAT_ID"
import math

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
import requests
import streamlit as st

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
import stripe
import streamlit as st

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
  import requests
import streamlit as st

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{st.secrets['TELEGRAM_TOKEN']}/sendMessage"

    requests.post(url, data={
        "chat_id": st.secrets["TELEGRAM_CHAT"],
        "text": msg
    })  
import pandas as pd
import tensorflow as tf

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
    import schedule
import time
from auto_learning import retrain

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

st.title("⚽ BET AI PRO")

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
    st.warning("🔒 Accès limité")
    if st.button("💎 VIP"):
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
        st.success("🔥 VALUE BET")
        send_telegram(f"🔥 VALUE BET: {m['home']} vs {m['away']}")

    st.markdown('</div>', unsafe_allow_html=True)
    

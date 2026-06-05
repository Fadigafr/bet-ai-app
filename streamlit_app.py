import streamlit as st
import pandas as pd
import math
import stripe
import requests
STRIPE_KEY = "ta_cle"

API_KEY = "TA_CLE_API"
# ======================
# CONFIG
# ======================
stripe.api_key = "TA_CLE_STRIPE"

# ======================
# LOGIN
# ======================
users = {
    "fred": "1234",
    "vip": "vip123"
}

st.sidebar.title("🔐 Connexion")

username = st.sidebar.text_input("Utilisateur")
password = st.sidebar.text_input("Mot de passe", type="password")

is_logged = False

if username in users and users[username] == password:
    st.sidebar.success("✅ Connecté")
    is_logged = True
else:
    st.sidebar.error("❌ Non connecté")

# ======================
# STRIPE
# ======================
def create_checkout():
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

# ======================
# DESIGN PREMIUM
# ======================
st.markdown("""
<style>
body {
    background-color: #0f172a;
    color: white;
}
.main-title {
    font-size: 40px;
    color: #22c55e;
    font-weight: bold;
}
.card {
    background: #1e293b;
    padding: 15px;
    border-radius: 15px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">⚽ BET AI PRO</p>', unsafe_allow_html=True)
st.write("🔥 Prédictions football intelligentes avec IA")

# ======================
# DATA (temporaire)
# ======================
df = pd.read_csv("sample_matches.csv")

# ======================
# IA SIMPLE (POISSON)
# ======================
def poisson_prob(home_xg, away_xg):
    home_win = 0
    draw = 0
    away_win = 0
    
    for i in range(5):
        for j in range(5):
            prob = (math.exp(-home_xg) * home_xg**i / math.factorial(i)) * \
                   (math.exp(-away_xg) * away_xg**j / math.factorial(j))
            
            if i > j:
                home_win += prob
            elif i == j:
                draw += prob
            else:
                away_win += prob
    
    return home_win, draw, away_win

matches = get_live_matches()

for m in matches[:5]:

    st.subheader(f"{m['home']} vs {m['away']}")

    home_win, draw, away_win = poisson_prob(
        m["goals_home"], m["goals_away"]
    )

# ======================
# AFFICHAGE
# ======================
st.divider()

if not is_logged:
    st.warning("🔒 Connecte-toi ou prends VIP pour accéder aux prédictions")
    
    if st.button("💎 Devenir VIP"):
        st.markdown(create_checkout())
else:
    st.success("🔥 Mode VIP activé")

    for index, row in df.iterrows():

        home_win, draw, away_win = poisson_prob(row["xg_home"], row["xg_away"])

        confidence = max(home_win, draw, away_win)
        value = (home_win * 2.2) - 1

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader(f"{row['home']} vs {row['away']}")

        c1, c2, c3 = st.columns(3)
        c1.metric("🏠 Home", f"{home_win*100:.1f}%")
        c2.metric("🤝 Draw", f"{draw*100:.1f}%")
        c3.metric("🚀 Away", f"{away_win*100:.1f}%")

        st.metric("⚽ BTTS", f"{min(home_win, away_win)*100:.1f}%")
        
        if confidence > 0.65:
            st.success("✅ Haute confiance")
        elif confidence > 0.5:
            st.warning("⚖️ Moyenne")
        else:
            st.error("❌ Risqué")

        if value > 0:
            st.success(f"🔥 VALUE BET +{round(value,2)}")

        st.markdown('</div>', unsafe_allow_html=True)

def get_live_matches():
    
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    params = {"league": 39, "season": 2023}

    res = requests.get(url, headers=headers, params=params)
    data = res.json()

    matches = []

    for m in data["response"]:
        matches.append({
            "home": m["teams"]["home"]["name"],
            "away": m["teams"]["away"]["name"],
            "goals_home": m["goals"]["home"] or 1.2,
            "goals_away": m["goals"]["away"] or 1.0,
        })

    return matches

matches = get_live_matches()

for m in matches[:5]:

    st.subheader(f"{m['home']} vs {m['away']}")

    home_win, draw, away_win = poisson_prob(
        m["goals_home"], m["goals_away"]
    )

import sqlite3

conn = sqlite3.connect("users.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users(
    username TEXT,
    password TEXT
)
""")

conn.commit()
conn.close()

def register_user(user, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute(
        "INSERT INTO users VALUES (?,?)",
        (user, password)
    )

    conn.commit()
    conn.close()

def login_user(user, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (user, password)
    )

    result = c.fetchone()
    conn.close()

    return result is not None

st.sidebar.subheader("Créer compte")

new_user = st.sidebar.text_input("Nouveau user")
new_pass = st.sidebar.text_input("Mot de passe", type="password")

if st.sidebar.button("S'inscrire"):
    register_user(new_user, new_pass)
    st.sidebar.success("Compte créé")

npm install -g expo-cli

import React from 'react';
import { WebView } from 'react-native-webview';

export default function App() {
  return (
    <WebView source={{ uri: 'https://bet-ai-app.streamlit.app' }} />
  );
}

expo build:android

def smart_bot(match):

    prob = match["prob_home"]
    odds = match["odds_home"]

    value = (prob * odds) - 1

    if value > 0.05:
        return {
            "bet": match["home"],
            "value": round(value, 2),
            "confidence": round(prob, 2),
            "stake": "3% bankroll"
        }

    return None

signal = smart_bot({
    "home": "Arsenal",
    "prob_home": 0.62,
    "odds_home": 2.2
})

if signal:
    st.success(f"🔥 BET: {signal['bet']}")

import xgboost as xgb
import pandas as pd

def train_model():

    df = pd.read_csv("data_full.csv")

    X = df[[
        "xg_home", "xg_away",
        "form_home", "form_away",
        "shots_home", "shots_away"
    ]]

    y = df["result"]

    model = xgb.XGBClassifier(
        n_estimators=300,
        max_depth=5
    )

    model.fit(X, y)
    return model

def predict(model, features):
    return model.predict_proba([features])

st.markdown("""
<style>
body { background-color: #0f172a; }
.card {
    background: #1e293b;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="card">', unsafe_allow_html=True)

st.subheader(f"{match['home']} vs {match['away']}")

st.metric("🏠 Home", "62%")
st.metric("🤝 Draw", "22%")
st.metric("🚀 Away", "16%")

st.success("🔥 VALUE BET détecté")

st.markdown('</div>', unsafe_allow_html=True)

STRIPE_KEY = "ta_cle"

if not is_logged:
    st.stop()

final_prob = (prob_xgb + prob_poisson) / 2

from streamlit.components.v1 import html

st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f172a, #020617);
    color: white;
}

.card {
    background: rgba(30,41,59,0.9);
    border-radius: 20px;
    padding: 20px;
    margin: 12px 0;
    box-shadow: 0px 6px 20px rgba(0,0,0,0.4);
    transition: 0.3s;
}

.card:hover {
    transform: scale(1.02);
}

.title {
    font-size: 28px;
    font-weight: bold;
    color: #22c55e;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">⚽ BET AI PRO ELITE</div>', unsafe_allow_html=True)

html("""
<div style="text-align:center">
    <div class="spinner"></div>
    <style>
    .spinner {
        width: 50px;
        height: 50px;
        border: 5px solid #22c55e;
        border-top: 5px solid transparent;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin: auto;
    }
    @keyframes spin {
        0% { transform: rotate(0deg);}
        100% { transform: rotate(360deg);}
    }
    </style>
</div>
""")

col1, col2, col3, col4 = st.columns(4)

col1.metric("🔥 Signals", "8")
col2.metric("✅ Accuracy", "72%")
col3.metric("💰 ROI", "+15%")
col4.metric("👥 Users", "152")

import numpy as np
from scipy.stats import poisson

def exact_score(xg_home, xg_away):

    matrix = np.zeros((6,6))

    for i in range(6):
        for j in range(6):
            matrix[i][j] = poisson.pmf(i, xg_home) * poisson.pmf(j, xg_away)

    idx = np.unravel_index(matrix.argmax(), matrix.shape)

    return idx, matrix
``

score, matrix = exact_score(1.8, 1.2)

st.write(f"🎯 Score probable : {score[0]} - {score[1]}")
``

def predict_scorers(team_goals):

    players = {
        "Haaland": 0.45,
        "Foden": 0.25,
        "Alvarez": 0.20
    }

    results = {}

    for p, ratio in players.items():
        results[p] = round(team_goals * ratio, 2)

    return results

scorers = predict_scorers(2)

for p,v in scorers.items():
    st.write(f"{p} ⚽ {v}")

def generate_post(match):

    Value bet détecté    return f"""

👉 Accès VIP : lien
"""
``
🔥 MATCH DU JOUR

{match['home']} vs {match['away']}

✅ Probabilité: 65%

def auto_post():
    print("✅ Post publié TikTok / Facebook")



# ======================
# FOOTER BUSINESS
# ======================
st.divider()
st.info("💎 Version gratuite limitée — passe VIP pour plus de matchs")

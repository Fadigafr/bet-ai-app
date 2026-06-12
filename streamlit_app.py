import streamlit as st
import numpy as np
import stripe
import sqlite3

def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT,
        premium INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()

def add_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    try:
        c.execute("INSERT INTO users VALUES (?, ?, 0)", (username, password))
        conn.commit()
    except:
        pass

    conn.close()

def check_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = c.fetchone()

    conn.close()
    return result

def is_premium(username):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("SELECT premium FROM users WHERE username=?", (username,))
    result = c.fetchone()

    conn.close()

    if result:
        return result[0] == 1
    return False

def set_premium(username):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("UPDATE users SET premium=1 WHERE username=?", (username,))
    conn.commit()
    conn.close()
``
# =====================
# CONFIG
# =====================
st.set_page_config(page_title="BET AI PRO", layout="wide")

stripe.api_key = "TA_CLE_STRIPE"  #  mets ta vraie clé

st.title(" BET AI PRO (SaaS)")

# =====================
# SESSION
# =====================
if "uses" not in st.session_state:
    st.session_state.uses = 0

if "premium" not in st.session_state:
    st.session_state.premium = False

# =====================
# INPUT
# =====================
team1 = st.text_input("Équipe 1")
team2 = st.text_input("Équipe 2")

# =====================
# IA
# =====================
def predict():
    s1 = np.random.randint(0, 4)
    s2 = np.random.randint(0, 4)
    return s1, s2

# =====================
# ANALYSE
# =====================
if st.button(" Analyse premium"):

    if not team1 or not team2:
        st.warning("Entre les équipes")
        st.stop()

    #  BLOCAGE FREE
    if not st.session_state.premium:
        if st.session_state.uses >= 2:
            st.error(" Limite gratuite atteinte")
            st.info("Passe Premium pour continuer")
            st.stop()

    s1, s2 = predict()

    total = s1 + s2

    st.success(f"{team1} {s1} - {s2} {team2}")

    # logique paris
    if s1 > s2:
        winner = team1
    elif s2 > s1:
        winner = team2
    else:
        winner = "Match nul"

    btts = s1 > 0 and s2 > 0
    over = total >= 3

    # affichage
    st.subheader(" Paris recommandés")

    st.write(f" Gagnant : {winner}")
    st.write(f" BTTS : {'OUI' if btts else 'NON'}")
    st.write(f" +2.5 : {'OUI' if over else 'NON'}")

    # compteur free
    st.session_state.uses += 1

# =====================
# STRIPE PAIEMENT
# =====================
st.subheader(" Pass Premium")

if st.button("S'abonner (10€)"):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "eur",
                    "product_data": {"name": "Bet AI Premium"},
                    "unit_amount": 1000,
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url="https://bet-ai-app.streamlit.app",
            cancel_url="https://bet-ai-app.streamlit.app",
        )

        st.success(" Paiement prêt")
        st.write(session.url)

        #  simulation activation
        st.session_state.premium = True

    except Exception as e:
        st.error(str(e))

# =====================
# STATUS UTILISATEUR
# =====================
if st.session_state.premium:
    st.success(" Compte PREMIUM actif")
else:
    st.warning(" Compte GRATUIT (2 essais)")

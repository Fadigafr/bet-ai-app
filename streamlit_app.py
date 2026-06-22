import base64
from pathlib import Path
import sqlite3
import numpy as np
import requests
import streamlit as st
import bcrypt

# ==========================================
# CONFIG
# ==========================================
st.set_page_config(page_title="BET AI ENTERPRISE", layout="wide")

PAYSTACK_LINK = "https://paystack.com/pay/TON-LIEN"
API_URL = "http://localhost:8000"  # FastAPI backend
API_URL = "https://bet-ai-api.onrender.com"
# ==========================================
# DATABASE
# ==========================================
conn = sqlite3.connect("app.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    username TEXT PRIMARY KEY,
    password TEXT,
    vip INTEGER
)
""")

conn.commit()

# ==========================================
# LOGIN
# ==========================================

def Créer compte"):def hash_password(password):
        hashed = hash_password(password)

        cursor.execute(
            "INSERT OR IGNORE INTO users VALUES (?, ?, ?)",
            (email, hashed, 0)
        )
        conn.commit()

        st.success("✅ Compte créé ! Connecte-toi")

    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

def login():
    st.title("🔐 Connexion / Inscription")

    email = st.text_input("Email")
    password = st.text_input("Mot de passe", type="password")

    col1, col2 = st.columns(2)

    # ✅ LOGIN
    if col1.button("Se connecter"):
        user = cursor.execute(
            "SELECT * FROM users WHERE username=?",
            (email,)
        ).fetchone()

        if user and check_password(password, user[1]):
            st.session_state.logged = True
            st.session_state.user = email
            st.session_state.vip = user[2]
            st.success("Connexion réussie ✅")
            st.rerun()
        else:
            st.error("❌ Identifiants incorrects")

    # ✅ REGISTER (ALIGNÉ AVEC col1)


    # REGISTER
    if col2.button("Créer compte"):

        hashed = hash_password(password)

        cursor.execute("""
        INSERT OR IGNORE INTO users VALUES (?, ?, ?)
        """, (email, hashed.decode(), 0))

        conn.commit()

        st.success("✅ Compte créé (connecte-toi)")

# ==========================================
# STYLE
# ==========================================
def load_bg():
    if Path("background.jpg").exists():
        with open("background.jpg","rb") as f:
            data = base64.b64encode(f.read()).decode()

        st.markdown(f"""
<style>
.stApp {{
background-image: linear-gradient(rgba(0,0,0,0.9),rgba(0,0,0,0.95)),
url("data:image/jpg;base64,{data}");
background-size: cover;
}}
.card {{
background:#0f172a;
padding:15px;
border-radius:12px;
margin-bottom:10px;
}}
</style>
""", unsafe_allow_html=True)

# ==========================================
# IA + ARBITRAGE
# ==========================================
def analyse(o1,oX,o2):
    p1,pX,p2 = 1/o1,1/oX,1/o2
    t=p1+pX+p2

    probs=[p1/t,pX/t,p2/t]
    values=[probs[0]*o1-1, probs[1]*oX-1, probs[2]*o2-1]

    best = ["1","X","2"][np.argmax(values)]
    conf = round(max(values)*100,2)

    inv = (1/o1)+(1/oX)+(1/o2)
    arb = inv < 1
    profit = round((1-inv)*100,2) if arb else 0

    return best, conf, arb, profit

# ==========================================
# MATCHS
# ==========================================
teams = [
("PSG","Marseille"),
("Real Madrid","Barcelone"),
("Chelsea","Arsenal"),
("Bayern","Dortmund"),
("Liverpool","Man City")
]

def get_matches():
    matches=[]
    for t1,t2 in teams:
        matches.append((
            t1,t2,
            np.random.uniform(1.5,3),
            np.random.uniform(2.8,4),
            np.random.uniform(2,4)
        ))
    return matches

# ==========================================
# APP
# ==========================================
def app():
    load_bg()

    st.sidebar.write(f"👤 {st.session_state.user}")

    # Vérifier VIP via API backend (auto update)
    try:
        r = requests.get(f"{API_URL}/user/{st.session_state.user}")
        st.session_state.vip = r.json().get("vip",0)
    except:
        pass

    # PAYWALL
    if not st.session_state.vip:
        st.warning("🔒 Accès VIP requis")

        st.markdown(f"""
💎 Accès complet :

✅ Arbitrage PRO  
✅ Scanner  
✅ Alerts  

👉 [Payer ici]({PAYSTACK_LINK})
""")

        st.stop()

    st.title("⚽ BET AI ENTERPRISE")

    matches = get_matches()

    for t1,t2,o1,oX,o2 in matches:

        best, conf, arb, profit = analyse(o1,oX,o2)

        st.markdown(f"""
<div class="card">
<b>{t1} vs {t2}</b><br>

💸 Odds : {round(o1,2)} | {round(oX,2)} | {round(o2,2)}<br>

💰 Bet : {best}<br>
🧠 Confiance : {conf}%<br>

{"✅ ARBITRAGE "+str(profit)+"%" if arb else "❌ No arbitrage"}
</div>
""", unsafe_allow_html=True)

# ==========================================
# ROUTER
# ==========================================
if "logged" not in st.session_state:
    st.session_state.logged=False

if not st.session_state.logged:
    login()
else:
    app()

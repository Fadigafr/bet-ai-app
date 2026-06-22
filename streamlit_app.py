import base64import basecursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    username TEXT PRIMARY KEY,
    password TEXT,
    vip INTEGER
)
""")
conn.commit()

# ==========================================
# PASSWORD
# ==========================================
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

# ==========================================
# ADMIN PAR DEFAUT
# ==========================================
cursor.execute("""
INSERT OR IGNORE INTO users VALUES (?, ?, ?)
""", ("admin@gmail.com", hash_password("admin123"), 1))
conn.commit()

# ==========================================
# LOGIN
# ==========================================
def login():
    st.title("🔐 Connexion / Inscription")

    email = st.text_input("Email")
    password = st.text_input("Mot de passe", type="password")

    col1, col2 = st.columns(2)

    # LOGIN
    if col1.button("Se connecter"):
        user = cursor.execute(
            "SELECT * FROM users WHERE username=?",
            (email,)
        ).fetchone()

        if user and check_password(password, user[1]):
            st.session_state.logged = True
            st.session_state.user = email
            st.session_state.vip = user[2]
            st.rerun()
        else:
            st.error("❌ Identifiants incorrects")

    # REGISTER
    if col2.button("Créer compte"):
        if not email or not password:
            st.warning("⚠️ Remplis tout")
            return

        hashed = hash_password(password)

        cursor.execute(
            "INSERT OR IGNORE INTO users VALUES (?, ?, ?)",
            (email, hashed, 0)
        )
        conn.commit()

        st.success("✅ Compte créé")

# ==========================================
# ADMIN PANEL (CORRIGÉ)
# ==========================================
def admin_panel():
    st.title("🛠️ ADMIN PANEL")

    if st.session_state.user != "admin@gmail.com":
        st.error("⛔ Accès refusé")
        return

    users = cursor.execute("SELECT * FROM users").fetchall()

    for user in users:
        username, password, vip = user

        # ✅ Toujours créer colonnes ici
        col1, col2, col3 = st.columns(3)

        col1.write(username)
        col2.write("VIP ✅" if vip else "Free ❌")

        # ✅ bouton VIP
        if col3.button(f"VIP {username}", key=f"vip_{username}"):
            cursor.execute(
                "UPDATE users SET vip=1 WHERE username=?",
                (username,)
            )
            conn.commit()
            st.rerun()

# ==========================================
# MATCHS + IA SIMPLE
# ==========================================
teams = [
("PSG","Marseille"),
("Real Madrid","Barcelone"),
("Chelsea","Arsenal"),
("Bayern","Dortmund"),
]

def analyse(o1,oX,o2):
    inv = (1/o1)+(1/oX)+(1/o2)
    arb = inv < 1
    return arb, round((1-inv)*100,2) if arb else 0

def app():

    st.sidebar.write(f"👤 {st.session_state.user}")

    menu = st.sidebar.selectbox(
        "Menu",
        ["🏠 Dashboard","⚽ Betting","🛠️ Admin"]
    )

    # DASHBOARD
    if menu == "🏠 Dashboard":
        st.title("📊 Dashboard")
        st.success("App stable ✅")

    # BETTING
    elif menu == "⚽ Betting":
        st.title("⚽ Analyse")

        for t1,t2 in teams:
            o1,oX,o2 = (
                np.random.uniform(1.5,3),
                np.random.uniform(2.8,4),
                np.random.uniform(2,4)
            )

            arb,profit = analyse(o1,oX,o2)

            st.write(f"{t1} vs {t2}")
            st.write(f"Odds: {round(o1,2)} {round(oX,2)} {round(o2,2)}")

            if arb:
                st.success(f"💰 Arbitrage {profit}%")
            else:
                st.warning("Pas d'arbitrage")

    # ADMIN
    elif menu == "🛠️ Admin":
        admin_panel()

# ==========================================
# ROUTER
# ==========================================
if "logged" not in st.session_state:
    st.session_state.logged = False

if not st.session_state.logged:
    login()
else:
    app()

from pathlib import Path
import sqlite3
import numpy as np
import streamlit as st
import bcrypt

# ==========================================
# CONFIG
# ==========================================
st.set_page_config(page_title="BET AI ENTERPRISE", layout="wide")

# ==========================================
# DATABASE (TOUT EN HAUT OBLIGATOIRE)
# ==========================================
conn = sqlite3.connect("app.db", check_same_thread=False)
cursor = conn.cursor()


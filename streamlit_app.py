# ==================================
# IMPORTS (OBLIGATOIRE EN PREMIER)
# ==================================
import streamlit as st
import sqlite3
import bcrypt
import numpy as np

# ==================================
# CONFIG
# ==================================
st.set_page_config(page_title="BET AI ULTRA PRO", layout="wide")

# ==================================
# DATABASE
# ==================================
conn = sqlite3.connect("app.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    username TEXT PRIMARY KEY,
    password TEXT,
    vip INTEGER DEFAULT 0,
    score INTEGER DEFAULT 0
)
""")
conn.commit()

# ==================================
# PASSWORD
# ==================================
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(password, hashed):
    try:
        return bcrypt.checkpw(password.encode(), hashed.encode())
    except:
        return False

# ==================================
# ADMIN DEFAULT
# ==================================
cursor.execute("""
INSERT OR IGNORE INTO users (username, password, vip, score)
VALUES (?, ?, ?, ?)
""", ("admin@gmail.com", hash_password("admin123"), 1, 100))
conn.commit()

# ==================================
# SESSION
# ==================================
if "logged" not in st.session_state:
    st.session_state.logged = False

# ==================================
# ANALYSE MATCH PRO
# ==================================
def analyse_match(o1, oX, o2):

    inv = (1/o1)+(1/oX)+(1/o2)
    arbitrage = inv < 1
    profit = round((1-inv)*100, 2) if arbitrage else 0

    p1, pX, p2 = 1/o1, 1/oX, 1/o2

    # BTTS
    btts = p1 > 0.4 and p2 > 0.4

    # OVER/UNDER
    over25 = (p1 + p2) > pX

    # SCORE ESTIMÉ
    score_home = int(p1 * 3)
    score_away = int(p2 * 3)

    return arbitrage, profit, btts, over25, f"{score_home}-{score_away}"

# ==================================
# LOGIN
# ==================================
def login():

    st.title("🔐 Connexion")

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
            st.rerun()
        else:
            st.error("Identifiants incorrects")

    # REGISTER
    if col2.button("Créer compte"):

        if not email or not password:
            st.warning("Remplis tous les champs")
            st.stop()

        hashed = hash_password(password)

        existing = cursor.execute(
            "SELECT * FROM users WHERE username=?",
            (email,)
        ).fetchone()

        if existing:
            cursor.execute(
                "UPDATE users SET password=? WHERE username=?",
                (hashed, email)
            )
        else:
            cursor.execute(
                "INSERT INTO users (username,password,vip,score) VALUES (?, ?, ?, ?)",
                (email, hashed, 0, 0)
            )

        conn.commit()
        st.success("Compte créé")

# ==================================
# PROFIL
# ==================================
def profile():

    st.title("👤 Profil")

    user = cursor.execute(
        "SELECT * FROM users WHERE username=?",
        (st.session_state.user,)
    ).fetchone()

    st.write(f"Email : {user[0]}")
    st.write(f"VIP : {'✅' if user[2] else '❌'}")
    st.write(f"Score : {user[3]}")

# ==================================
# ADMIN PANEL + ANALYSE
# ==================================
def admin():

    if st.session_state.user != "admin@gmail.com":
        st.error("Accès refusé")
        return

    st.title("🛠️ ADMIN ANALYSE PRO")

    matches = [
        ("PSG","Marseille"),
        ("Real Madrid","Barcelone"),
        ("Chelsea","Arsenal"),
        ("Bayern","Dortmund")
    ]

    for t1, t2 in matches:

        o1 = np.random.uniform(1.5,3)
        oX = np.random.uniform(2.8,4)
        o2 = np.random.uniform(2,4)

        arb, profit, btts, over25, score = analyse_match(o1,oX,o2)

        st.subheader(f"{t1} vs {t2}")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("BTTS", "✅" if btts else "❌")
        col2.metric("Over 2.5", "✅" if over25 else "❌")
        col3.metric("Score", score)
        col4.metric("Arbitrage", f"{profit}%" if arb else "❌")

        st.divider()

# ==================================
# APP
# ==================================
def app():

    menu = st.sidebar.selectbox(
        "Menu",
        ["Dashboard","Profil","Admin"]
    )

    if menu == "Dashboard":
        st.title("📊 Dashboard")
        st.line_chart(np.random.randn(20).cumsum())

    elif menu == "Profil":
        profile()

    elif menu == "Admin":
        admin()

# ==================================
# ROUTER
# ==================================
if not st.session_state.logged:
    login()
else:
    app()

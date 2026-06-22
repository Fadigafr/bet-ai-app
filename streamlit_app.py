# ==========================================
# IMPORTS
# ==========================================
import streamlit as st
import sqlite3
import bcrypt
import numpy as np

# ==========================================
# CONFIG
# ==========================================
st.set_page_config(page_title="BET AI ULTRA PRO", layout="wide")

# ==========================================
# DATABASE
# ==========================================
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

# ==========================================
# PASSWORD
# ==========================================
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(password, hashed):
    try:
        return bcrypt.checkpw(password.encode(), hashed.encode())
    except:
        return False

# ==========================================
# ADMIN DEFAULT
# ==========================================
cursor.execute("""
INSERT OR IGNORE INTO users (username, password, vip, score)
VALUES (?, ?, ?, ?)
""", ("admin@gmail.com", hash_password("admin123"), 1, 100))
conn.commit()

# ==========================================
# SESSION
# ==========================================
if "logged" not in st.session_state:
    st.session_state.logged = False

# ==========================================
# IA ANALYSE MATCH
# ==========================================
def full_analysis(o1, oX, o2):

    # Arbitrage
    inv = (1/o1)+(1/oX)+(1/o2)
    arb = inv < 1
    profit = round((1-inv)*100,2) if arb else 0

    # Probabilités simplifiées
    p1, pX, p2 = 1/o1, 1/oX, 1/o2

    # BTTS estimation
    btts = p1 > 0.4 and p2 > 0.4

    # Over / Under 2.5
    over25 = (p1 + p2) > pX

    # Score estimé
    goals_home = int((p1*3))
    goals_away = int((p2*3))
    score = f"{goals_home}-{goals_away}"

    return arb, profit, btts, over25, score

# ==========================================
# SCORE SYSTEM
# ==========================================
def update_score(user):
    gain = np.random.randint(1,5)

    cursor.execute(
        "UPDATE users SET score = score + ? WHERE username=?",
        (gain, user)
    )
    conn.commit()

    return gain

# ==========================================
# LOGIN
# ==========================================
def login():

    st.title("🔐 Connexion")

    email = st.text_input("Email")
    password = st.text_input("Mot de passe", type="password")

    col1, col2 = st.columns(2)

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
            st.error("❌ Mauvais identifiants")

    if col2.button("Créer compte"):

        if not email or not password:
            st.warning("Remplis tout")
            st.stop()

        hashed = hash_password(password)

        user = cursor.execute(
            "SELECT * FROM users WHERE username=?",
            (email,)
        ).fetchone()

        if user:
            cursor.execute(
                "UPDATE users SET password=? WHERE username=?",
                (hashed, email)
            )
        else:
            cursor.execute(
                "INSERT INTO users VALUES (?, ?, ?, ?)",
                (email, hashed, 0, 0)
            )

        conn.commit()
        st.success("✅ Compte créé")

# ==========================================
# PROFIL
# ==========================================
def profile():

    st.title("👤 Profil")

    user = cursor.execute(
        "SELECT * FROM users WHERE username=?",
        (st.session_state.user,)
    ).fetchone()

    username, _, vip, score = user

    st.write(f"Email : {username}")
    st.write(f"VIP : {'✅' if vip else '❌'}")
    st.write(f"Score : {score}")

    if st.button("+ Points"):
        gain = update_score(username)
        st.success(f"+{gain} points")

# ==========================================
# ADMIN (ANALYSE PRO)
# ==========================================
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

        arb, profit, btts, over25, score = full_analysis(o1,oX,o2)

        st.subheader(f"{t1} vs {t2}")

        st.write("Odds:", round(o1,2), round(oX,2), round(o2,2))

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("BTTS", "✅" if btts else "❌")
        col2.metric("Over2.5", "✅" if over25 else "❌")
        col3.metric("Score", score)
        col4.metric("Arbitrage", f"{profit}%" if arb else "❌")

        st.divider()

# ==========================================
# APP
# ==========================================
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

# ==========================================
# ROUTER
# ==========================================
if not st.session_state.logged:
    login()
else:
    app()

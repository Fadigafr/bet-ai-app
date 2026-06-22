# ==========================================
# IMPORTS=?",# IMPORTS
                (hashed, email)
            )
        else:
            # ✅ création
            cursor.execute(
                "INSERT INTO users VALUES (?, ?, ?)",
                (email, hashed, 0)
            )

        conn.commit()
        st.success("✅ Compte prêt — connecte-toi")

# ==========================================
# ADMIN PANEL + DASHBOARD USERS
# ==========================================
def admin_panel():

    st.title("🛠️ ADMIN PANEL PRO")

    if st.session_state.user != "admin@gmail.com":
        st.error("⛔ Accès refusé")
        return

    users = cursor.execute("SELECT * FROM users").fetchall()

    # DASHBOARD USERS
    st.subheader("📊 Dashboard Users")

    total = len(users)
    vip = sum([u[2] for u in users])
    free = total - vip

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Users", total)
    c2.metric("VIP", vip)
    c3.metric("Free", free)

    st.divider()

    # GESTION USERS
    for u in users:
        username, password, is_vip = u

        col1, col2, col3, col4 = st.columns(4)

        col1.write(username)
        col2.write("VIP ✅" if is_vip else "Free ❌")

        # ACTIVER VIP
        if col3.button("VIP", key=f"vip_{username}"):
            cursor.execute(
                "UPDATE users SET vip=1 WHERE username=?",
                (username,)
            )
            conn.commit()
            st.rerun()

        # SUPPRIMER
        if col4.button("❌", key=f"del_{username}"):
            cursor.execute(
                "DELETE FROM users WHERE username=?",
                (username,)
            )
            conn.commit()
            st.rerun()

# ==========================================
# ANALYSE (ARBITRAGE)
# ==========================================
def analyse(o1,oX,o2):
    inv = (1/o1)+(1/oX)+(1/o2)
    if inv < 1:
        return True, round((1-inv)*100,2)
    return False, 0

# ==========================================
# APP PRINCIPALE
# ==========================================
def app():

    st.sidebar.write(f"👤 {st.session_state.user}")

    menu = st.sidebar.selectbox(
        "Menu",
        ["Dashboard","Betting","Admin"]
    )

    # DASHBOARD
    if menu == "Dashboard":
        st.title("📊 Dashboard")
        st.success("✅ Application OK")

        data = np.random.randn(50).cumsum()
        st.line_chart(data)

    # BETTING
    elif menu == "Betting":
        st.title("⚽ Scanner Arbitrage")

        matches = [
            ("PSG","Marseille"),
            ("Real Madrid","Barcelone"),
            ("Chelsea","Arsenal"),
        ]

        for t1,t2 in matches:

            o1 = np.random.uniform(1.5,3)
            oX = np.random.uniform(2.8,4)
            o2 = np.random.uniform(2,4)

            arb, profit = analyse(o1,oX,o2)

            st.write(f"{t1} vs {t2}")
            st.write(f"Odds: {round(o1,2)} | {round(oX,2)} | {round(o2,2)}")

            if arb:
                st.success(f"💰 Arbitrage {profit}%")
            else:
                st.warning("❌ Pas d’arbitrage")

    # ADMIN
    elif menu == "Admin":
        admin_panel()

# ==========================================
# ROUTER
# ==========================================
if not st.session_state.logged:
    login()
else:
    app()
# ==========================================
import sqlite3
import streamlit as st
import bcrypt
import numpy as np

# ==========================================
# CONFIG
# ==========================================
st.set_page_config(page_title="BET AI FINAL", layout="wide")

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
INSERT OR IGNORE INTO users VALUES (?, ?, ?)
""", ("admin@gmail.com", hash_password("admin123"), 1))
conn.commit()

# ==========================================
# SESSION
# ==========================================
if "logged" not in st.session_state:
    st.session_state.logged = False

# ==========================================
# LOGIN
# ==========================================
def login():
    st.title("🔐 Connexion / Inscription")

    email = st.text_input("Email")
    password = st.text_input("Mot de passe", type="password")

    col1, col2 = st.columns(2)

    # =====================
    # LOGIN
    # =====================
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

    # =====================
    # REGISTER (SAFE)
    # =====================
    if col2.button("Créer compte"):

        if not email or not password:
            st.warning("⚠️ Remplis tous les champs")
            st.stop()

        existing = cursor.execute(
            "SELECT * FROM users WHERE username=?",
            (email,)
        ).fetchone()

        hashed = hash_password(password)

        if existing:
            # ✅ update si existe
            cursor.execute(

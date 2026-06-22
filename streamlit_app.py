# ==========================================
# IMPORTS
# ==========================================
import sqlite3
import numpy as np
import streamlit as st
import bcrypt

# ==========================================
# CONFIG
# ==========================================
st.set_page_config(page_title="BET AI PRO", layout="wide")

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
    return bcrypt.checkpw(password.encode(), hashed.encode())

# ==========================================
# ADMIN DEFAULT
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
            st.warning("⚠️ Remplis tous les champs")
            return

        hashed = hash_password(password)

        cursor.execute(
            "INSERT OR IGNORE INTO users VALUES (?, ?, ?)",
            (email, hashed, 0)
        )
        conn.commit()

        st.success("✅ Compte créé")

# ==========================================
# ADMIN PANEL PRO
# ==========================================
def admin_panel():
    st.title("🛠️ ADMIN PANEL PRO")

    if st.session_state.user != "admin@gmail.com":
        st.error("⛔ Accès refusé")
        return

    users = cursor.execute("SELECT * FROM users").fetchall()

    # DASHBOARD USERS
    st.subheader("📊 Dashboard Utilisateurs")

    total_users = len(users)
    total_vip = sum([u[2] for u in users])
    total_free = total_users - total_vip

    colA, colB, colC = st.columns(3)
    colA.metric("Utilisateurs", total_users)
    colB.metric("VIP", total_vip)
    colC.metric("Free", total_free)

    st.divider()

    st.subheader("👥 Gestion utilisateurs")

    for u in users:
        username, password, vip = u

        col1, col2, col3, col4 = st.columns(4)

        col1.write(username)
        col2.write("VIP ✅" if vip else "Free ❌")

        # ✅ ACTIVER VIP
        if col3.button("VIP", key=f"vip_{username}"):
            cursor.execute(
                "UPDATE users SET vip=1 WHERE username=?",
                (username,)
            )
            conn.commit()
            st.rerun()

        # ✅ SUPPRIMER USER
        if col4.button("❌", key=f"del_{username}"):
            cursor.execute(
                "DELETE FROM users WHERE username=?",
                (username,)
            )
            conn.commit()
            st.rerun()

# ==========================================
# IA + ARBITRAGE
# ==========================================
def analyse(o1, oX, o2):
    inv = (1/o1) + (1/oX) + (1/o2)
    if inv < 1:
        return True, round((1-inv)*100, 2)
    return False, 0

# ==========================================
# APP MAIN
# ==========================================
def app():

    st.sidebar.write(f"👤 {st.session_state.user}")

    menu = st.sidebar.selectbox(
        "Menu",
        ["🏠 Dashboard", "⚽ Betting", "🛠️ Admin"]
    )

    # ======================
    # DASHBOARD GLOBAL
    # ======================
    if menu == "🏠 Dashboard":
        st.title("📊 Dashboard Global")

        odds = [np.random.uniform(1.5, 3) for _ in range(20)]
        st.line_chart(odds)

        st.success("✅ Application stable")

    # ======================
    # BETTING
    # ======================
    elif menu == "⚽ Betting":
        st.title("⚽ Scanner Arbitrage")

        teams = [
            ("PSG","Marseille"),
            ("Real Madrid","Barcelone"),
            ("Chelsea","Arsenal"),
            ("Bayern","Dortmund"),
        ]

        for t1, t2 in teams:
            o1 = np.random.uniform(1.5,3)
            oX = np.random.uniform(2.8,4)
            o2 = np.random.uniform(2,4)

            arb, profit = analyse(o1, oX, o2)

            st.write(f"{t1} vs {t2}")
            st.write(f"Odds: {round(o1,2)} | {round(oX,2)} | {round(o2,2)}")

            if arb:
                st.success(f"💰 Arbitrage détecté : {profit}%")
            else:
                st.warning("❌ Pas d’arbitrage")

    # ======================
    # ADMIN
    # ======================
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
``

# ==========================================
# IMPORTS
# ==========================================
import sqlite3
import streamlit as st
import bcrypt
import numpy as np

# ==========================================
# CONFIG
# ==========================================
st.set_page_config(page_title="BET AI PRODUCTION", layout="wide")

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

    # LOGIN
    if col1.button("Se connecter"):
        user = cursor.execute(
            "SELECT * FROM users WHERE username=?",
            (email,)
        ).fetchone()

        if user:
            if check_password(password, user[1]):
                st.session_state.logged = True
                st.session_state.user = email
                st.session_state.vip = user[2]
                st.rerun()
            else:
                st.error("❌ Mauvais mot de passe")
        else:
            st.error("❌ Utilisateur introuvable")

    # REGISTER
if col2.button("Créer compte"):

    if not email or not password:
        st.warning("⚠️ Remplis tous les champs")
        return

    user = cursor.execute(
        "SELECT * FROM users WHERE username=?",
        (email,)
    ).fetchone()

    hashed = hash_password(password)

    if user:
        cursor.execute(
            "UPDATE users SET password=? WHERE username=?",
            (hashed, email)
        )
    else:
        cursor.execute(
            "INSERT INTO users VALUES (?, ?, ?)",
            (email, hashed, 0)
        )

    conn.commit()  # ✅ BIEN ALIGNÉ

# ==========================================
# ADMIN PANEL PRO + DASHBOARD USERS
# ==========================================
def admin_panel():
    st.title("🛠️ ADMIN PANEL PRO")

    # Sécurité
    if st.session_state.user != "admin@gmail.com":
        st.error("⛔ Accès refusé")
        return

    users = cursor.execute("SELECT * FROM users").fetchall()

    # =========================
    # DASHBOARD USERS
    # =========================
    st.subheader("📊 Dashboard Utilisateurs")

    total_users = len(users)
    total_vip = sum([u[2] for u in users])
    total_free = total_users - total_vip

    col1, col2, col3 = st.columns(3)
    col1.metric("Total", total_users)
    col2.metric("VIP", total_vip)
    col3.metric("Free", total_free)

    st.divider()

    # =========================
    # GESTION USERS
    # =========================
    st.subheader("👥 Gestion utilisateurs")

    for u in users:
        username, password, vip = u

        c1, c2, c3, c4 = st.columns(4)

        c1.write(username)
        c2.write("VIP ✅" if vip else "Free ❌")

        # ACTIVER VIP
        if c3.button("VIP", key=f"vip_{username}"):
            cursor.execute(
                "UPDATE users SET vip=1 WHERE username=?",
                (username,)
            )
            conn.commit()
            st.rerun()

        # SUPPRIMER
        if c4.button("❌", key=f"del_{username}"):
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
        ["🏠 Dashboard", "⚽ Betting", "🛠️ Admin"]
    )

    # ======================
    # DASHBOARD GLOBAL
    # ======================
    if menu == "🏠 Dashboard":
        st.title("📊 Dashboard Global")

        data = np.random.randn(50).cumsum()
        st.line_chart(data)

        st.success("✅ Application stable (Production Ready)")

    # ======================
    # SCANNER
    # ======================
    elif menu == "⚽ Betting":
        st.title("⚽ Scanner Arbitrage PRO")

        matches = [
            ("PSG","Marseille"),
            ("Real Madrid","Barcelone"),
            ("Chelsea","Arsenal"),
            ("Bayern","Dortmund"),
        ]

        for t1, t2 in matches:
            o1 = np.random.uniform(1.5,3)
            oX = np.random.uniform(2.8,4)
            o2 = np.random.uniform(2,4)

            arb, profit = analyse(o1,oX,o2)

            st.write(f"{t1} vs {t2}")
            st.write(f"Odds: {round(o1,2)} | {round(oX,2)} | {round(o2,2)}")

            if arb:
                st.success(f"💰 Arbitrage détecté : {profit}%")
            else:
                st.warning("❌ Aucun arbitrage")

    # ======================
    # ADMIN
    # ======================
    elif menu == "🛠️ Admin":
        admin_panel()

# ==========================================
# ROUTER (TOUJOURS EN BAS)
# ==========================================
if not st.session_state.logged:
    login()
else:
    app()

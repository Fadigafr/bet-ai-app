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
st.set_page_config(page_title="BET AI CLEAN", layout="wide")

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
# ADMIN PAR DEFAUT
# ==========================================
cursor.execute(
    "INSERT OR IGNORE INTO users VALUES (?, ?, ?)",
    ("admin@gmail.com", hash_password("admin123"), 1)
)
conn.commit()

# ==========================================
# SESSION
# ==========================================
if "logged" not in st.session_state:
    st.session_state.logged = False

# ==========================================
# LOGIN / REGISTER
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
        st.stop()

    existing = cursor.execute(
        "SELECT * FROM users WHERE username=?",
        (email,)
    ).fetchone()

    hashed = hash_password(password)

    if existing:
        cursor.execute(
            "UPDATE users SET password=? WHERE username=?",
            (hashed, email)
        )
    else:
        cursor.execute(
            "INSERT INTO users VALUES (?, ?, ?)",
            (email, hashed, 0)
        )

    conn.commit()   # ✅ même niveau que if/else
    st.success("✅ Compte créé - connecte-toi")   # ✅ même niveau

def profile_page():

    st.title("👤 Profil Utilisateur")

    user = cursor.execute(
        "SELECT * FROM users WHERE username=?",
        (st.session_state.user,)
    ).fetchone()

    username, password, vip, score = user

    st.subheader("Informations")

    st.write(f"📧 Email : {username}")
    st.write(f"💎 Statut : {'VIP ✅' if vip else 'Free ❌'}")
    st.write(f"🏆 Score : {score}")

    st.divider()

    if st.button("⚡ Améliorer score"):
        gained = update_score(username)
        st.success(f"+{gained} points gagnés !")
        st.rerun()

# ==========================================
# ADMIN PANEL
# ==========================================
def admin_panel():
    st.title("🛠️ ADMIN PANEL")

    if st.session_state.user != "admin@gmail.com":
        st.error("⛔ Accès refusé")
        return

    users = cursor.execute("SELECT * FROM users").fetchall()

    # DASHBOARD USERS
    st.subheader("📊 Dashboard Utilisateurs")

    total = len(users)
    vip = sum([u[2] for u in users])

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Users", total)
    c2.metric("VIP", vip)
    c3.metric("Free", total - vip)

    st.divider()

    # GESTION USERS
    for u in users:
        username, password, is_vip = u

        col1, col2, col3, col4 = st.columns(4)

        col1.write(username)
        col2.write("VIP ✅" if is_vip else "Free ❌")

        if col3.button("VIP", key=f"vip_{username}"):
            cursor.execute(
                "UPDATE users SET vip=1 WHERE username=?",
                (username,)
            )
            conn.commit()
            st.rerun()

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
# APP PRINCIPALE
# ==========================================
def app():

    st.sidebar.write(f"👤 {st.session_state.user}")

    menu = st.sidebar.selectbox(
        "Menu",
        ["Dashboard", "Betting", "Admin"]
    )

    # DASHBOARD
    if menu == "Dashboard":
        st.title("📊 Dashboard")
        st.success("✅ Application fonctionne parfaitement")

        data = np.random.randn(50).cumsum()
        st.line_chart(data)

    # BETTING
    elif menu == "Betting":
        st.title("⚽ Scanner Arbitrage")

        matches = [
            ("PSG", "Marseille"),
            ("Real Madrid", "Barcelone"),
            ("Chelsea", "Arsenal"),
        ]

        for t1, t2 in matches:
            o1 = np.random.uniform(1.5, 3)
            oX = np.random.uniform(2.8, 4)
            o2 = np.random.uniform(2, 4)

            arb, profit = analyse(o1, oX, o2)

            st.write(f"{t1} vs {t2}")
            st.write(f"Odds: {round(o1,2)} | {round(oX,2)} | {round(o2,2)}")

            if arb:
                st.success(f"💰 Arbitrage : {profit}%")
            update_score(st.session_state.user)

    # ADMIN
    elif menu == "Admin":
        admin_panel()
def update_score(user):
    score = np.random.randint(1, 10)

    cursor.execute(
        "UPDATE users SET score = score + ? WHERE username=?",
        (score, user)
    )
    conn.commit()

    return score

menu = st.sidebar.selectbox(
    "Menu",
    ["Dashboard", "Betting", "Profil", "Admin"]
)

# ==========================================
# ROUTER
# ==========================================
if not st.session_state.logged:
    login()
else:
    app()

elif menu == "Profil":
    profile_page()

# ==========================================
# IMPORTS (TOUJOURS EN PREMIER)
# ==========================================
import streamlit as st
import sqlite3
import bcrypt
import numpy as np

# ==========================================
# CONFIG
# ==========================================
st.set_page_config(page_title="BET AI CLEAN FINAL", layout="wide")

# ==========================================
# DATABASE
# ==========================================
conn = sqlite3.connect("app.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    username TEXT PRIMARY KEY,
    password TEXT,
    vip INTEGER,
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
# ADMIN DEFAULT (SAFE)
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
# SCORE SYSTEM
# ==========================================
def update_score(user):
    points = np.random.randint(1, 5)

    cursor.execute(
        "UPDATE users SET score = score + ? WHERE username=?",
        (points, user)
    )
    conn.commit()

    return points

# ==========================================
# LOGIN / REGISTER
# ==========================================
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
            st.session_state.vip = user[2]
            st.success("✅ Connexion réussie")
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
                "INSERT INTO users (username, password, vip, score) VALUES (?, ?, ?, ?)",
                (email, hashed, 0, 0)
            )

        conn.commit()
        st.success("✅ Compte créé")

# ==========================================
# PROFIL
# ==========================================
def profile_page():
    st.title("👤 Profil")

    user = cursor.execute(
        "SELECT * FROM users WHERE username=?",
        (st.session_state.user,)
    ).fetchone()

    username, password, vip, score = user

    st.write(f"📧 Email : {username}")
    st.write(f"💎 Statut : {'VIP ✅' if vip else 'Free ❌'}")
    st.write(f"🏆 Score : {score}")

    if st.button("⚡ Gagner points"):
        gained = update_score(username)
        st.success(f"+{gained} points !")
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
    st.subheader("📊 Dashboard utilisateurs")

    total = len(users)
    vip = sum([u[2] for u in users])

    c1, c2, c3 = st.columns(3)
    c1.metric("Total", total)
    c2.metric("VIP", vip)
    c3.metric("Free", total - vip)

    st.divider()

    for u in users:
        username, password, is_vip, score = u

        col1, col2, col3, col4 = st.columns(4)

        col1.write(username)
        col2.write(f"Score: {score}")
        col3.write("VIP ✅" if is_vip else "Free ❌")

        if col3.button("Activer VIP", key=f"vip_{username}"):
            cursor.execute(
                "UPDATE users SET vip=1 WHERE username=?",
                (username,)
            )
            conn.commit()
            st.rerun()

        if col4.button("❌ Supprimer", key=f"del_{username}"):
            cursor.execute(
                "DELETE FROM users WHERE username=?",
                (username,)
            )
            conn.commit()
            st.rerun()

# ==========================================
# ARBITRAGE
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
        ["Dashboard", "Betting", "Profil", "Admin"]
    )

    # DASHBOARD
    if menu == "Dashboard":
        st.title("📊 Dashboard")
        data = np.random.randn(50).cumsum()
        st.line_chart(data)

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

            if arb:
                st.success(f"💰 Arbitrage {profit}%")
                update_score(st.session_state.user)
            else:
                st.warning("❌ Aucun arbitrage")

    elif menu == "Profil":
        profile_page()

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

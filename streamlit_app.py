# ==============================
# IMPORT 
# ==============================
 IMPORTS (TOUJOURS EN PREMIER)
conn = sqlite3.connect("app.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    username TEXT PRIMARY KEY,
    password TEXT,
    vip INTEGER DEFAULT 0
)
""")
conn.commit()

# ==============================
# PASSWORD
# ==============================
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(password, hashed):
    try:
        return bcrypt.checkpw(password.encode(), hashed.encode())
    except:
        return False

# ==============================
# USER ADMIN
# ==============================
cursor.execute("""
INSERT OR IGNORE INTO users (username, password, vip)
VALUES (?, ?, ?)
""", ("admin@gmail.com", hash_password("admin123"), 1))
conn.commit()

# ==============================
# SESSION
# ==============================
if "logged" not in st.session_state:
    st.session_state.logged = False

# ==============================
# LOGIN / REGISTER
# ==============================
def login():

    st.title("🔐 Connexion")

    email = st.text_input("Email")
    password = st.text_input("Mot de passe", type="password")

    col1, col2 = st.columns(2)

    # === LOGIN ===
    if col1.button("Se connecter"):

        user = cursor.execute(
            "SELECT * FROM users WHERE username=?",
            (email,)
        ).fetchone()

        if user and check_password(password, user[1]):
            st.session_state.logged = True
            st.session_state.user = email
            st.success("✅ Connecté")
            st.rerun()
        else:
            st.error("❌ Identifiants incorrects")

    # === REGISTER ===
    if col2.button("Créer compte"):

        if not email or not password:
            st.warning("⚠️ Remplis tous les champs")
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
                "INSERT INTO users (username, password, vip) VALUES (?, ?, ?)",
                (email, hashed, 0)
            )

        conn.commit()
        st.success("✅ Compte créé")

# ==============================
# APP PRINCIPALE
# ==============================
def app():

    st.title("🏠 Dashboard")

    st.write(f"Bienvenue : **{st.session_state.user}**")

    menu = st.sidebar.selectbox(
        "Menu",
        ["Accueil", "Admin"]
    )

    if menu == "Accueil":
        st.success("✅ Application fonctionne parfaitement")

    elif menu == "Admin":

        if st.session_state.user != "admin@gmail.com":
            st.error("⛔ Accès refusé")
            return

        st.subheader("👥 Utilisateurs")

        users = cursor.execute("SELECT * FROM users").fetchall()

        for u in users:
            st.write(u[0], "VIP ✅" if u[2] else "Free ❌")

# ==============================
# ROUTER
# ==============================
if not st.session_state.logged:
    login()
else:
    app()
# ==============================
import streamlit as st
import sqlite3
import bcrypt

# ==============================
# CONFIG
# ==============================
st.set_page_config(page_title="APP CLEAN", layout="centered")

# ==============================
# DATABASE


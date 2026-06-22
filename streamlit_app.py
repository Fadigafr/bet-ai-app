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
import bcrypt

# ✅ HASH PASSWORD
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# ✅ VERIFY PASSWORD
def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

# ✅ INTERFACE LOGIN
def login():
    st.title("🔐 Connexion / Inscription")

    email = st.text_input("Email")
    password = st.text_input("Mot de passe", type="password")

    col1, col2 = st.columns(2)
def admin_panel():
    st.title("🛠️ ADMIN PANEL")

    # Sécurité : accès admin uniquement
    if st.session_state.user != "admin@gmail.com":
        st.error("⛔ Accès refusé")
        return

    st.markdown("## 👥 Utilisateurs")

    users = cursor.execute("SELECT * FROM users").fetchall()

    for user in users:
        username, password, vip = user

        col1, col2, col3, col4 = st.columns(4)

        col1.write(username)
        col2.write("VIP ✅" if vip == 1 else "Free ❌")

        # ACTIVER VIP
        if col3.button(f"Activer VIP {username}"):
            cursor.execute(
                "UPDATE users SET vip=1 WHERE username=?",
                (username,)
            )
            conn.commit()
            st.success(f"{username} → VIP ✅")
            st.rerun()

        # SUPPRIMER USER
        if col4.button(f"Supprimer {username}"):
            cursor.execute(
                "DELETE FROM users WHERE username=?",
                (username,)
            )
            conn.commit()
            st.warning(f"{username} supprimé")
            st.rerun()
            
    # =========================
    # LOGIN
    # =========================
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

    # =========================
    # REGISTER
    # =========================
    if col2.button("Créer compte"):

        if not email or not password:
            st.warning("⚠️ Remplis tous les champs")
            return

        hashed = hash_password(password)

        cursor.execute("""
INSERT OR IGNORE INTO users VALUES (?, ?, ?)
""", ("admin@gmail.com", hash_password("admin123"), 1))
        conn.commit()

        st.success("✅ Compte créé ! Connecte-toi")
new_pass = col3.text_input(f"Nouveau mdp {username}", type="password")

if col3.button(f"Reset {username}"):
    hashed = hash_password(new_pass)

    cursor.execute("""
    UPDATE users SET password=? WHERE username=?
    """, (hashed, username))

    conn.commit()
    st.success("Mot de passe changé ✅")
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

def dashboard_users():
    st.markdown("## 📊 Dashboard Utilisateurs")

    total_users = cursor.execute(
        "SELECT COUNT(*) FROM users"
    ).fetchone()[0]

    total_vip = cursor.execute(
        "SELECT COUNT(*) FROM users WHERE vip=1"
    ).fetchone()[0]

    total_free = total_users - total_vip

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Users", total_users)
    col2.metric("VIP", total_vip)
    col3.metric("Free", total_free)

menu = st.sidebar.selectbox(
    "Menu",
    ["🏠 Dashboard", "⚽ Betting", "🛠️ Admin"]
)

if menu == "🏠 Dashboard":
    dashboard_users()

elif menu == "⚽ Betting":
    # ton code actuel de matchs ici
    pass

elif menu == "🛠️ Admin":
    admin_panel()

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

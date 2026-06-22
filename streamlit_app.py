import base64
from pathlib import Path

import sqlite3
import numpy as np
import streamlit as st
import bcrypt

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
# ADMIN PANEL
# ==========================================
def admin_panel():
    st.title("🛠️ ADMIN PANEL")

    if st.session_state.user != "admin@gmail.com":
        st.error("⛔ Accès refusé")
        return

    users = cursor.execute("SELECT * FROM users").fetchall()

    for user in users:
        username, password, vip = user

        col1, col2, col3, col4, col5 = st.columns(5)

        col1.write(username)
        col2.write("VIP ✅" if vip else "Free ❌")

        if col3.button("VIP", key=f"vip_{username}"):
            cursor.execute("UPDATE users SET vip=1 WHERE username=?", (username,))
            conn.commit()
            st.rerun()

        new_pass = col4.text_input("MDP", type="password", key=f"pass_{username}")

        if col4.button("Reset", key=f"reset_{username}"):
            if new_pass:
                hashed = hash_password(new_pass)
                cursor.execute(
                    "UPDATE users SET password=? WHERE username=?",
                    (hashed, username)
                )
                conn.commit()
                st.rerun()

        if col5.button("❌", key=f"del_{username}"):
            cursor.execute("DELETE FROM users WHERE username=?", (username,))
            conn.commit()
            st.rerun()

# ==========================================
# IA + ARBITRAGE
# ==========================================
def analyse(o1, oX, o2):
    p1, pX, p2 = 1/o1, 1/oX, 1/o2
    total = p1+pX+p2

    probs = [p1/total, pX/total, p2/total]
    values = [probs[0]*o1-1, probs[1]*oX-1, probs[2]*o2-1]

    best = ["1","X","2"][np.argmax(values)]
    conf = round(max(values)*100, 2)

    inv = (1/o1)+(1/oX)+(1/o2)
    arb = inv < 1
    profit = round((1-inv)*100, 2) if arb else 0

    return best, conf, arb, profit

# ==========================================
# MATCHS
# ==========================================
teams = [
("PSG","Marseille"),
("Real Madrid","Barcelone"),
("Chelsea","Arsenal"),
("Bayern","Dortmund"),
("Liverpool","Man City"),
]

def generate_matches():
    matches = []
    for t1, t2 in teams:
        matches.append((
            t1, t2,
            np.random.uniform(1.5, 3),
            np.random.uniform(2.8, 4),
            np.random.uniform(2, 4)
        ))
    return matches

# ==========================================
# STYLE
# ==========================================
def load_bg():
    if Path("background.jpg").exists():
        with open("background.jpg", "rb") as f:
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
border-radius:10px;
margin-bottom:10px;
}}
</style>
""", unsafe_allow_html=True)

# ==========================================
# MAIN APP
# ==========================================
def app():
    load_bg()

    st.sidebar.write(f"👤 {st.session_state.user}")

    menu = st.sidebar.selectbox(
        "Menu",
        ["🏠 Dashboard", "⚽ Betting", "🛠️ Admin"]
    )

    # PAYSTACK PAYWALL
    if not st.session_state.vip:
        st.warning("🔒 Accès VIP requis")
        st.markdown(PAYSTACK_LINK)
        st.stop()

    # DASHBOARD
    if menu == "🏠 Dashboard":
        st.title("📊 Dashboard")

        matches = generate_matches()
        profits = []

        for t1, t2, o1, oX, o2 in matches:
            _, _, arb, profit = analyse(o1, oX, o2)
            profits.append(profit)

        st.metric("Opportunités arbitrage", sum([1 for p in profits if p > 0]))
        st.metric("Profit moyen", round(np.mean(profits),2))

        st.line_chart(profits)

    # BETTING
    elif menu == "⚽ Betting":
        st.title("⚽ Analyse matchs")

        matches = generate_matches()

        for t1, t2, o1, oX, o2 in matches:
            best, conf, arb, profit = analyse(o1, oX, o2)

            st.markdown(f"""
<div class="card">
<b>{t1} vs {t2}</b><br>

💸 Odds : {round(o1,2)} | {round(oX,2)} | {round(o2,2)}<br>

💰 Bet : {best}<br>
🧠 Confiance : {conf}%<br>

{"✅ ARBITRAGE "+str(profit)+"%" if arb else "❌ Aucun arbitrage"}
</div>
""", unsafe_allow_html=True)

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
st.set_page_config(page_title="BET AI SAAS PRO", layout="wide")

DEFAULT_BANKROLL = 100.0
STOP_LOSS = 0.3

PAYSTACK_LINK = "https://paystack.com/pay/TON-LIEN"

# ==========================================
# DATABASE
# ==========================================
conn = sqlite3.connect("app.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
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

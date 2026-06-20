import base64
from pathlib import Path
import sqlite3
import numpy as np
import requests
import streamlit as st

# ==============================================
# CONFIG
# ==============================================
st.set_page_config(page_title="BET AI SAAS PRO", layout="wide")

DEFAULT_BANKROLL = 100.0
MAX_STAKE = 0.10
STOP_LOSS = 0.30

# ==============================================
# SESSION
# ==============================================
if "bankroll" not in st.session_state:
    st.session_state.bankroll = DEFAULT_BANKROLL

# ==============================================
# DATABASE
# ==============================================
conn = sqlite3.connect("bets.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS bets (
    id INTEGER PRIMARY KEY,
    match TEXT,
    prediction TEXT,
    confidence REAL,
    profit REAL,
    result REAL
)
""")

conn.commit()

# ==============================================
# UI DESIGN
# ==============================================
def load_bg():
    if Path("background.jpg").exists():
        with open("background.jpg","rb") as f:
            data = base64.b64encode(f.read()).decode()

        st.markdown(f"""
        <style>
        .stApp {{
            background-image:
            linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.95)),
            url("data:image/jpg;base64,{data}");
            background-size: cover;
        }}

        .card {{
            background: rgba(15,23,42,0.85);
            padding: 18px;
            border-radius: 16px;
            margin-bottom: 12px;
            border: 1px solid #22c55e40;
        }}
        </style>
        """, unsafe_allow_html=True)

# ==============================================
# IA ENGINE
# ==============================================
def probs(o1,oX,o2):
    p1,pX,p2=1/o1,1/oX,1/o2
    t=p1+pX+p2
    return p1/t,pX/t,p2/t

def poisson(p1,p2):
    return np.random.poisson(p1*2.3), np.random.poisson(p2*2.1)

def value(prob,odd):
    return prob*odd-1

def confidence(v,p):
    return max(0,min(100,round((v+p)*100/2,1)))

def kelly(bank,prob,odd):
    edge = prob*odd-1
    if edge <= 0:
        return 0
    k = edge/(odd-1)
    return min(bank*k, bank*MAX_STAKE)

# ==============================================
# ARBITRAGE
# ==============================================
def arbitrage(o1,oX,o2):
    inv=(1/o1)+(1/oX)+(1/o2)
    if inv<1:
        return True, round((1-inv)*100,2)
    return False,0

# ==============================================
# TELEGRAM ALERT
# ==============================================
def send_telegram(msg):
    TOKEN=st.secrets.get("TELEGRAM_TOKEN","")
    CHAT=st.secrets.get("TELEGRAM_CHAT_ID","")

    if not TOKEN or not CHAT:
        return

    url=f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url,data={"chat_id":CHAT,"text":msg})

# ==============================================
# FAKE DATA (100 MATCHES)
# ==============================================
def generate_matches(n=100):
    np.random.seed(42)
    matches=[]
    for i in range(n):
        o1=np.random.uniform(1.5,3)
        oX=np.random.uniform(2.8,4)
        o2=np.random.uniform(1.8,4)
        matches.append((f"Team{i}",f"Team{i+1}",o1,oX,o2))
    return matches

# ==============================================
# MAIN
# ==============================================
def main():
    load_bg()

    st.title("🔥 BET AI SAAS PRO")

    bankroll=st.session_state.bankroll

    if bankroll <= DEFAULT_BANKROLL*(1-STOP_LOSS):
        st.error("⛔ STOP LOSS atteint")
        st.stop()

    matches=generate_matches(100)

    total_profit=0
    total_bets=0
    wins=0

    st.markdown("## 📊 Analyse en cours...")

    for team1,team2,o1,oX,o2 in matches:

        p1,pX,p2=probs(o1,oX,o2)
        gh,ga=poisson(p1,p2)

        v1,vX,v2=value(p1,o1),value(pX,oX),value(p2,o2)

        values={"1":v1,"X":vX,"2":v2}
        best=max(values,key=values.get)

        prob={"1":p1,"X":pX,"2":p2}[best]
        val=values[best]

        conf=confidence(val,prob)
        stake=kelly(bankroll,prob,{"1":o1,"X":oX,"2":o2}[best])

        arb,profit=arbitrage(o1,oX,o2)

        if arb and profit>2:
            send_telegram(f"ARBITRAGE: {team1} vs {team2} profit {profit}%")

        # SIMULATION RESULTAT
        result = np.random.choice([1,-1])
        gain = stake if result==1 else -stake

        total_profit += gain
        total_bets +=1

        if result==1:
            wins+=1

        cursor.execute("""
        INSERT INTO bets (match,prediction,confidence,profit,result)
        VALUES (?,?,?,?,?)
        """,(f"{team1} vs {team2}",best,conf,profit,gain))

        conn.commit()

        # UI
        st.markdown(f"""
<div class="card">
<b>⚽ {team1} vs {team2}</b><br>

💰 Value : {best} ({round(val,2)})<br>
🧠 Confiance : {conf}%<br>

🎯 Score : {gh}-{ga}<br>
💸 Mise : {round(stake,2)} €<br>

</div>
""", unsafe_allow_html=True)

    # ======================================
    # DASHBOARD ANALYTICS
    # ======================================
    st.markdown("## 📈 DASHBOARD ANALYTICS")

    roi = (total_profit / DEFAULT_BANKROLL) * 100
    winrate = (wins / total_bets) * 100 if total_bets else 0

    col1,col2,col3=st.columns(3)

    col1.metric("Profit total", f"{round(total_profit,2)} €")
    col2.metric("ROI", f"{round(roi,2)} %")
    col3.metric("Winrate", f"{round(winrate,2)} %")

    # GRAPHIQUE
    data = cursor.execute("SELECT result FROM bets").fetchall()
    curve = np.cumsum([x[0] for x in data])

    st.line_chart(curve)

    # HISTORIQUE
    st.markdown("## 📊 Historique récents")

    history=cursor.execute("SELECT match,profit,result FROM bets ORDER BY id DESC LIMIT 10").fetchall()

    for h in history:
        st.write(h)

    # BANKROLL
    st.markdown("## 💳 Bankroll")
    st.metric("Capital initial", f"{DEFAULT_BANKROLL} €")
    st.metric("Profit actuel", f"{round(total_profit,2)} €")

# ==============================================
if __name__=="__main__":
    main()

import base64
from pathlib import Path

import numpy as np
import requests
import streamlit as st

# ==========================================
# CONFIG
# ==========================================
st.set_page_config(page_title="BET AI ULTRA PRO", layout="wide")

DEFAULT_BANKROLL = 100.0
MAX_STAKE = 0.10
STOP_LOSS = 0.30

# ==========================================
# SESSION
# ==========================================
if "bankroll" not in st.session_state:
    st.session_state.bankroll = DEFAULT_BANKROLL

# ==========================================
# UI DESIGN
# ==========================================
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
            border: 1px solid #22c55e30;
        }}

        </style>
        """, unsafe_allow_html=True)

# ==========================================
# IA ENGINE
# ==========================================
def probs(o1,oX,o2):
    p1,pX,p2 = 1/o1,1/oX,1/o2
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
    if edge<=0:
        return 0
    k = edge/(odd-1)
    return min(bank*k, bank*MAX_STAKE)

# ==========================================
# ARBITRAGE ENGINE
# ==========================================
def arbitrage(o1,oX,o2):
    inv = (1/o1)+(1/oX)+(1/o2)
    if inv<1:
        return True, round((1-inv)*100,2)
    return False, 0

def arb_stakes(bank,o1,oX,o2):
    inv=(1/o1)+(1/oX)+(1/o2)
    return (
        bank*(1/o1)/inv,
        bank*(1/oX)/inv,
        bank*(1/o2)/inv
    )

# ==========================================
# DATA (SIMULATION OU API)
# ==========================================
def generate_matches(n=100):
    np.random.seed(1)
    matches=[]
    for i in range(n):
        t1=f"Team{i}"
        t2=f"Team{i+1}"
        o1=np.random.uniform(1.5,3)
        oX=np.random.uniform(2.8,4)
        o2=np.random.uniform(1.8,4)
        matches.append((t1,t2,o1,oX,o2))
    return matches

# ==========================================
# MAIN
# ==========================================
def main():
    load_bg()

    st.title("⚽ BET AI ULTRA PRO — SCANNER 100 MATCHS")

    bankroll=st.session_state.bankroll

    if bankroll <= DEFAULT_BANKROLL*(1-STOP_LOSS):
        st.error("⛔ Stop-loss atteint")
        st.stop()

    matches = generate_matches(100)

    arb_count=0
    best_bets=[]

    for team1,team2,o1,oX,o2 in matches:

        p1,pX,p2 = probs(o1,oX,o2)

        gh,ga = poisson(p1,p2)

        v1,vX,v2 = value(p1,o1),value(pX,oX),value(p2,o2)

        values={"1":v1,"X":vX,"2":v2}
        best=max(values,key=values.get)

        prob={"1":p1,"X":pX,"2":p2}[best]
        val=values[best]

        conf = confidence(val,prob)

        stake = kelly(bankroll,prob,{"1":o1,"X":oX,"2":o2}[best])

        arb,profit = arbitrage(o1,oX,o2)

        if arb:
            arb_count +=1
            s1,sX,s2 = arb_stakes(bankroll,o1,oX,o2)

        best_bets.append((team1,team2,conf,best))

        # =====================================
        # UI CARD
        # =====================================
        st.markdown(f"""
<div class="card">

<h4>⚽ {team1} vs {team2}</h4>

📊 Odds : {round(o1,2)} | {round(oX,2)} | {round(o2,2)}  

🧠 Confiance IA : <b>{conf}%</b>  
💰 Value : <b>{best} ({round(val,2)})</b>  

🎯 Score IA : {gh}-{ga}  
📈 {'OVER 2.5' if gh+ga>=3 else 'UNDER 2.5'}  

💸 Mise Kelly : {round(stake,2)} €

</div>
""", unsafe_allow_html=True)

        # =====================================
        # ARBITRAGE UI
        # =====================================
        if arb:
            st.success(f"""
💰 ARBITRAGE DÉTECTÉ

Profit : {profit}%

Mises :
1 → {round(s1,2)} €
X → {round(sX,2)} €
2 → {round(s2,2)} €
""")

    # =====================================
    # STATS
    # =====================================
    st.markdown("## 📊 RÉSULTATS")

    st.metric("Arbitrages trouvés", arb_count)

    # TOP IA
    st.markdown("## 🧠 TOP IA")

    for m in sorted(best_bets, key=lambda x:x[2], reverse=True)[:10]:
        st.write(f"{m[0]} vs {m[1]} → {m[3]} ({m[2]}%)")

    # BANKROLL
    st.markdown("## 💳 BANKROLL")
    st.metric("Capital", f"{round(bankroll,2)} €")


# ==========================================
if __name__ == "__main__":
    main()

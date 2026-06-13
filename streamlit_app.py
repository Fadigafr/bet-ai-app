import time
import numpy as np
import requests

TOKEN = "TON_TOKEN"
CHAT_ID = "TON_CHAT_ID"

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text
    })

def generate_prono():

    team1 = "PSG"
    team2 = "OM"

    s1 = np.random.randint(1, 3)
    s2 = np.random.randint(0, 2)

    message = f"""
 PRONO AUTO

{team1} vs {team2}
Score : {s1}-{s2}
"""

    send_message(message)
    
from telegram_bot import send_message

def generate_prono():

    team1 = "PSG"
    team2 = "Marseille"

    # IA simple
    s1 = np.random.randint(1, 3)
    s2 = np.random.randint(0, 2)

    total = s1 + s2

    btts = s1 > 0 and s2 > 0
    over = total >= 3

    # logique pari
    combo = ["1X"]

    if btts:
        combo.append("BTTS")

    if over:
        combo.append("+2.5")

    message = f"""
 PRONO IA AUTOMATIQUE

{team1} vs {team2}

 Score : {s1}-{s2}
 BTTS : {'OUI' if btts else 'NON'}
 +2.5 : {'OUI' if over else 'NON'}

 COMBINÉ :
{" + ".join(combo)}

 Confiance : 85%
"""

    send_message(message)

generate_prono()

TOKEN = "TON_TOKEN"
CHAT_ID = "TON_CHAT_ID"

def send():
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": " PRONO DU JOUR"
    })
def save_result(team1, team2, result):
    with open("data.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow([team1, team2, result])
API_KEY = "TA_CLE_API"

def get_odds():
    url = "https://v3.football.api-sports.io/odds?league=39&season=2024"

    headers = {
        "x-apisports-key": API_KEY
    }

    r = requests.get(url, headers=headers)
    data = r.json()

    odds_data = []

    for match in data["response"][:5]:
        teams = match["teams"]
        home = teams["home"]["name"]
        away = teams["away"]["name"]

        # exemple simple (structure API variable)
        odds_data.append({
            "home": home,
            "away": away,
            "odd1": 1.80,
            "oddX": 3.20,
            "odd2": 4.50
        })

    return odds_data
# =====================
# CONFIG
# =====================
st.set_page_config(page_title="BET AI PRO", layout="wide")

# =====================
# STYLE PREMIUM MOBILE
# =====================
st.markdown("""
<style>

/* Background */
body {
    background-color: #f5f7fa;
}

/* Header */
.header {
    background-color: #1f8c96;
    padding: 15px;
    color: white;
    font-size: 22px;
    font-weight: bold;
    text-align: center;
    border-radius: 10px;
}

/* Tabs */
.tab {
    display: inline-block;
    padding: 10px 15px;
    margin-right: 5px;
    background: #e0e0e0;
    border-radius: 8px;
    font-weight: bold;
}

/* Active tab */
.active-tab {
    background: #f4c542;
}

/* Card */
.card {
    background-color: white;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 12px;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
}

/* Tip */
.tip {
    color: green;
    font-weight: bold;
    font-size: 18px;
}

/* Probability */
.prob {
    display: inline-block;
    padding: 5px 10px;
    background: #eef2f7;
    border-radius: 6px;
    margin-right: 5px;
}

</style>
""", unsafe_allow_html=True)

# =====================
# HEADER
# =====================
st.markdown('<div class="header"> BET AI PREMIUM</div>', unsafe_allow_html=True)

# =====================
# NAVIGATION TABS
# =====================
st.markdown("""
<div>
    <span class="tab active-tab">1X2</span>
    <span class="tab">Over/Under</span>
    <span class="tab">BTTS</span>
    <span class="tab">Score</span>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# =====================
# MATCHS (SIMULATION)
# =====================
matches = [
    ("Atletico GO", "CRB"),
    ("SalPa", "KUPS Akatemia"),
    ("Dinamo Batumi", "Dila"),
]

# =====================
# IA SIMPLE
# =====================
def analyse(team1, team2):
    prob1 = np.random.randint(45, 75)
    probX = np.random.randint(10, 25)
    prob2 = 100 - prob1 - probX

    if prob1 > prob2:
        tip = "1"
        odd = round(1.3 + (100 - prob1)/100, 2)
def predict_proba():

    attack1 = np.random.uniform(1.2, 2.5)
    attack2 = np.random.uniform(1.0, 2.2)

    defense1 = np.random.uniform(0.8, 1.8)
    defense2 = np.random.uniform(0.8, 1.8)

    xg1 = attack1 * (2 - defense2)
    xg2 = attack2 * (2 - defense1)

    total = xg1 + xg2

    prob1 = xg1 / total
    prob2 = xg2 / total
    probX = 1 - (prob1 + prob2)

    return prob1, probX, prob2
def value_bet(prob, odd):
    implied = 1 / odd

    if prob > implied:
        return True
    return False

matches = get_odds()

for m in matches:

    prob1, probX, prob2 = predict_proba()

    v1 = value_bet(prob1, m["odd1"])
    vX = value_bet(probX, m["oddX"])
    v2 = value_bet(prob2, m["odd2"])

    best = None

    if v1:
        best = "1"
    elif vX:
        best = "X"
    elif v2:
        best = "2"
    else:
        best = "Aucune value"

    st.markdown(f"""
    <div class="card">
        <b>{m["home"]} vs {m["away"]}</b><br><br>

        Prob IA : {round(prob1*100)}% | {round(probX*100)}% | {round(prob2*100)}%<br>
        Cotes : {m["odd1"]} / {m["oddX"]} / {m["odd2"]}<br><br>

         VALUE : <b>{best}</b>
    </div>
    """, unsafe_allow_html=True)

def generate_script():

    return """
 PRONO DU JOUR

PSG vs OM

 BTTS
 +2.5 buts

 Cote : 3.40

 Clique lien en bio
"""

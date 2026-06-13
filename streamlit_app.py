import streamlit as st
import numpy as np

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

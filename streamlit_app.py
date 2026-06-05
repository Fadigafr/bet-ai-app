import streamlit as st
import pandas as pd
import math
import stripe

# ======================
# CONFIG
# ======================
stripe.api_key = "TA_CLE_STRIPE"

# ======================
# LOGIN
# ======================
users = {
    "fred": "1234",
    "vip": "vip123"
}

st.sidebar.title("🔐 Connexion")

username = st.sidebar.text_input("Utilisateur")
password = st.sidebar.text_input("Mot de passe", type="password")

is_logged = False

if username in users and users[username] == password:
    st.sidebar.success("✅ Connecté")
    is_logged = True
else:
    st.sidebar.error("❌ Non connecté")

# ======================
# STRIPE
# ======================
def create_checkout():
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        mode='subscription',
        line_items=[{
            'price_data': {
                'currency': 'eur',
                'unit_amount': 1000,
                'recurring': {'interval': 'month'},
                'product_data': {'name': 'BET AI PRO VIP'},
            },
            'quantity': 1,
        }],
        success_url='https://bet-ai-app.streamlit.app',
        cancel_url='https://bet-ai-app.streamlit.app',
    )
    return session.url

# ======================
# DESIGN PREMIUM
# ======================
st.markdown("""
<style>
body {
    background-color: #0f172a;
    color: white;
}
.main-title {
    font-size: 40px;
    color: #22c55e;
    font-weight: bold;
}
.card {
    background: #1e293b;
    padding: 15px;
    border-radius: 15px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">⚽ BET AI PRO</p>', unsafe_allow_html=True)
st.write("🔥 Prédictions football intelligentes avec IA")

# ======================
# DATA (temporaire)
# ======================
df = pd.read_csv("sample_matches.csv")

# ======================
# IA SIMPLE (POISSON)
# ======================
def poisson_prob(home_xg, away_xg):
    home_win = 0
    draw = 0
    away_win = 0
    
    for i in range(5):
        for j in range(5):
            prob = (math.exp(-home_xg) * home_xg**i / math.factorial(i)) * \
                   (math.exp(-away_xg) * away_xg**j / math.factorial(j))
            
            if i > j:
                home_win += prob
            elif i == j:
                draw += prob
            else:
                away_win += prob
    
    return home_win, draw, away_win

# ======================
# AFFICHAGE
# ======================
st.divider()

if not is_logged:
    st.warning("🔒 Connecte-toi ou prends VIP pour accéder aux prédictions")
    
    if st.button("💎 Devenir VIP"):
        st.markdown(create_checkout())
else:
    st.success("🔥 Mode VIP activé")

    for index, row in df.iterrows():

        home_win, draw, away_win = poisson_prob(row["xg_home"], row["xg_away"])

        confidence = max(home_win, draw, away_win)
        value = (home_win * 2.2) - 1

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader(f"{row['home']} vs {row['away']}")

        c1, c2, c3 = st.columns(3)
        c1.metric("🏠 Home", f"{home_win*100:.1f}%")
        c2.metric("🤝 Draw", f"{draw*100:.1f}%")
        c3.metric("🚀 Away", f"{away_win*100:.1f}%")

        st.metric("⚽ BTTS", f"{min(home_win, away_win)*100:.1f}%")
        
        if confidence > 0.65:
            st.success("✅ Haute confiance")
        elif confidence > 0.5:
            st.warning("⚖️ Moyenne")
        else:
            st.error("❌ Risqué")

        if value > 0:
            st.success(f"🔥 VALUE BET +{round(value,2)}")

        st.markdown('</div>', unsafe_allow_html=True)

# ======================
# FOOTER BUSINESS
# ======================
st.divider()
st.info("💎 Version gratuite limitée — passe VIP pour plus de matchs")

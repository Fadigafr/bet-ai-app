import streamlit as st
import requests
import pandas as pd
import numpy as np
import stripe

# ================================
# CONFIG APP
# ================================
st.set_page_config(page_title="Bet AI PRO MAX", layout="wide")

# ================================
# CONFIG STRIPE
# ================================
stripe.api_key = "TA_CLE_STRIPE"  # (require '[clj-http.client :as client])

(client/get "https://free-api-live-football-data.p.rapidapi.com/football-players-search" {:headers {:x-rapidapi-key "acddc25c4amsh1b5de20e73be716p1933dfjsn4e554c3a6bf4"
                                                                                                    :x-rapidapi-host "free-api-live-football-data.p.rapidapi.com"
                                                                                                    :Content-Type "application/json"}
                                                                                          :query-params {:search "m"}})

# ================================
# INTERFACE
# ================================
st.title(" BET AI PRO MAX")
st.markdown("Analyse intelligente des matchs de football")

# ================================
# SECTION ANALYSE
# ================================
st.subheader(" Analyse de match")

team1 = st.text_input("Équipe 1")
team2 = st.text_input("Équipe 2")

if st.button("Lancer Analyse"):
    if team1 and team2:
        st.info("Analyse en cours...")

        # Simulation IA (propre)
        score_team1 = np.random.randint(0, 4)
        score_team2 = np.random.randint(0, 4)

        st.success(" Résultat IA")

        st.markdown(f"""
        ###  Résultat prédit
        **{team1} {score_team1} - {score_team2} {team2}**
        """)

        # Probabilité
        prob = np.random.randint(60, 95)
        st.write(f" Confiance IA : {prob}%")

    else:
        st.warning("Remplis les équipes")

# ================================
# SECTION PAIEMENT
# ================================
st.subheader(" Abonnement Premium")

if st.button("S'abonner (10€)"):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "eur",
                    "product_data": {
                        "name": "Abonnement Bet AI PRO"
                    },
                    "unit_amount": 1000,
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url="https://bet-ai-app.streamlit.app",
            cancel_url="https://bet-ai-app.streamlit.app",
        )

        st.success(" Paiement prêt")
        st.markdown(f"[ Payer ici]({session.url})")

    except Exception as e:
        st.error(f"Erreur : {str(e)}")

# ================================
# FOOTER
# ================================
st.markdown("---")
st.caption("Bet AI PRO MAX © 2026")

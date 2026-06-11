import streamlit as st
import requests
import pandas as pd
import stripe

# CONFIG
st.set_page_config(page_title="Bet AI Pro", layout="wide")

# Stripe
stripe.api_key = "TA_CLE_STRIPE"

# UI
st.title(" BET AI PRO MAX")
st.write("Prédictions football intelligentes")

# Bouton paiement
if st.button("S'abonner (10€)"):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "eur",
                    "product_data": {
                        "name": "Abonnement Bet AI"
                    },
                    "unit_amount": 1000,
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url="https://your-app.streamlit.app",
            cancel_url="https://your-app.streamlit.app",
        )
        st.success("Paiement lancé ")
        st.markdown(session.url)
    except Exception as e:
        st.error(str(e))

# Fake prediction (propre)
if st.button("Analyser match"):
    st.write(" Analyse en cours...")
    score = "2 - 1"
    st.success(f"Score prédit : {score}")

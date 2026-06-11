import streamlit as st
import json
import hashlib
import os

# Fichier utilisateurs
USER_FILE = "users.json"

# Charger utilisateurs
def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return {}

# Sauvegarder utilisateurs
def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

# Hash mot de passe
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

users = load_users()

menu = st.sidebar.selectbox("Menu", ["Login", "Créer compte"])

if menu == "Créer compte":
    st.subheader("Créer un compte")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("S'inscrire"):
        if username not in users:
            users[username] = hash_password(password)
            save_users(users)
            st.success("Compte créé ✅")
        else:
            st.error("Utilisateur existe déjà")

elif menu == "Login":
    st.subheader("Connexion")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Se connecter"):
        if username in users and users[username] == hash_password(password):
            st.session_state["user"] = username
            st.success("Connecté ✅")
        else:
            st.error("Erreur login")

# Vérifier connexion
if "user" not in st.session_state:
    st.stop()

st.write(f"Bienvenue {st.session_state['user']}")

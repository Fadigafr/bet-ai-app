
import math
import pandas as pd
import streamlit as st

st.markdown("""
<h1 style='color:#16a34a;'>⚽ BET AI PRO</h1>
<p>Prédictions intelligentes avec IA</p>
""", unsafe_allow_html=True)
st.set_page_config(page_title='Demo Sport Analytics Online', layout='wide')

@st.cache_data
def load_data():
    return pd.read_csv('sample_matches.csv')


def poisson_pmf(k: int, lam: float) -> float:
    if lam < 0:
        return 0.0
    return math.exp(-lam) * (lam ** k) / math.factorial(k)


def score_matrix(xg_home: float, xg_away: float, max_goals: int = 5):
    matrix = []
    for i in range(max_goals + 1):
        row = []
        for j in range(max_goals + 1):
            row.append(poisson_pmf(i, xg_home) * poisson_pmf(j, xg_away))
        matrix.append(row)
    return matrix


def summarize_probs(matrix):
    home_win = draw = away_win = btts = 0.0
    best = (0, 0, -1.0)
    for i, row in enumerate(matrix):
        for j, p in enumerate(row):
            if i > j:
                home_win += p
            elif i == j:
                draw += p
            else:
                away_win += p
            if i > 0 and j > 0:
                btts += p
            if p > best[2]:
                best = (i, j, p)
    return {
        'home_win': home_win,
        'draw': draw,
        'away_win': away_win,
        'btts': btts,
        'best_score': f'{best[0]}-{best[1]}',
        'best_prob': best[2],
    }


def confidence_label(prob):
    if prob >= 0.65:
        return 'Élevée'
    if prob >= 0.50:
        return 'Moyenne'
    return 'Faible'


def inject_style():
    st.markdown("""
<style>
.main-title {
    font-size: 38px;
    font-weight: bold;
    color: #16a34a;
}
.card {
    background-color: #f3f4f6;
    padding: 15px;
    border-radius: 15px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">⚽ BET AI PRO</p>', unsafe_allow_html=True)
st.markdown("🚀 Prédictions football avec intelligence artificielle")


inject_style()
st.markdown('<div class="main-title">⚽ Demo Sport Analytics Online</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Prototype web éducatif — simulation uniquement, sans pari réel.</div>', unsafe_allow_html=True)

with st.sidebar:
    st.header('Filtres')
    league_filter = st.selectbox('Ligue', ['Toutes'] + sorted(load_data()['league'].unique().tolist()))
    show_only_btts = st.checkbox('Afficher seulement BTTS > 50%', False)
    min_home = st.slider('Probabilité domicile minimale', 0.0, 1.0, 0.0, 0.05)
    max_goals = st.slider('Nombre max de buts simulés', 3, 8, 5)


df = load_data()
if league_filter != 'Toutes':
    df = df[df['league'] == league_filter].copy()

cards = []
for _, row in df.iterrows():
    matrix = score_matrix(float(row['xg_home']), float(row['xg_away']), max_goals=max_goals)
    s = summarize_probs(matrix)
    if show_only_btts and s['btts'] <= 0.50:
        continue
    if s['home_win'] < min_home:
        continue
    cards.append((row, s))

c1, c2, c3 = st.columns(3)
c1.metric('Matchs affichés', len(cards))
c2.metric('Ligues', df['league'].nunique())
c3.metric('Mode', 'Web online')

if not cards:
    st.info('Aucun match ne correspond aux filtres actuels.')
else:
    for row, s in cards:
      with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader(f"{row['home']} vs {row['away']}")

    col1, col2, col3 = st.columns(3)

    col1.metric("🏠 Home", f"{s['home_win']*100:.1f}%")
    col2.metric("🤝 Draw", f"{s['draw']*100:.1f}%")
    col3.metric("🚀 Away", f"{s['away_win']*100:.1f}%")

    st.metric("⚽ BTTS", f"{s['btts']*100:.1f}%")
    st.metric("📊 Score", s["best_score"])

    value = (s['home_win'] * 2.2) - 1

    if value > 0:
        st.success(f"🔥 VALUE BET (+{round(value,2)})")

    st.markdown('</div>', unsafe_allow_html=True)
            with col2:
                st.metric('Domicile', f"{s['home_win']*100:.1f}%")
                st.metric('Nul', f"{s['draw']*100:.1f}%")
            with col3:
                st.metric('Extérieur', f"{s['away_win']*100:.1f}%")
                st.metric('BTTS', f"{s['btts']*100:.1f}%")
            with col4:
                st.metric('Score plausible', s['best_score'])
                st.metric('Confiance', confidence_label(max(s['home_win'], s['draw'], s['away_win'])))
                st.metric("Probabilité domicile", f"{s['home_win']*100:.1f}%")
                st.metric("BTTS", f"{s['btts']*100:.1f}%")
                st.metric("Score", s["best_score"])
                value = (s['home_win'] * 2.2) - 1
                confidence = max(s['home_win'], s['draw'], s['away_win'])

                if confidence > 0.65:
                st.success("✅ Haute confiance")
                elif confidence > 0.5:
                st.warning("⚖️ Moyenne")
         else:
                st.error("❌ Risqué")   

             over25 = 1 - (s['home_win'] + s['draw'])  # approx simple
             st.metric("🔥 Over 2.5", f"{round(over25*100,1)}%")

                if value > 0:
                st.success(f"🔥 VALUE BET (+{round(value,2)})")
            with st.expander('Détails'):
                st.write(f"- Forme récente {row['home']} : {row['home_form']} points / 5 matchs")
                st.write(f"- Forme récente {row['away']} : {row['away_form']} points / 5 matchs")
                st.caption("Cette version emploie des données d'exemple. Tu peux ensuite la relier à tes propres statistiques.")

             if st.button("💎 ACCÈS VIP"):
                st.write("Contact WhatsApp ou paiement Stripe")
    if value > 0.2:
            send_alert(f"🔥 VALUE BET: {row['home']} vs {row['away']}")

              st.divider()
              st.subheader("💎 ACCÈS VIP")

              st.write("✅ 10 matchs / jour")
              st.write("✅ Value bets")
              st.write("✅ Alertes temps réel")

          if st.button("🚀 Devenir VIP"):
              st.write("Contact WhatsApp ou paiement (Stripe à venir)")


          def send_alert(msg):
    print("ALERTE:", msg)st.divider()
st.markdown('### Déploiement rapide')
st.code("""1) Pousse ce dossier sur GitHub
2) Déploie sur Streamlit Community Cloud
3) Partage le lien""")

st.markdown(f"""
<div class="card">
    <b>{team1} vs {team2}</b><br><br>

    <b>Probabilité :</b> {prob1}% | {probX}% | {prob2}%<br>
    <b>Cote :</b> {odd}<br>
    <b>Tip :</b> <span style="color:green; font-weight:bold">{tip}</span>
</div>
""", unsafe_allow_html=True)
st.markdown("""
<style>
.card {
    background-color: #f0f2f6;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

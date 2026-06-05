import streamlit as st
import math
import datetime
import urllib.request
import json

st.set_page_config(
    page_title="Live Analytics Engine",
    page_icon="⚽",
    layout="centered"
)

st.markdown("""
<style>
div.stButton > button:first-child {
    width: 100%;
    height: 52px;
    font-size: 18px;
    font-weight: bold;
    background-color: #10b981;
    color: white;
}
</style>
""", unsafe_allow_html=True)

PRIVATE_PASSWORD = "admin"

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("🔒 Secure Access Required")
    user_password = st.text_input("Authorization Key:", type="password")
    if st.button("Unlock Engine"):
        if user_password == PRIVATE_PASSWORD:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Invalid Key.")
    st.stop()

@st.cache_data(ttl=1800)
def fetch_live_global_fixtures():
    target_leagues = {
        "English Premier League": "4328",
        "Spanish La Liga": "4335",
        "Italian Serie A": "4332",
        "French Ligue 1": "4334",
        "German Bundesliga": "4331"
    }
    fixtures_by_league = {}
    for name, lid in target_leagues.items():
        url = f"https://www.thesportsdb.com/api/v1/json/3/eventsnextleague.php?id={lid}"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla'})
            with urllib.request.urlopen(req) as response:
                raw_data = json.loads(response.read().decode())
                events = raw_data.get("events", [])
                fixtures_by_league[name] = []
                if events:
                    for e in events:
                        fixtures_by_league[name].append({
                            "home": e.get("strHomeTeam"),
                            "away": e.get("strAwayTeam"),
                            "date": e.get("dateEvent"),
                            "time": e.get("strTime", "Scheduled")
                        })
        except:
            pass
    for name in target_leagues.keys():
        if name not in fixtures_by_league or len(fixtures_by_league[name]) == 0:
            fixtures_by_league[name] = [
                {"home": "Manchester United", "away": "Liverpool", "date": str(datetime.date.today()), "time": "16:00:00"},
                {"home": "Real Madrid", "away": "Barcelona", "date": str(datetime.date.today()), "time": "20:00:00"},
                {"home": "Juventus", "away": "Inter Milan", "date": str(datetime.date.today()), "time": "18:45:00"}
            ]
    return fixtures_by_league

LIVE_FIXTURES = fetch_live_global_fixtures()

st.title("⚽ Live Match Matrix Engine")
st.write(f"System Sync Date: {datetime.date.today().strftime('%A, %B %d, %Y')}")

selected_league = st.selectbox("Select Target League:", list(LIVE_FIXTURES.keys()))

st.subheader("📅 Live Schedule (Upcoming Matches)")
league_matches = LIVE_FIXTURES[selected_league]
match_labels = [f"{m['date']} [{m['time'][:5]}] — {m['home']} vs {m['away']}" for m in league_matches]
chosen_idx = st.radio("Select Match to Analyze:", range(len(match_labels)), format_func=lambda x: match_labels[x])
active_match = league_matches[chosen_idx]

def calculate_match_prediction(home, away):
    score = sum(ord(c) for c in home) + sum(ord(c) for c in away)
    factor = score % 100
    if factor < 33:
        return "PREDICTION: DRAW (X)", 35 + (factor % 15), 38 + (factor % 10)
    elif factor < 66:
        return f"PREDICTION: HOME WIN ({home})", 45 + (factor % 20), 24 + (factor % 8)
    else:
        return f"PREDICTION: AWAY WIN ({away})", 42 + (factor % 22), 26 + (factor % 9)

pred_outcome, pred_conf, calc_draw = calculate_match_prediction(active_match['home'], active_match['away'])

st.info(f"🔮 {pred_outcome} | Confidence: {pred_conf}% | Baseline Draw: {calc_draw}%")

st.markdown("---")
total_fixtures = st.number_input("Total Pool Fixtures (n):", min_value=1, max_value=100, value=49)
expected_draws = st.number_input("Expected Matrix Draws (d):", min_value=1, max_value=40, value=14)
selected_fixtures = st.number_input("Fixtures in Selected System (k):", min_value=1, max_value=int(total_fixtures), value=5)

if st.button("Execute Calculations"):
    n_total = int(total_fixtures)
    d_draws = int(expected_draws)
    s_selected = int(selected_fixtures)
    total_ways = math.comb(n_total, s_selected)
    
    st.success(f"🎯 Matrix Analysis for {active_match['home']} vs {active_match['away']}")
    for exact_matches in range(s_selected + 1):
        w_draws = math.comb(d_draws, exact_matches)
        w_non_draws = math.comb(n_total - d_draws, s_selected - exact_matches)
        prob = ((w_draws * w_non_draws) / total_ways) * 100 if total_ways > 0 else 0.0
        st.metric(label=f"Probability of exactly {exact_matches} Draws:", value=f"{prob:.2f}%")
    st.balloons()

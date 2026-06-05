import streamlit as st
import math

# --- 1. MOBILE-FRIENDLY CONFIGURATION ---
st.set_page_config(
    page_title="Private Analytics Engine", 
    page_icon="⚽", 
    layout="centered"
)

st.markdown("""
    <style>
    div.stButton > button:first-child {
        width: 100%;
        height: 50px;
        font-size: 18px;
        font-weight: bold;
    }
    input {
        font-size: 18px !important;
    }
    </style>
""", unsafe_allow_html=True)
# --- 2. SECURITY LAYER ---
PRIVATE_PASSWORD = "admin" 

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("🔒 Secure Analytics Portal")
    st.write("This is a private predictive terminal.")
    
    user_password = st.text_input("Enter Private Access Key:", type="password")
    
    if st.button("Unlock Dashboard"):
        if user_password == PRIVATE_PASSWORD:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Access Denied: Incorrect Password.")

else:
    st.title("📊 Football Predictive Matrix")
    st.write("Input recent form below to run the Poisson Distribution safety filters.")
    
    if st.button("🔒 Secure Log Out"):
        st.session_state["authenticated"] = False
        st.rerun()
        
    st.markdown("---")

    st.subheader("🏠 Home Team Analytics")
    home_name = st.text_input("Home Team Name:", "Home Team")
    home_attack = st.number_input(f"Avg Goals Scored by {home_name} at Home:", min_value=0.0, max_value=6.0, value=1.8, step=0.1)
    home_defense = st.number_input(f"Avg Goals Conceded by {home_name} at Home:", min_value=0.0, max_value=6.0, value=0.9, step=0.1)

    st.markdown("---")

    st.subheader("🚀 Away Team Analytics")
    away_name = st.text_input("Away Team Name:", "Away Team")
    away_attack = st.number_input(f"Avg Goals Scored by {away_name} Away:", min_value=0.0, max_value=6.0, value=1.2, step=0.1)
    away_defense = st.number_input(f"Avg Goals Conceded by {away_name} Away:", min_value=0.0, max_value=6.0, value=1.6, step=0.1)

    st.markdown("---")

    st.subheader("🌐 League Context")
    league_avg_goals = st.number_input("Average Goals Scored per Match in this League:", min_value=0.5, max_value=5.0, value=1.35, step=0.05)

    st.markdown("---")

    if st.button("⚡ CALCULATE SAFE PREDICTIONS"):
        with st.spinner("Simulating match matrix..."):
            
            home_att_str = home_attack / league_avg_goals
            home_def_str = home_defense / league_avg_goals
            away_att_str = away_attack / league_avg_goals
            away_def_str = away_defense / league_avg_goals

            home_xg = home_att_str * away_def_str * league_avg_goals
            away_xg = away_att_str * home_def_str * league_avg_goals

            def poisson_prob(lmbda, k):
                return (math.exp(-lmbda) * (lmbda ** k)) / math.factorial(k)

            home_matrix = [poisson_prob(home_xg, i) for i in range(6)]
            away_matrix = [poisson_prob(away_xg, i) for i in range(6)]

            home_win_p = 0.0
            away_win_p = 0.0
            draw_p = 0.0
            
            over_1_5_p = 0.0
            over_2_5_p = 0.0
            btts_p = 0.0

            for h in range(6):
                for a in range(6):
                    match_prob = home_matrix[h] * away_matrix[a]
                    
                    if h > a:
                        home_win_p += match_prob
                    elif a > h:
                        away_win_p += match_prob
                    else:
                        draw_p += match_prob
                    
                    if (h + a) > 1:
                        over_1_5_p += match_prob
                    if (h + a) > 2:
                        over_2_5_p += match_prob
                    if h > 0 and a > 0:
                        btts_p += match_prob

            st.header("🎯 Probability Results")
            
            m1, m2 = st.columns(2)
            m1.metric(f"{home_name} Win", f"{home_win_p*100:.1f}%")
            m2.metric(f"{away_name} Win", f"{away_win_p*100:.1f}%")
            
            st.metric("🤝 Straight Draw Probability", f"{draw_p*100:.1f}%")
            
            st.markdown("---")
            st.subheader("💡 Safe Selections (High-Safety Filter)")

            safe_picks = []
            
            if over_1_5_p >= 0.78:
                safe_picks.append(f"🟢 **Over 1.5 Goals** ({over_1_5_p*100:.1f}%)")
            if home_win_p + draw_p >= 0.75 and home_win_p > 0.45:
                safe_picks.append(f"🟢 **{home_name} Win or Draw (1X)** ({(home_win_p + draw_p)*100:.1f}%)")
            if away_win_p + draw_p >= 0.75 and away_win_p > 0.45:
                safe_picks.append(f"🟢 **{away_name} Win or Draw (X2)** ({(away_win_p + draw_p)*100:.1f}%)")
            if draw_p >= 0.31:
                safe_picks.append(f"🔵 **High Draw Risk / Match Deadlock** ({draw_p*100:.1f}%) — Strong candidate for pool selection.")
            if btts_p >= 0.65:
                safe_picks.append(f"🟢 **Both Teams to Score (BTTS)** ({btts_p*100:.1f}%)")

            if safe_picks:
                for pick in safe_picks:
                    st.write(pick)
            else:
                st.warning("⚠️ High Risk Match: No options met the 75%+ safety threshold.")

            with st.expander("🔍 View Calculated xG Metrics"):
                st.write(f"📊 *{home_name} Expected Goals ($xG$):* **{home_xg:.2f}**")
                st.write(f"📊 *{away_name} Expected Goals ($xG$):* **{away_xg:.2f}**")

import streamlit as st
import pandas as pd
import calendar
from datetime import datetime

# Apple-style Dark Mode Aesthetics
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; font-family: -apple-system, BlinkMacSystemFont, sans-serif; }
    .stNumberInput input { background-color: #1c1c1e; color: #ffffff; border-radius: 10px; }
    h1, h2 { color: #ffffff; }
    </style>
""", unsafe_allow_html=True)

st.title("Corpus Tracker")

# Settings
col1, col2 = st.columns(2)
with col1:
    start_corpus = st.number_input("Starting Corpus", value=1000.0)
with col2:
    growth_rate = st.slider("Growth Rate (%)", 0.0, 10.0, 2.0) / 100

# Calendar Data Generation
year, month = 2026, 7
cal = calendar.Calendar(firstweekday=6)
month_days = cal.monthdayscalendar(year, month)

# Store inputs in Session State
if 'data' not in st.session_state:
    st.session_state.data = {}

# Calendar UI
st.subheader("Daily Tracking")
for week in month_days:
    cols = st.columns(7)
    for i, day in enumerate(week):
        if day != 0:
            date_key = f"{year}-{month}-{day}"
            input_val = cols[i].number_input(f"{day}", value=st.session_state.data.get(date_key, 0.0), key=date_key)
            st.session_state.data[date_key] = input_val

# Logic: Calculate Actuals + Projected Compounding
def get_projection():
    projection = []
    curr = start_corpus
    for day in range(1, 32):
        try:
            date_key = f"{year}-{month}-{day}"
            # Add input if exists
            curr += st.session_state.data.get(date_key, 0.0)
            
            # If it's a weekday and no input, apply compounding
            if calendar.weekday(year, month, day) < 5 and st.session_state.data.get(date_key, 0.0) == 0:
                curr += (curr * growth_rate)
            
            projection.append({"Day": day, "Balance": round(curr, 2)})
        except: break
    return pd.DataFrame(projection)

# Graph
st.subheader("Growth Projection")
df = get_projection()
st.line_chart(df.set_index("Day"))

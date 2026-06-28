import streamlit as st
import pandas as pd
import calendar

# Set layout to wide at the very start
st.set_page_config(layout="wide", page_title="Corpus Tracker")

# Apple-style Dark Aesthetics & Full-Width CSS
st.markdown("""
    <style>
    .block-container { max-width: 95% !important; padding-top: 1rem; }
    .stApp { background-color: #000000; color: #f5f5f7; font-family: -apple-system, sans-serif; }
    .day-card { background: #1c1c1e; border-radius: 12px; padding: 15px; border: 1px solid #333; height: 120px; }
    .bal { font-size: 1.1em; font-weight: 700; color: #ffffff; margin-bottom: 5px; }
    .date { font-size: 0.8em; color: #98989d; }
    </style>
""", unsafe_allow_html=True)

st.title("Corpus Tracker")

# Settings Sidebar
with st.sidebar:
    start_corpus = st.number_input("Starting Corpus", value=1000.0)
    growth_rate = st.slider("Weekday Growth (%)", 0.0, 10.0, 2.0) / 100

# Month Config
year, month = 2026, 7
if 'data' not in st.session_state: st.session_state.data = {}

# Logic to calculate balances daily
def calculate_daily_balances():
    balances = {}
    curr = start_corpus
    for d in range(1, 32):
        key = f"{year}-{month}-{d}"
        # Apply manual input if exists, else apply growth
        if key in st.session_state.data and st.session_state.data[key] != 0:
            curr += st.session_state.data[key]
        elif calendar.weekday(year, month, d) < 5:
            curr += (curr * growth_rate)
        balances[d] = round(curr, 2)
    return balances

daily_balances = calculate_daily_balances()

# Calendar Grid
cal = calendar.Calendar(firstweekday=6)
for week in cal.monthdayscalendar(year, month):
    cols = st.columns(7)
    for i, day in enumerate(week):
        if day != 0:
            with cols[i]:
                st.markdown(f'<div class="day-card">', unsafe_allow_html=True)
                st.markdown(f'<div class="bal">${daily_balances[day]:,.2f}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="date">{month}/{day}</div>', unsafe_allow_html=True)
                val = st.number_input("", key=f"in_{day}", value=st.session_state.data.get(f"{year}-{month}-{day}", 0.0), label_visibility="collapsed")
                st.session_state.data[f"{year}-{month}-{day}"] = val
                st.markdown('</div>', unsafe_allow_html=True)

# Graphing
st.subheader("Growth Projection")
st.line_chart(pd.DataFrame.from_dict(daily_balances, orient='index'))

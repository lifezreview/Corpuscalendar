import streamlit as st
import pandas as pd
import calendar
from datetime import datetime

# --- Apple Aesthetic CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #f5f5f7; font-family: -apple-system, BlinkMacSystemFont, sans-serif; }
    .day-box { background-color: #1c1c1e; padding: 10px; border-radius: 12px; margin: 5px; text-align: center; }
    .balance-text { font-size: 1.2em; font-weight: bold; color: #ffffff; }
    .date-text { font-size: 0.8em; color: #98989d; }
    </style>
""", unsafe_allow_html=True)

st.title("Corpus Tracker")

# Settings
col1, col2 = st.columns([1, 1])
with col1: start_corpus = st.number_input("Starting Corpus", value=1000.0)
with col2: growth_rate = st.slider("Daily Growth Rate (%)", 0.0, 10.0, 2.0) / 100

# Logic
year, month = 2026, 7
cal = calendar.Calendar(firstweekday=6)
month_days = cal.monthdayscalendar(year, month)

if 'data' not in st.session_state: st.session_state.data = {}

# Display Calendar Grid
st.subheader("Monthly Overview")
for week in month_days:
    cols = st.columns(7)
    for i, day in enumerate(week):
        if day != 0:
            date_key = f"{year}-{month}-{day}"
            # Track compounding balance
            # For simplicity, calculating real-time balance based on previous inputs
            cols[i].markdown(f'<div class="day-box">', unsafe_allow_html=True)
            cols[i].markdown(f'<div class="date-text">{day}</div>', unsafe_allow_html=True)
            
            # User input for profit/loss on that day
            val = cols[i].number_input("", value=st.session_state.data.get(date_key, 0.0), key=date_key, label_visibility="collapsed")
            st.session_state.data[date_key] = val
            
            # Simple balance estimation display
            estimated_balance = start_corpus + sum(st.session_state.data.values())
            cols[i].markdown(f'<div class="balance-text">${estimated_balance:.2f}</div>', unsafe_allow_html=True)
            cols[i].markdown('</div>', unsafe_allow_html=True)

# Graph
st.subheader("Compounded Growth Path")
# Re-calculating logic for the chart
data_list = []
curr = start_corpus
for d in range(1, 32):
    k = f"{year}-{month}-{d}"
    if k in st.session_state.data: curr += st.session_state.data[k]
    elif calendar.weekday(year, month, d) < 5: curr += (curr * growth_rate)
    data_list.append(curr)

st.line_chart(data_list)

import streamlit as st
import pandas as pd
import calendar
from datetime import datetime
import os

# Configuration
DATA_FILE = "user_data.csv"

# Load or Initialize Data
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=["Date", "ProfitLoss"])

st.set_page_config(layout="wide")
st.title("📈 Corpus Tracker")

# Sidebar - Settings
with st.sidebar:
    st.header("Global Settings")
    start_corpus = st.number_input("Starting Corpus", value=1000.0)
    current_year = st.number_input("Year", value=2026)
    current_month = st.selectbox("Month", range(1, 13), index=5)

# Calendar Logic
cal = calendar.Calendar(firstweekday=6)
month_days = cal.monthdayscalendar(current_year, current_month)

# Display Calendar
st.subheader(f"{calendar.month_name[current_month]} {current_year}")
cols = st.columns(7)
for i, day_name in enumerate(["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]):
    cols[i].write(f"**{day_name}**")

for week in month_days:
    cols = st.columns(7)
    for i, day in enumerate(week):
        if day != 0:
            date_str = f"{current_year}-{current_month:02d}-{day:02d}"
            # Input for specific day
            val = cols[i].number_input(f"{day}", key=date_str, value=0.0, step=1.0)
            if val != 0:
                # Update DataFrame
                df = df[df["Date"] != date_str]
                df = pd.concat([df, pd.DataFrame([{"Date": date_str, "ProfitLoss": val}])])
                df.to_csv(DATA_FILE, index=False)

# Graphing
st.subheader("Growth Projection")
if not df.empty:
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')
    df['Balance'] = start_corpus + df['ProfitLoss'].cumsum()
    st.line_chart(df.set_index('Date')['Balance'])

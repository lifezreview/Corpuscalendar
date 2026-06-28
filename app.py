import streamlit as st
import calendar
import pandas as pd

st.set_page_config(page_title="Corpus Growth Calculator", layout="wide")
st.title("📈 Corpus Growth Projection")

# Sidebar for inputs
with st.sidebar:
    start_corpus = st.number_input("Starting Corpus", value=1000.0, step=100.0)
    growth_rate = st.slider("Daily Growth Rate (%)", 0.0, 10.0, 2.0) / 100
    year = st.number_input("Year", value=2026)
    month = st.selectbox("Month", range(1, 13), index=6)

# Logic
def get_data(start_corpus, growth_rate, year, month):
    data = []
    current_corpus = start_corpus
    cal = calendar.Calendar()
    for day_info in cal.itermonthdates(year, month):
        if day_info.month != month: continue
        
        is_weekday = day_info.weekday() < 5
        growth = 0
        if is_weekday:
            growth = current_corpus * growth_rate
            current_corpus += growth
            
        data.append({
            "Date": day_info.strftime("%Y-%m-%d"),
            "Day": day_info.strftime("%A"),
            "Start": round(current_corpus - growth, 2),
            "Growth": round(growth, 2),
            "End": round(current_corpus, 2)
        })
    return pd.DataFrame(data)

df = get_data(start_corpus, growth_rate, year, month)

# Display
st.table(df)
st.metric("Final Projected Corpus", f"{df['End'].iloc[-1]:,.2f}")

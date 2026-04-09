import streamlit as st
import pandas as pd
import sqlite3
from database import create_database
from scheduler import start_scheduler, logs
import threading

# -------- PAGE CONFIG --------
st.set_page_config(
    page_title="Web Scraper Scheduler",
    layout="wide"
)

# -------- CREATE DATABASE --------
create_database()

# -------- TITLE --------
st.markdown(
    "<h1 style='text-align:center;color:#38bdf8;'>Automated Web Scraper Scheduler</h1>",
    unsafe_allow_html=True
)

# -------- SESSION STATE --------
if 'scheduler_started' not in st.session_state:
    st.session_state.scheduler_started = False

# -------- START SCHEDULER FUNCTION --------
def start_thread():
    thread = threading.Thread(target=start_scheduler, daemon=True)
    thread.start()
    st.session_state.scheduler_started = True

# -------- BUTTON --------
if not st.session_state.scheduler_started:
    if st.button("Start Scheduler"):
        start_thread()
        st.success("✅ Scheduler Started!")
else:
    st.info("🟢 Scheduler is running in background...")

# -------- LOGS --------
st.subheader("📜 Scraper Logs (Last 10)")
if len(logs) == 0:
    st.write("No logs yet...")
else:
    for log in logs[-10:][::-1]:
        st.write(log)

# -------- DATA TABLE --------
st.subheader("📊 Scraped Data")

try:
    conn = sqlite3.connect("data/scraped_data.db")
    df = pd.read_sql("SELECT * FROM products", conn)

    if df.empty:
        st.warning("No data available yet. Run the scraper first.")
    else:
        # ✅ FIXED HERE
        st.dataframe(df, width="stretch")

except Exception as e:
    st.error(f"Error loading data: {e}")

# -------- DOWNLOAD CSV --------
st.subheader("⬇️ Download Data")

if 'df' in locals() and not df.empty:
    st.download_button(
        label="Download CSV",
        data=df.to_csv(index=False),
        file_name="scraped_data.csv",
        mime="text/csv"
    )
else:
    st.write("No data to download.") 
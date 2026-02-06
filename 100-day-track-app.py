import streamlit as st
import time
from datetime import datetime, timedelta

st.set_page_config(page_title="100 Day Challenge", layout="wide")

# --- 1. SETUP STATE ---
if 'ticks' not in st.session_state:
    st.session_state.ticks = {}  # Store: {day_number: timestamp}
if 'start_date' not in st.session_state:
    st.session_state.start_date = datetime.now().date()

# --- 2. HEADER & COUNTDOWN ---
st.title("🔥 100 Days of Greatness")

col1, col2, col3 = st.columns(3)
with col1:
    new_start = st.date_input("Challenge Start Date", st.session_state.start_date)
    st.session_state.start_date = new_start

# Calculate Countdown
end_date = st.session_state.start_date + timedelta(days=100)
days_left = (end_date - datetime.now().date()).days

with col2:
    st.metric("Days Completed", f"{len(st.session_state.ticks)} / 100")
with col3:
    st.metric("Days Remaining", f"{max(0, days_left)}")

st.progress(len(st.session_state.ticks) / 100)

# --- 3. THE 100-DAY GRID ---
st.write("### Your Progress Map")
cols = st.columns(10) # 10x10 Grid

for i in range(1, 101):
    with cols[(i-1) % 10]:
        # Check if this day is already done
        is_done = i in st.session_state.ticks
        
        if is_done:
            # Display a "Checked" status
            st.button(f"✅ Day {i}", key=f"day_{i}", disabled=True)
        else:
            # Display a clickable button for the current/next day
            if st.button(f"Day {i}", key=f"day_{i}"):
                # RECORD DATA
                now = datetime.now()
                st.session_state.ticks[i] = now
                
                # ANIMATION
                st.balloons()
                st.toast(f"Day {i} smashed! Keep going!")
                time.sleep(0.5)
                st.rerun()

# --- 4. DATA & TIME ANALYSIS ---
st.divider()
st.subheader("⏳ Time Analysis")

if len(st.session_state.ticks) > 1:
    # Sort the days completed to find the gap between the last two
    completed_days = sorted(st.session_state.ticks.keys())
    last_day = completed_days[-1]
    prev_day = completed_days[-2]
    
    time_gap = st.session_state.ticks[last_day] - st.session_state.ticks[prev_day]
    
    # Simple formatting for the time gap
    hours, remainder = divmod(time_gap.total_seconds(), 3600)
    minutes, _ = divmod(remainder, 60)
    
    st.info(f"It took you **{int(hours)}h {int(minutes)}m** between your last two ticks!")

# Clock since last tick
if st.session_state.ticks:
    last_tick_time = max(st.session_state.ticks.values())
    since_last = datetime.now() - last_tick_time
    st.write(f"⏱️ **Time since last tick:** {str(since_last).split('.')[0]}")
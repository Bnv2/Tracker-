import streamlit as st
import time
import random
from datetime import datetime, timedelta

# 1. PAGE SETUP (Wide & Compact)
st.set_page_config(page_title="100 Days Progress", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS to shrink the button sizes so they fit on one screen
st.markdown("""
    <style>
    div.stButton > button {
        width: 100%;
        padding: 5px;
        font-size: 10px !important;
    }
    .metric-container { background-color: #f0f2f6; padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. STATE MANAGEMENT
if 'ticks' not in st.session_state:
    st.session_state.ticks = {}
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""

# 3. USER ONBOARDING
if not st.session_state.user_name:
    with st.container():
        name = st.text_input("Enter your name to begin:")
        if st.button("Start My Journey"):
            st.session_state.user_name = name
            st.rerun()
    st.stop()

# 4. MOTIVATION & HEADER
quotes = [
    "One day at a time.", "Believe you can and you're halfway there.",
    "Don't stop until you're proud.", "Great things take time.",
    "Small steps lead to big results."
]

st.title(f"🔥 Let's go {st.session_state.user_name}, you got this!")
st.caption(f"💡 {random.choice(quotes)}")

# 5. DASHBOARD METRICS (Timeline & Progress)
col1, col2, col3 = st.columns([2, 1, 1])

# Timeline Calculation
start_date = datetime.now().date() # For this demo, starting today
total_days = 100
days_passed = len(st.session_state.ticks)
progress_pct = days_passed / total_days

with col1:
    st.write(f"**Journey Progress:** {days_passed}%")
    st.progress(progress_pct)
    # Timeline visualization
    st.write(f"🚩 Start {'—' * 20} 🎯 Day 100")

with col2:
    if st.session_state.ticks:
        last_tick = max(st.session_state.ticks.values())
        diff = datetime.now() - last_tick
        # Showing Hours, Minutes, AND Seconds
        secs = int(diff.total_seconds())
        st.metric("Time Since Last Tick", f"{secs // 3600}h {(secs % 3600) // 60}m {secs % 60}s")
    else:
        st.metric("Time Since Last Tick", "Ready?")

with col3:
    st.metric("Completion Rate", f"{days_passed}/100")

# 6. THE 100-DAY COMPACT GRID
st.write("### Progress Grid")
# Using 20 columns to make it very short and avoid scrolling
grid_cols = st.columns(20) 

for i in range(1, 101):
    col_idx = (i-1) % 20
    with grid_cols[col_idx]:
        is_done = i in st.session_state.ticks
        
        # We use a toggle-like behavior: If clicked while done, it UNTICKS.
        if is_done:
            if st.button(f"✅{i}", key=f"d{i}", help="Click to untick"):
                del st.session_state.ticks[i]
                st.rerun()
        else:
            if st.button(f"{i}", key=f"d{i}"):
                st.session_state.ticks[i] = datetime.now()
                st.balloons()
                st.rerun()

# 7. INTERVAL LOG
if st.session_state.ticks:
    with st.expander("View Detailed Intervals"):
        sorted_times = sorted(st.session_state.ticks.items())
        for idx, (day, timestamp) in enumerate(sorted_times):
            if idx > 0:
                prev_time = sorted_times[idx-1][1]
                gap = timestamp - prev_time
                g_sec = int(gap.total_seconds())
                st.write(f"Day {sorted_times[idx-1][0]} → Day {day}: {g_sec // 3600}h {(g_sec % 3600) // 60}m {g_sec % 60}s")

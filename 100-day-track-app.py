import streamlit as st
import random
import time
from datetime import datetime

# 1. PAGE SETUP
st.set_page_config(page_title="100 Days Progress", layout="wide")

# 2. STYLING
st.markdown("""
    <style>
    div.stButton > button { height: 60px !important; font-size: 16px !important; font-weight: bold !important; }
    .quote-style { font-size: 150% !important; font-style: italic; color: #4A90E2; text-align: center; }
    .interval-text { font-family: monospace; color: #555; }
    </style>
    """, unsafe_allow_html=True)

# 3. STATE MANAGEMENT
if 'ticks' not in st.session_state:
    st.session_state.ticks = {}
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'current_quote' not in st.session_state:
    quotes = ["One day at a time.", "Believe you can and you're halfway there.", "Stay consistent.", "Progress over perfection."]
    st.session_state.current_quote = random.choice(quotes)

# 4. LOGIN
if not st.session_state.user_name:
    st.title("🏆 100-Day Challenge")
    name = st.text_input("Enter your name:")
    if st.button("Start"):
        st.session_state.user_name = name
        st.rerun()
    st.stop()

# 5. HEADER
st.title(f"🔥 Let's go {st.session_state.user_name}!")
st.markdown(f'<p class="quote-style">💡 {st.session_state.current_quote}</p>', unsafe_allow_html=True)

# 6. THE FRAGMENTED LIVE STATS (Ticks every 1s)
@st.fragment(run_every="1s")
def render_live_stats():
    col1, col2, col3 = st.columns([2, 1, 1])
    days_passed = len(st.session_state.ticks)
    
    with col1:
        st.write(f"**Journey Progress:** {days_passed}%")
        st.progress(days_passed / 100)
    
    with col2:
        if st.session_state.ticks:
            last_tick = max(st.session_state.ticks.values())
            diff = datetime.now() - last_tick
            secs = int(diff.total_seconds())
            st.metric("Time Since Last Tick", f"{secs // 3600}h {(secs % 3600) // 60}m {secs % 60}s")
        else:
            st.metric("Time Since Last Tick", "Ready?")
            
    with col3:
        st.metric("Completed", f"{days_passed}/100")

render_live_stats()

# 7. THE HISTORY SECTION (Calculation logic)
st.divider()
if len(st.session_state.ticks) > 1:
    with st.expander("⏳ View Detailed Intervals (How long each day took)"):
        # Sort ticks by day number
        sorted_days = sorted(st.session_state.ticks.keys())
        
        for i in range(1, len(sorted_days)):
            day_current = sorted_days[i]
            day_prev = sorted_days[i-1]
            
            time_diff = st.session_state.ticks[day_current] - st.session_state.ticks[day_prev]
            td_secs = int(time_diff.total_seconds())
            
            # Formatting the duration
            duration = f"{td_secs // 3600}h {(td_secs % 3600) // 60}m {td_secs % 60}s"
            st.write(f"**Day {day_prev} → Day {day_current}:** {duration}")

# 8. THE PROGRESS GRID
st.write("### Progress Grid")
grid_cols = st.columns(10) 

# Handle Skip Warning
if 'skip_warning' in st.session_state and st.session_state.skip_warning:
    day = st.session_state.skip_warning
    st.warning(f"⚠️ Skip Warning: You are jumping to Day {day}!")
    c1, c2 = st.columns(2)
    if c1.button("Confirm Skip", use_container_width=True):
        st.session_state.ticks[day] = datetime.now()
        st.session_state.skip_warning = None
        st.balloons()
        st.rerun()
    if c2.button("Cancel", use_container_width=True):
        st.session_state.skip_warning = None
        st.rerun()
else:
    for i in range(1, 101):
        with grid_cols[(i-1) % 10]:
            is_done = i in st.session_state.ticks
            if is_done:
                if st.button(f"✅ {i}", key=f"d{i}", use_container_width=True):
                    del st.session_state.ticks[i]
                    st.rerun()
            else:
                if st.button(f"{i}", key=f"d{i}", use_container_width=True):
                    # Anti-skip check
                    if i > 1 and (i - 1) not in st.session_state.ticks:
                        st.session_state.skip_warning = i
                        st.rerun()
                    else:
                        st.session_state.ticks[i] = datetime.now()
                        st.balloons()
                        st.rerun()

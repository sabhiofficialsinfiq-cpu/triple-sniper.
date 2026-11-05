import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="1pm Dear ZB GUESSING",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS for Professional Dark UI
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #0E1117;
        color: #FFFFFF;
    }
    /* Header Styling */
    .header-title {
        color: #4A90E2;
        font-size: 36px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 0px;
    }
    .header-subtitle {
        color: #A0AAB5;
        font-size: 16px;
        text-align: center;
        margin-top: 5px;
        margin-bottom: 20px;
    }
    /* Result Cards (A, B, C) */
    .number-box {
        background-color: #1A1F2B;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        border: 2px solid #2E3A4E;
        margin-bottom: 10px;
    }
    .number-box-A { border-color: #4A90E2; }
    .number-box-B { border-color: #50E3C2; }
    .number-box-C { border-color: #E94E77; }
    
    .box-label { color: #A0AAB5; font-size: 14px; font-weight: bold; }
    .box-number { color: #FFFFFF; font-size: 48px; font-weight: bold; margin: 0; }
    
    /* Large Output Number */
    .big-output {
        background-color: #1A1F2B;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        border: 1px solid #2E3A4E;
        font-size: 60px;
        font-weight: bold;
        letter-spacing: 10px;
        color: #FFFFFF;
        margin: 20px 0;
    }
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1A1F2B;
        border-radius: 5px;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #4A90E2 !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Header Section
st.markdown('<div class="header-title">1pm Dear ZB GUESSING</div>', unsafe_allow_html=True)
st.markdown('<div class="header-subtitle">Ion Saliu Mathematics | 3-Digit Precision Engine</div>', unsafe_allow_html=True)

# Draws Loaded Badge
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.info("🗄️ Draws Loaded: 400+")

st.divider()

# 4. Input Section (Sidebar)
with st.sidebar:
    st.header("📥 Data Input")
    uploaded_file = st.file_uploader("📸 Upload Result Photo", type=["jpg", "jpeg", "png"])
    manual_input = st.text_input("Or Enter Yesterday's Number (3-Digits)", max_chars=3)
    
    st.divider()
    run_button = st.button("🚀 RUN 1PM DEAR ZB GUESSING", use_container_width=True, type="primary")
    st.caption("Powered by FFG Mathematics & Gemini AI")

# 5. Output Section (Main Dashboard)
if run_button:
    # Placeholder for backend logic (We will connect this later)
    # For now, showing dummy data to visualize the UI
    
    tab1, tab2 = st.tabs(["🎯 Single Board Sniper", "🏆 Top 5 Pro Engine"])
    
    # --- TAB 1: SINGLE BOARD ---
    with tab1:
        st.success("✅ PLAY THIS 1 BOARD")
        st.caption("Saliu Filters Passed (Sum Median: 13) | Score: 153")
        
        # A, B, C Boxes
        colA, colB, colC = st.columns(3)
        with colA:
            st.markdown('<div class="number-box number-box-A"><div class="box-label">A (1st)</div><div class="box-number">4</div></div>', unsafe_allow_html=True)
        with colB:
            st.markdown('<div class="number-box number-box-B"><div class="box-label">B (2nd)</div><div class="box-number">5</div></div>', unsafe_allow_html=True)
        with colC:
            st.markdown('<div class="number-box number-box-C"><div class="box-label">C (3rd)</div><div class="box-number">1</div></div>', unsafe_allow_html=True)
            
        # Big Number Output
        st.markdown('<div class="big-output">4 5 1</div>', unsafe_allow_html=True)
        
        # Buttons
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
        with col_btn2:
            st.button("📋 Copy Exact Number", use_container_width=True)
            
        # Expander for Box Play
        with st.expander("📦 Show Box Play (Permutations)"):
            st.write("451, 415, 541, 514, 145, 154")
            
    # --- TAB 2: TOP 5 PRO ENGINE ---
    with tab2:
        st.info("💡 Top 5 Predictions for the next draw")
        
        # Loop to show 5 ranks (Dummy Data)
        dummy_ranks = [
            {"rank": 1, "a": 7, "b": 9, "c": 2, "sum": 18, "score": 82},
            {"rank": 2, "a": 3, "b": 6, "c": 1, "sum": 10, "score": 79},
            {"rank": 3, "a": 4, "b": 8, "c": 5, "sum": 17, "score": 41},
            {"rank": 4, "a": 7, "b": 6, "c": 2, "sum": 15, "score": 82},
            {"rank": 5, "a": 7, "b": 8, "c": 2, "sum": 17, "score": 81}
        ]
        
        for item in dummy_ranks:
            st.markdown(f"#### RANK #{item['rank']} (Score: {item['score']})")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f'<div class="number-box number-box-A"><div class="box-label">A (1st)</div><div class="box-number">{item["a"]}</div></div>', unsafe_allow_html=True)
            with c2:
                st.markdown(f'<div class="number-box number-box-B"><div class="box-label">B (2nd)</div><div class="box-number">{item["b"]}</div></div>', unsafe_allow_html=True)
            with c3:
                st.markdown(f'<div class="number-box number-box-C"><div class="box-label">C (3rd)</div><div class="box-number">{item["c"]}</div></div>', unsafe_allow_html=True)
            
            st.markdown(f'<div class="big-output" style="font-size: 40px; padding: 10px;">{item["a"]} {item["b"]} {item["c"]}</div>', unsafe_allow_html=True)
            st.caption(f"Sum: {item['sum']}")
            st.divider()

else:
    st.info("👈 Please upload a photo or enter the number in the sidebar and click 'RUN' to get predictions.")
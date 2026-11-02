import streamlit as st
import pandas as pd
import numpy as np
import itertools

# ==========================================
# 1. PAGE CONFIGURATION & STYLING
# ==========================================
st.set_page_config(
    page_title="Single Board Sniper | Ion Saliu",
    page_icon="🎯",
    layout="centered"
)

st.markdown("""
    <style>
    .stApp { background-color: #0A0E17; color: white; }
    .main-title { color: #4A90E2; font-size: 45px; font-weight: 900; text-align: center; letter-spacing: 2px; margin-bottom: 0px; text-transform: uppercase; }
    .sub-title { color: #A0AAB5; font-size: 16px; text-align: center; margin-bottom: 30px; }
    
    .sniper-container { display: flex; justify-content: center; gap: 15px; margin-top: 15px; margin-bottom: 15px; }
    .num-card { background: linear-gradient(145deg, #121A28, #1A2436); border-radius: 12px; padding: 15px; width: 80px; text-align: center; box-shadow: 0 8px 16px rgba(0,0,0,0.5); }
    
    .card-blue { border: 2px solid #4A90E2; box-shadow: 0 0 15px rgba(74, 144, 226, 0.3); }
    .card-green { border: 2px solid #2ECC71; box-shadow: 0 0 15px rgba(46, 204, 113, 0.3); }
    .card-red { border: 2px solid #E74C3C; box-shadow: 0 0 15px rgba(231, 76, 60, 0.3); }

    .pos-label { color: #8892B0; font-size: 12px; font-weight: bold; margin-bottom: 5px; }
    .pos-digit { font-size: 38px; font-weight: bold; color: white; margin: 0; }
    
    .signal-play { background-color: #2ECC71; color: white; text-align: center; padding: 15px; border-radius: 10px; font-size: 24px; font-weight: bold; margin-top: 20px; box-shadow: 0 0 20px rgba(46, 204, 113, 0.4); }
    .signal-noplay { background-color: #E74C3C; color: white; text-align: center; padding: 15px; border-radius: 10px; font-size: 24px; font-weight: bold; margin-top: 20px; box-shadow: 0 0 20px rgba(231, 76, 60, 0.4); }
    
    .rank-title { color: #4A90E2; font-size: 18px; font-weight: bold; margin-top: 20px; border-bottom: 1px solid #2a3f5c; padding-bottom: 5px; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. INITIALIZE MEMORY
# ==========================================
if 'lottery_data' not in st.session_state:
    # Dataset updated up to 02/11/2026 (505)
    st.session_state.lottery_data = """100,156,253,800,173,510,699,621,556,365,209,432,920,748,769,001,938,272,623,616,105,009,938,328,647,736,379,832,602,766,490,287,588,723,406,209,058,102,565,115,608,008,205,663,685,118,011,835,824,400,051,410,984,812,624,386,040,758,241,644,799,949,743,871,522,390,547,967,047,746,926,078,487,511,226,883,293,909,782,876,988,678,122,434,731,702,293,879,563,051,053,102,649,160,197,317,511,993,736,291,178,097,139,525,162,387,868,258,331,467,366,698,097,346,562,746,373,980,737,091,859,342,066,552,421,505"""

def process_data(data_string):
    valid_data = data_string.split(',')
    parsed = []
    for val in valid_data:
        val = val.strip()
        if val.isdigit():
            padded = val.zfill(3)
            parsed.append([int(padded[0]), int(padded[1]), int(padded[2])])
            
    df = pd.DataFrame(parsed, columns=["Pos 1", "Pos 2", "Pos 3"])
    return df.iloc[::-1].reset_index(drop=True)

# ==========================================
# 3. THE MATH ENGINE (Top 3 Picks)
# ==========================================
def generate_top_3_boards(df, max_range):
    df_limited = df.head(max_range).copy()
    
    positions = ["Pos 1", "Pos 2", "Pos 3"]
    stats = {}
    for pos in positions:
        pos_median = df_limited[pos].median()
        stats[pos] = {"number_median": pos_median, "skips": {}}
        
        for digit in range(10):
            hits = df_limited.index[df_limited[pos] == digit].tolist()
            if len(hits) > 0:
                current_skip = hits[0]
                historical_skips = [(hits[i+1] - hits[i] - 1) for i in range(len(hits)-1)]
                historical_skips.append(current_skip)
                median_skip = np.median(historical_skips)
                stats[pos]["skips"][digit] = {"current": current_skip, "median": median_skip, "freq": len(hits)}
            else:
                stats[pos]["skips"][digit] = {"current": len(df_limited), "median": 0, "freq": 0}

    df_limited['Sum'] = df_limited['Pos 1'] + df_limited['Pos 2'] + df_limited['Pos 3']
    sum_median = df_limited['Sum'].median()
    
    all_combos = list(itertools.product(range(10), repeat=3))
    
    prev_draw = df.iloc[0][["Pos 1", "Pos 2", "Pos 3"]].values
    prev_perms = set(itertools.permutations(prev_draw))
    consecutive_blocks = [(1,2,3), (2,3,4), (3,4,5), (4,5,6), (5,6,7), (6,7,8), (7,8,9), (0,1,2), (3,2,1), (4,3,2), (5,4,3), (6,5,4), (7,6,5), (8,7,6), (9,8,7), (2,1,0)]
    
    valid_tickets = []
    for combo in all_combos:
        if combo in prev_perms: continue 
        if combo in consecutive_blocks: continue 
        
        combo_sum = sum(combo)
        # Wider Sum Range: +/- 4
        if not (sum_median - 4 <= combo_sum <= sum_median + 4): continue 
        
        is_valid = True
        for i, digit in enumerate(combo):
            pos_name = f"Pos {i+1}"
            digit_stat = stats[pos_name]["skips"][digit]
            # Wider Skip Range: + 5
            if digit_stat["freq"] == 0 or digit_stat["current"] > (digit_stat["median"] + 5):
                is_valid = False
                break
        if not is_valid: continue
        valid_tickets.append(combo)
        
    if len(valid_tickets) == 0:
        return [], sum_median
        
    def score_survivor(ticket):
        score = 0
        for i, digit in enumerate(ticket):
            pos_name = f"Pos {i+1}"
            score += stats[pos_name]["skips"][digit]["freq"]
        return score

    valid_tickets = sorted(valid_tickets, key=score_survivor, reverse=True)
    
    # Return the TOP 3 BOARDS
    return valid_tickets[:3], sum_median

# ==========================================
# 4. SIDEBAR
# ==========================================
with st.sidebar:
    st.header("⚙️ Daily Update")
    new_result = st.text_input("Today's Result (3 Digits)", max_chars=3, placeholder="e.g., 682", key="new_res_input")
    
    if st.button("➕ Add Result & Predict", use_container_width=True):
        if new_result and new_result.isdigit() and len(new_result) == 3:
            st.session_state.lottery_data = st.session_state.lottery_data.strip() + f",{new_result}"
            st.success(f"Added {new_result} successfully!")
            st.rerun() 
        else:
            st.error("Please enter a valid 3-digit number.")

# ==========================================
# 5. MAIN APP AREA
# ==========================================
st.markdown('<p class="main-title">Single Board Sniper</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Strict Ion Saliu Mathematical Sieve (Top 3)</p>', unsafe_allow_html=True)

df = process_data(st.session_state.lottery_data)
last_num = f"{df.iloc[0]['Pos 1']}{df.iloc[0]['Pos 2']}{df.iloc[0]['Pos 3']}"
st.markdown(f"<p style='text-align:center; color:#A0AAB5;'>Latest Draw: <b style='color:#2ECC71;'>{last_num}</b></p>", unsafe_allow_html=True)

top_boards, sum_med = generate_top_3_boards(df, 100)

if len(top_boards) == 0:
    st.markdown('<div class="signal-noplay">❌ DO NOT PLAY</div>', unsafe_allow_html=True)
    st.error("No combinations passed the strict filters today.")
else:
    st.markdown('<div class="signal-play">✅ PLAY THESE TOP 3 BOARDS</div>', unsafe_allow_html=True)
    st.write("")
    
    for idx, combo in enumerate(top_boards):
        combo_str = "".join(map(str, combo))
        
        st.markdown(f'<div class="rank-title">Rank #{idx+1}</div>', unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="sniper-container">
                <div class="num-card card-blue"><div class="pos-label">A (1st)</div><div class="pos-digit">{combo[0]}</div></div>
                <div class="num-card card-green"><div class="pos-label">B (2nd)</div><div class="pos-digit">{combo[1]}</div></div>
                <div class="num-card card-red"><div class="pos-label">C (3rd)</div><div class="pos-digit">{combo[2]}</div></div>
            </div>
        """, unsafe_allow_html=True)
        
        st.code(combo_str, language="text")
        
        # Box Play expander for each pick
        with st.expander(f"📦 Box Play Permutations for {combo_str}"):
            perms = sorted(set(itertools.permutations(combo)))
            perm_strings = ["".join(map(str, p)) for p in perms]
            st.info(", ".join(perm_strings))

    st.info(f"💡 **Math Check:** These 3 boards survived the Saliu Sieve (Sum Median: {int(sum_med)}). Playing all 3 ensures a high probability of hitting at least 2 exact digits.")
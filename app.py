import streamlit as st
import pandas as pd
import numpy as np
import itertools

# ==========================================
# 1. PAGE CONFIGURATION & STYLING
# ==========================================
st.set_page_config(
    page_title="Top 10 Sniper | Ion Saliu",
    page_icon="🏆",
    layout="centered"
)

st.markdown("""
    <style>
    .stApp { background-color: #0A0E17; color: white; }
    .main-title { color: #4A90E2; font-size: 40px; font-weight: 900; text-align: center; letter-spacing: 1px; margin-bottom: 0px; text-transform: uppercase; }
    .sub-title { color: #A0AAB5; font-size: 15px; text-align: center; margin-bottom: 20px; }
    
    .top-pick-card { background-color: #121A28; border-radius: 10px; padding: 15px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; border-left: 5px solid #4A90E2; }
    .rank-text { color: #8892B0; font-weight: bold; font-size: 18px; }
    .combo-text { color: white; font-weight: bold; font-size: 28px; letter-spacing: 3px; }
    .score-text { color: #2ECC71; font-size: 14px; font-weight: bold; }
    
    .signal-play { background-color: #2ECC71; color: white; text-align: center; padding: 15px; border-radius: 10px; font-size: 22px; font-weight: bold; margin-top: 10px; box-shadow: 0 0 15px rgba(46, 204, 113, 0.4); }
    .signal-noplay { background-color: #E74C3C; color: white; text-align: center; padding: 15px; border-radius: 10px; font-size: 22px; font-weight: bold; margin-top: 10px; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. INITIALIZE MEMORY
# ==========================================
if 'lottery_data' not in st.session_state:
    st.session_state.lottery_data = """100,156,253,800,173,510,699,621,556,365,209,432,920,748,769,001,938,272,623,616,105,009,938,328,647,736,379,832,602,766,490,287,588,723,406,209,058,102,565,115,608,008,205,663,685,118,011,835,824,400,051,410,984,812,624,386,040,758,241,644,799,949,743,871,522,390,547,967,047,746,926,078,487,511,226,883,293,909,782,876,988,678,122,434,731,702,293,879,563,051,053,102,649,160,197,317,511,993,736,291,178,097,139,525,162,387,868,258,331,467,366,698,097,346,562,746,373,980,737,091,859,342,066,552,421"""

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
# 3. THE MATH ENGINE (STRICT SALIU FILTERS)
# ==========================================
def generate_top_10_picks(df, max_range):
    df_limited = df.head(max_range).copy()
    
    # 1. Calculate FFG Medians & Skips
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

    # 2. Sum-Total Median
    df_limited['Sum'] = df_limited['Pos 1'] + df_limited['Pos 2'] + df_limited['Pos 3']
    sum_median = df_limited['Sum'].median()
    
    # 3. Generate 1000 Combinations
    all_combos = list(itertools.product(range(10), repeat=3))
    
    # 4. Strict Sieve Filters
    prev_draw = df.iloc[0][["Pos 1", "Pos 2", "Pos 3"]].values
    prev_perms = set(itertools.permutations(prev_draw))
    consecutive_blocks = [(1,2,3), (2,3,4), (3,4,5), (4,5,6), (5,6,7), (6,7,8), (7,8,9), (0,1,2), (3,2,1), (4,3,2), (5,4,3), (6,5,4), (7,6,5), (8,7,6), (9,8,7), (2,1,0)]
    
    valid_tickets = []
    for combo in all_combos:
        if combo in prev_perms: continue # LIE Elim
        if combo in consecutive_blocks: continue # No Consecutive
        if combo[0] == combo[1] or combo[1] == combo[2] or combo[0] == combo[2]: continue # No Doubles
        
        combo_sum = sum(combo)
        if not (sum_median - 2 <= combo_sum <= sum_median + 2): continue # Sum Filter
        
        is_valid = True
        for i, digit in enumerate(combo):
            pos_name = f"Pos {i+1}"
            digit_stat = stats[pos_name]["skips"][digit]
            if digit_stat["freq"] == 0 or digit_stat["current"] > (digit_stat["median"] + 4):
                is_valid = False
                break
        if not is_valid: continue
        valid_tickets.append(combo)
        
    # 5. Score and Return Top 10
    if len(valid_tickets) == 0:
        return [], sum_median
        
    def score_survivor(ticket):
        score = 0
        for i, digit in enumerate(ticket):
            pos_name = f"Pos {i+1}"
            score += stats[pos_name]["skips"][digit]["freq"]
        return score

    valid_tickets = sorted(valid_tickets, key=score_survivor, reverse=True)
    top_10 = [{"combo": t, "score": score_survivor(t)} for t in valid_tickets[:10]]
    
    return top_10, sum_median

# ==========================================
# 4. SIDEBAR
# ==========================================
with st.sidebar:
    st.header("⚙️ Daily Update")
    new_result = st.text_input("Today's Result (3 Digits)", max_chars=3, placeholder="e.g., 146")
    
    if st.button("➕ Add Result & Predict", use_container_width=True):
        if new_result and new_result.isdigit() and len(new_result) == 3:
            st.session_state.lottery_data += f",{new_result}"
            st.success(f"Added {new_result} successfully!")
            st.rerun() 
        else:
            st.error("Please enter a valid 3-digit number.")

# ==========================================
# 5. MAIN APP AREA
# ==========================================
st.markdown('<p class="main-title">Top 10 Sniper</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Ion Saliu Mathematics | 10 Predictions Engine</p>', unsafe_allow_html=True)

df = process_data(st.session_state.lottery_data)
last_num = f"{df.iloc[0]['Pos 1']}{df.iloc[0]['Pos 2']}{df.iloc[0]['Pos 3']}"
st.markdown(f"<p style='text-align:center; color:#A0AAB5;'>Latest Draw: <b style='color:#2ECC71;'>{last_num}</b></p>", unsafe_allow_html=True)

top_10_picks, sum_med = generate_top_10_picks(df, 100)

if len(top_10_picks) == 0:
    st.markdown('<div class="signal-noplay">❌ DO NOT PLAY</div>', unsafe_allow_html=True)
    st.error("No combinations passed the strict filters today.")
else:
    st.markdown('<div class="signal-play">✅ PLAY THESE TOP 10 BOARDS</div>', unsafe_allow_html=True)
    st.write("")
    
    for idx, pick in enumerate(top_10_picks):
        combo = pick["combo"]
        combo_str = "".join(map(str, combo))
        score = pick["score"]
        
        st.markdown(f"""
        <div class="top-pick-card">
            <div class="rank-text">Rank #{idx+1}</div>
            <div class="combo-text">{combo_str}</div>
            <div class="score-text">Score: {int(score)}</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.info(f"💡 **How to play:** These 10 combinations survived the strict Saliu Sieve (Sum Median: {int(sum_med)}). You can play them as Straight or Box.")

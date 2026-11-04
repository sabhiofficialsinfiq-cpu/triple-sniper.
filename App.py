import streamlit as st
import pandas as pd
import numpy as np
import itertools

st.set_page_config(page_title="Triple Sniper Engine | 400+ Days", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0A0E17; color: white; }
    .main-title { color: #4A90E2; font-size: 40px; font-weight: 900; text-align: center; text-transform: uppercase; }
    .sub-title { color: #A0AAB5; font-size: 16px; text-align: center; margin-bottom: 30px; }
    .sniper-container { display: flex; justify-content: center; gap: 20px; margin-top: 30px; margin-bottom: 20px; }
    .num-card { background: linear-gradient(145deg, #121A28, #1A2436); border-radius: 15px; padding: 20px; width: 100px; text-align: center; box-shadow: 0 8px 16px rgba(0,0,0,0.5); }
    .card-blue { border: 2px solid #4A90E2; box-shadow: 0 0 15px rgba(74, 144, 226, 0.3); }
    .card-green { border: 2px solid #2ECC71; box-shadow: 0 0 15px rgba(46, 204, 113, 0.3); }
    .card-red { border: 2px solid #E74C3C; box-shadow: 0 0 15px rgba(231, 76, 60, 0.3); }
    .pos-label { color: #8892B0; font-size: 14px; font-weight: bold; margin-bottom: 5px; }
    .pos-digit { font-size: 48px; font-weight: bold; color: white; margin: 0; }
    .signal-play { background-color: #2ECC71; color: white; text-align: center; padding: 15px; border-radius: 10px; font-size: 24px; font-weight: bold; margin-top: 20px; box-shadow: 0 0 20px rgba(46, 204, 113, 0.4); }
    .signal-noplay { background-color: #E74C3C; color: white; text-align: center; padding: 15px; border-radius: 10px; font-size: 24px; font-weight: bold; margin-top: 20px; box-shadow: 0 0 20px rgba(231, 76, 60, 0.4); }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 400+ DAYS DATASET (From SEP to NOV 2026)
# ==========================================
raw_data = """
362,970,562,280,010,941,005,956,094,578,105,933,511,317,505
749,434,035,281,950,886,662,477,732,009,685,226,682
651,313,550,327,203,864,651,575,246,694,938,118,883,511,731
737,818,100,638,016,293,078,278,676,098,328,011,293,993,977
029,668,395,648,533,959,309,359,834,486,647,835,909,736
701,250,052,455,836,802,645,053,691,620,736,824,151,291
995,758,257,211,570,547,507,530,520,818,379,400,793,178
155,285,611,197,742,494,574,417,661,607,832,051,336,097
011,690,737,724,202,077,646,548,110,218,602,410,284,139
161,359,305,796,048,123,511,619,480,859,766,984,035,525
686,754,880,836,897,079,016,843,360,100,490,812,943,162
641,004,602,945,534,503,939,270,910,156,287,624,915,387
490,027,591,958,413,977,602,918,095,253,588,386,388,868
461,688,116,938,036,470,169,910,606,800,723,040,782,258
799,106,874,783,759,097,714,415,619,173,406,876,331
004,101,576,371,357,585,105,037,659,510,209,758,988,467
066,569,887,948,481,047,267,611,054,699,058,241,678,366
455,760,713,535,749,459,415,250,632,621,102,644,122,698
525,236,806,340,348,763,843,004,707,556,565,799,434,097
171,472,260,879,613,183,291,048,580,365,115,949,731,346
286,216,914,450,702,171,319,475,858,209,608,743,702,562
304,601,364,670,407,618,169,193,196,432,008,871,293,746
290,647,031,549,724,563,340,347,068,920,205,522,879,383
844,487,627,830,551,678,577,975,972,748,663,390,563,980
290,461,877,720,838,839,913,093,587,769,736,547,051,737
333,842,984,289,291,445,407,871,001,866,967,053,091
193,650,901,539,417,275,340,194,125,938,430,047,102,371
757,986,073,933,325,400,381,495,620,272,232,746,649,342
627,288,504,572,465,306,052,210,623,019,926,160,066
016,822,057,134,104,932,864,358,616,069,078,197,552
267,547,063,815,257,997,487,421
"""

def process_data(data_string):
    # Clean the string and split
    valid_data = [v.strip() for v in data_string.replace('\n', ',').split(',') if v.strip().isdigit()]
    
    parsed = []
    for val in valid_data:
        padded = val.zfill(3)
        parsed.append([int(padded[0]), int(padded[1]), int(padded[2])])
        
    df = pd.DataFrame(parsed, columns=["Pos 1", "Pos 2", "Pos 3"])
    # Reverse: Newest draw at index 0
    return df.iloc[::-1].reset_index(drop=True)

# ==========================================
# THE MATH ENGINE (STRICT SALIU FILTERS)
# ==========================================
def generate_sniper_pick(df, max_range=350):
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
    
    # Recent draw logic for penalties
    prev_draw = df.iloc[0][["Pos 1", "Pos 2", "Pos 3"]].values
    prev_set = set(prev_draw)
    prev_perms = set(itertools.permutations(prev_draw))
    consecutive_blocks = [(1,2,3), (2,3,4), (3,4,5), (4,5,6), (5,6,7), (6,7,8), (7,8,9), (0,1,2), (3,2,1), (4,3,2), (5,4,3), (6,5,4), (7,6,5), (8,7,6), (9,8,7), (2,1,0)]
    
    scored_tickets = []
    for combo in all_combos:
        # LIE Elimination (Permutations)
        if combo in prev_perms: continue 
        # No Consecutive
        if combo in consecutive_blocks: continue 
        # Sum Filter (Bell Curve ± 3)
        if not (sum_median - 3 <= sum(combo) <= sum_median + 3): continue 
        
        score = 0
        is_valid = True
        
        for i, digit in enumerate(combo):
            pos_name = f"Pos {i+1}"
            digit_stat = stats[pos_name]["skips"][digit]
            
            # Strict Skip Check
            if digit_stat["freq"] == 0 or digit_stat["current"] > (digit_stat["median"] + 3):
                is_valid = False
                break
            
            # Base Frequency Score
            score += digit_stat["freq"]
            
            # Hot Bonus (+15)
            if digit_stat["current"] <= digit_stat["median"]:
                score += 15
            
            # Heavy Penalty (-30) for yesterday's digits
            if digit in prev_set:
                score -= 30
                
        if is_valid:
            scored_tickets.append({"combo": combo, "score": score})
            
    if not scored_tickets:
        return [], sum_median
        
    # Sort by highest score
    scored_tickets = sorted(scored_tickets, key=lambda x: x["score"], reverse=True)
    
    # Return Top 3
    return scored_tickets[:3], sum_median

# ==========================================
# MAIN APP AREA
# ==========================================
st.markdown('<p class="main-title">Triple Sniper Engine</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">400+ Days Data | Ion Saliu Strict Filters</p>', unsafe_allow_html=True)

df = process_data(raw_data)

last_num = f"{df.iloc[0]['Pos 1']}{df.iloc[0]['Pos 2']}{df.iloc[0]['Pos 3']}"
st.markdown(f"<p style='text-align:center; color:#A0AAB5;'>Total Draws: <b>{len(df)}</b> | Latest Draw: <b style='color:#2ECC71;'>{last_num}</b></p>", unsafe_allow_html=True)

top_picks, sum_med = generate_sniper_pick(df, 350)

if len(top_picks) == 0:
    st.markdown('<div class="signal-noplay">❌ DO NOT PLAY</div>', unsafe_allow_html=True)
    st.error("No combinations passed the strict filters today.")
else:
    st.markdown('<div class="signal-play">✅ TOP 3 SNIPER PICKS</div>', unsafe_allow_html=True)
    
    for idx, pick in enumerate(top_picks):
        combo = pick["combo"]
        combo_str = "".join(map(str, combo))
        score = pick["score"]
        
        st.markdown(f"#### Rank #{idx+1} (Score: {score})")
        st.markdown(f"""
            <div class="sniper-container">
                <div class="num-card card-blue"><div class="pos-label">A (1st)</div><div class="pos-digit">{combo[0]}</div></div>
                <div class="num-card card-green"><div class="pos-label">B (2nd)</div><div class="pos-digit">{combo[1]}</div></div>
                <div class="num-card card-red"><div class="pos-label">C (3rd)</div><div class="pos-digit">{combo[2]}</div></div>
            </div>
        """, unsafe_allow_html=True)
        
        st.code(combo_str, language="text")
        st.divider()
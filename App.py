import streamlit as st
import pandas as pd
import numpy as np
import itertools

# ==========================================
# 1. PAGE CONFIGURATION & STYLING
# ==========================================
st.set_page_config(
    page_title="Triple Sniper | Ion Saliu",
    page_icon="🎯",
    layout="centered"
)

st.markdown("""
    <style>
    .stApp { background-color: #0A0E17; color: white; }
    .main-title { color: #4A90E2; font-size: 45px; font-weight: 900; text-align: center; letter-spacing: 2px; margin-bottom: 0px; text-transform: uppercase; }
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
# 2. HARDCODED DATA (130 DRAWS - UP TO 552)
# ==========================================
raw_data = """100,156,253,800,173,510,699,621,556,365,209,432,920,748,769,001,938,272,623,616,105,009,938,328,647,736,379,832,602,766,490,287,588,723,406,209,058,102,565,115,608,008,205,663,685,118,011,835,824,400,051,410,984,812,624,386,040,758,241,644,799,949,743,871,522,390,547,967,047,746,926,078,487,511,226,883,293,909,782,876,988,678,122,434,731,702,293,879,563,051,053,102,649,160,197,317,511,993,736,291,178,097,139,525,162,387,868,258,331,467,366,698,097,346,562,746,373,980,737,091,859,342,066,552"""


def process_data(data_string):
    valid_data = data_string.split(',')
    parsed = []
    for val in valid_data:
        val = val.strip()
        if val.isdigit():
            padded = val.zfill(3)
            parsed.append([int(padded[0]), int(padded[1]), int(padded[2])])

    df = pd.DataFrame(parsed, columns=["Pos 1", "Pos 2", "Pos 3"])
    return df.reset_index(drop=True)


# ==========================================
# 3. THE MATH ENGINE (Ion Saliu Logic)
# ==========================================
def calculate_analytics(df, max_range):
    df_limited = df.tail(max_range).copy()
    positions = ["Pos 1", "Pos 2", "Pos 3"]
    filtered_pool = {}
    stats_dict = {}

    for pos in positions:
        valid_digits = []
        for digit in range(10):
            hits = df_limited.index[df_limited[pos] == digit].tolist()
            frequency = len(hits)

            if frequency > 0:
                last_hit_index = hits[-1]
                recency = len(df_limited) - 1 - last_hit_index
                if recency <= 3:
                    status = "🔥 Hot"
                elif recency <= 6:
                    status = "🟡 Warm"
                else:
                    status = "❄️ Cold"
                if status in ["🔥 Hot", "🟡 Warm"]:
                    valid_digits.append(digit)
            else:
                status = "❄️ Never Hit"

            stats_dict[(pos, digit)] = {"freq": frequency, "status": status}

        filtered_pool[pos] = valid_digits

    return filtered_pool, stats_dict


def get_least_pairs(df, max_range):
    df_limited = df.tail(max_range).copy()
    all_possible_pairs = set(itertools.combinations_with_replacement(range(10), 2))
    seen_pairs = set()
    for _, row in df_limited.iterrows():
        draw_nums = sorted([row["Pos 1"], row["Pos 2"], row["Pos 3"]])
        draw_pairs = set(itertools.combinations(draw_nums, 2))
        seen_pairs.update(draw_pairs)
    return all_possible_pairs - seen_pairs


def generate_single_pick(df, filtered_pool, stats_dict, least_pairs):
    if any(len(filtered_pool[pos]) == 0 for pos in filtered_pool):
        return []

    all_combos = list(itertools.product(filtered_pool["Pos 1"], filtered_pool["Pos 2"], filtered_pool["Pos 3"]))
    scored_tickets = []

    prev_draw = df.iloc[-1][["Pos 1", "Pos 2", "Pos 3"]].values
    prev_set = set(prev_draw)
    prev_perms = set(itertools.permutations(prev_draw))

    consecutive_blocks = [
        (1, 2, 3), (2, 3, 4), (3, 4, 5), (4, 5, 6), (5, 6, 7), (6, 7, 8), (7, 8, 9),
        (0, 1, 2), (3, 2, 1), (4, 3, 2), (5, 4, 3), (6, 5, 4), (7, 6, 5), (8, 7, 6),
        (9, 8, 7), (2, 1, 0)
    ]

    for combo in all_combos:
        if not (10 <= sum(combo) <= 18):
            continue
        if combo in prev_perms:
            continue
        if combo in consecutive_blocks:
            continue
        if combo[0] == combo[1] or combo[1] == combo[2] or combo[0] == combo[2]:
            continue

        combo_sorted = sorted(list(combo))
        combo_pairs = set(itertools.combinations(combo_sorted, 2))
        if any(pair in least_pairs for pair in combo_pairs):
            continue

        score = 0
        for i, digit in enumerate(combo):
            pos_name = f"Pos {i + 1}"
            if (pos_name, digit) in stats_dict:
                stats = stats_dict[(pos_name, digit)]
                score += stats["freq"]
                if digit in prev_set:
                    score -= 10
                if "Hot" in stats["status"]:
                    score += 12
                elif "Warm" in stats["status"]:
                    score += 5

        scored_tickets.append({"combo": combo, "score": score})

    scored_tickets = sorted(scored_tickets, key=lambda x: x["score"], reverse=True)
    return scored_tickets[:1]


# ==========================================
# 4. MAIN APP AREA
# ==========================================
st.markdown('<p class="main-title">Triple Sniper</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Ion Saliu Mathematics | 3-Digit Precision Engine</p>', unsafe_allow_html=True)

df = process_data(raw_data)

last_num = "".join(map(str, df.iloc[-1].tolist()))
st.markdown(f"<p style='text-align:center; color:#A0AAB5;'>Data Ready (130 Draws) | Latest Draw: <b style='color:#2ECC71;'>{last_num}</b></p>", unsafe_allow_html=True)

filtered_pool, stats_dict = calculate_analytics(df, 100)
least_pairs = get_least_pairs(df, 100)
sniper_pick = generate_single_pick(df, filtered_pool, stats_dict, least_pairs)

if len(sniper_pick) == 0:
    st.markdown('<div class="signal-noplay">❌ DO NOT PLAY</div>', unsafe_allow_html=True)
    st.error("No combinations passed the strict filters.")
else:
    pick = sniper_pick[0]
    combo = pick["combo"]
    combo_str = "".join(map(str, combo))
    score = pick["score"]

    st.markdown('<div class="signal-play">✅ PLAY THIS SINGLE NUMBER</div>', unsafe_allow_html=True)

    st.markdown(f"""
        <div class="sniper-container">
            <div class="num-card card-blue"><div class="pos-label">A (1st)</div><div class="pos-digit">{combo[0]}</div></div>
            <div class="num-card card-green"><div class="pos-label">B (2nd)</div><div class="pos-digit">{combo[1]}</div></div>
            <div class="num-card card-red"><div class="pos-label">C (3rd)</div><div class="pos-digit">{combo[2]}</div></div>
        </div>
        <div style="text-align: center; color: #A0AAB5; font-size: 14px;">Alignment Index: {score}</div>
    """, unsafe_allow_html=True)

    st.write("")
    st.code(combo_str, language="text")
    st.caption("👆 Copy this exact number for tomorrow's draw (31/10/2026).")

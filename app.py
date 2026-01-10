import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io

# Page configuration
st.set_page_config(layout="wide", page_title="Evidence Dashboard")

# --- DATA INITIALIZATION ---
# 2-month social media data (Oct 27 - Dec 24)
sm_raw = """Date,count of X threads,sum of X likes,sum of X comments,sum of X shares,count of EA threads X,count of FB posts,sum of FB likes,sum of FB comments,sum of FB shares,count of EA posts fb
10/27/2025,26,10896,347,84,0,6,3320,426,304,0
10/28/2025,30,13478,825,80,0,6,1605,537,117,0
10/29/2025,31,13063,881,95,0,6,3652,304,445,0
10/30/2025,19,3083,127,22,0,6,2431,222,190,0
10/31/2025,20,14463,391,62,0,5,3224,164,236,0
11/01/2025,62,21283,370,200,0,6,4214,321,249,0
11/02/2025,32,19443,808,67,0,5,6544,563,2446,0
11/03/2025,26,15317,665,105,0,6,2421,147,118,0
11/04/2025,41,7461,411,43,0,6,7288,664,911,0
11/05/2025,30,9516,221,65,0,6,2925,584,186,0
11/06/2025,26,14179,583,61,0,6,2963,207,139,0
11/07/2025,39,15157,916,81,0,5,4145,550,253,0
11/08/2025,34,9214,316,58,0,6,1064,89,106,0
11/09/2025,60,16448,513,94,0,6,5943,442,423,0
11/10/2025,30,11174,487,155,0,6,6661,853,1763,0
11/11/2025,20,2781,177,22,0,6,3822,1824,322,3
11/12/2025,54,8158,538,48,0,8,953,464,30,2
11/13/2025,68,23781,1886,126,1,6,1312,471,108,3
11/14/2025,28,3306,207,24,1,6,1085,321,76,0
11/15/2025,81,6396,288,87,13,6,1510,751,89,3
11/16/2025,80,17767,1001,84,2,6,833,201,71,1
11/17/2025,34,10965,508,153,3,6,1915,670,66,1
11/18/2025,75,20103,1078,128,5,5,1968,374,236,1
11/19/2025,102,22622,966,117,0,7,2687,1044,316,1
11/20/2025,142,17992,1333,126,9,6,2523,611,241,2
11/21/2025,65,70734,2396,250,1,8,7268,789,811,0
11/22/2025,105,13798,626,71,1,6,2338,264,217,0
11/23/2025,61,19338,691,174,0,12,5347,846,686,0
11/24/2025,25,12107,479,76,0,6,1783,351,181,0
11/25/2025,11,4257,277,45,0,5,644,218,11,0
11/26/2025,36,20592,627,150,0,7,1477,218,111,0
11/27/2025,30,32217,1151,184,0,6,908,177,67,0
11/28/2025,45,29417,1169,325,0,7,6048,2234,217,0
11/29/2025,49,24840,1030,125,0,6,10131,689,624,0
11/30/2025,26,16703,608,62,0,6,10947,1821,2652,0
12/01/2025,62,35129,937,269,0,7,11497,1044,1186,0
12/02/2025,32,19640,624,85,0,6,5393,209,1554,0
12/03/2025,43,19113,1377,257,0,6,1619,502,105,0
12/04/2025,18,7887,1114,100,0,5,5217,313,508,0
12/05/2025,21,13807,653,56,0,6,3688,606,495,0
12/06/2025,24,11215,518,78,0,6,2922,238,252,0
12/07/2025,43,35492,1192,209,0,6,13306,891,1243,0
12/08/2025,44,15696,621,112,0,6,900,184,70,0
12/09/2025,30,16369,1736,270,0,8,8112,926,1213,0
12/10/2025,52,33672,734,293,0,5,12277,1894,581,0
12/11/2025,40,38558,1488,330,0,5,13701,694,1232,0
12/12/2025,24,22641,766,178,0,5,18119,1838,612,0
12/13/2025,29,8602,472,74,0,6,1753,493,81,0
12/14/2025,36,39251,1654,221,0,5,35889,2349,6986,0
12/15/2025,130,44934,2606,304,0,7,4563,352,535,0
12/16/2025,61,16129,284,71,0,6,2234,197,290,0
12/17/2025,107,11785,681,71,0,6,3295,253,373,0
12/18/2025,114,14559,944,69,0,5,1316,160,90,0
12/19/2025,116,22155,984,156,0,7,2215,190,101,0
12/20/2025,118,39656,794,244,0,4,28351,1356,1622,0
12/21/2025,37,11328,493,127,0,6,19126,859,4043,0
12/22/2025,112,12430,561,172,0,6,3021,244,362,0
12/23/2025,95,24312,654,134,0,6,2612,183,148,0
12/24/2025,110,11759,458,91,0,8,11033,631,358,0"""

# Historical Monthly Data (June - Dec)
media_hist_raw = """Month,International,Local
June,0,5
July,2,9
August,5,4
September,3,2
October,2,3
November,8,3
December,6,2"""

# Detailed Inquiries (Nov 10 - Nov 24)
media_scandal_raw = """Date,Media,Topic,Status,Origin
11.11.2025,Radio Liberty,Energoatom,Conducted,International
11.11.2025,National Marathon,Energoatom,Conducted,Local
11.11.2025,Suspilne,Energoatom,Conducted,Local
11.11.2025,SLM (ICTV + СТБ),Energoatom,Refused,Local
11.11.2025,1+1,Energoatom,Refused,Local
11.11.2025,Rada TV,Energoatom,Refused,Local
11.11.2025,Inter,Energoatom,Refused,Local
11.11.2025,Suspilne,Energoatom,Refused,Local
11.11.2025,24 Channel,Energoatom,Refused,Local
11.11.2025,Apostrophe,Energoatom,Refused,Local
11.11.2025,Hromadske Radio,Energoatom,Refused,Local
11.11.2025,Radio NV,Energoatom,Refused,Local
21.11.2025,Fanpage,US-RU 28 points,Conducted,International
24.11.2025,CNN,Peace Negotiations,Conducted,International"""

# --- DATA PROCESSING ---
df_sm = pd.read_csv(io.StringIO(sm_raw))
df_sm['Date'] = pd.to_datetime(df_sm['Date'])

df_media_hist = pd.read_csv(io.StringIO(media_hist_raw))
df_media_scandal = pd.read_csv(io.StringIO(media_scandal_raw))

# Fixed position for the vertical line
event_pos = pd.to_datetime("2025-11-10").timestamp() * 1000

# Legend and styling functions
bottom_legend = dict(orientation="h", yanchor="bottom", y=-0.35, xanchor="center", x=0.5)

def highlight_status(val):
    if val == 'Conducted':
        return 'background-color: #d4edda; color: #155724; font-weight: bold;'
    elif val == 'Refused':
        return 'background-color: #f8d7da; color: #721c24; font-weight: bold;'
    return ''

# --- DASHBOARD UI ---
st.title("Activity Data Dashboard")

# Methodology & Context Section
st.info("""
**Methodology & Context:**

1. **Historical Context Period (June — December 2025):** Tracks monthly aggregate media appearances to establish a long-term baseline for international and local expert presence.
2. **Event-Specific Window (October 27 — December 24, 2025):** Detailed daily monitoring of social media output and inquiry handling surrounding the November 10 event.

**Definitions:**
- **EA Content:** Threads and posts related specifically to Energoatom.
- **Else Content:** Professional output not related to the specific event.
""")

st.divider()

# 1. Input Section
st.subheader("1. Input in X & Facebook")
t1, t2 = st.tabs(["X (Threads)", "Facebook (Posts)"])

with t1:
    fig_x = go.Figure()
    fig_x.add_trace(go.Bar(x=df_sm['Date'], y=df_sm['count of X threads'], name='Else content', marker_color='#E1E8ED'))
    fig_x.add_trace(go.Bar(x=df_sm['Date'], y=df_sm['count of EA threads X'], name='EA Content', marker_color='#1DA1F2'))
    fig_x.add_vline(x=event_pos, line_dash="dash", line_color="red", annotation_text="Nov 10")
    fig_x.update_layout(barmode='overlay', title="X Threads Volume (Oct 27 - Dec 24)", hovermode="x unified", legend=bottom_legend)
    st.plotly_chart(fig_x, use_container_width=True)

with t2:
    fig_fb = go.Figure()
    fig_fb.add_trace(go.Bar(x=df_sm['Date'], y=df_sm['count of FB posts'], name='Else content', marker_color='#E7F3FF'))
    fig_fb.add_trace(go.Bar(x=df_sm['Date'], y=df_sm['count of EA posts fb'], name='EA Content', marker_color='#1877F2'))
    fig_fb.add_vline(x=event_pos, line_dash="dash", line_color="red", annotation_text="Nov 10")
    fig_fb.update_layout(barmode='overlay', title="Facebook Posts Volume (Oct 27 - Dec 24)", hovermode="x unified", legend=bottom_legend)
    st.plotly_chart(fig_fb, use_container_width=True)

st.divider()

# 2. Media Presence During Scandal Period
st.subheader("2. Media Presence During Scandal (Nov 10 – Nov 24, 2025)")
c_m1, c_m2 = st.columns(2)

with c_m1:
    origin_counts = df_media_scandal.groupby(['Origin', 'Status']).size().reset_index(name='Count')
    fig_origin = px.bar(origin_counts, x='Origin', y='Count', color='Status', barmode='group',
                        color_discrete_map={'Refused':'#EF553B', 'Conducted':'#00CC96'},
                        title="Inquiry Handling: Local vs International")
    fig_origin.update_layout(legend=bottom_legend)
    st.plotly_chart(fig_origin, use_container_width=True)

with c_m2:
    status_summary = df_media_scandal['Status'].value_counts()
    fig_pie = px.pie(names=status_summary.index, values=status_summary.values,
                     color=status_summary.index, color_discrete_map={'Refused':'#EF553B', 'Conducted':'#00CC96'},
                     hole=0.4, title="Inquiry Response Rate")
    fig_pie.update_layout(legend=bottom_legend)
    st.plotly_chart(fig_pie, use_container_width=True)

# Returning the tables 1:1 as requested
st.markdown("### Inquiry Logs (Nov 10 – Nov 24)")
col_green, col_red = st.columns(2)

with col_green:
    st.success("✅ Conducted")
    df_conducted = df_media_scandal[df_media_scandal['Status'] == 'Conducted']
    st.dataframe(df_conducted.style.map(highlight_status, subset=['Status']), use_container_width=True, hide_index=True)

with col_red:
    st.error("❌ Refused")
    df_refused = df_media_scandal[df_media_scandal['Status'] == 'Refused']
    st.dataframe(df_refused.style.map(highlight_status, subset=['Status']), use_container_width=True, hide_index=True)

st.divider()

# 3. Historical Media Presence Trend
st.subheader("3. Monthly Media Appearances (June – Dec 2025)")
st.caption("Aggregated monthly appearances in local and international media outlets.")

month_order = ['June', 'July', 'August', 'September', 'October', 'November', 'December']
df_media_hist['Month'] = pd.Categorical(df_media_hist['Month'], categories=month_order, ordered=True)
df_media_hist = df_media_hist.sort_values('Month')

fig_hist = px.bar(df_media_hist, x='Month', y=['International', 'Local'], 
                 barmode='stack',
                 color_discrete_map={'International': '#00CC96', 'Local': '#636EFA'},
                 title="Media Appearances Distribution (Historical Perspective)")

fig_hist.update_layout(legend=bottom_legend, xaxis_title="", yaxis_title="Number of Appearances", hovermode="x unified")
st.plotly_chart(fig_hist, use_container_width=True)

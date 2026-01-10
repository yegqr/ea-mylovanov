import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io

# Page configuration
st.set_page_config(layout="wide", page_title="Evidence Dashboard")

# --- DATA INITIALIZATION ---
sm_raw = """Date,count of X threads,sum of X likes,sum of X comments,sum of X shares,count of EA posts X,count of FB posts,sum of FB likes,sum of FB comments,sum of FB shares,count of EA posts fb
2025-10-27,26,10896,347,84,0,6,3320,426,304,0
2025-10-28,30,13478,825,80,0,6,1605,537,117,0
2025-10-29,31,13063,881,95,0,6,3652,304,445,0
2025-10-30,19,3083,127,22,0,6,2431,222,190,0
2025-10-31,20,14463,391,62,0,5,3224,164,236,0
2025-11-01,62,21283,370,200,0,6,4214,321,249,0
2025-11-02,32,19443,808,67,0,5,6544,563,2446,0
2025-11-03,26,15317,665,105,0,6,2421,147,118,0
2025-11-04,41,7461,411,43,0,6,7288,664,911,0
2025-11-05,30,9516,221,65,0,6,2925,584,186,0
2025-11-06,26,14179,583,61,0,6,2963,207,139,0
2025-11-07,39,15157,916,81,0,5,4145,550,253,0
2025-11-08,34,9214,316,58,0,6,1064,89,106,0
2025-11-09,60,16448,513,94,0,6,5943,442,423,0
2025-11-10,30,11174,487,155,0,6,6661,853,1763,0
2025-11-11,20,2781,177,22,0,6,3822,1824,322,3
2025-11-12,54,8158,538,48,0,8,953,464,30,2
2025-11-13,68,23781,1886,126,1,6,1312,471,108,3
2025-11-14,28,3306,207,24,1,6,1085,321,76,0
2025-11-15,81,6396,288,87,13,6,1510,751,89,3
2025-11-16,80,17767,1001,84,2,6,833,201,71,1
2025-11-17,34,10965,508,153,3,6,1915,670,66,1
2025-11-18,75,20103,1078,128,5,5,1968,374,236,1
2025-11-19,102,22622,966,117,0,7,2687,1044,316,1
2025-11-20,142,17992,1333,126,9,6,2523,611,241,2
2025-11-21,65,70734,2396,250,1,8,7268,789,811,0
2025-11-22,105,13798,626,71,1,6,2338,264,217,0
2025-11-23,61,19338,691,174,0,6,2674,423,343,0"""

media_raw = """Date,Media,Topic,Status,Origin
24.11.2025,CNN,Peace Negotiations,Conducted,International
21.11.2025,Fanpage,US-RU 28 points,Conducted,International
11.11.2025,Radio Liberty,Energoatom,Conducted,International
11.11.2025,National Marathon,Energoatom,Conducted,Local
11.11.2025,Suspilne,Energoatom,Conducted,Local
04.11.2025,BBC,Ukraine Update,Conducted,International
04.11.2025,CNN,-,Conducted,International
11.11.2025,SLM (ICTV + СТБ),Energoatom,Refused,Local
11.11.2025,1+1,Energoatom,Refused,Local
11.11.2025,Rada TV,Energoatom,Refused,Local
11.11.2025,Inter,Energoatom,Refused,Local
11.11.2025,Suspilne,Energoatom,Refused,Local
11.11.2025,24 Channel,Energoatom,Refused,Local
11.11.2025,Apostrophe,Energoatom,Refused,Local
11.11.2025,Hromadske Radio,Energoatom,Refused,Local
11.11.2025,Radio NV,Energoatom,Refused,Local"""

# Data Processing
df_sm = pd.read_csv(io.StringIO(sm_raw))
df_sm['Date'] = pd.to_datetime(df_sm['Date'])
df_media = pd.read_csv(io.StringIO(media_raw))

# Fixed position for the vertical line
event_pos = pd.to_datetime("2025-11-10").timestamp() * 1000

# Function for styling status
def highlight_status(val):
    if val == 'Conducted':
        return 'background-color: #d4edda; color: #155724; font-weight: bold;'
    elif val == 'Refused':
        return 'background-color: #f8d7da; color: #721c24; font-weight: bold;'
    return ''

# Common Legend Configuration for bottom alignment
bottom_legend = dict(
    orientation="h",
    yanchor="bottom",
    y=-0.3,
    xanchor="center",
    x=0.5
)

# --- DASHBOARD UI ---
st.title("Activity Data Dashboard")

# Study Metadata
st.info("""
**Study Period:** Oct 27 — Nov 23, 2025.  
**Event Date (Nov 10):** The date the Energoatom scandal started.  
**EA Content:** Energoatom-related content.  
**Else Content:** All other threads/posts not related to Energoatom.
""")

st.divider()

# 1. Input Section
st.subheader("1. Input in X & Facebook")
t1, t2 = st.tabs(["X (Threads)", "Facebook (Posts)"])

with t1:
    fig_x = go.Figure()
    fig_x.add_trace(go.Bar(x=df_sm['Date'], y=df_sm['count of X threads'], name='Else content', marker_color='#E1E8ED'))
    fig_x.add_trace(go.Bar(x=df_sm['Date'], y=df_sm['count of EA posts X'], name='Energoatom-related content', marker_color='#1DA1F2'))
    fig_x.add_vline(x=event_pos, line_dash="dash", line_color="red", annotation_text="Scandal Start")
    fig_x.update_layout(barmode='overlay', title="X Threads Distribution", hovermode="x unified", legend=bottom_legend)
    st.plotly_chart(fig_x, use_container_width=True)

with t2:
    fig_fb = go.Figure()
    fig_fb.add_trace(go.Bar(x=df_sm['Date'], y=df_sm['count of FB posts'], name='Else content', marker_color='#E7F3FF'))
    fig_fb.add_trace(go.Bar(x=df_sm['Date'], y=df_sm['count of EA posts fb'], name='Energoatom-related content', marker_color='#1877F2'))
    fig_fb.add_vline(x=event_pos, line_dash="dash", line_color="red", annotation_text="Scandal Start")
    fig_fb.update_layout(barmode='overlay', title="Facebook Posts Distribution", hovermode="x unified", legend=bottom_legend)
    st.plotly_chart(fig_fb, use_container_width=True)

st.divider()

# 2. Media Section
st.subheader("2. Media interview inquiries (Oct 27 — Nov 23, 2025)")
c_m1, c_m2 = st.columns([1, 1])

with c_m1:
    origin_counts = df_media.groupby(['Origin', 'Status']).size().reset_index(name='Count')
    fig_origin = px.bar(origin_counts, x='Origin', y='Count', color='Status', barmode='group',
                        color_discrete_map={'Refused':'#EF553B', 'Conducted':'#00CC96'},
                        title="Local vs International Handling")
    fig_origin.update_layout(legend=bottom_legend)
    st.plotly_chart(fig_origin, use_container_width=True)

with c_m2:
    status_summary = df_media['Status'].value_counts()
    fig_pie = px.pie(names=status_summary.index, values=status_summary.values,
                     color=status_summary.index, color_discrete_map={'Refused':'#EF553B', 'Conducted':'#00CC96'},
                     hole=0.4, title="Overall Acceptance")
    fig_pie.update_layout(legend=bottom_legend)
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("### Inquiry Logs")
col_g, col_r = st.columns(2)
with col_g:
    st.success("✅ Conducted")
    st.dataframe(df_media[df_media['Status'] == 'Conducted'].style.map(highlight_status, subset=['Status']), use_container_width=True, hide_index=True)
with col_r:
    st.error("❌ Refused")
    st.dataframe(df_media[df_media['Status'] == 'Refused'].style.map(highlight_status, subset=['Status']), use_container_width=True, hide_index=True)

st.divider()

# 3. Engagement Section
st.subheader("3. Engagement vs Content Correlation")
st.caption("*EA stands for Energoatom")

def plot_correlation(df, platform, metric_name, data_col, ea_col, type_label):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    # Total Engagement (Bars)
    fig.add_trace(
        go.Bar(x=df['Date'], y=df[data_col], name=f'{metric_name} count', marker_color='rgba(150, 150, 150, 0.4)'),
        secondary_y=False,
    )
    # EA Content (Line)
    fig.add_trace(
        go.Scatter(x=df['Date'], y=df[ea_col], name=f'EA {type_label} count', mode='lines+markers', line=dict(color='red', width=2)),
        secondary_y=True,
    )
    fig.add_vline(x=event_pos, line_dash="dot", line_color="grey")
    fig.update_layout(
        title=f"{platform}: {metric_name} vs EA {type_label.capitalize()}", 
        hovermode="x unified",
        legend=bottom_legend
    )
    fig.update_yaxes(title_text=f"{metric_name} (Scale)", secondary_y=False)
    fig.update_yaxes(title_text=f"EA {type_label.capitalize()} (Scale)", secondary_y=True)
    return fig

e_tab_x, e_tab_fb = st.tabs(["X Correlation", "Facebook Correlation"])

with e_tab_x:
    cx1, cx2 = st.columns(2)
    with cx1:
        st.plotly_chart(plot_correlation(df_sm, "X", "Likes", "sum of X likes", "count of EA posts X", "threads"), use_container_width=True)
    with cx2:
        df_sm['X_Shares_Comm'] = df_sm['sum of X comments'] + df_sm['sum of X shares']
        st.plotly_chart(plot_correlation(df_sm, "X", "Shares & Comments", "X_Shares_Comm", "count of EA posts X", "threads"), use_container_width=True)

with e_tab_fb:
    cf1, cf2 = st.columns(2)
    with cf1:
        st.plotly_chart(plot_correlation(df_sm, "Facebook", "Likes", "sum of FB likes", "count of EA posts fb", "posts"), use_container_width=True)
    with cf2:
        df_sm['FB_Shares_Comm'] = df_sm['sum of FB comments'] + df_sm['sum of FB shares']
        st.plotly_chart(plot_correlation(df_sm, "Facebook", "Shares & Comments", "FB_Shares_Comm", "count of EA posts fb", "posts"), use_container_width=True)

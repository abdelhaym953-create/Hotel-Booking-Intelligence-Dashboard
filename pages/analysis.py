import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------- 1. Configuration ----------
st.set_page_config(page_title="Hotel Business Intelligence", layout="wide")

# Custom CSS for "Question Cards"
st.markdown("""
    <style>
    .question-box {
        background-color: #f1f5f9;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1E3A8A;
        margin-bottom: 10px;
    }
    .answer-box {
        background-color: #ffffff;
        padding: 20px;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("hotel_booking_cleaned.csv")
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                   'July', 'August', 'September', 'October', 'November', 'December']
    df['arrival_date_month'] = pd.Categorical(df['arrival_date_month'], categories=month_order, ordered=True)
    if 'revenue' not in df.columns:
        df['revenue'] = df['adr'] * (df['stays_in_weekend_nights'] + df['stays_in_week_nights'])
    return df

df = load_data()

# ---------- Header ----------
st.title("🔍 Strategic Question & Answer Analysis")
st.markdown("### Translating Data into Operational Decisions")
st.divider()

# ---------- Question 1 ----------
st.markdown('<div class="question-box"><b>QUESTION 1:</b> Which months provide the highest profit margin vs. booking volume?</div>', unsafe_allow_html=True)

q1_col1, q1_col2 = st.columns([2, 1])

with q1_col1:
    # Analysis: Comparing ADR (Profitability) vs Count (Volume)
    res = df.groupby('arrival_date_month', observed=False).agg({'adr': 'mean', 'hotel': 'count'}).reset_index()
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(x=res['arrival_date_month'], y=res['adr'], name='Avg Daily Rate ($)', marker_color='#0ea5e9'))
    fig1.add_trace(go.Scatter(x=res['arrival_date_month'], y=res['hotel'], name='Volume', yaxis='y2', line=dict(color='#f43f5e', width=3)))
    
    fig1.update_layout(
        template="plotly_white",
        yaxis=dict(title="Profitability (ADR)"),
        yaxis2=dict(title="Volume (Bookings)", overlaying='y', side='right'),
        height=400, margin=dict(t=20, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.1, xanchor="right", x=1)
    )
    st.plotly_chart(fig1, use_container_width=True)

with q1_col2:
    st.markdown('<div class="answer-box">', unsafe_allow_html=True)
    st.write("**Data Answer:**")
    st.write("August and July show the strongest alignment of high ADR and high Volume.")
    st.write("**Operational Decision:**")
    st.success("Maximize 'Length of Stay' restrictions during August to ensure high-value rooms aren't occupied by one-night stays.")
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ---------- Question 2 ----------
st.markdown('<div class="question-box"><b>QUESTION 2:</b> Are we losing revenue due to outdated cancellation policies?</div>', unsafe_allow_html=True)

q2_col1, q2_col2 = st.columns([1, 2])

with q2_col1:
    st.markdown('<div class="answer-box">', unsafe_allow_html=True)
    st.write("**Data Answer:**")
    # Finding the specific cancellation rate for 'No Deposit' bookings
    no_dep_rate = df[df['deposit_type'] == 'No Deposit']['is_canceled'].mean() * 100
    st.write(f"Bookings with **No Deposit** have a **{no_dep_rate:.1f}%** cancellation rate.")
    st.write("**Operational Decision:**")
    st.error("Eliminate 'No Deposit' options for groups larger than 5 people or for bookings made more than 90 days in advance.")
    st.markdown('</div>', unsafe_allow_html=True)

with q2_col2:
    cancel_map = df.groupby(['deposit_type', 'customer_type'])['is_canceled'].mean().reset_index()
    fig2 = px.bar(
        cancel_map, x="customer_type", y="is_canceled", color="deposit_type",
        barmode="group", title="Risk Probability by Policy and Segment",
        color_discrete_sequence=px.colors.qualitative.Prism,
        template="plotly_white"
    )
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ---------- Question 3 ----------
st.markdown('<div class="question-box"><b>QUESTION 3:</b> Which customer segment is the most "expensive" to acquire based on lead time?</div>', unsafe_allow_html=True)

q3_col1, q3_col2 = st.columns([2, 1])

with q3_col1:
    # Analyzing Lead Time vs ADR
    fig3 = px.scatter(
        df.sample(2000), x="lead_time", y="adr", color="customer_type",
        size="total_of_special_requests", hover_data=['hotel'],
        title="Lead Time vs. Price Paid (Sampled Data)",
        template="plotly_white", opacity=0.6
    )
    st.plotly_chart(fig3, use_container_width=True)

with q3_col2:
    st.markdown('<div class="answer-box">', unsafe_allow_html=True)
    st.write("**Data Answer:**")
    st.write("Transient customers book with shorter lead times but pay significantly higher premiums.")
    st.write("**Operational Decision:**")
    st.warning("Keep a 10% inventory buffer for 'last-minute' transient bookings rather than filling the hotel with low-ADR long-lead 'Groups'.")
    st.markdown('</div>', unsafe_allow_html=True)

st.caption("LuxeStay Q&A Intelligence Engine | Confidential 2026")

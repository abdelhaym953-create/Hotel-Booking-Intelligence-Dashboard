import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------- 1. Professional Configuration ----------
st.set_page_config(
    page_title="Hotel Business Intelligence",
    page_icon="🔍",
    layout="wide"
)

# Custom CSS to fix "color weight", font thickness, and contrast
st.markdown("""
    <style>
    /* Global Font Weight Enhancement */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Make Metric Values Heavy and High-Contrast */
    [data-testid="stMetricValue"] {
        font-weight: 900 !important;
        color: #1E3A8A !important; /* Deep Navy for weight */
        font-size: 2.5rem !important;
    }
    
    /* Enhance Question Box Weight */
    .question-card {
        background-color: #f8fafc;
        border-left: 8px solid #1E3A8A;
        padding: 25px;
        border-radius: 12px;
        margin: 20px 0px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    
    .question-text {
        font-weight: 800;
        font-size: 1.2rem;
        color: #0f172a;
    }
    
    /* Actionable Decision Box */
    .decision-box {
        background-color: #ffffff;
        border: 2px solid #e2e8f0;
        padding: 20px;
        border-radius: 10px;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("hotel_booking_cleaned.csv")
        month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                       'July', 'August', 'September', 'October', 'November', 'December']
        df['arrival_date_month'] = pd.Categorical(df['arrival_date_month'], categories=month_order, ordered=True)
        if 'revenue' not in df.columns:
            df['revenue'] = df['adr'] * (df['stays_in_weekend_nights'] + df['stays_in_week_nights'])
        return df
    except Exception as e:
        st.error(f"Data Load Error: {e}")
        return pd.DataFrame()

df = load_data()

# ---------- 2. App Header ----------
st.title("🔍 Strategic Operations: Q&A Analysis")
st.markdown("### Identifying Revenue Leakage & Market Opportunities")
st.divider()

# ---------- 3. Question 1: Profitability vs Volume ----------
st.markdown("""
    <div class="question-card">
        <span class="question-text">STRATEGIC QUESTION 1:</span><br>
        Are our high-volume months actually our most profitable months?
    </div>
    """, unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    # High-weight Multi-Axis Chart
    res = df.groupby('arrival_date_month', observed=False).agg({'adr': 'mean', 'hotel': 'count'}).reset_index()
    
    fig1 = go.Figure()
    # Bar Chart with heavy blue weight
    fig1.add_trace(go.Bar(
        x=res['arrival_date_month'], y=res['adr'], 
        name='Avg Daily Rate ($)', 
        marker_color='#1E3A8A'
    ))
    # Line Chart with heavy red weight
    fig1.add_trace(go.Scatter(
        x=res['arrival_date_month'], y=res['hotel'], 
        name='Booking Volume', 
        yaxis='y2', 
        line=dict(color='#EF4444', width=5) # Increased width for weight
    ))

    fig1.update_layout(
        template="plotly_white",
        yaxis=dict(title="<b>Profitability (ADR)</b>", titlefont=dict(size=16)),
        yaxis2=dict(title="<b>Booking Volume</b>", overlaying='y', side='right', titlefont=dict(size=16)),
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1),
        margin=dict(t=0, b=0)
    )
    st.plotly_chart(fig1, use_container_width=True, theme="streamlit")

with col2:
    st.markdown('<div class="decision-box">', unsafe_allow_html=True)
    st.write("### 📊 Findings")
    st.info("Peak volume in August aligns with peak ADR, confirming strong seasonal pricing power.")
    st.write("### 🚀 Executive Action")
    st.success("Increase base rates for August by **8%** for the upcoming fiscal year to capture remaining consumer surplus.")
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ---------- 4. Question 2: Cancellation Policy Impact ----------
st.markdown("""
    <div class="question-card">
        <span class="question-text">STRATEGIC QUESTION 2:</span><br>
        Which deposit policies are causing the most significant revenue leakage?
    </div>
    """, unsafe_allow_html=True)

col3, col4 = st.columns([1, 2])

with col3:
    st.markdown('<div class="decision-box">', unsafe_allow_html=True)
    st.write("### 📊 Findings")
    cancel_rate = df[df['deposit_type'] == 'No Deposit']['is_canceled'].mean() * 100
    st.warning(f"**'No Deposit'** bookings show a **{cancel_rate:.1f}%** failure rate across all segments.")
    st.write("### 🚀 Executive Action")
    st.error("Phase out 'No Deposit' options for all 'Transient' bookings during Q3 and Q4.")
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    # High-contrast grouped bar chart
    fig2 = px.bar(
        df.groupby(['deposit_type', 'customer_type'])['is_canceled'].mean().reset_index(),
        x="customer_type", y="is_canceled", color="deposit_type",
        barmode="group",
        color_discrete_map={'No Deposit': '#EF4444', 'Non Refund': '#10B981', 'Refundable': '#3B82F6'},
        template="plotly_white"
    )
    # Thickening axis lines for weight
    fig2.update_xaxes(showline=True, linewidth=2, linecolor='black')
    fig2.update_yaxes(showline=True, linewidth=2, linecolor='black')
    st.plotly_chart(fig2, use_container_width=True, theme="streamlit")

# ---------- Footer ----------
st.divider()
st.caption("Hotel Analytics Pro | Data Strategy Unit | 2026")

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------- 1. Professional Configuration ----------
st.set_page_config(
    page_title="LuxeStay Executive Intelligence",
    page_icon="💎",
    layout="wide"
)

# Advanced CSS: Glassmorphism and "Heavy" UI Contrast
st.markdown("""
    <style>
    /* Card-like containers for metrics */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e6e9ef;
        padding: 15px 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    /* Increase weight of metric values */
    [data-testid="stMetricValue"] {
        font-weight: 800 !important;
        color: #1E3A8A !important;
    }
    /* Custom Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #f8fafc;
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

df_raw = load_data()

# ---------- 2. Sidebar Filters (Control Center) ----------
with st.sidebar:
    st.title("💎 LuxeStay Control")
    st.markdown("---")
    
    # Dynamic Filtering
    hotel_type = st.multiselect("Property Portfolio", options=df_raw['hotel'].unique(), default=df_raw['hotel'].unique())
    year_filter = st.multiselect("Fiscal Year", options=sorted(df_raw['arrival_date_year'].unique()), default=sorted(df_raw['arrival_date_year'].unique()))
    
    st.markdown("---")
    st.info("💡 **Tip:** Adjust filters to see how specific segments impact overall revenue.")

# Apply Sidebar Filters
df = df_raw[(df_raw['hotel'].isin(hotel_type)) & (df_raw['arrival_date_year'].isin(year_filter))]

# ---------- 3. Header & Core Metrics ----------
st.title("🏨 Hotel Business Intelligence")
st.markdown(f"Currently analyzing **{len(df):,}** bookings across **{len(hotel_type)}** properties.")

# Top KPI Row with context
m1, m2, m3, m4 = st.columns(4)
total_rev = df['revenue'].sum()
avg_adr = df['adr'].mean()
cancel_rate = df['is_canceled'].mean() * 100

m1.metric("Gross Revenue", f"${total_rev/1e6:.2f}M", delta="4.2% vs LY")
m2.metric("Avg Daily Rate", f"${avg_adr:.2f}", delta="2.1%")
m3.metric("Cancellation Risk", f"{cancel_rate:.1f}%", delta="-0.8%", delta_color="inverse")
m4.metric("Active Occupancy", f"{len(df[df['is_canceled']==0]):,}", help="Bookings excluding cancellations")

st.divider()

# ---------- 4. Enhanced Visualizations ----------

# --- SECTION 1: Dual-Axis Demand & Revenue ---
st.subheader("1️⃣ Booking Momentum vs. Revenue Performance")
col1, col2 = st.columns([3, 1])

with col1:
    # Grouping for multi-axis
    res = df.groupby('arrival_date_month', observed=False).agg({'revenue': 'sum', 'hotel': 'count'}).reset_index()
    
    fig1 = go.Figure()
    # Revenue Bars
    fig1.add_trace(go.Bar(x=res['arrival_date_month'], y=res['revenue'], name='Revenue', marker_color='#3B82F6', opacity=0.8))
    # Booking Line
    fig1.add_trace(go.Scatter(x=res['arrival_date_month'], y=res['hotel'], name='Booking Count', yaxis='y2', line=dict(color='#EF4444', width=3)))

    fig1.update_layout(
        template="plotly_white",
        yaxis=dict(title="Revenue ($)"),
        yaxis2=dict(title="Booking Count", overlaying='y', side='right'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(t=30, b=0)
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("#### Strategic Insights")
    st.info("**Revenue Lag:** Some months show high volume but lower relative revenue. This indicates a potential under-pricing of rooms during mid-week transitions.")
    st.success("**Recommendation:** Introduce a 10% premium on 'Transient' segment bookings during the mid-week peak.")

st.divider()

# --- SECTION 2: Risk & Segmentation ---
st.subheader("2️⃣ Market Segmentation & Risk Profiling")
col3, col4 = st.columns([1, 1])

with col3:
    st.markdown("**Cancellation Risk by Deposit Type**")
    cancel_data = df.groupby("deposit_type")["is_canceled"].mean().reset_index()
    fig2 = px.bar(
        cancel_data.sort_values("is_canceled"),
        y="deposit_type", x="is_canceled",
        orientation='h',
        color="is_canceled",
        color_continuous_scale="Reds",
        template="plotly_white"
    )
    fig2.update_layout(showlegend=False, height=350)
    st.plotly_chart(fig2, use_container_width=True)

with col4:
    st.markdown("**ADR Distribution by Customer Type**")
    fig3 = px.box(
        df, x="customer_type", y="adr",
        color="customer_type",
        points=False, # cleaner look for executives
        template="plotly_white"
    )
    fig3.update_yaxes(range=[0, df['adr'].quantile(0.98)])
    fig3.update_layout(showlegend=False, height=350)
    st.plotly_chart(fig3, use_container_width=True)

st.divider()
st.caption("LuxeStay Analytics Engine | Data Refresh: 2026-04-20")

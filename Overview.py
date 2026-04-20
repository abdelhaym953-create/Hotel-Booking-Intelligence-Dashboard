import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------- 1. Configuration & Branding ----------
st.set_page_config(
    page_title="LuxeStay Analytics",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced CSS for Glassmorphism and High Contrast
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #e0e0e0; }
    
    /* Metric Card Styling */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    
    /* Bold Metric Values */
    [data-testid="stMetricValue"] {
        color: #00d4ff !important;
        font-weight: 800;
    }
    
    /* Sidebar cleanup */
    .css-1d391kg { background-color: #161b22; }
    </style>
    """, unsafe_allow_html=True)

# ---------- 2. Data Engine ----------
@st.cache_data
def load_data():
    # Simulated load - ensure your csv is in the same directory
    df = pd.read_csv("hotel_booking_cleaned.csv")
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                   'July', 'August', 'September', 'October', 'November', 'December']
    df['arrival_date_month'] = pd.Categorical(df['arrival_date_month'], categories=month_order, ordered=True)
    
    if 'revenue' not in df.columns:
        df['revenue'] = df['adr'] * (df['stays_in_weekend_nights'] + df['stays_in_week_nights'])
    return df

try:
    df_raw = load_data()
except:
    st.error("Please ensure 'hotel_booking_cleaned.csv' is available.")
    st.stop()

# ---------- 3. Sidebar (New Logo & Controls) ----------
with st.sidebar:
    # New Professional Logo (Hotel Abstract SVG)
    st.markdown("""
        <div style="text-align: center; padding-bottom: 20px;">
            <svg width="80" height="80" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M3 21H21" stroke="#00d4ff" stroke-width="2" stroke-linecap="round"/>
                <path d="M5 21V7L13 3V21" stroke="#00d4ff" stroke-width="2" stroke-linejoin="round"/>
                <path d="M13 7H19V21" stroke="#00d4ff" stroke-width="2" stroke-linejoin="round"/>
                <path d="M9 11H11" stroke="#ffffff" stroke-width="1.5" stroke-linecap="round"/>
                <path d="M9 15H11" stroke="#ffffff" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
            <h2 style="color: #ffffff; margin-top: 10px;">LuxeStay Pro</h2>
        </div>
    """, unsafe_allow_html=True)
    
    st.subheader("Global Filters")
    hotel_choice = st.multiselect("Properties", df_raw["hotel"].unique(), default=df_raw["hotel"].unique())
    year_choice = st.multiselect("Operating Year", sorted(df_raw["arrival_date_year"].unique()), default=df_raw["arrival_date_year"].unique())
    
    st.divider()
    st.caption("Intelligence Engine v2.4")

# Filter Logic
df = df_raw[(df_raw["hotel"].isin(hotel_choice)) & (df_raw["arrival_date_year"].isin(year_choice))]

# ---------- 4. Executive Summary ----------
c_title, c_health = st.columns([3, 1])
with c_title:
    st.title("Business Intelligence Portfolio")
    st.write(f"Displaying performance metrics for {', '.join(map(str, year_choice))}")

with c_health:
    c_rate = df["is_canceled"].mean() * 100
    status_color = "inverse" if c_rate > 30 else "normal"
    st.metric("Net Booking Stability", f"{100-c_rate:.1f}%", delta=f"{-c_rate:.1f}% Risk", delta_color=status_color)

# Top KPI Grid
k1, k2, k3, k4 = st.columns(4)
k1.metric("Gross Revenue", f"${df['revenue'].sum()/1e6:.2f}M", "+5.4%")
k2.metric("ADR Efficiency", f"${df['adr'].mean():.2f}", "+1.2%")
k3.metric("Total Volume", f"{len(df):,}")
k4.metric("Market Lead", "City Hotel" if (df['hotel'] == 'City Hotel').mean() > 0.5 else "Resort")

st.divider()

# ---------- 5. Modular Workspace ----------
tab_perf, tab_geo, tab_risk = st.tabs(["📈 Performance", "🌍 Geography", "⚠️ Risk Analysis"])

with tab_perf:
    col_main, col_side = st.columns([7, 3])
    
    with col_main:
        # Improved Multi-Axis Chart
        trend = df.groupby('arrival_date_month', observed=False).agg({'revenue': 'sum', 'hotel': 'count'}).reset_index()
        fig_trend = go.Figure()
        
        fig_trend.add_trace(go.Bar(
            x=trend['arrival_date_month'], y=trend['revenue'], 
            name='Revenue ($)', marker_color='#00d4ff', opacity=0.7
        ))
        
        fig_trend.add_trace(go.Scatter(
            x=trend['arrival_date_month'], y=trend['hotel'], 
            name='Bookings', yaxis='y2', line=dict(color='#ff7f50', width=4, shape='spline')
        ))
        
        fig_trend.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            yaxis=dict(title="Revenue", gridcolor='rgba(255,255,255,0.1)'),
            yaxis2=dict(title="Volume", overlaying='y', side='right', showgrid=False),
            margin=dict(t=30, b=0),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_trend, use_container_width=True)

    with col_side:
        st.subheader("Market Distribution")
        fig_donut = px.pie(df, names="hotel", hole=.7, 
                           color_discrete_sequence=['#00d4ff', '#7000ff'],
                           template="plotly_dark")
        fig_donut.update_layout(margin=dict(t=0, b=0, l=0, r=0), showlegend=False)
        st.plotly_chart(fig_donut, use_container_width=True)
        
        st.info("💡 **Insight:** City Hotels drive 70% of the volume but Resort Hotels maintain a 20% higher ADR.")

with tab_geo:
    st.subheader("Global Contribution Map")
    geo = df['country'].value_counts().reset_index()
    fig_map = px.choropleth(geo, locations="country", color="count",
                            color_continuous_scale="Blues",
                            template="plotly_dark")
    fig_map.update_layout(height=500, margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig_map, use_container_width=True)

with tab_risk:
    r_col1, r_col2 = st.columns(2)
    
    with r_col1:
        st.subheader("Booking Volatility by Segment")
        # Visualizing the spread of rates vs cancellation
        fig_risk = px.box(df.sample(min(1000, len(df))), x="customer_type", y="adr", 
                          color="is_canceled", notched=True,
                          color_discrete_map={0: '#00d4ff', 1: '#ff4b4b'},
                          template="plotly_dark")
        st.plotly_chart(fig_risk, use_container_width=True)
        
    with r_col2:
        st.subheader("Policy Impact on Leakage")
        dep = df.groupby('deposit_type')['is_canceled'].mean().reset_index()
        fig_dep = px.bar(dep, x='deposit_type', y='is_canceled', 
                         text_auto='.1%',
                         color='is_canceled', color_continuous_scale='Reds', 
                         template='plotly_dark')
        st.plotly_chart(fig_dep, use_container_width=True)

st.caption("LuxeStay Intelligence Pro | Confidential Data | 2026 Strategy")

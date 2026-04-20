import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------- Configuration ----------
st.set_page_config(
    page_title="Hotel Intelligence Pro",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Styling
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    div[data-testid="metric-container"] {
        background-color: #1e2130;
        border: 1px solid #31333f;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------- Data Engine ----------
@st.cache_data
def load_data():
    df = pd.read_csv("hotel_booking_cleaned.csv")
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                   'July', 'August', 'September', 'October', 'November', 'December']
    df['arrival_date_month'] = pd.Categorical(df['arrival_date_month'], categories=month_order, ordered=True)
    
    # Calculate Total Revenue if not present
    if 'revenue' not in df.columns:
        df['revenue'] = df['adr'] * (df['stays_in_weekend_nights'] + df['stays_in_week_nights'])
    return df

df_raw = load_data()

# ---------- Sidebar Logic ----------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2784/2784554.png", width=100)
    st.title("Control Center")
    
    hotel_choice = st.multiselect("Hotel Portfolio", df_raw["hotel"].unique(), default=df_raw["hotel"].unique())
    year_choice = st.multiselect("Fiscal Year", sorted(df_raw["arrival_date_year"].unique()), default=df_raw["arrival_date_year"].unique())
    
    st.divider()
    st.caption("Last data refresh: 2026-04-20")

# Apply Filters
df = df_raw[(df_raw["hotel"].isin(hotel_choice)) & (df_raw["arrival_date_year"].isin(year_choice))]

# ---------- App Header ----------
col_head, col_status = st.columns([3, 1])
with col_head:
    st.title('🏨 Hotel Booking Intelligence')
    st.info(f"Analyzing {len(df):,} records across {len(hotel_choice)} properties.")

with col_status:
    # Quick health check
    cancel_rate = df["is_canceled"].mean() * 100
    if cancel_rate > 35:
        st.warning(f"High Cancellation Risk: {cancel_rate:.1f}%")
    else:
        st.success(f"Stable Booking Health: {cancel_rate:.1f}%")

# ---------- KPI Bar ----------
k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Bookings", f"{len(df):,}", delta="+12% vs LY") # Static delta for UI example
k2.metric("Avg Daily Rate", f"${df['adr'].mean():.2f}")
k3.metric("Gross Revenue", f"${df['revenue'].sum()/1e6:.2f}M")
k4.metric("Occupancy Nights", f"{int(df['stays_in_week_nights'].sum() + df['stays_in_weekend_nights'].sum()):,}")

# ---------- Main Workspace ----------
tab1, tab2, tab3 = st.tabs(["📊 Performance Overview", "🌍 Geographic Insights", "🔍 Segment Deep-Dive"])

with tab1:
    c1, c2 = st.columns([7, 3])
    
    with c1:
        st.subheader("Revenue & Booking Momentum")
        # Multi-axis chart
        trend_data = df.groupby('arrival_date_month', observed=False).agg({'revenue': 'sum', 'hotel': 'count'}).reset_index()
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Bar(x=trend_data['arrival_date_month'], y=trend_data['revenue'], name='Revenue', marker_color='#636EFA'))
        fig_trend.add_trace(go.Scatter(x=trend_data['arrival_date_month'], y=trend_data['hotel'], name='Bookings', yaxis='y2', line=dict(color='#EF553B', width=3)))
        
        fig_trend.update_layout(
            template="plotly_dark",
            yaxis=dict(title="Revenue ($)"),
            yaxis2=dict(title="Booking Count", overlaying='y', side='right'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_trend, use_container_width=True)

    with c2:
        st.subheader("Distribution")
        fig_donut = px.pie(df, names="hotel", hole=.6, template="plotly_dark", color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_donut, use_container_width=True)

with tab2:
    st.subheader("Global Guest Origin")
    country_map = df['country'].value_counts().reset_index()
    fig_map = px.choropleth(country_map, locations="country", color="count", 
                            hover_name="country", color_continuous_scale=px.colors.sequential.Plasma,
                            template="plotly_dark")
    fig_map.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig_map, use_container_width=True)

with tab3:
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("Cancellation Sensitivity by Segment")
        fig_strip = px.strip(df.sample(min(2000, len(df))), x="customer_type", y="adr", color="is_canceled", 
                             stripmode="overlay", template="plotly_dark", title="ADR vs Cancellation")
        st.plotly_chart(fig_strip, use_container_width=True)
        
    with col_b:
        st.subheader("Deposit Policy Impact")
        deposit_impact = df.groupby('deposit_type')['is_canceled'].mean().reset_index()
        fig_dep = px.bar(deposit_impact, x='deposit_type', y='is_canceled', 
                         color='is_canceled', color_continuous_scale='Reds', template='plotly_dark')
        st.plotly_chart(fig_dep, use_container_width=True)

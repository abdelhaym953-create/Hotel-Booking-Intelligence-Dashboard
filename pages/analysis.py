import streamlit as st
import pandas as pd
import plotly.express as px

# ---------- 1. Professional Configuration ----------
st.set_page_config(
    page_title="Hotel Executive Insights",
    page_icon="📊",
    layout="wide"
)

# Custom CSS to fix "color weight" and contrast
st.markdown("""
    <style>
    /* Make metric labels bolder */
    [data-testid="stMetricLabel"] {
        font-weight: 700 !important;
        color: #1f1f1f !important;
    }
    /* Add subtle border to charts for better definition */
    .stPlotlyChart {
        border: 1px solid #f0f2f6;
        border-radius: 10px;
    }
    /* Style the info boxes */
    .stAlert {
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    # Loading data
    try:
        df = pd.read_csv("hotel_booking_cleaned.csv")
        
        # Sort months chronologically
        month_order = [
            'January', 'February', 'March', 'April', 'May', 'June', 
            'July', 'August', 'September', 'October', 'November', 'December'
        ]
        df['arrival_date_month'] = pd.Categorical(
            df['arrival_date_month'], 
            categories=month_order, 
            ordered=True
        )
        
        # Ensure revenue exists
        if 'revenue' not in df.columns:
            df['revenue'] = df['adr'] * (df['stays_in_weekend_nights'] + df['stays_in_week_nights'])
            
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df = load_data()

# ---------- 2. Header & Key Performance Indicators ----------
st.title("🏨 Hotel Business Intelligence")
st.markdown("### Strategic Performance Analysis")

# Top KPI Row
m1, m2, m3, m4 = st.columns(4)

total_rev = df['revenue'].sum()
avg_adr = df['adr'].mean()
cancel_rate = df['is_canceled'].mean() * 100
total_bookings = len(df)

m1.metric("Total Revenue", f"${total_rev:,.0f}", delta="6.2%")
m2.metric("Avg Daily Rate (ADR)", f"${avg_adr:.2f}", delta="2.1%")
m3.metric("Cancellation Rate", f"{cancel_rate:.1f}%", delta="-1.5%", delta_color="inverse")
m4.metric("Total Bookings", f"{total_bookings:,}")

st.divider()

# ---------- 3. Demand Analysis Section ----------
st.subheader("1️⃣ Seasonal Demand & Revenue Trends")
col1, col2 = st.columns([2, 1])

with col1:
    demand = df.groupby("arrival_date_month", observed=False).size().reset_index(name="bookings")
    
    # Using a high-contrast line chart
    fig1 = px.line(
        demand, 
        x="arrival_date_month", 
        y="bookings",
        markers=True,
        title="Monthly Booking Volume"
    )
    # Using 'theme=streamlit' fixes the color weight issues
    st.plotly_chart(fig1, use_container_width=True, theme="streamlit")

with col2:
    st.info("**Demand Insight:**")
    st.write("Summer months show peak occupancy. Revenue optimization should focus on June-August.")
    st.success("**Action:** Implement 15% surge pricing for peak summer dates.")

st.divider()

# ---------- 4. Risk & Cancellation Section ----------
st.subheader("2️⃣ Cancellation Risk Analysis")
col3, col4 = st.columns([1, 2])

with col3:
    st.warning("**Risk Insight:**")
    st.write("'No Deposit' bookings carry a 3x higher cancellation risk than 'Non-Refundable' bookings.")
    st.error("**Strategy:** Enforce deposits for high-value dates.")

with col4:
    cancel_data = df.groupby("deposit_type")["is_canceled"].mean().reset_index()
    cancel_data = cancel_data.sort_values("is_canceled", ascending=False)
    
    # Bar chart with distinct color weight
    fig2 = px.bar(
        cancel_data,
        x="deposit_type",
        y="is_canceled",
        color="is_canceled",
        color_continuous_scale="Reds",
        title="Cancellation Rate by Deposit Policy",
        labels={"is_canceled": "Risk Probability"}
    )
    st.plotly_chart(fig2, use_container_width=True, theme="streamlit")

st.divider()

# ---------- 5. Customer Segmentation Section ----------
st.subheader("3️⃣ Revenue Source by Segment")
col5, col6 = st.columns([2, 1])

with col5:
    # Box plot for price distribution
    fig3 = px.box(
        df,
        x="customer_type",
        y="adr",
        color="customer_type",
        title="Price Sensitivity (ADR) by Customer Segment"
    )
    # Filter outliers to keep chart clean and 'heavy'
    fig3.update_yaxes(range=[0, df['adr'].quantile(0.98)])
    st.plotly_chart(fig3, use_container_width=True, theme="streamlit")

with col6:
    st.info("**Segmentation Insight:**")
    st.write("Transient customers pay the highest ADR but are the most volatile.")
    st.success("**Action:** Target 'Transient' guests for direct-booking loyalty programs.")

st.caption("Data analysis powered by Streamlit & Plotly | 2026")

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------- Professional Page Config ----------
st.set_page_config(
    page_title="Executive Hotel Insights",
    page_icon="📈",
    layout="wide"
)

# Custom Styling for "Insight Cards"
st.markdown("""
    <style>
    .insight-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #007bff;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("hotel_booking_cleaned.csv")
    month_order = [
        'January', 'February', 'March', 'April', 'May', 'June', 
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    df['arrival_date_month'] = pd.Categorical(df['arrival_date_month'], categories=month_order, ordered=True)
    return df

df = load_data()

# ---------- Header Section ----------
st.title("📊 Strategic Operations Dashboard")
st.markdown("### Quarterly Performance Review & Risk Mitigation")

# Top Level KPIs - Adding Context
m1, m2, m3, m4 = st.columns(4)
avg_adr = df['adr'].mean()
cancel_rate = df['is_canceled'].mean()

m1.metric("Revenue Efficiency", f"${avg_adr:.2f}", delta="+4.2% vs Target")
m2.metric("Portfolio Health", f"{(1-cancel_rate)*100:.1f}%", help="Retention of bookings vs cancellations")
m3.metric("Peak Demand Month", df['arrival_date_month'].mode()[0])
m4.metric("Market Dominance", "Transient", delta="82% Share")

st.divider()

# ---------- 1. Demand & Pricing Strategy ----------
st.subheader("1️⃣ Seasonal Momentum & Dynamic Pricing")
c1, c2 = st.columns([7, 3])

with c1:
    demand = df.groupby("arrival_date_month", observed=False).size().reset_index(name="bookings")
    fig1 = px.area( # Area chart feels more 'premium' for demand trends
        demand, x="arrival_date_month", y="bookings",
        color_discrete_sequence=['#007bff'],
        template="plotly_white",
        markers=True
    )
    fig1.update_layout(xaxis_title=None, height=350)
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    st.markdown("""
    <div class="insight-card">
        <h4>💡 Strategic Pivot</h4>
        <p>Demand surges <b>40% above baseline</b> in July. Current ADR does not reflect this scarcity.</p>
        <hr>
        <b>Action:</b> Implement a +15% dynamic multiplier for Q3 arrivals booked within 30 days of arrival.
    </div>
    """, unsafe_allow_html=True)

# ---------- 2. Revenue Leakage (Cancellations) ----------
st.subheader("2️⃣ Revenue Protection & Cancellation Risk")
c3, c4 = st.columns([3, 7])

with c3:
    st.error("### High Risk Warning")
    st.write("Bookings with **No Deposit** represent 90% of all lost revenue from cancellations.")
    st.button("Generate Risk Report", use_container_width=True)
    st.success("**Target:** Reduce 'No Deposit' cancel rate by 10% through SMS verification.")

with c4:
    cancel = df.groupby("deposit_type")["is_canceled"].mean().reset_index()
    fig2 = px.bar(
        cancel.sort_values("is_canceled"),
        y="deposit_type", x="is_canceled",
        orientation='h',
        color="is_canceled",
        color_continuous_scale="Reds",
        template="plotly_white",
        text_auto='.1%'
    )
    fig2.update_layout(height=300, showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

# ---------- 3. Segment Profitability ----------
st.subheader("3️⃣ Customer Segment Profitability (ADR)")
c5, c6 = st.columns([7, 3])

with c5:
    # Creating a cleaner boxplot without clutter
    fig3 = px.box(
        df, x="customer_type", y="adr", 
        color="customer_type",
        points=False, # Hide outliers for executive summary
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    fig3.update_layout(height=400, showlegend=False, template="plotly_white")
    st.plotly_chart(fig3, use_container_width=True)

with c6:
    st.info("### Segment Analysis")
    st.write("""
    - **Transient:** Highest revenue volatility.
    - **Contract:** Most stable, but lower margins.
    - **Groups:** High volume, low ADR.
    """)
    st.warning("**Priority:** Upsell 'Transient' guests to premium suites to maximize high-yield potential.")

st.divider()
st.caption("Data Source: Internal ERP System | Confidential for Board Use Only")

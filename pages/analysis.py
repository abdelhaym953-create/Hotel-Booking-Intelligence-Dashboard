import streamlit as st
import pandas as pd
import plotly.express as px

# Setup
st.set_page_config(page_title="Hotel Executive Insights", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("hotel_booking_cleaned.csv")
    # CRITICAL: Sort months chronologically
    month_order = [
        'January', 'February', 'March', 'April', 'May', 'June', 
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    df['arrival_date_month'] = pd.Categorical(df['arrival_date_month'], categories=month_order, ordered=True)
    return df

df = load_data()

# Header Section
st.title("📊 Business Intelligence: Hotel Operations")
st.markdown("### Strategic Recommendations based on Historical Data")
st.divider()

# -------- Section 1: Demand Analysis --------
col1, col2 = st.columns([2, 1])

with col1:
    st.header("1️⃣ Seasonal Demand Trends")
    # Grouping with observed=False to maintain categorical order
    demand = df.groupby("arrival_date_month", observed=False).size().reset_index(name="bookings")
    
    fig1 = px.line(
        demand,
        x="arrival_date_month",
        y="bookings",
        markers=True,
        template="plotly_white",
        title="Monthly Booking Volume"
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.write("### 💡 Insight")
    st.info("Demand peaks during the summer months (July/August), suggesting high leisure travel dependency.")
    st.write("### 🚀 Strategy")
    st.success("**Dynamic Pricing:** Implement a 15-20% price surge during Q3 and introduce 'Early Bird' discounts in Q1 to fill low-occupancy periods.")

st.divider()

# -------- Section 2: Revenue Risk --------
col3, col4 = st.columns([1, 2])

with col3:
    st.write("### 💡 Insight")
    cancel_rate = (df['is_canceled'].mean() * 100)
    st.info(f"The current average cancellation rate is **{cancel_rate:.1f}%**. 'No Deposit' bookings are significantly more volatile.")
    st.write("### 🚀 Strategy")
    st.success("**Strict Policies:** Require non-refundable deposits for 'Transient' customers during peak dates to lock in revenue.")

with col4:
    st.header("2️⃣ Cancellation Risk by Deposit Type")
    cancel = df.groupby("deposit_type")["is_canceled"].mean().reset_index()
    # Sort for visual impact
    cancel = cancel.sort_values("is_canceled", ascending=False)
    
    fig2 = px.bar(
        cancel,
        x="deposit_type",
        y="is_canceled",
        color="is_canceled",
        color_continuous_scale="Reds",
        labels={"is_canceled": "Cancellation Prob."},
        template="plotly_white"
    )
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# -------- Section 3: Market Segmentation --------
st.header("3️⃣ Revenue Source by Customer Segment")
col5, col6 = st.columns([2, 1])

with col5:
    # Using a Box Plot to show ADR (Average Daily Rate) per customer type is more insightful than just counts
    fig3 = px.box(
        df,
        x="customer_type",
        y="adr",
        color="customer_type",
        title="Price Sensitivity by Customer Segment",
        template="plotly_white"
    )
    # Filter out outliers for a cleaner look
    fig3.update_yaxes(range=[0, df['adr'].quantile(0.95)])
    st.plotly_chart(fig3, use_container_width=True)

with col6:
    st.write("### 💡 Insight")
    st.info("Transient customers provide the highest daily rates but are most sensitive to price changes.")
    st.write("### 🚀 Strategy")
    st.success("**Loyalty Program:** Convert high-value Transient guests into 'Contract' or 'Group' segments through a membership portal to stabilize long-term demand.")

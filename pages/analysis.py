import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📈 Business Insights & Decision Making")

@st.cache_data
def load_data():
    return pd.read_csv("hotel_booking_cleaned.csv")

df = load_data()

# -------- Demand Analysis --------

st.header("1️⃣ When is demand highest?")

demand = df.groupby("arrival_date_month").size().reset_index(name="bookings")

fig1 = px.line(
    demand,
    x="arrival_date_month",
    y="bookings",
    markers=True
)

st.plotly_chart(fig1,use_container_width=True)

st.info("""
Insight:
Demand increases during peak seasons.

Decision:
Increase room prices during high-demand months.
""")

# -------- Cancellation --------

st.header("2️⃣ What causes cancellations?")

cancel = df.groupby("deposit_type")["is_canceled"].mean().reset_index()

fig2 = px.bar(
    cancel,
    x="deposit_type",
    y="is_canceled",
    color="is_canceled"
)

st.plotly_chart(fig2,use_container_width=True)

st.info("""
Insight:
Bookings without deposits cancel more often.

Decision:
Encourage customers to pay deposits.
""")

# -------- Customer Type --------

st.header("3️⃣ Which customers book the most?")

cust = df["customer_type"].value_counts().reset_index()
cust.columns=["type","count"]

fig3 = px.bar(
    cust,
    x="type",
    y="count",
    color="count"
)

st.plotly_chart(fig3,use_container_width=True)

st.info("""
Insight:
Transient customers dominate bookings.

Decision:
Focus marketing campaigns on individual travelers.
""")
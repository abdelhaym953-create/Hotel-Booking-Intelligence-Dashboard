import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Hotel Analytics",
    layout="wide",
)

# ---------- Styling ----------


# ---------- Title ----------

st.title('🏨 Hotel Booking Intelligence Dashboard')

# ---------- Load Data ----------

@st.cache_data
def load_data():
    return pd.read_csv("hotel_booking_cleaned.csv")

df = load_data()

# ---------- Filters ----------

st.sidebar.header("Filters")

hotel = st.sidebar.multiselect(
    "Hotel Type",
    df["hotel"].unique(),
    default=df["hotel"].unique()
)

year = st.sidebar.multiselect(
    "Year",
    df["arrival_date_year"].unique(),
    default=df["arrival_date_year"].unique()
)

df = df[
    (df["hotel"].isin(hotel)) &
    (df["arrival_date_year"].isin(year))
]

# ---------- KPIs ----------

total_bookings = len(df)
cancel_rate = df["is_canceled"].mean()*100
avg_price = df["adr"].mean()
revenue = df["revenue"].sum()

col1,col2,col3,col4 = st.columns(4)

col1.metric("📅 Total Bookings",f"{total_bookings:,}")
col2.metric("❌ Cancellation Rate",f"{cancel_rate:.1f}%")
col3.metric("💰 Avg Price",f"${avg_price:.0f}")
col4.metric("🏦 Revenue",f"${revenue:,.0f}")

st.divider()

# ---------- Charts ----------

col1,col2 = st.columns(2)

bookings_month = df.groupby("arrival_date_month").size().reset_index(name="bookings")

fig1 = px.bar(
    bookings_month,
    x="arrival_date_month",
    y="bookings",
    color="bookings",
    color_continuous_scale="viridis",
    title="Bookings by Month"
)

hotel_dist = df["hotel"].value_counts().reset_index()
hotel_dist.columns=["hotel","count"]

fig2 = px.pie(
    hotel_dist,
    names="hotel",
    values="count",
    hole=0.4,
    title="Hotel Type Distribution"
)

col1.plotly_chart(fig1,use_container_width=True)
col2.plotly_chart(fig2,use_container_width=True)

# ---------- Country ----------

country = df["country"].value_counts().head(10).reset_index()
country.columns=["country","count"]

fig3 = px.bar(
    country,
    x="country",
    y="count",
    color="count",
    color_continuous_scale="plasma",
    title="Top Countries"
)

st.plotly_chart(fig3,use_container_width=True)
import streamlit as st
import pandas as pd
import plotly.express as px

# ---------- Configuration ----------
st.set_page_config(
    page_title="Hotel Analytics",
    page_icon="🏨",
    layout="wide",
)

# Custom CSS for a cleaner look
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    [data-testid="stMetricValue"] {
        font-size: 28px;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------- Load Data ----------
@st.cache_data
def load_data():
    # Adding a dummy 'revenue' col if it doesn't exist for the sake of the demo
    df = pd.read_csv("hotel_booking_cleaned.csv")
    
    # Ensure date columns are handled or sorted correctly
    month_order = [
        'January', 'February', 'March', 'April', 'May', 'June', 
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    df['arrival_date_month'] = pd.Categorical(df['arrival_date_month'], categories=month_order, ordered=True)
    return df

try:
    df_raw = load_data()
except Exception as e:
    st.error(f"Could not load data: {e}")
    st.stop()

# ---------- Sidebar ----------
st.sidebar.header("🔍 Global Filters")

# Using a container for better organization
with st.sidebar:
    hotel = st.multiselect(
        "Select Hotel Type",
        options=df_raw["hotel"].unique(),
        default=df_raw["hotel"].unique()
    )

    year = st.multiselect(
        "Select Arrival Year",
        options=sorted(df_raw["arrival_date_year"].unique()),
        default=sorted(df_raw["arrival_date_year"].unique())
    )

# Filter Logic
df = df_raw[
    (df_raw["hotel"].isin(hotel)) & 
    (df_raw["arrival_date_year"].isin(year))
]

# ---------- Header & KPIs ----------
st.title('🏨 Hotel Booking Intelligence')
st.markdown(f"Showing data for **{', '.join(map(str, year))}**")

# Calculate KPIs
total_bookings = len(df)
cancel_rate = df["is_canceled"].mean() * 100
avg_price = df["adr"].mean()
# Using .get() to handle cases where revenue might be missing
total_revenue = df["revenue"].sum() if "revenue" in df.columns else (df["adr"] * (df["stays_in_weekend_nights"] + df["stays_in_week_nights"])).sum()

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpi1.metric("Total Bookings", f"{total_bookings:,}", help="Total number of confirmed and canceled bookings")
kpi2.metric("Cancellation Rate", f"{cancel_rate:.1f}%", delta=f"{-cancel_rate:.1f}%", delta_color="inverse")
kpi3.metric("Avg Daily Rate (ADR)", f"${avg_price:.2f}")
kpi4.metric("Estimated Revenue", f"${total_revenue:,.0f}")

st.divider()

# ---------- Main Visuals ----------
col_left, col_right = st.columns([6, 4])

with col_left:
    # 1. Monthly Trend (Better sorting)
    st.subheader("Monthly Booking Volume")
    bookings_month = df.groupby("arrival_date_month", observed=False).size().reset_index(name="bookings")
    
    fig_line = px.line(
        bookings_month,
        x="arrival_date_month",
        y="bookings",
        markers=True,
        template="plotly_white",
        color_discrete_sequence=["#00CC96"]
    )
    fig_line.update_layout(xaxis_title=None, yaxis_title="Number of Bookings")
    st.plotly_chart(fig_line, use_container_width=True)

with col_right:
    # 2. Donut Chart
    st.subheader("Market Share")
    hotel_dist = df["hotel"].value_counts().reset_index()
    hotel_dist.columns = ["hotel", "count"]
    
    fig_pie = px.pie(
        hotel_dist, 
        names="hotel", 
        values="count", 
        hole=0.5,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_pie.update_layout(showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=-0.2))
    st.plotly_chart(fig_pie, use_container_width=True)

# ---------- Bottom Section ----------
st.divider()
col_bot1, col_bot2 = st.columns(2)

with col_bot1:
    st.subheader("Top 10 Guest Countries")
    country_data = df["country"].value_counts().head(10).reset_index()
    country_data.columns = ["country", "count"]
    
    fig_bar = px.bar(
        country_data,
        x="count",
        y="country",
        orientation='h',
        color="count",
        color_continuous_scale="Blues"
    )
    fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_bar, use_container_width=True)

with col_bot2:
    st.subheader("Revenue vs. Cancellation")
    # A more insightful view: are expensive rooms canceled more often?
    fig_scatter = px.box(
        df,
        x="is_canceled",
        y="adr",
        color="is_canceled",
        notched=True,
        title="Price Distribution by Cancellation Status",
        labels={"is_canceled": "Canceled (1=Yes)", "adr": "Average Daily Rate"}
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

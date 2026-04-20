import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------- 1. Configuration & Theme ----------
st.set_page_config(page_title="Hotel Analytics Pro", page_icon="🏨", layout="wide")

# Modern CSS for Bento-style KPI cards
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .kpi-card {
        background-color: #161b22;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #30363d;
        text-align: center;
        transition: 0.3s;
    }
    .kpi-card:hover { border-color: #fbbf24; transform: translateY(-5px); }
    .kpi-label { color: #8b949e; font-size: 14px; text-transform: uppercase; letter-spacing: 1px; }
    .kpi-value { color: #fbbf24; font-size: 32px; font-weight: bold; margin: 10px 0; }
    </style>
    """, unsafe_allow_html=True)

# ---------- 2. Data Engine ----------
@st.cache_data
def load_data():
    df = pd.read_csv("hotel_booking_cleaned.csv")
    
    # Pre-processing
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                   'July', 'August', 'September', 'October', 'November', 'December']
    df['arrival_date_month'] = pd.Categorical(df['arrival_date_month'], categories=month_order, ordered=True)
    
    # Calculate Revenue if missing
    if "revenue" not in df.columns:
        df["revenue"] = df["adr"] * (df["stays_in_weekend_nights"] + df["stays_in_week_nights"])
    
    return df

try:
    df_raw = load_data()
except Exception as e:
    st.error(f"Error: Ensure 'hotel_booking_cleaned.csv' is in the folder. {e}")
    st.stop()

# ---------- 3. Professional Sidebar ----------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3009/3009489.png", width=80)
    st.title("Filters")
    
    selected_hotels = st.multiselect("Hotel Type", df_raw["hotel"].unique(), default=df_raw["hotel"].unique())
    selected_years = st.select_slider("Select Year Range", options=sorted(df_raw["arrival_date_year"].unique().tolist()), value=sorted(df_raw["arrival_date_year"].unique().tolist()))
    
    st.divider()
    st.caption("Developed by Mohamed | Data Analyst")

# Filter logic
df = df_raw[
    (df_raw["hotel"].isin(selected_hotels)) & 
    (df_raw["arrival_date_year"].isin(selected_years if isinstance(selected_years, list) else [selected_years]))
]

# ---------- 4. Header & KPI Section ----------
st.title('🏨 Hotel Booking Intelligence')
st.markdown(f"Analytical overview for selected hotels in **{selected_years}**")

# KPI Calculations
total_bookings = len(df)
cancel_rate = df["is_canceled"].mean() * 100
avg_price = df["adr"].mean()
total_rev = df["revenue"].sum()

# Custom KPI Display
c1, c2, c3, c4 = st.columns(4)

def kpi_box(col, label, value, prefix=""):
    with col:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{prefix}{value}</div>
            </div>
        """, unsafe_allow_html=True)

kpi_box(c1, "Total Bookings", f"{total_bookings:,}")
kpi_box(c2, "Cancellation Rate", f"{cancel_rate:.1f}%")
kpi_box(c3, "Avg Daily Rate", f"{avg_price:.2f}", "$")
kpi_box(c4, "Total Revenue", f"{total_rev/1e6:.1f}M", "$")

st.write("<br>", unsafe_allow_html=True)

# ---------- 5. Tabbed Insights ----------
tab_overview, tab_pricing, tab_demographics = st.tabs(["📈 Market Overview", "💰 Pricing Analysis", "🌍 Demographics"])

with tab_overview:
    col_l, col_r = st.columns([7, 3])
    
    with col_l:
        st.subheader("Booking Demand Trend")
        bookings_month = df.groupby(["arrival_date_month", "hotel"], observed=False).size().reset_index(name="count")
        fig_trend = px.line(bookings_month, x="arrival_date_month", y="count", color="hotel",
                           markers=True, template="plotly_dark", 
                           color_discrete_sequence=["#fbbf24", "#60a5fa"])
        fig_trend.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_trend, use_container_width=True)

    with col_r:
        st.subheader("Booking Mix")
        fig_donut = px.pie(df, names="hotel", hole=0.6, template="plotly_dark",
                          color_discrete_sequence=["#fbbf24", "#1e293b"])
        fig_donut.update_layout(showlegend=False)
        st.plotly_chart(fig_donut, use_container_width=True)

with tab_pricing:
    st.subheader("ADR Distribution: Canceled vs. Non-Canceled")
    fig_box = px.box(df, x="is_canceled", y="adr", color="hotel", notched=True,
                    template="plotly_dark", color_discrete_sequence=["#fbbf24", "#60a5fa"],
                    labels={"is_canceled": "Canceled (1=Yes)", "adr": "Price (ADR)"})
    st.plotly_chart(fig_box, use_container_width=True)
    st.info("💡 **Insight:** High ADR (price) often correlates with higher cancellation rates in City Hotels.")

with tab_demographics:
    col_map, col_list = st.columns([2, 1])
    
    with col_map:
        st.subheader("Global Guest Distribution")
        country_counts = df["country"].value_counts().reset_index()
        fig_map = px.choropleth(country_counts, locations="country", color="count",
                               color_continuous_scale="YlOrBr", template="plotly_dark")
        st.plotly_chart(fig_map, use_container_width=True)
        
    with col_list:
        st.subheader("Top Markets")
        top_countries = country_counts.head(10)
        st.dataframe(top_countries, hide_index=True, use_container_width=True)

# ---------- 6. Export Section ----------
st.divider()
with st.expander("📥 Export Filtered Data"):
    st.write("Download the current view for offline reporting.")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", data=csv, file_name="hotel_data_export.csv", mime="text/csv")

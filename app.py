
# ETHIOPIA COFFEE MARKET DASHBOARD
# Developed By: Awoke Tiruneh
# Bahir Dar University
# Data Science Project
# Import Required Libraries
# Import Streamlit library for building the interactive dashboard
import streamlit as st
# Import Pandas for data loading, cleaning, and analysis
import pandas as pd
# Import Plotly Express for creating interactive charts with simple syntax
import plotly.express as px
# Import Plotly Graph Objects for advanced and customized visualizations
import plotly.graph_objects as go
st.set_page_config(
    page_title="Ethiopia Coffee Market Dashboard",  # Title shown in the browser tab
    page_icon="☕",                                  # Icon displayed in the browser tab
    layout="wide",                                  # Use full screen width for dashboard content
    initial_sidebar_state="expanded"                # Open sidebar automatically when app starts
)
# Custom CSS Styling
# Modify Streamlit default layout:
# - Add small left and right margins
# - Use full available screen width for dashboard components
st.markdown(
    """
<style>
/* 1. Main Page Margin and Padding Adjustments */
.block-container {
    padding-top: 0rem !important; /* - Reduce top padding */
    padding-bottom: 0rem !important;
    padding-left: 0rem !important;
    padding-right: 0rem !important;
    max-width: 100% !important;
}
/* 2. Narrowing the large gap between vertical elements */
div[data-testid="stVerticalBlock"] {
    gap: 0rem !important;
}
div[data-testid="stVerticalBlock"] > div {
    gap: 0rem !important;
    margin-bottom: 0.1rem !important;
}
/* 3. Removing extra space around Headings (h1, h2, h3) */
h1, h2, h3 {
    margin-top: 0.8rem !important;
    margin-bottom: 0.2rem !important;
    padding-top: 0.2rem !important;
    padding-bottom: 0.2rem !important;
}
/* 4. Narrowing the gap between horizontal columns (for KPIs) */
div[data-testid="stHorizontalBlock"] {
    gap: 0.3rem !important;
}
</style>
""",
    unsafe_allow_html=True,
)
st.markdown(
    """
<div style="background-color: #4A2C11; padding: 15px; border-radius: 6px; color: white; margin-bottom: 2px;">   
    <h1 style="margin: 0; color: white; font-size: 2rem;">☕ Ethiopia Coffee Market Dashboard</h1>   
    <p style="margin: 5px 0 0 0; color: #F5E6CA; font-size: 1.05rem;">   
        Analytical dashboard — Use the filters on the left to explore prices, trading volume and market trends.
    </p>
</div>
""",
    unsafe_allow_html=True,
)  

# Apply custom CSS to remove Streamlit's default top header
# This creates a cleaner dashboard interface without the default toolbar area
st.markdown("""
<style>
header[data-testid="stHeader"]{   /* Hide Streamlit Default Header*/
    display:none;  /* Remove the default Streamlit header from the page */
}
</style>
""", unsafe_allow_html=True)  # Allow custom CSS styling in Streamlit
# Load Cleaned Coffee Dataset with Caching
@st.cache_data  # Cache dataset in RAM to optimize dashboard responsiveness
def load_data():
    # Read the preprocessed coffee market dataset
    df = pd.read_csv("cleaned_coffee_data.csv")
    # Ensure Year and Day columns are cast to numeric data types
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df["Day"] = pd.to_numeric(df["Day"], errors="coerce")
    return df
# Load cached data into dataframe
df = load_data()
# Sidebar Filters
# Filters Title
st.sidebar.header("🔎 Filters")
# Space after button
st.sidebar.markdown("<br>", unsafe_allow_html=True)
# Reset Button
if st.sidebar.button("🔄 Reset Filters"):
    st.session_state["year_filter"] = "All"
    st.session_state["month_filter"] = "All"
    st.session_state["day_filter"] = "All"
    st.session_state["warehouse_filter"] = "All"
    st.session_state["symbol_filter"] = "All"
    st.rerun()
# Year Filter
year_options = sorted(
    df["Year"].dropna().astype(int).unique().tolist()
)
selected_year = st.sidebar.selectbox(
    "Select Year",
    options=["All"] + year_options,
    key="year_filter"
)
# Month Filter
month_options = sorted(
    df["Month"].dropna().unique().tolist()
)
selected_month = st.sidebar.selectbox(
    "Select Month",
    options=["All"] + month_options,
    key="month_filter"
)
# Day Filter
day_options = sorted(
    df["Day"].dropna().astype(int).unique().tolist()
)
selected_day = st.sidebar.selectbox(
    "Select Day",
    options=["All"] + day_options,
    key="day_filter"
)
# Warehouse Filter
warehouse_options = sorted(
    df["Warehouse"].dropna().unique().tolist()
)

selected_warehouse = st.sidebar.selectbox(
    "Select Warehouse",
    options=["All"] + warehouse_options,
    key="warehouse_filter"
)
# Coffee Symbol Filter
symbol_options = sorted(
    df["Symbol"].dropna().unique().tolist()
)
selected_symbol = st.sidebar.selectbox(
    "Select Coffee Symbol",
    options=["All"] + symbol_options,
    key="symbol_filter"
)
# Apply Selected Filters
filtered_df = df.copy()
# Filter by Year
if selected_year != "All":
    filtered_df = filtered_df[
        filtered_df["Year"] == selected_year
    ]
# Filter by Month
if selected_month != "All":
    filtered_df = filtered_df[
        filtered_df["Month"] == selected_month
    ]
# Filter by Day
if selected_day != "All":
    filtered_df = filtered_df[
        filtered_df["Day"] == selected_day
    ]
# Filter by Warehouse
if selected_warehouse != "All":
    filtered_df = filtered_df[
        filtered_df["Warehouse"] == selected_warehouse
    ]
# Filter by Coffee Symbol
if selected_symbol != "All":
    filtered_df = filtered_df[
        filtered_df["Symbol"] == selected_symbol
    ]
# Display Number of Filtered Records
st.sidebar.success(
    f"Total Records: {len(filtered_df):,}"
)
# Custom Sidebar Styling
st.markdown("""
<style>

/* Sidebar Background Color */
section[data-testid="stSidebar"] {
    background-color: #4A2C11 !important;
    border-right: 0px solid #DDD;
}

/* Sidebar Header Color */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: white !important;
}

/* Sidebar Widget Labels */
section[data-testid="stSidebar"] label[data-testid="stWidgetLabel"] p {
    color: #F5E6CA !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
}

/* Sidebar Text */
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span {
    color: #F5E6CA !important;
}

/* Total Records Box Text */
section[data-testid="stSidebar"] .stAlert {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# Compact KPI Styling

st.markdown("""
<style>

/* KPI Cards */
div[data-testid="stMetric"] {
    background-color: #D4AF37;
    padding: 2px 2px !important;
    border-radius: 10px;
    border: 1px solid #B8860B;
    box-shadow: 0px 2px 5px rgba(0,0,0,0.15);
    min-height: 5px !important;
}
/* KPI Label */
div[data-testid="stMetricLabel"] {
    color: #3E2723 !important;
    font-size: 8px !important;
    font-weight: 600 !important;
    line-height: 1.2 !important;
}
/* KPI Value */
div[data-testid="stMetricValue"] {
    color: #2E1B0E !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    line-height: 1.2 !important;
}
/* Reduce column spacing */
div[data-testid="column"] {
    padding-left: 0px;
    padding-right: 0px;
}
</style>
""", unsafe_allow_html=True)
# KPI Section Header
st.markdown("""
<div style="
    background-color:#1B5E20;
    color:white;
    font-size:15px;
    font-weight:700;
    padding:6px 10px;
    border-radius:8px;
    text-align:center;
    margin-top:0px;
    margin-bottom:15px;
">
☕ Key Performance Indicators (KPIs) Overview
</div>
""", unsafe_allow_html=True)
# KPI Calculations
# Aggregate summary metrics from the filtered DataFrame
total_volume = filtered_df["Volume (Ton)"].sum()
avg_opening = filtered_df["Opening Price"].mean()
avg_closing = filtered_df["Closing Price"].mean()
highest_price = filtered_df["High"].max()
lowest_price = filtered_df["Low"].min()
total_warehouses = filtered_df["Warehouse"].nunique()
total_symbols = filtered_df["Symbol"].nunique()
# Dynamic YoY (Year-over-Year) Price Growth Calculation
# Year-over-Year Growth Calculation
yoy_str = "N/A"
try:
    if selected_year == "All":

        # Compare latest year vs previous year
        yearly_avg = (
            filtered_df.groupby("Year")["Closing Price"]
            .mean()
            .reset_index()
            .sort_values("Year")
        )

        if len(yearly_avg) >= 2:
            latest_price = yearly_avg.iloc[-1]["Closing Price"]
            prev_price = yearly_avg.iloc[-2]["Closing Price"]

            if prev_price > 0:
                growth = ((latest_price - prev_price) / prev_price) * 100
                yoy_str = f"{growth:+.2f}%"

    else:
        current_year_int = int(selected_year)
        prev_year_int = current_year_int - 1

        # Start from full dataset
        temp_df = df.copy()

        # Keep other active filters
        if selected_month != "All":
            temp_df = temp_df[temp_df["Month"] == selected_month]

        if selected_day != "All":
            temp_df = temp_df[temp_df["Day"] == selected_day]

        if selected_warehouse != "All":
            temp_df = temp_df[temp_df["Warehouse"] == selected_warehouse]

        if selected_symbol != "All":
            temp_df = temp_df[temp_df["Symbol"] == selected_symbol]

        # Calculate average closing price
        curr_avg = temp_df[
            temp_df["Year"] == current_year_int
        ]["Closing Price"].mean()

        prev_avg = temp_df[
            temp_df["Year"] == prev_year_int
        ]["Closing Price"].mean()

        if (
            pd.notnull(curr_avg)
            and pd.notnull(prev_avg)
            and prev_avg > 0
        ):
            growth = ((curr_avg - prev_avg) / prev_avg) * 100
            yoy_str = f"{growth:+.2f}%"

except Exception:
    yoy_str = "N/A"

# KPI Cards Display - Single Row (8 KPIs)

col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)

with col1:
    st.metric("📦 Total Volume", f"{total_volume:,.0f} Ton")

with col2:
    st.metric("💰 Avg Opening", f"{avg_opening:,.2f} ETB")

with col3:
    st.metric("💵 Avg Closing", f"{avg_closing:,.2f} ETB")

with col4:
    st.metric("📈 Highest Price", f"{highest_price:,.2f} ETB")

with col5:
    st.metric("📉 Lowest Price", f"{lowest_price:,.2f} ETB")

with col6:
    st.metric("🏢 Warehouses", total_warehouses)

with col7:
    st.metric("☕ Symbols", total_symbols)

with col8:
    st.metric("📊 YoY Growth", yoy_str)
# 🎯 MARKET INSIGHTS SECTION (ALIGNED WITH GRAPH ORDER)

st.markdown("""
<div style="
    background-color:#8B0000;
    color:white;
    font-size:15px;
    font-weight:700;
    padding:8px 12px;
    border-radius:8px;
    text-align:center;
    margin-top:0px;
    margin-bottom:15px;
">
☕ Market insight summary
</div>
""", unsafe_allow_html=True)


# 1. Helper Function for Insight Cards
def create_blue_card(
    title,
    value,
    subtext="",
    bg_color="#0F172A",
    border_color="#3B82F6",
    text_color="#F8FAFC",
    sub_color="#94A3B8",
):
    subtext_html = (
        f'<p style="margin: 2px 0 0 0; font-size: 12px; color: {border_color}; font-weight: 700; line-height: 1.1;">{subtext}</p>'
        if subtext
        else ""
    )

    html_code = f"""
    <div style="
        background-color:  #4A2C11;
        border-left: 4px solid {border_color};
        padding: 6px 0px;
        border-radius: 6px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.15);
        margin-bottom: 10px;
        margin-top: 0.8rem !important;
        height: 50%;
        display: flex;
        flex-direction: column;
        justify-content: center;
    ">
        <p style="margin: 0; font-size: 15px; color: {sub_color}; font-weight: 600; line-height: 0;">{title}</p>
        <h3 style="margin: 2px 0; color: {text_color}; font-size: 15px; font-weight: bold; line-height: 1.1;">{value}</h3>
        {subtext_html}
    </div>
    """
    return st.markdown(html_code, unsafe_allow_html=True)
# 2. CALCULATIONS & DISPLAY (MATCHING GRAPH ORDER)
if not filtered_df.empty:
    # 1. Best Price Year & Price Data
    yearly_price = filtered_df.groupby("Year")["Closing Price"].mean().reset_index()
    if not yearly_price.empty:
        best_price_year = yearly_price.loc[yearly_price["Closing Price"].idxmax(), "Year"]
        highest_avg_price = yearly_price["Closing Price"].max()
    else:
        best_price_year, highest_avg_price = "N/A", 0

    # 2. Peak Volume Year
    yearly_volume = filtered_df.groupby("Year")["Volume (Ton)"].sum().reset_index()
    if not yearly_volume.empty:
        peak_vol_year = yearly_volume.loc[yearly_volume["Volume (Ton)"].idxmax(), "Year"]
        peak_volume = yearly_volume["Volume (Ton)"].max()
    else:
        peak_vol_year, peak_volume = "N/A", 0

    # 3. Peak Month
    monthly_price = filtered_df.groupby("Month")["Closing Price"].mean().reset_index()
    if not monthly_price.empty:
        peak_month = monthly_price.loc[monthly_price["Closing Price"].idxmax(), "Month"]
    else:
        peak_month = "N/A"

    # 4. Top Symbol & Top Warehouse
    top_symbol = filtered_df.groupby("Symbol")["Volume (Ton)"].sum().idxmax() if not filtered_df.empty else "N/A"
    top_warehouse = filtered_df.groupby("Warehouse")["Volume (Ton)"].sum().idxmax() if not filtered_df.empty else "N/A"

    # 5. Overall Trend
    if len(yearly_price) > 1:
        first_price = yearly_price["Closing Price"].iloc[0]
        last_price = yearly_price["Closing Price"].iloc[-1]
        trend = "📈 Upward" if last_price >= first_price else "📉 Downward"
    else:
        trend = "➡️ Stable"

    # 6. Gain Ratio
    if "Change" in filtered_df.columns:
        positive_days = (filtered_df["Change"] > 0).sum()
        gain_ratio = (positive_days / len(filtered_df)) * 100
    else:
        gain_ratio = 0

    # 7. Top Gainer Calculation (Replaces Volatility)
    df_gainer_calc = filtered_df.copy()
    if "Percentage Change (%)" not in df_gainer_calc.columns and "Percentage Change" not in df_gainer_calc.columns:
        if "Opening Price" in df_gainer_calc.columns and "Closing Price" in df_gainer_calc.columns:
            df_gainer_calc["Percentage Change (%)"] = (
                (df_gainer_calc["Closing Price"] - df_gainer_calc["Opening Price"]) / df_gainer_calc["Opening Price"]
            ) * 100

    pct_col = "Percentage Change (%)" if "Percentage Change (%)" in df_gainer_calc.columns else "Percentage Change"

    if pct_col in df_gainer_calc.columns:
        avg_gain = df_gainer_calc.groupby("Symbol")[pct_col].mean()
        if not avg_gain.empty:
            top_gainer_symbol = avg_gain.idxmax()
            top_gainer_val = avg_gain.max()
        else:
            top_gainer_symbol, top_gainer_val = "N/A", 0
    else:
        top_gainer_symbol, top_gainer_val = "N/A", 0
        
    # --- DISPLAY CARDS (PERFECTLY ALIGNED WITH GRAPHS 1-8) ---

    c1, c2, c3, c4, c5, c6, c7, c8 = st.columns(8)

    # 1. Matches Graph 1: Top Symbols (Bar Chart)
    with c1:
        create_blue_card(
            "☕ Top Symbol",
            top_symbol,
            "Most Traded",
            "#0F172A", "#3B82F6", "#FFFFFF", "#94A3B8"
        )

    # 2. Matches Graph 2: Yearly Price (Bar Chart)
    with c2:
        create_blue_card(
            "💰 Best Price Year",
            str(best_price_year),
            f"{highest_avg_price:,.0f} ETB",
            "#0F172A", "#3B82F6", "#FFFFFF", "#94A3B8"
        )

    # 3. Matches Graph 3: Price Trend (Line Chart)
    with c3:
        create_blue_card(
            "📈 Price Trend",
            trend,
            "Market Direction",
            "#0F172A", "#3B82F6", "#FFFFFF", "#94A3B8"
        )

    # 4. Matches Graph 4: Warehouse Volume (Bar Chart)
    with c4:
        create_blue_card(
            "🏢 Top Warehouse",
            top_warehouse,
            "Top Location",
            "#0F172A", "#3B82F6", "#FFFFFF", "#94A3B8"
        )

    # 5. Matches Graph 5: High vs Low (Line Chart / Market Sentiment)
    with c5:
        create_blue_card(
            "🟢 Gain Ratio",
            f"{gain_ratio:.1f}%",
            "Positive Days",
            "#1E293B", "#4ADE80", "#FFFFFF", "#CBD5E1"
        )

    # 6. Matches Graph 6: Volume Trend (Bar Chart)
    with c6:
        create_blue_card(
            "📦 Peak Volume Year",
            str(peak_vol_year),
            f"{peak_volume:,.0f} Ton",
            "#1E293B", "#60A5FA", "#FFFFFF", "#CBD5E1"
        )

    # 7. Matches Graph 7: Seasonality (Line Chart)s
    with c7:
        create_blue_card(
            "🗓️ Peak Month",
            str(peak_month),
            "Highest Avg Price",
            "#1E293B", "#60A5FA", "#FFFFFF", "#CBD5E1"
        )

    # 8. Matches Graph 8: Top 5 Gainers (Horizontal Bar Chart)
    with c8:
        create_blue_card(
            "🚀 Top Gainer",
            top_gainer_symbol,
            f"+{top_gainer_val:.2f}% Avg",
            "#1E293B", "#22C55E", "#FFFFFF", "#CBD5E1"
        )

else:
    st.warning("⚠️ No data available for selected filters.")
# 📊 FOUR CHARTS IN ONE ROW
col1, col2, col3, col4 = st.columns(4)
# ☕ Top 10 Coffee Symbols
with col1:
    top_symbols = (
        filtered_df.groupby("Symbol")["Volume (Ton)"]
        .sum()
        .reset_index()
        .sort_values("Volume (Ton)", ascending=False)
        .head(10)
    )

    fig_symbol = px.bar(
        top_symbols,
        x="Symbol",
        y="Volume (Ton)",
        title="☕ Top Symbols"
    )

    fig_symbol.update_layout(
        template="plotly_white",
        height=200,
        margin=dict(t=40, b=5, l=0, r=0),
        plot_bgcolor="#F5F1E8",
        paper_bgcolor="#F5F1E8",
        showlegend=False,
        title_x=0.25,
        yaxis=dict(showgrid=False)
    )
    fig_symbol.update_traces(marker_color="#2C1D11")

    st.plotly_chart(
        fig_symbol,
        use_container_width=True,
        config={"displayModeBar": False}
    )
# 📅 Yearly Market Performance
with col2:
    yearly_market = (
        filtered_df.groupby("Year")
        .agg({
            "Closing Price": "mean",
            "Volume (Ton)": "sum"
        })
        .reset_index()
    )
    fig_yearly = px.bar(
        yearly_market,
        x="Year",
        y="Closing Price",
        title="📅 Yearly Price"
    )
    fig_yearly.update_layout(
        template="plotly_white",
        height=200,
        margin=dict(t=40, b=5, l=0, r=0),
        plot_bgcolor="#F5F1E8",
        paper_bgcolor="#F5F1E8",
        showlegend=False,
        title_x=0.25,
        yaxis=dict(showgrid=False)
    )
    fig_yearly.update_traces(marker_color="#3D2314")

    st.plotly_chart(
        fig_yearly,
        use_container_width=True,
        config={"displayModeBar": False}
    )
# ☕ Closing Price Trend
with col3:

    temp_df = filtered_df.copy()

    temp_df["Trade Date"] = pd.to_datetime(
        temp_df["Trade Date"],
        errors="coerce"
    )

    temp_df = temp_df.dropna(subset=["Trade Date"])

    monthly_price = (
        temp_df
        .set_index("Trade Date")
        .resample("ME")["Closing Price"]
        .mean()
        .reset_index()
    )

    fig_price = px.line(
        monthly_price,
        x="Trade Date",
        y="Closing Price",
        title="📈 Price Trend"
    )

    fig_price.update_layout(
        template="plotly_white",
        height=200,
        margin=dict(t=40, b=20, l=0, r=0),
        plot_bgcolor="#F5F1E8",
        paper_bgcolor="#F5F1E8",
        showlegend=False,
        title_x=0.25,
        yaxis=dict(showgrid=False)
    )
    fig_price.update_traces(
        line=dict(
            color="#121212",
            width=2
        )
    )
    st.plotly_chart(
        fig_price,
        use_container_width=True,
        config={"displayModeBar": False}
    )
# 🏭 Trading Volume by Warehouse
with col4:
    warehouse_volume = (
        filtered_df.groupby("Warehouse")["Volume (Ton)"]
        .sum()
        .reset_index()
        .sort_values("Volume (Ton)", ascending=False)
    )
    fig_warehouse = px.bar(
        warehouse_volume,
        x="Warehouse",
        y="Volume (Ton)",
        title="🏭 Warehouse Volume"
    )

    fig_warehouse.update_layout(
        template="plotly_white",
        height=200,
        margin=dict(t=40, b=5, l=0, r=0),
        plot_bgcolor="#F5F1E8",
        paper_bgcolor="#F5F1E8",
        showlegend=False,
        title_x=0.2,
        yaxis=dict(showgrid=False)
    )
    fig_warehouse.update_traces(
        marker_color="#264653",
    )
    st.plotly_chart(
        fig_warehouse,
        use_container_width=True,
        config={"displayModeBar": False}
    )
# ROW: High-Low Trend | Volume Trend | Seasonality | Volatility
col1, col2, col3, col4 = st.columns(4)
# 📈 1. Monthly High vs Low Price Trend
with col1:

    df_temp = filtered_df.copy()

    df_temp["Trade Date"] = pd.to_datetime(
        df_temp["Trade Date"],
        errors="coerce"
    )

    df_temp = df_temp[
        (df_temp["High"] > 0)
        & (df_temp["Low"] > 0)
    ]

    df_monthly_range = (
        df_temp
        .set_index("Trade Date")
        .resample("ME")
        .agg({
            "High": "max",
            "Low": "min"
        })
        .reset_index()
    )

    df_melted = df_monthly_range.melt(
        id_vars=["Trade Date"],
        value_vars=["High", "Low"],
        var_name="Price Type",
        value_name="Price (ETB)"
    )

    fig_high_low = px.line(
        df_melted,
        x="Trade Date",
        y="Price (ETB)",
        color="Price Type",
        title="📈 High vs Low",
        color_discrete_map={
            "High":"#2A9D8F",
            "Low": "#C87D55",
        }
    )

    fig_high_low.update_layout(
        template="plotly_white",
        height=200,
        plot_bgcolor="#F5F1E8",
        paper_bgcolor="#F5F1E8",
        hovermode="x unified",
        yaxis=dict(showgrid=False),
        title_x=0.15,
        margin=dict(t=40, b=5, l=0, r=0)
    )
    fig_high_low.update_traces(
        line=dict(width=2)
    )
    st.plotly_chart(
        fig_high_low,
        use_container_width=True,
        config={"displayModeBar": False}
    )
# 📦 2. Yearly Coffee Trading Volume Trend
with col2:
    df_volume = filtered_df.copy()
    df_volume["Trade Date"] = pd.to_datetime(
        df_volume["Trade Date"],
        errors="coerce"
    )

    df_volume["Year"] = (
        df_volume["Trade Date"]
        .dt.year
    )

    df_yearly_volume = (
        df_volume.groupby("Year")["Volume (Ton)"]
        .sum()
        .reset_index()
    )

    fig_yearly_volume = px.bar(
        df_yearly_volume,
        x="Year",
        y="Volume (Ton)",
        title="📦 Volume Trend"
    )

    fig_yearly_volume.update_layout(
        template="plotly_white",
        height=200,
        plot_bgcolor="#FAF6EE",
        paper_bgcolor="#FAF6EE",
        yaxis=dict(showgrid=False),
        xaxis=dict(type="category"),
        title_x=0.15,
        margin=dict(t=40, b=5, l=0, r=0)
    )
    fig_yearly_volume.update_traces(
        marker_color="#0F172A"
    )
    st.plotly_chart(
        fig_yearly_volume,
        use_container_width=True,
        config={"displayModeBar": False}
    )
# 📅 3. Monthly Price Seasonality
with col3:
    df_season = filtered_df.copy()
    df_season["Trade Date"] = pd.to_datetime(
        df_season["Trade Date"],
        errors="coerce"
    )
    df_season["Month_Name"] = (
        df_season["Trade Date"]
        .dt.month_name()
    )
    month_order = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]
    monthly_pattern = (
        df_season.groupby("Month_Name")["Closing Price"]
        .mean()
        .reset_index()
    )
    monthly_pattern["Month_Name"] = pd.Categorical(
        monthly_pattern["Month_Name"],
        categories=month_order,
        ordered=True
    )
    monthly_pattern = monthly_pattern.sort_values(
        "Month_Name"
    )
    fig_seasonality = px.line(
        monthly_pattern,
        x="Month_Name",
        y="Closing Price",
        markers=True,
        title="📅 Seasonality"
    )

    fig_seasonality.update_traces(
        line=dict(
            color="#2C1D11",
            width=2
        )
    )

    fig_seasonality.update_layout(
        template="plotly_white",
        height=200,
        plot_bgcolor="#F5F1E8",
        paper_bgcolor="#F5F1E8",
        yaxis=dict(showgrid=False),
        title_x=0.15,
        margin=dict(t=40, b=5, l=0, r=0)
    )

    st.plotly_chart(
        fig_seasonality,
        use_container_width=True,
        config={"displayModeBar": False}
    )
# 📊 4. Price Volatility by Coffee Symbol
# GRAPH 8: TOP 5 GAINERS (HORIZONTAL BAR CHART - DARK BROWN)
with col4:  # 4th column in Row 2
    df_gainer = filtered_df.copy()

    if "Percentage Change (%)" not in df_gainer.columns:
        df_gainer["Percentage Change (%)"] = (
            (df_gainer["Closing Price"] - df_gainer["Opening Price"]) / df_gainer["Opening Price"]
        ) * 100

    # 1. Select Top 5 Symbols by average percentage growth
    top_gainers_df = (
        df_gainer.groupby("Symbol")["Percentage Change (%)"]
        .mean()
        .reset_index()
        .sort_values("Percentage Change (%)", ascending=True)  # Horizontal chart requires ascending order for pr
        .tail(5)  # Top 5
    )

    # 2. Build Horizontal Bar Chart
    fig_gainers = px.bar(
        top_gainers_df,
        x="Percentage Change (%)",
        y="Symbol",
        orientation="h",
        title="🚀 Top 5 Gainers (%)"
    )

    # Dark Brown color adjustment
    fig_gainers.update_traces(
        marker_color="#4A2E19",  # Rich Dark Brown / Coffee tone
        texttemplate="%{x:.2f}%",  # በ Bar አሞሌዎች ላይ ፐርሰንቱን ያሳያል
        textposition="outside"
    )

    fig_gainers.update_layout(
        template="plotly_white",
        height=200,
        plot_bgcolor="#F5F1E8",
        paper_bgcolor="#F5F1E8",
        yaxis=dict(showgrid=False),
        xaxis=dict(showgrid=True, gridcolor="#E2E8F0"),
        title_x=0.15,
        margin=dict(t=40, b=10, l=0, r=30)
    )

    st.plotly_chart(
        fig_gainers,
        use_container_width=True,
        config={"displayModeBar": False}
    )
# SIMPLE TIME SERIES FORECASTING (NEXT 3 MONTHS

st.markdown("""
<div style="
    background-color: #4A2C11;
    color:white;
    font-size:15px;
    font-weight:700;
    padding:8px 12px;
    border-radius:8px;
    text-align:center;
    margin-top:0px;
    margin-bottom:15px;
">
☕ 3-Year Price Forecast Model
</div>
""", unsafe_allow_html=True)
# ==============================
# Coffee Price Trend --- 3-Year Forecast
# ==============================

forecast_data = filtered_df.copy()

forecast_data["Trade Date"] = pd.to_datetime(
    forecast_data["Trade Date"],
    errors="coerce"
)

forecast_data = forecast_data.dropna(
    subset=["Trade Date", "Closing Price"]
)

if not forecast_data.empty:

    monthly_price = (
        forecast_data
        .groupby(
            forecast_data["Trade Date"].dt.to_period("M")
        )["Closing Price"]
        .mean()
        .reset_index()
    )

    monthly_price["Trade Date"] = (
        monthly_price["Trade Date"]
        .dt.to_timestamp()
    )

    monthly_price = (
        monthly_price
        .sort_values("Trade Date")
        .reset_index(drop=True)
    )

    forecast_df = pd.DataFrame()

    if len(monthly_price) >= 6:

        last_date = monthly_price["Trade Date"].iloc[-1]

        last_price = monthly_price["Closing Price"].iloc[-1]

        # Generate Next 3 Years (36 Months)

        future_dates = [
            last_date + pd.DateOffset(months=i)
            for i in range(1, 37)
        ]

        recent_trend = (
            monthly_price["Closing Price"].iloc[-1]
            - monthly_price["Closing Price"].iloc[-6]
        ) / 5

        forecast_prices = [
            last_price + (recent_trend * i)
            for i in range(1, 37)
        ]

        forecast_df = pd.DataFrame({
            "Trade Date": future_dates,
            "Closing Price": forecast_prices
        })

        fig_trend = go.Figure()

        # Historical Price

        fig_trend.add_trace(
            go.Scatter(
                x=monthly_price["Trade Date"],
                y=monthly_price["Closing Price"],
                mode="lines",
                name="Historical Price",
                line=dict(
                    color="#4A2C11",
                    width=2
                )
            )
        )

        # Forecast Price

        if not forecast_df.empty:

            forecast_x = pd.concat(
                [
                    monthly_price[
                        ["Trade Date"]
                    ].tail(1),

                    forecast_df[
                        ["Trade Date"]
                    ]
                ],
                ignore_index=True
            )["Trade Date"]

            forecast_y = pd.concat(
                [
                    monthly_price[
                        ["Closing Price"]
                    ].tail(1),

                    forecast_df[
                        ["Closing Price"]
                    ]
                ],
                ignore_index=True
            )["Closing Price"]

            fig_trend.add_trace(
                go.Scatter(
                    x=forecast_x,
                    y=forecast_y,
                    mode="lines+markers",
                    name="3-Year Forecast",
                    line=dict(
                        color="#E67E22",
                        width=2,
                        dash="dot"
                    )
                )
            )

        fig_trend.update_layout(

            title="📈 Coffee Price Trend --- 3-Year Forecast",

            margin=dict(
                l=10,
                r=10,
                t=40,
                b=10
            ),

            height=280,

            xaxis_title="Date",

            yaxis_title="Average Closing Price",

            hovermode="x unified",

            template="plotly_white",

            plot_bgcolor="#F5F1E8",

            paper_bgcolor="#F5F1E8",

            yaxis=dict(
                showgrid=False
            )
        )

        st.plotly_chart(
            fig_trend,
            width="stretch",
            config={
                "displayModeBar": False
            }
        )

    else:

        st.info(
            "At least 6 months of historical data is required "
            "for the 3-year forecast."
        )

else:

    st.info(
        "No sufficient time-series data was found "
        "for the selected filters."
    )
    
# EXECUTIVE SUMMARY

with st.expander("📌 Executive Summary", expanded=False):

    summary_text = f"""
    The Ethiopian coffee market recorded a total trading volume of
    {total_volume:,.0f} tons.

    {top_symbol} was the most actively traded coffee symbol, while
    {top_warehouse} handled the highest trading volume.

    The highest average coffee price was observed in {best_price_year}.

    Overall market movement shows a {trend.lower()} trend.

    Market activity peaked in {peak_month}, and
    {gain_ratio:.1f}% of trading days recorded positive price changes.

    Based on the selected filters, the market demonstrates
    strong trading performance.
    """

    st.write(summary_text)
    
# DATASET PREVIEW
with st.expander("📋 Dataset Preview", expanded=False):

    st.markdown(
        """
        <div style="
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 10px;
        ">
            Preview of the filtered dataset
        </div>
        """,
        unsafe_allow_html=True
    )

    st.dataframe(
        filtered_df,
        hide_index=True,
        width="stretch",
        height=300
    )

# 📥 DOWNLOAD FILTERED DATASET
# Encode as UTF-8 to support different characters
csv = filtered_df.to_csv(    # Convert filtered DataFrame into CSV format
    index=False
).encode("utf-8")
# Create download button for users
# Allows users to export filtered coffee market data
st.download_button(
    label="📥 Download Filtered Dataset",
    data=csv,
    file_name="filtered_coffee_data.csv",
    key="download_filtered_data",
)

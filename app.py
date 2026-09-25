import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

from database import get_market_summary, get_mortgage_schedule


# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent
POSTER_PATH = BASE_DIR / "assets" / "carney_poster.png"


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="MapleMetrics",
    page_icon="🍁",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# PREMIUM DESIGN
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at 80% 0%,
                rgba(190, 30, 45, 0.13),
                transparent 28%
            ),
            linear-gradient(
                180deg,
                #080c12 0%,
                #0c1118 45%,
                #090d13 100%
            );
        color: #f5f7fa;
    }

    .block-container {
        max-width: 1550px;
        padding-top: 1.6rem;
        padding-bottom: 4rem;
    }

    [data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #080d13 0%,
                #0b1119 100%
            );
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    h1 {
        font-size: 3.4rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.045em !important;
        margin-bottom: 0.15rem !important;
    }

    h2 {
        letter-spacing: -0.025em;
        font-weight: 750 !important;
    }

    h3 {
        letter-spacing: -0.015em;
        font-weight: 700 !important;
    }

    .hero-eyebrow {
        text-transform: uppercase;
        letter-spacing: 0.17em;
        color: #ef4655;
        font-size: 0.76rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }

    .hero-copy {
        color: #aeb8c5;
        font-size: 1rem;
        line-height: 1.65;
        max-width: 900px;
        margin-bottom: 1.6rem;
    }

    .section-note {
        color: #929eac;
        font-size: 0.90rem;
        margin-top: -0.35rem;
        margin-bottom: 1rem;
    }

    .poster-label {
        text-transform: uppercase;
        letter-spacing: 0.14em;
        color: #ef4655;
        font-weight: 700;
        font-size: 0.72rem;
        margin-bottom: 0.55rem;
    }

    [data-testid="stMetric"] {
        background:
            linear-gradient(
                145deg,
                rgba(255,255,255,0.055),
                rgba(255,255,255,0.022)
            );
        border: 1px solid rgba(255,255,255,0.09);
        border-radius: 18px;
        padding: 18px 20px;
        min-height: 125px;
    }

    [data-testid="stMetric"]:hover {
        border-color: rgba(239,70,85,0.42);
    }

    [data-testid="stMetricLabel"] {
        color: #9ea8b5;
        font-size: 0.76rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    [data-testid="stMetricValue"] {
        font-size: 1.95rem;
        font-weight: 760;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        overflow: hidden;
    }

    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {
        background-color: #111822 !important;
        border-color: rgba(255,255,255,0.10) !important;
    }

    hr {
        border: none;
        border-top: 1px solid rgba(255,255,255,0.075);
        margin-top: 2rem;
        margin-bottom: 2rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# LOAD MARKET DATA
# =========================================================

df = get_market_summary()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown("# 🍁 MapleMetrics")
st.sidebar.caption("Canadian Real Estate Intelligence")

st.sidebar.divider()

st.sidebar.markdown("### Market Filters")

province_options = ["All"] + sorted(
    df["province"].unique().tolist()
)

selected_province = st.sidebar.selectbox(
    "Province",
    province_options
)

filtered_df = df.copy()

if selected_province != "All":
    filtered_df = filtered_df[
        filtered_df["province"] == selected_province
    ]


city_options = ["All"] + sorted(
    filtered_df["city"].unique().tolist()
)

selected_city = st.sidebar.selectbox(
    "City",
    city_options
)

if selected_city != "All":
    filtered_df = filtered_df[
        filtered_df["city"] == selected_city
    ]


st.sidebar.divider()

st.sidebar.caption(
    "Python • SQL • SQLite • Pandas • Plotly • Streamlit"
)


# =========================================================
# TOP SEARCH / PERIOD
# =========================================================

search_col, period_col = st.columns([4, 1])

with search_col:
    search_term = st.text_input(
        "Search",
        placeholder="Search cities, provinces, or markets...",
        label_visibility="collapsed"
    )

with period_col:
    selected_period = st.selectbox(
        "Period",
        ["Aug 2026"],
        label_visibility="collapsed"
    )


if search_term:
    search_mask = (
        filtered_df["city"].str.contains(
            search_term,
            case=False,
            na=False
        )
        |
        filtered_df["province"].str.contains(
            search_term,
            case=False,
            na=False
        )
        |
        filtered_df["property_type"].str.contains(
            search_term,
            case=False,
            na=False
        )
    )

    filtered_df = filtered_df[search_mask]


# =========================================================
# HERO
# =========================================================

st.markdown(
    '<div class="hero-eyebrow">Canadian Housing Intelligence</div>',
    unsafe_allow_html=True
)

st.title("🍁 MapleMetrics")

st.markdown(
    """
    <div class="hero-copy">
        Premium Canadian real-estate analytics powered by SQL,
        Python, financial modelling and recursive database logic.
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# MARKET OVERVIEW
# =========================================================

if not filtered_df.empty:

    highest_price_row = filtered_df.loc[
        filtered_df["price"].idxmax()
    ]

    highest_sales_row = filtered_df.loc[
        filtered_df["sales"].idxmax()
    ]

    average_price = filtered_df["price"].mean()
    average_yoy = filtered_df["yoy_change"].mean()


    # -----------------------------------------------------
    # KPI CARDS
    # -----------------------------------------------------

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    with kpi1:
        st.metric(
            "Highest Market Price",
            f"${highest_price_row['price']:,.0f}",
            highest_price_row["city"]
        )

    with kpi2:
        st.metric(
            "Highest Sales Volume",
            f"{highest_sales_row['sales']:,.0f}",
            highest_sales_row["city"]
        )

    with kpi3:
        st.metric(
            "Average Market Price",
            f"${average_price:,.0f}"
        )

    with kpi4:
        st.metric(
            "Average YoY Change",
            f"{average_yoy:.1f}%"
        )


    st.divider()


    # =====================================================
    # MARKET CHARTS + POSTER
    # =====================================================

    market_area, poster_area = st.columns(
        [3.1, 1.05],
        gap="large"
    )


    # -----------------------------------------------------
    # LEFT MARKET ANALYTICS
    # -----------------------------------------------------

    with market_area:

        chart_left, chart_right = st.columns(
            [1.55, 1]
        )

        with chart_left:

            st.subheader(
                "Market Price Comparison"
            )

            st.markdown(
                '<div class="section-note">'
                'Composite market price by major Canadian city'
                '</div>',
                unsafe_allow_html=True
            )

            price_chart = px.bar(
                filtered_df,
                x="city",
                y="price",
                text="price",
                labels={
                    "city": "",
                    "price": "Market Price"
                }
            )

            price_chart.update_traces(
                texttemplate="$%{text:,.0f}",
                textposition="outside",
                marker_line_width=0
            )

            price_chart.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(
                    l=10,
                    r=10,
                    t=15,
                    b=10
                ),
                showlegend=False,
                yaxis=dict(
                    tickprefix="$",
                    tickformat=",",
                    gridcolor="rgba(255,255,255,0.06)"
                ),
                xaxis=dict(
                    gridcolor="rgba(0,0,0,0)"
                )
            )

            st.plotly_chart(
                price_chart,
                use_container_width=True
            )


        with chart_right:

            st.subheader(
                "Sales Volume"
            )

            st.markdown(
                '<div class="section-note">'
                'Properties sold by market'
                '</div>',
                unsafe_allow_html=True
            )

            sales_chart = px.bar(
                filtered_df,
                x="city",
                y="sales",
                text="sales",
                labels={
                    "city": "",
                    "sales": "Sales"
                }
            )

            sales_chart.update_traces(
                texttemplate="%{text:,.0f}",
                textposition="outside",
                marker_line_width=0
            )

            sales_chart.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(
                    l=10,
                    r=10,
                    t=15,
                    b=10
                ),
                showlegend=False,
                yaxis=dict(
                    tickformat=",",
                    gridcolor="rgba(255,255,255,0.06)"
                ),
                xaxis=dict(
                    gridcolor="rgba(0,0,0,0)"
                )
            )

            st.plotly_chart(
                sales_chart,
                use_container_width=True
            )


        # -------------------------------------------------
        # MARKET TABLE
        # -------------------------------------------------

        st.subheader("Latest Market Data")

        st.markdown(
            '<div class="section-note">'
            'Canadian housing market data — latest available period'
            '</div>',
            unsafe_allow_html=True
        )

        market_display = filtered_df.rename(
            columns={
                "city": "City",
                "province": "Province",
                "period": "Period",
                "property_type": "Market Segment",
                "price": "Price (CAD)",
                "yoy_change": "YoY Change",
                "sales": "Sales"
            }
        )

        st.dataframe(
            market_display.style.format(
                {
                    "Price (CAD)": "${:,.0f}",
                    "YoY Change": "{:.1f}%",
                    "Sales": "{:,.0f}"
                }
            ),
            width="stretch",
            hide_index=True
        )


    # -----------------------------------------------------
    # RIGHT POSTER
    # -----------------------------------------------------

    with poster_area:

        st.markdown(
            '<div class="poster-label">'
            'Canadian Market Mood'
            '</div>',
            unsafe_allow_html=True
        )

        if POSTER_PATH.exists():

            st.image(
                str(POSTER_PATH),
                use_container_width=True
            )

        else:

            st.info(
                "Add the generated poster as "
                "assets/carney_poster.png"
            )


else:

    st.warning(
        "No market data found for the selected filters."
    )


# =========================================================
# MORTGAGE LAB
# =========================================================

st.divider()

st.markdown("## 🏠 Mortgage Lab")

st.markdown(
    """
    <div class="section-note">
        Model a Canadian mortgage scenario and generate a
        full amortization schedule using recursive SQL.
    </div>
    """,
    unsafe_allow_html=True
)


input_left, input_right = st.columns(2)


with input_left:

    home_price = st.number_input(
        "Home Price (CAD)",
        min_value=100000,
        max_value=5000000,
        value=900000,
        step=25000
    )

    down_payment_pct = st.slider(
        "Down Payment",
        min_value=5,
        max_value=50,
        value=20,
        format="%d%%"
    )


with input_right:

    interest_rate = st.slider(
        "Mortgage Rate",
        min_value=1.0,
        max_value=10.0,
        value=4.5,
        step=0.1,
        format="%.1f%%"
    )

    amortization_years = st.selectbox(
        "Amortization",
        [15, 20, 25, 30],
        index=2
    )


# =========================================================
# MORTGAGE CALCULATIONS
# =========================================================

down_payment = (
    home_price
    * down_payment_pct
    / 100
)

principal = (
    home_price
    - down_payment
)

monthly_rate = (
    interest_rate
    / 100
    / 12
)

months = (
    amortization_years
    * 12
)

payment = (
    principal
    * monthly_rate
    * (1 + monthly_rate) ** months
    / (
        (1 + monthly_rate) ** months
        - 1
    )
)


# =========================================================
# RECURSIVE SQL SCHEDULE
# =========================================================

schedule = get_mortgage_schedule(
    principal=principal,
    payment=payment,
    annual_rate=interest_rate / 100,
    months=months
)


total_interest = schedule["interest"].sum()

total_paid = schedule["payment"].sum()


# =========================================================
# MORTGAGE KPI CARDS
# =========================================================

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric(
        "Down Payment",
        f"${down_payment:,.0f}"
    )

with m2:
    st.metric(
        "Mortgage Principal",
        f"${principal:,.0f}"
    )

with m3:
    st.metric(
        "Monthly Payment",
        f"${payment:,.2f}"
    )

with m4:
    st.metric(
        "Total Interest",
        f"${total_interest:,.0f}"
    )


st.divider()


# =========================================================
# MORTGAGE CHARTS
# =========================================================

balance_col, financing_col = st.columns(
    [1.65, 1]
)


with balance_col:

    st.subheader(
        "Mortgage Balance Over Time"
    )

    mortgage_chart = go.Figure()

    mortgage_chart.add_trace(
        go.Scatter(
            x=schedule["month"],
            y=schedule["closing_balance"],
            mode="lines",
            name="Closing Balance",
            fill="tozeroy"
        )
    )

    mortgage_chart.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(
            l=10,
            r=10,
            t=20,
            b=10
        ),
        yaxis=dict(
            tickprefix="$",
            tickformat=",",
            gridcolor="rgba(255,255,255,0.06)"
        ),
        xaxis=dict(
            title="Month",
            gridcolor="rgba(255,255,255,0.03)"
        ),
        showlegend=False
    )

    st.plotly_chart(
        mortgage_chart,
        use_container_width=True
    )


with financing_col:

    st.subheader(
        "Financing Mix"
    )

    financing_chart = go.Figure(
        data=[
            go.Pie(
                labels=[
                    "Principal",
                    "Interest"
                ],
                values=[
                    principal,
                    total_interest
                ],
                hole=0.70
            )
        ]
    )

    financing_chart.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(
            l=10,
            r=10,
            t=20,
            b=10
        )
    )

    st.plotly_chart(
        financing_chart,
        use_container_width=True
    )


# =========================================================
# MORTGAGE SUMMARY
# =========================================================

st.subheader("Financing Summary")

summary1, summary2 = st.columns(2)

with summary1:
    st.metric(
        "Total Mortgage Payments",
        f"${total_paid:,.0f}"
    )

with summary2:
    st.metric(
        "Total Financing Cost",
        f"${principal + total_interest:,.0f}"
    )


# =========================================================
# AMORTIZATION TABLE
# =========================================================

st.divider()

st.subheader(
    "Amortization Schedule"
)

st.markdown(
    """
    <div class="section-note">
        Month-by-month recursive SQL mortgage calculation.
    </div>
    """,
    unsafe_allow_html=True
)


schedule_display = schedule.rename(
    columns={
        "month": "Month",
        "opening_balance": "Opening Balance",
        "payment": "Payment",
        "interest": "Interest",
        "principal_paid": "Principal Paid",
        "closing_balance": "Closing Balance"
    }
)


st.dataframe(
    schedule_display.style.format(
        {
            "Opening Balance": "${:,.2f}",
            "Payment": "${:,.2f}",
            "Interest": "${:,.2f}",
            "Principal Paid": "${:,.2f}",
            "Closing Balance": "${:,.2f}"
        }
    ),
    width="stretch",
    hide_index=True
)


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "MapleMetrics • Canadian Real Estate Analytics • "
    "Built with Python, SQL, SQLite, Pandas, Plotly and Streamlit"
)
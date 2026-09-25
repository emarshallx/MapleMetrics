import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from pathlib import Path
from PIL import Image

from database import get_market_summary, get_mortgage_schedule


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
POSTER_PATH = BASE_DIR / "assets" / "carney_poster.png"


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="MapleMetrics",
    page_icon="🍁",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# GLOBAL CSS
# ============================================================

st.html(
    """
    <style>

    html, body, [class*="css"] {
        font-family:
            Inter,
            -apple-system,
            BlinkMacSystemFont,
            "Segoe UI",
            sans-serif;
    }

    .stApp {
        background:
            radial-gradient(
                circle at 82% 5%,
                rgba(180, 20, 42, 0.16),
                transparent 25%
            ),
            linear-gradient(
                135deg,
                #071019 0%,
                #0b1119 45%,
                #090c12 100%
            );
        color: #f8fafc;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stSidebar"] {
        display: none;
    }

    .block-container {
        max-width: 1750px;
        padding-top: 0.8rem;
        padding-left: 1rem;
        padding-right: 1rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 {
        color: #f8fafc;
    }

    .nav-shell {
        min-height: 890px;
        background:
            linear-gradient(
                180deg,
                rgba(8, 16, 25, 0.98),
                rgba(5, 12, 19, 0.98)
            );
        border:
            1px solid rgba(255,255,255,0.07);
        border-radius: 18px;
        padding: 20px 14px;
        box-shadow:
            0 22px 60px rgba(0,0,0,0.35);
    }

    .brand {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 1.35rem;
        font-weight: 800;
        margin-bottom: 24px;
    }

    .brand-leaf {
        color: #ef3340;
        font-size: 1.8rem;
    }

    .nav-item {
        padding: 11px 13px;
        margin-bottom: 6px;
        border-radius: 9px;
        color: #aeb8c5;
        font-size: 0.9rem;
    }

    .nav-active {
        padding: 11px 13px;
        margin-bottom: 6px;
        border-radius: 9px;
        background:
            linear-gradient(
                90deg,
                rgba(225,36,53,0.40),
                rgba(120,18,29,0.18)
            );
        border-left:
            3px solid #ff4054;
        color: white;
        font-size: 0.9rem;
        font-weight: 650;
    }

    .nav-divider {
        border-top:
            1px solid rgba(255,255,255,0.08);
        margin: 18px 0;
    }

    .nav-bottom {
        margin-top: 230px;
        color: #7f8997;
        text-transform: uppercase;
        letter-spacing: 0.26em;
        line-height: 1.8;
        font-size: 0.68rem;
    }

    .hero {
        border-radius: 18px;
        padding: 20px 24px 22px 24px;
        margin-bottom: 14px;
        border:
            1px solid rgba(255,255,255,0.07);
        background:
            radial-gradient(
                circle at 80% 10%,
                rgba(230,40,55,0.24),
                transparent 31%
            ),
            linear-gradient(
                115deg,
                #101823 0%,
                #121823 55%,
                #2a1017 100%
            );
        box-shadow:
            0 20px 60px rgba(0,0,0,0.30);
    }

    .hero-kicker {
        color: #ef4655;
        text-transform: uppercase;
        letter-spacing: 0.18em;
        font-size: 0.70rem;
        font-weight: 700;
    }

    .hero-title {
        font-family:
            Georgia,
            "Times New Roman",
            serif;
        font-size: 3.2rem;
        font-weight: 800;
        line-height: 1;
        margin: 5px 0 6px 0;
    }

    .hero-title-white {
        color: white;
    }

    .hero-title-red {
        color: #ef3340;
    }

    .hero-subtitle {
        font-family:
            Georgia,
            "Times New Roman",
            serif;
        color: #f2f4f7;
        font-size: 1.35rem;
        font-weight: 650;
        margin-bottom: 5px;
    }

    .hero-description {
        color: #abb4c0;
        font-size: 0.92rem;
    }

    [data-testid="stMetric"] {
        min-height: 121px;
        padding: 16px 16px;
        background:
            linear-gradient(
                145deg,
                rgba(18,28,39,0.96),
                rgba(11,18,27,0.96)
            );
        border:
            1px solid rgba(255,255,255,0.08);
        border-radius: 14px;
        box-shadow:
            inset 0 1px 0 rgba(255,255,255,0.025),
            0 12px 35px rgba(0,0,0,0.20);
    }

    [data-testid="stMetricLabel"] {
        color: #9da7b5;
        font-size: 0.75rem;
        font-weight: 650;
        letter-spacing: 0.02em;
    }

    [data-testid="stMetricValue"] {
        color: white;
        font-size: 1.65rem;
        font-weight: 800;
    }

    [data-testid="stMetricDelta"] {
        font-weight: 650;
    }

    .panel-title {
        font-size: 1.0rem;
        font-weight: 750;
        color: white;
    }

    .panel-subtitle {
        color: #8d98a7;
        font-size: 0.74rem;
        margin-bottom: 4px;
    }

    .poster-label {
        color: #ef4655;
        text-transform: uppercase;
        font-size: 0.67rem;
        font-weight: 750;
        letter-spacing: 0.14em;
        margin-bottom: 7px;
    }

    div[data-testid="stDataFrame"] {
        border:
            1px solid rgba(255,255,255,0.08);
        border-radius: 12px;
        overflow: hidden;
    }

    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {
        background: #101821 !important;
        border-color:
            rgba(255,255,255,0.10) !important;
    }

    [data-testid="stNumberInput"] input {
        background:
            #101821 !important;
    }

    .stButton button {
        width: 100%;
        background:
            linear-gradient(
                90deg,
                #c71f30,
                #ef3340
            );
        border:
            1px solid #f24a57;
        color:
            white;
        border-radius:
            9px;
        font-weight:
            750;
    }

    .stButton button:hover {
        color: white;
        border-color: #ff7a84;
    }

    hr {
        border: none;
        border-top:
            1px solid rgba(255,255,255,0.08);
    }

    </style>
    """
)


# ============================================================
# LOAD DATA
# ============================================================

df = get_market_summary()


# ============================================================
# THREE-COLUMN SHELL
# ============================================================

nav_col, main_col, right_col = st.columns(
    [0.82, 3.65, 1.55],
    gap="medium",
)


# ============================================================
# LEFT NAVIGATION
# ============================================================

with nav_col:

    st.html(
        """
        <div class="nav-shell">

            <div class="brand">
                <span class="brand-leaf">🍁</span>
                <span>MapleMetrics</span>
            </div>

            <div class="nav-active">
                ▰ &nbsp;&nbsp;Dashboard
            </div>

            <div class="nav-item">
                ⌂ &nbsp;&nbsp;Housing Market
            </div>

            <div class="nav-item">
                ↗ &nbsp;&nbsp;Market Trends
            </div>

            <div class="nav-item">
                ⌖ &nbsp;&nbsp;Cities & Provinces
            </div>

            <div class="nav-item">
                ▦ &nbsp;&nbsp;Property Types
            </div>

            <div class="nav-item">
                ▣ &nbsp;&nbsp;Mortgage Lab
            </div>

            <div class="nav-item">
                ◉ &nbsp;&nbsp;Data Explorer
            </div>

            <div class="nav-divider"></div>

            <div class="nav-item">
                ▤ &nbsp;&nbsp;Saved Reports
            </div>

            <div class="nav-item">
                ⚙ &nbsp;&nbsp;Settings
            </div>

            <div class="nav-bottom">
                DATA<br>
                INSIGHTS<br>
                A STRONGER<br>
                CANADA
            </div>

        </div>
        """
    )


# ============================================================
# MAIN COLUMN
# ============================================================

with main_col:

    search_col, date_col = st.columns(
        [4, 1],
        gap="small",
    )

    with search_col:

        search_text = st.text_input(
            "Search",
            placeholder="🔍 Search cities, provinces, or markets...",
            label_visibility="collapsed",
        )

    with date_col:

        st.selectbox(
            "Period",
            ["Aug 2026"],
            label_visibility="collapsed",
        )


    filtered_df = df.copy()

    if search_text:

        search_mask = (
            filtered_df["city"].str.contains(
                search_text,
                case=False,
                na=False,
            )
            |
            filtered_df["province"].str.contains(
                search_text,
                case=False,
                na=False,
            )
            |
            filtered_df["property_type"].str.contains(
                search_text,
                case=False,
                na=False,
            )
        )

        filtered_df = filtered_df[
            search_mask
        ]


    # ========================================================
    # HERO
    # ========================================================

    st.html(
        """
        <div class="hero">

            <div class="hero-kicker">
                Canadian Housing Intelligence
            </div>

            <div class="hero-title">
                <span class="hero-title-white">Maple</span><span class="hero-title-red">Metrics</span>
            </div>

            <div class="hero-subtitle">
                Canadian Real Estate Market Analytics
            </div>

            <div class="hero-description">
                Data-driven insights for a stronger housing market.
            </div>

        </div>
        """
    )


    # ========================================================
    # KPIs + CHARTS + TABLE
    # ========================================================

    if not filtered_df.empty:

        highest_price = filtered_df.loc[
            filtered_df["price"].idxmax()
        ]

        highest_sales = filtered_df.loc[
            filtered_df["sales"].idxmax()
        ]

        average_price = filtered_df["price"].mean()
        average_yoy = filtered_df["yoy_change"].mean()


        k1, k2, k3, k4 = st.columns(
            4,
            gap="small",
        )

        with k1:
            st.metric(
                "🏠 Market Price",
                f"${highest_price['price']:,.0f}",
                f"{highest_price['yoy_change']:.1f}% YoY",
            )

        with k2:
            st.metric(
                "▥ Sales Volume",
                f"{highest_sales['sales']:,.0f}",
                highest_sales["city"],
            )

        with k3:
            st.metric(
                "◆ Average Price",
                f"${average_price:,.0f}",
                "Selected markets",
            )

        with k4:
            st.metric(
                "% Average YoY Change",
                f"{average_yoy:.1f}%",
            )


        st.write("")


        price_panel, sales_panel = st.columns(
            [1.6, 1],
            gap="medium",
        )


        with price_panel:

            st.html(
                """
                <div class="panel-title">
                    🏠 Average Home Price by Major City
                </div>

                <div class="panel-subtitle">
                    Composite benchmark price (CAD)
                </div>
                """
            )

            price_fig = px.line(
                filtered_df,
                x="city",
                y="price",
                markers=True,
            )

            price_fig.update_traces(
                line=dict(
                    width=3,
                    color="#ef3340",
                ),
                marker=dict(
                    size=8,
                    color="#ff6a75",
                ),
            )

            price_fig.update_layout(
                template="plotly_dark",
                height=290,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(
                    l=8,
                    r=8,
                    t=12,
                    b=5,
                ),
                showlegend=False,
                yaxis=dict(
                    tickprefix="$",
                    tickformat=",",
                    gridcolor="rgba(255,255,255,0.06)",
                ),
                xaxis=dict(
                    gridcolor="rgba(255,255,255,0.03)",
                ),
            )

            st.plotly_chart(
                price_fig,
                use_container_width=True,
            )


        with sales_panel:

            st.html(
                """
                <div class="panel-title">
                    ▥ Sales Volume by City
                </div>

                <div class="panel-subtitle">
                    Number of properties sold
                </div>
                """
            )

            sales_fig = px.bar(
                filtered_df,
                x="city",
                y="sales",
                text="sales",
            )

            sales_fig.update_traces(
                texttemplate="%{text:,.0f}",
                textposition="outside",
                marker_color="#ef3340",
            )

            sales_fig.update_layout(
                template="plotly_dark",
                height=290,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(
                    l=8,
                    r=8,
                    t=12,
                    b=5,
                ),
                showlegend=False,
                yaxis=dict(
                    tickformat=",",
                    gridcolor="rgba(255,255,255,0.06)",
                ),
                xaxis=dict(
                    gridcolor="rgba(0,0,0,0)",
                ),
            )

            st.plotly_chart(
                sales_fig,
                use_container_width=True,
            )


        st.html(
            """
            <div class="panel-title">
                ◉ Latest Market Data
            </div>

            <div class="panel-subtitle">
                Canadian housing market data — latest available period
            </div>
            """
        )


        display_df = filtered_df.rename(
            columns={
                "city": "City",
                "province": "Province",
                "period": "Period",
                "property_type": "Property Type",
                "price": "Price (CAD)",
                "yoy_change": "YoY Change",
                "sales": "Sales",
            }
        )


        st.dataframe(
            display_df.style.format(
                {
                    "Price (CAD)": "${:,.0f}",
                    "YoY Change": "{:.1f}%",
                    "Sales": "{:,.0f}",
                }
            ),
            width="stretch",
            hide_index=True,
            height=240,
        )

    else:

        st.warning(
            "No market data matches your search."
        )


# ============================================================
# RIGHT COLUMN
# ============================================================

with right_col:

    st.html(
        """
        <div class="poster-label">
            Canadian Market Mood
        </div>
        """
    )


    if POSTER_PATH.exists():

        try:

            poster = Image.open(
                POSTER_PATH
            )

            st.image(
                poster,
                use_container_width=True,
            )

        except Exception:

            st.error(
                "The poster file exists but is not a valid image. "
                "Replace assets/carney_poster.png with the actual PNG."
            )

    else:

        st.info(
            "Add assets/carney_poster.png"
        )


    st.markdown(
        "### 🧮 Mortgage Lab"
    )

    st.caption(
        "Explore monthly payments and affordability."
    )


    home_price = st.number_input(
        "Home Price (CAD)",
        min_value=100000,
        max_value=5000000,
        value=750000,
        step=25000,
    )


    down_payment_pct = st.slider(
        "Down Payment",
        min_value=5,
        max_value=50,
        value=20,
        format="%d%%",
    )


    interest_rate = st.slider(
        "Mortgage Rate",
        min_value=1.0,
        max_value=10.0,
        value=4.5,
        step=0.1,
        format="%.1f%%",
    )


    amortization_years = st.selectbox(
        "Amortization",
        [15, 20, 25, 30],
        index=2,
    )


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
        /
        (
            (1 + monthly_rate) ** months
            - 1
        )
    )


    schedule = get_mortgage_schedule(
        principal=principal,
        payment=payment,
        annual_rate=interest_rate / 100,
        months=months,
    )


    st.metric(
        "Estimated Monthly Payment",
        f"${payment:,.2f}",
    )


    st.button(
        "Calculate Payment  →"
    )


# ============================================================
# FULL-WIDTH MORTGAGE INTELLIGENCE
# ============================================================

st.write("")
st.divider()

st.markdown(
    "## Mortgage Intelligence"
)

st.caption(
    "Recursive SQL amortization and financing analysis."
)


total_interest = schedule[
    "interest"
].sum()


total_paid = schedule[
    "payment"
].sum()


m1, m2, m3, m4 = st.columns(
    4
)


with m1:

    st.metric(
        "Down Payment",
        f"${down_payment:,.0f}",
    )


with m2:

    st.metric(
        "Mortgage Principal",
        f"${principal:,.0f}",
    )


with m3:

    st.metric(
        "Monthly Payment",
        f"${payment:,.2f}",
    )


with m4:

    st.metric(
        "Total Interest",
        f"${total_interest:,.0f}",
    )


balance_col, financing_col = st.columns(
    [1.7, 1]
)


with balance_col:

    mortgage_fig = go.Figure()

    mortgage_fig.add_trace(
        go.Scatter(
            x=schedule["month"],
            y=schedule["closing_balance"],
            mode="lines",
            fill="tozeroy",
            name="Mortgage Balance",
            line=dict(
                color="#ef3340",
                width=3,
            ),
        )
    )


    mortgage_fig.update_layout(
        template="plotly_dark",
        height=360,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(
            l=10,
            r=10,
            t=35,
            b=10,
        ),
        title="Mortgage Balance Over Time",
        yaxis=dict(
            tickprefix="$",
            tickformat=",",
            gridcolor="rgba(255,255,255,0.06)",
        ),
        xaxis=dict(
            title="Month",
            gridcolor="rgba(255,255,255,0.03)",
        ),
        showlegend=False,
    )


    st.plotly_chart(
        mortgage_fig,
        use_container_width=True,
    )


with financing_col:

    financing_fig = go.Figure(
        data=[
            go.Pie(
                labels=[
                    "Principal",
                    "Interest",
                ],
                values=[
                    principal,
                    total_interest,
                ],
                hole=0.72,
            )
        ]
    )


    financing_fig.update_layout(
        template="plotly_dark",
        height=360,
        title="Financing Mix",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )


    st.plotly_chart(
        financing_fig,
        use_container_width=True,
    )


# ============================================================
# AMORTIZATION TABLE
# ============================================================

st.markdown(
    "### Amortization Schedule"
)


schedule_display = schedule.rename(
    columns={
        "month": "Month",
        "opening_balance": "Opening Balance",
        "payment": "Payment",
        "interest": "Interest",
        "principal_paid": "Principal Paid",
        "closing_balance": "Closing Balance",
    }
)


st.dataframe(
    schedule_display.style.format(
        {
            "Opening Balance": "${:,.2f}",
            "Payment": "${:,.2f}",
            "Interest": "${:,.2f}",
            "Principal Paid": "${:,.2f}",
            "Closing Balance": "${:,.2f}",
        }
    ),
    width="stretch",
    hide_index=True,
)


# ============================================================
# FOOTER
# ============================================================

st.divider()


st.caption(
    "MapleMetrics • Canadian Real Estate Analytics • "
    "Python • SQL • SQLite • Pandas • Plotly • Streamlit"
)
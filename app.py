from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go


# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------

st.set_page_config(
    page_title="European Cost of Living Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

PROJECT_ROOT = Path(__file__).resolve().parent
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "eu27_earnings_affordability_final.csv"

GEO_COL = "geo"

# A single, deliberate palette used everywhere (CSS + matplotlib) so the
# dashboard reads as one designed product instead of default-theme charts
# next to default-theme widgets.
PALETTE = {
    "ink": "#1A1F2B",         # near-black text
    "muted": "#6B7280",       # secondary text / gridlines
    "bg": "#F7F8FA",          # page background
    "card": "#FFFFFF",        # card background
    "border": "#E5E7EB",      # hairlines
    "primary": "#1F4E79",     # deep blue — primary series / accents
    "primary_soft": "#5B84A8",
    "accent": "#C9A227",      # muted gold — reference lines, highlights
    "positive": "#2E7D5B",    # green — gains
    "negative": "#B3462C",    # muted red/rust — losses
    "scenario_100": "#1F4E79",
    "scenario_50": "#C9A227",
}

FONT_STACK = "'Inter', 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif"


# -------------------------------------------------------------------
# Global styling — CSS
# -------------------------------------------------------------------

def inject_css() -> None:
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {{
            font-family: {FONT_STACK};
        }}

        .stApp {{
            background-color: {PALETTE['bg']};
        }}

        /* Hide default Streamlit chrome for a cleaner, less "app-template" feel */
        #MainMenu, footer {{visibility: hidden;}}
        header[data-testid="stHeader"] {{background: transparent;}}

        .block-container {{
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1200px;
        }}

        /* ---------------- Hero header ---------------- */
        .hero {{
            padding: 2rem 2.25rem;
            border-radius: 14px;
            background: linear-gradient(135deg, {PALETTE['primary']} 0%, #16324F 100%);
            color: #FFFFFF;
            margin-bottom: 1.75rem;
        }}
        .hero .eyebrow {{
            text-transform: uppercase;
            letter-spacing: 0.12em;
            font-size: 0.72rem;
            font-weight: 600;
            color: {PALETTE['accent']};
            margin-bottom: 0.5rem;
        }}
        .hero h1 {{
            font-size: 2rem;
            font-weight: 800;
            margin: 0 0 0.6rem 0;
            color: #FFFFFF;
            letter-spacing: -0.02em;
        }}
        .hero p {{
            font-size: 0.98rem;
            line-height: 1.55;
            color: #D7E0EA !important;
            margin: 0;
            max-width: 760px;
        }}
        .hero h1 {{
            color: #FFFFFF !important;
        }}

        /* ---------------- Section headers ---------------- */
        .section-title {{
            font-size: 1.15rem;
            font-weight: 700;
            color: {PALETTE['ink']};
            margin: 0 0 0.15rem 0;
            letter-spacing: -0.01em;
        }}
        .section-subtitle {{
            font-size: 0.87rem;
            color: {PALETTE['muted']};
            margin: 0 0 1rem 0;
        }}

        /* ---------------- KPI cards ---------------- */
        .kpi-card {{
            background: {PALETTE['card']};
            border: 1px solid {PALETTE['border']};
            border-radius: 12px;
            padding: 1.1rem 1.3rem;
            box-shadow: 0 1px 2px rgba(16, 24, 40, 0.04);
            height: 100%;
        }}
        .kpi-label {{
            font-size: 0.76rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: {PALETTE['muted']};
            margin-bottom: 0.35rem;
        }}
        .kpi-value {{
            font-size: 1.65rem;
            font-weight: 800;
            color: {PALETTE['ink']};
            letter-spacing: -0.02em;
            line-height: 1.1;
        }}
        .kpi-sub {{
            font-size: 0.78rem;
            color: {PALETTE['muted']};
            margin-top: 0.3rem;
        }}

        /* ---------------- Chart card wrapper ---------------- */
        .chart-card {{
            background: {PALETTE['card']};
            border: 1px solid {PALETTE['border']};
            border-radius: 12px;
            padding: 1.25rem 1.4rem 0.6rem 1.4rem;
            margin-bottom: 1.4rem;
        }}

        /* ---------------- Sidebar ---------------- */
        section[data-testid="stSidebar"] {{
            background-color: {PALETTE['card']};
            border-right: 1px solid {PALETTE['border']};
        }}
        section[data-testid="stSidebar"] .stMarkdown h2 {{
            color: {PALETTE['ink']};
            font-weight: 600;
        }}

        /* Force readable text on every Streamlit widget, regardless of the
           light/dark theme the app happens to be running under. Streamlit
           renders widget option text inside nested <p>/<span> tags rather
           than directly on the <label>, so we target those explicitly
           instead of relying on inherited color. */
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
        section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
        .stRadio label p,
        .stRadio [data-testid="stMarkdownContainer"] p,
        .stMultiSelect label p,
        .stMultiSelect span,
        .stSelectbox label p,
        [data-testid="stCaptionContainer"],
        [data-testid="stCaptionContainer"] p {{
            color: {PALETTE['ink']} !important;
        }}
        [data-testid="stCaptionContainer"],
        [data-testid="stCaptionContainer"] p {{
            color: {PALETTE['muted']} !important;
        }}

        /* Multiselect chips */
        .stMultiSelect [data-baseweb="tag"] {{
            background-color: {PALETTE['primary']} !important;
        }}
        .stMultiSelect [data-baseweb="tag"] span {{
            color: #FFFFFF !important;
        }}

        /* ---------------- Tabs ---------------- */
        button[data-baseweb="tab"] {{
            font-weight: 600;
            font-size: 0.92rem;
        }}
        button[data-baseweb="tab"] p {{
            color: {PALETTE['muted']} !important;
        }}
        button[data-baseweb="tab"][aria-selected="true"] p {{
            color: {PALETTE['primary']} !important;
        }}
        div[data-baseweb="tab-highlight"] {{
            background-color: {PALETTE['primary']} !important;
        }}

        /* General body / markdown text, in case the surrounding theme is dark */
        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] li {{
            color: {PALETTE['ink']};
        }}

        /* Divider replacement spacing */
        hr {{
            border-color: {PALETTE['border']};
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def kpi_card(label: str, value: str, sub: str = "") -> str:
    sub_html = f'<div class="kpi-sub">{sub}</div>' if sub else ""
    return (
        f'<div class="kpi-card">'
        f'<div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}</div>'
        f"{sub_html}"
        f"</div>"
    )


def section_header(title: str, subtitle: str = "") -> None:
    sub_html = f'<div class="section-subtitle">{subtitle}</div>' if subtitle else ""
    st.markdown(
        f'<div class="section-title">{title}</div>{sub_html}',
        unsafe_allow_html=True,
    )


# -------------------------------------------------------------------
# Matplotlib styling — one shared look for every chart
# -------------------------------------------------------------------

def apply_chart_style(fig, ax) -> None:
    fig.patch.set_facecolor(PALETTE["card"])
    ax.set_facecolor(PALETTE["card"])

    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    for spine in ("left", "bottom"):
        ax.spines[spine].set_color(PALETTE["border"])

    ax.tick_params(colors=PALETTE["muted"], labelsize=9)
    ax.xaxis.label.set_color(PALETTE["ink"])
    ax.yaxis.label.set_color(PALETTE["ink"])
    ax.xaxis.label.set_fontsize(10)
    ax.yaxis.label.set_fontsize(10)

    ax.grid(axis="x", color=PALETTE["border"], linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)

    legend = ax.get_legend()
    if legend is not None:
        legend.get_frame().set_edgecolor(PALETTE["border"])
        legend.get_frame().set_facecolor(PALETTE["card"])
        legend.get_frame().set_linewidth(0.8)


plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["axes.titleweight"] = "bold"
plt.rcParams["axes.titlesize"] = 12
plt.rcParams["axes.edgecolor"] = PALETTE["border"]
plt.rcParams["text.color"] = PALETTE["ink"]


# -------------------------------------------------------------------
# Data loading
# -------------------------------------------------------------------

@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    """Load the final processed dataset."""
    return pd.read_csv(path)


inject_css()

df = load_data(DATA_PATH)


# -------------------------------------------------------------------
# Hero / page header
# -------------------------------------------------------------------

st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">Eurostat · 2025 Edition</div>
        <h1>European Cost of Living &amp; Affordability</h1>
        <p>
            A comparative look at net earnings, price levels and affordability
            across the 27 EU member states, contrasting outcomes at
            <strong>100%</strong> and <strong>50%</strong> of average earnings.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# -------------------------------------------------------------------
# Sidebar filters
# -------------------------------------------------------------------

st.sidebar.markdown("## Filters")

countries = sorted(df[GEO_COL].unique())

selected_countries = st.sidebar.multiselect(
    "Countries",
    options=countries,
    default=countries,
)

scenario = st.sidebar.radio(
    "Earnings scenario",
    options=["100% average earnings", "50% average earnings"],
)

st.sidebar.markdown("---")
st.sidebar.caption(
    "Data: Eurostat. Affordability index is relative to the EU27 average (=100)."
)


# Filter data
filtered_df = df[df[GEO_COL].isin(selected_countries)].copy()

if filtered_df.empty:
    st.warning("Please select at least one country.")
    st.stop()


# Select scenario columns
if scenario == "100% average earnings":
    earnings_col = "net_earnings_eur"
    affordability_col = "affordability_index"
    earnings_index_col = "earnings_index"
    scenario_color = PALETTE["scenario_100"]
else:
    earnings_col = "net_earnings_50_eur"
    affordability_col = "affordability_index_50"
    earnings_index_col = "earnings_index_50"
    scenario_color = PALETTE["scenario_50"]


# -------------------------------------------------------------------
# KPI calculations
# -------------------------------------------------------------------

average_earnings = filtered_df[earnings_col].mean()
average_pli = filtered_df["pli"].mean()
average_affordability = filtered_df[affordability_col].mean()

highest_affordability = filtered_df.loc[filtered_df[affordability_col].idxmax()]
lowest_affordability = filtered_df.loc[filtered_df[affordability_col].idxmin()]


# -------------------------------------------------------------------
# KPI cards
# -------------------------------------------------------------------

section_header("Key indicators", scenario)

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(
        kpi_card("Average net earnings", f"€{average_earnings:,.0f}"),
        unsafe_allow_html=True,
    )
with k2:
    st.markdown(
        kpi_card("Average price level", f"{average_pli:.1f}", "EU27 = 100"),
        unsafe_allow_html=True,
    )
with k3:
    st.markdown(
        kpi_card("Average affordability", f"{average_affordability:.1f}", "EU27 = 100"),
        unsafe_allow_html=True,
    )
with k4:
    st.markdown(
        kpi_card("Countries selected", f"{len(filtered_df)}", f"of {len(df)} total"),
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)


# -------------------------------------------------------------------
# Tabbed chart sections
# -------------------------------------------------------------------

tab_overview, tab_ranking, tab_comparison, tab_details = st.tabs(
    ["Overview", "Affordability ranking", "100% vs 50% comparison", "Country details"]
)


# ---------------- Overview: scatter ----------------
with tab_overview:
    section_header(
        "Price levels vs. net earnings",
        "Each point is a country; the trend line shows the overall relationship.",
    )

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)

    scatter_df = filtered_df.copy()
    fig, ax = plt.subplots(figsize=(10, 6.2))

    ax.scatter(
        scatter_df["pli"],
        scatter_df[earnings_col],
        s=60,
        color=scenario_color,
        edgecolor="white",
        linewidth=0.8,
        zorder=3,
    )

    for _, row in scatter_df.iterrows():
        ax.annotate(
            row[GEO_COL],
            (row["pli"], row[earnings_col]),
            xytext=(5, 5),
            textcoords="offset points",
            fontsize=8,
            color=PALETTE["muted"],
        )

    x = scatter_df["pli"]
    y = scatter_df[earnings_col]

    if len(scatter_df) >= 2:
        slope, intercept = np.polyfit(x, y, 1)
        x_line = np.linspace(x.min(), x.max(), 100)
        y_line = slope * x_line + intercept

        ax.plot(
            x_line,
            y_line,
            color=PALETTE["ink"],
            linewidth=1.6,
            linestyle="-",
            label="Linear trend",
            zorder=2,
        )

    ax.axvline(
        100,
        color=PALETTE["accent"],
        linestyle="--",
        linewidth=1.3,
        label="EU27 PLI = 100",
        zorder=1,
    )

    eu27_earnings = (
        df.loc[df[GEO_COL] == "EU27_2020", earnings_col].iloc[0]
        if "EU27_2020" in df[GEO_COL].values
        else None
    )

    if eu27_earnings is not None:
        ax.axhline(
            eu27_earnings,
            color=PALETTE["primary_soft"],
            linestyle="--",
            linewidth=1.3,
            label=f"EU27 earnings = €{eu27_earnings:,.0f}",
            zorder=1,
        )

    ax.set_xlabel("Price Level Index (EU27 = 100)")
    ax.set_ylabel("Annual net earnings (€)")
    ax.legend(frameon=True, fontsize=8.5, loc="best")

    apply_chart_style(fig, ax)
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)

    if len(scatter_df) >= 2:
        correlation = x.corr(y)
        st.caption(
            f"Pearson correlation: **{correlation:.3f}**  |  R²: **{correlation ** 2:.3f}**"
        )

    st.markdown("</div>", unsafe_allow_html=True)


# ---------------- Affordability ranking ----------------
with tab_ranking:
    section_header(
        f"Affordability index — {scenario}",
        "Hover over a bar to see the exact value.",
    )

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)

    ranking_df = filtered_df.sort_values(affordability_col, ascending=True)

    bar_colors = [
        PALETTE["positive"] if v >= 100 else PALETTE["negative"]
        for v in ranking_df[affordability_col]
    ]

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=ranking_df[affordability_col],
            y=ranking_df["Geopolitical entity (reporting)"],
            orientation="h",
            marker=dict(color=bar_colors, line=dict(width=0)),
            hovertemplate="<b>%{y}</b><br>Affordability index: %{x:.1f}<extra></extra>",
        )
    )

    fig.add_vline(
        x=100,
        line_dash="dash",
        line_color=PALETTE["ink"],
        line_width=1.3,
        annotation_text="EU27 = 100",
        annotation_position="top",
        annotation_font_color=PALETTE["ink"],
        annotation_font_size=11,
    )

    fig.update_layout(
        height=max(420, 26 * len(ranking_df)),
        margin=dict(l=10, r=20, t=10, b=40),
        plot_bgcolor=PALETTE["card"],
        paper_bgcolor=PALETTE["card"],
        font=dict(family=FONT_STACK, color=PALETTE["ink"], size=12),
        xaxis=dict(
            title="Affordability Index",
            gridcolor=PALETTE["border"],
            zeroline=False,
        ),
        yaxis=dict(title="", gridcolor=PALETTE["border"]),
        hoverlabel=dict(
            bgcolor=PALETTE["ink"],
            font_color="#FFFFFF",
            font_size=12,
        ),
        showlegend=False,
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.caption("Green bars indicate above-average affordability; rust bars indicate below-average.")

    st.markdown("</div>", unsafe_allow_html=True)

    hc1, hc2 = st.columns(2)
    with hc1:
        st.markdown(
            kpi_card(
                "Most affordable",
                str(highest_affordability[GEO_COL]),
                f"Index {highest_affordability[affordability_col]:.1f}",
            ),
            unsafe_allow_html=True,
        )
    with hc2:
        st.markdown(
            kpi_card(
                "Least affordable",
                str(lowest_affordability[GEO_COL]),
                f"Index {lowest_affordability[affordability_col]:.1f}",
            ),
            unsafe_allow_html=True,
        )


# ---------------- 100% vs 50% comparison ----------------
with tab_comparison:
    section_header(
        "Affordability: 100% vs. 50% of average earnings",
        "Each line connects the same country's affordability under both scenarios.",
    )

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)

    comparison_df = filtered_df.sort_values("affordability_change").copy()

    fig, ax = plt.subplots(figsize=(10, max(6, 0.34 * len(comparison_df))))

    y_positions = range(len(comparison_df))

    for i, (_, row) in enumerate(comparison_df.iterrows()):
        ax.plot(
            [row["affordability_index"], row["affordability_index_50"]],
            [i, i],
            color=PALETTE["border"],
            linewidth=2.2,
            zorder=1,
        )

        ax.scatter(
            row["affordability_index"],
            i,
            s=55,
            color=PALETTE["scenario_100"],
            edgecolor="white",
            linewidth=0.6,
            zorder=3,
            label="100% average earnings" if i == 0 else "",
        )

        ax.scatter(
            row["affordability_index_50"],
            i,
            s=55,
            color=PALETTE["scenario_50"],
            edgecolor="white",
            linewidth=0.6,
            zorder=3,
            label="50% average earnings" if i == 0 else "",
        )

    ax.set_yticks(list(y_positions))
    ax.set_yticklabels(comparison_df["Geopolitical entity (reporting)"])

    ax.axvline(
        100,
        color=PALETTE["ink"],
        linestyle="--",
        linewidth=1.3,
        label="EU27 = 100",
        zorder=2,
    )

    ax.set_xlabel("Affordability Index")
    ax.set_ylabel("")
    ax.legend(frameon=True, fontsize=8.5, loc="best")

    apply_chart_style(fig, ax)
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    section_header("Affordability change (100% → 50%)")

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)

    change_df = filtered_df.sort_values("affordability_change").copy()

    fig, ax = plt.subplots(figsize=(10, max(5, 0.32 * len(change_df))))

    bar_colors = [
        PALETTE["positive"] if v >= 0 else PALETTE["negative"]
        for v in change_df["affordability_change"]
    ]

    ax.barh(
        change_df["Geopolitical entity (reporting)"],
        change_df["affordability_change"],
        color=bar_colors,
        height=0.62,
        zorder=3,
    )

    ax.axvline(0, color=PALETTE["ink"], linewidth=1.3, zorder=2)

    ax.set_xlabel("Change in Affordability Index")
    ax.set_ylabel("")

    apply_chart_style(fig, ax)
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ---------------- Country details ----------------
with tab_details:
    section_header("Country details")

    selected_country = st.selectbox(
        "Select a country",
        options=sorted(df["Geopolitical entity (reporting)"].unique()),
    )

    country = df[df["Geopolitical entity (reporting)"] == selected_country].iloc[0]

    d1, d2, d3, d4 = st.columns(4)

    with d1:
        st.markdown(
            kpi_card("Price Level Index", f"{country['pli']:.1f}"),
            unsafe_allow_html=True,
        )
    with d2:
        st.markdown(
            kpi_card("Net earnings — 100%", f"€{country['net_earnings_eur']:,.0f}"),
            unsafe_allow_html=True,
        )
    with d3:
        st.markdown(
            kpi_card("Affordability — 100%", f"{country['affordability_index']:.1f}"),
            unsafe_allow_html=True,
        )
    with d4:
        st.markdown(
            kpi_card("Affordability — 50%", f"{country['affordability_index_50']:.1f}"),
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    with st.expander("View underlying data", expanded=False):
        display_columns = [
            GEO_COL,
            "pli",
            "net_earnings_eur",
            "affordability_index",
            "net_earnings_50_eur",
            "affordability_index_50",
            "affordability_change",
        ]

        st.dataframe(
            filtered_df[display_columns].sort_values(GEO_COL),
            use_container_width=True,
            hide_index=True,
        )


# -------------------------------------------------------------------
# Footer
# -------------------------------------------------------------------

st.markdown(
    f"""
    <div style="margin-top: 2rem; padding-top: 1rem; border-top: 1px solid {PALETTE['border']};
                font-size: 0.8rem; color: {PALETTE['muted']};">
        Source: Eurostat, 2025 · European Cost of Living &amp; Affordability Analysis
    </div>
    """,
    unsafe_allow_html=True,
)

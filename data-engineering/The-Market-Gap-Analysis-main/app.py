import pandas as pd
import plotly.express as px
import streamlit as st

# ============================================================
# CONFIG
# ============================================================
st.set_page_config(page_title="The Sugar Trap", layout="wide", initial_sidebar_state="expanded")

DATA_PATH = "cleaned_snacks_data.csv"
NON_SNACK_LABEL = "Non-Snack / Other"
REQUIRED_COLUMNS = ["product_name", "brands", "primary_category", "sugars_100g", "proteins_100g"]
ALL_LABEL = "All Categories"

ORANGE = "#E8622C"
NAVY = "#0B1F3A"
NAVY_LIGHT = "#16305A"
NAVY_LIGHTER = "#26456E"
TEXT_LIGHT = "#F2F4F8"

st.markdown(
    f"""
    <style>
    .stApp {{ background-color: {NAVY}; color: {TEXT_LIGHT}; }}
    header[data-testid="stHeader"] {{
        background-color: {NAVY};
        box-shadow: none;
    }}
    div[data-testid="stToolbarActions"] {{ display: none; }}
    #MainMenu {{ visibility: hidden; }}
    footer {{ visibility: hidden; }}

    section[data-testid="stSidebar"] {{
        background-color: {NAVY_LIGHT};
    }}

    .sticky-title {{
        position: sticky;
        top: 0;
        z-index: 998;
        background-color: {NAVY};
        border-bottom: 1px solid {NAVY_LIGHTER};
        padding: 14px 0;
        margin: 0 0 1.5rem 0;
        text-align: center;
    }}
    .sticky-title h1 {{ margin: 0; font-size: 1.8rem; }}

    div[data-testid="stMetric"] {{
        background-color: {NAVY_LIGHT};
        border: 1px solid {NAVY_LIGHTER};
        border-radius: 10px;
        padding: 12px;
    }}
    div[data-testid="stMetricValue"] {{ color: {ORANGE}; }}
    .key-insight-box {{
        background-color: {NAVY_LIGHT};
        border-left: 5px solid {ORANGE};
        border-radius: 8px;
        padding: 20px 24px;
        font-size: 17px;
        line-height: 1.6;
    }}
    div[role="radiogroup"] label {{
        background-color: {NAVY_LIGHT};
        border-radius: 6px;
        padding: 6px 10px;
        margin-bottom: 4px;
        width: 100%;
    }}
    </style>

    <div class="sticky-title">
        <h1>The Sugar Trap</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    missing_cols = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing_cols:
        st.error(f"Missing columns: {missing_cols}")
        st.stop()
    return df

df = load_data()
snack_df = df[df["primary_category"] != NON_SNACK_LABEL].copy()
all_categories = sorted(snack_df["primary_category"].unique())

with st.sidebar:
    st.markdown("### Filters")
    st.markdown("**Category**")
    selected_category = st.radio(
        "Category", options=[ALL_LABEL] + all_categories, index=0, label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown("**Sensitivity**")
    protein_max = float(snack_df["proteins_100g"].max())
    sugar_max = float(snack_df["sugars_100g"].max())
    high_protein_threshold = st.slider("Protein, at least (g)", 0.0, round(protein_max, 1), min(10.0, protein_max), step=0.5)
    low_sugar_threshold = st.slider("Sugar, at most (g)", 0.0, round(sugar_max, 1), min(5.0, sugar_max), step=0.5)

if selected_category == ALL_LABEL:
    filtered_df = snack_df.copy()
else:
    filtered_df = snack_df[snack_df["primary_category"] == selected_category].copy()

quadrant_df = filtered_df[
    (filtered_df["proteins_100g"] >= high_protein_threshold)
    & (filtered_df["sugars_100g"] <= low_sugar_threshold)
]
category_quadrant_counts = (
    snack_df.groupby("primary_category")
    .apply(lambda g: ((g["proteins_100g"] >= high_protein_threshold) & (g["sugars_100g"] <= low_sugar_threshold)).sum())
    .sort_values()
)
category_totals = snack_df["primary_category"].value_counts()
opportunity_category = category_quadrant_counts.index[0]
opportunity_count = int(category_quadrant_counts.iloc[0])
opportunity_total = int(category_totals.get(opportunity_category, 0))
overall_gap_pct = (len(quadrant_df) / len(filtered_df) * 100) if len(filtered_df) else 0

k1, k2, k3, k4 = st.columns(4)
k1.metric("Products analyzed", f"{len(filtered_df):,}")
k2.metric("Viewing", selected_category if selected_category != ALL_LABEL else "All categories")
k3.metric("Products in the gap", f"{len(quadrant_df):,}")
k4.metric("Gap as % of view", f"{overall_gap_pct:.1f}%")

st.markdown("")
st.markdown(
    f"""<div class="key-insight-box"><b>Key Insight</b><br><br>
    Based on the data, the biggest market opportunity is in
    <b style="color:{ORANGE};">{opportunity_category}</b>,
    specifically targeting products with <b style="color:{ORANGE};">{high_protein_threshold:g}g</b>
    of protein and less than <b style="color:{ORANGE};">{low_sugar_threshold:g}g</b> of sugar.
    Only {opportunity_count} of {opportunity_total:,} existing products in that category currently meet that profile.
    </div>""",
    unsafe_allow_html=True,
)
st.markdown("")

color_map = {cat: NAVY_LIGHTER for cat in all_categories}
color_map[opportunity_category] = ORANGE
fig = px.scatter(
    filtered_df, x="sugars_100g", y="proteins_100g", color="primary_category",
    color_discrete_map=color_map, hover_data=["product_name", "brands"],
    labels={"sugars_100g": "Sugar (g per 100g)", "proteins_100g": "Protein (g per 100g)", "primary_category": "Category"},
    opacity=0.65, height=550,
)
fig.update_layout(legend_title_text="", margin=dict(t=10, l=10, r=10, b=10), plot_bgcolor=NAVY, paper_bgcolor=NAVY, font_color=TEXT_LIGHT)
fig.add_shape(type="rect", x0=0, x1=low_sugar_threshold, y0=high_protein_threshold,
              y1=filtered_df["proteins_100g"].max() * 1.05 if len(filtered_df) else 1,
              fillcolor=ORANGE, opacity=0.15, line=dict(color=ORANGE, width=2, dash="dash"))
fig.add_annotation(x=low_sugar_threshold / 2 if low_sugar_threshold > 0 else 0.5,
                    y=filtered_df["proteins_100g"].max() * 1.0 if len(filtered_df) else 1,
                    text="Almost nobody's here yet", showarrow=False, font=dict(color=ORANGE, size=13))
st.plotly_chart(fig, use_container_width=True)

with st.expander("View the underlying products"):
    st.dataframe(
        filtered_df[["product_name", "brands", "primary_category", "sugars_100g", "proteins_100g"]]
        .sort_values("proteins_100g", ascending=False),
        use_container_width=True,
    )

st.divider()
st.markdown("## Who Owns This Shelf?")
st.markdown(
    "A nutrition gap doesn't automatically mean an easy opening, if a handful of "
    "giant brands already dominate that category, breaking in is a much harder fight "
    "than the nutrition chart alone suggests. This checks the competitive side of "
    "the same question."
)

shelf_df = snack_df[snack_df["primary_category"] == opportunity_category].copy()
shelf_df["brands"] = shelf_df["brands"].fillna("Unbranded / Unknown")
brand_counts = shelf_df["brands"].value_counts().head(8)
top3_share = (shelf_df["brands"].value_counts().head(3).sum() / len(shelf_df) * 100) if len(shelf_df) else 0
unique_brands = shelf_df["brands"].nunique()

b1, b2 = st.columns([1, 2])
with b1:
    st.metric(f"Unique brands in {opportunity_category}", f"{unique_brands:,}")
    st.metric("Share held by top 3 brands", f"{top3_share:.1f}%")
    if top3_share < 30:
        st.markdown("")
    elif top3_share < 60:
        st.markdown("**Moderately concentrated** — a few brands lead, but there's room.")
    else:
        st.markdown("**Highly concentrated** — a small number of brands control this category.")

with b2:
    brand_fig = px.bar(
        x=brand_counts.values, y=brand_counts.index, orientation="h",
        labels={"x": "Number of products", "y": ""}, color_discrete_sequence=[ORANGE],
    )
    brand_fig.update_layout(plot_bgcolor=NAVY, paper_bgcolor=NAVY, font_color=TEXT_LIGHT,
                             margin=dict(t=10, l=10, r=10, b=10), yaxis=dict(autorange="reversed"))
    st.plotly_chart(brand_fig, use_container_width=True)
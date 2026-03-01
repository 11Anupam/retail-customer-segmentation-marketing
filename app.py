import streamlit as st
import plotly.express as px
import pandas as pd

# --- Page Config ---
st.set_page_config(page_title="Customer Segmentation", page_icon="🛍️", layout="wide")

# --- Load & Clean ---
rfm = pd.read_csv("rfm.csv")
rfm["Segment"] = rfm["Segment"].astype(str).str.strip()
rfm["CustomerID"] = rfm["CustomerID"].astype(int)
rfm["Frequency"] = rfm["Frequency"].clip(lower=1)

# --- Config ---
colors = {
    "Champions": "#2ecc71",
    "Loyal Customers": "#3498db",
    "At-Risk": "#f39c12",
    "Lost": "#e74c3c"
}

recommendations = {
    "Champions": "Reward them with loyalty programs. Ask for reviews. Make them brand ambassadors.",
    "Loyal Customers": "Upsell premium products. Offer early access to new arrivals.",
    "At-Risk": "Send win-back emails. Offer a discount. Remind them what they're missing.",
    "Lost": "Last-chance campaign with a strong offer. If no response, deprioritize ad spend."
}

icons = {
    "Champions": "🏆",
    "Loyal Customers": "💛",
    "At-Risk": "⚠️",
    "Lost": "💔"
}

# --- Header ---
st.title("🛍️ Customer Segmentation Dashboard")
st.markdown("#### RFM Analysis + K-Means Clustering | Anupam Gajbhiye · SIIB MBA-IB")
st.markdown("---")

# --- Dropdown ---
segment_options = ["All Segments"] + sorted(rfm["Segment"].unique().tolist())
segment = st.selectbox("🎛️ Select a Customer Segment to Explore", segment_options)

st.markdown("---")

# --- Filter ---
filtered = rfm if segment == "All Segments" else rfm[rfm["Segment"] == segment]

# --- Banner ---
if segment != "All Segments":
    c = colors.get(segment, "#888")
    st.markdown(
        f"""<div style='background:{c}22; border-left:5px solid {c};
        padding:14px 20px; border-radius:0 10px 10px 0; margin-bottom:20px;'>
        <h3 style='color:{c}; margin:0 0 5px 0'>{icons[segment]} {segment}</h3>
        <p style='margin:0; font-size:15px'>📋 <b>Recommendation:</b> {recommendations[segment]}</p>
        </div>""",
        unsafe_allow_html=True
    )

# --- Metrics ---
st.markdown("### 📊 Segment Metrics")
c1, c2, c3, c4 = st.columns(4)
c1.metric("👥 Customers",      f"{filtered.shape[0]:,}")
c2.metric("🕐 Avg Recency",    f"{filtered['Recency'].mean():.1f} days")
c3.metric("🔁 Avg Frequency",  f"{filtered['Frequency'].mean():.1f}")
c4.metric("💰 Avg Monetary",   f"${filtered['Monetary'].mean():,.1f}")

st.markdown("---")

# ============================================================
# CHART 1 — Donut: count directly from filtered or full rfm
# ============================================================
st.markdown("### 🍩 Customer Distribution by Segment")

# Always count from FULL rfm so all segments always show
counts = rfm["Segment"].value_counts().reset_index()
counts.columns = ["Segment", "Count"]

# Pull selected segment slice out
counts["pull"] = counts["Segment"].apply(lambda x: 0.12 if x == segment else 0)

fig1 = px.pie(
    counts,
    values="Count",
    names="Segment",
    hole=0.5,
    color="Segment",
    color_discrete_map=colors,
    title=f"Total Customers: {rfm.shape[0]:,}"
)
fig1.update_traces(
    textinfo="label+percent+value",
    textposition="outside",
    pull=counts["pull"].tolist()
)
fig1.update_layout(
    height=450,
    showlegend=True,
    margin=dict(t=60, b=40, l=20, r=20)
)
st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

# ============================================================
# CHART 2 — Scatter: Recency vs Monetary, dynamic highlight
# ============================================================
st.markdown("### 🫧 Recency vs Monetary Value")

rfm_plot = rfm.copy()
if segment != "All Segments":
    rfm_plot["color_col"] = rfm_plot["Segment"].apply(
        lambda x: segment if x == segment else "Others"
    )
    cmap = {segment: colors.get(segment, "#888"), "Others": "#333344"}
else:
    rfm_plot["color_col"] = rfm_plot["Segment"]
    cmap = colors

fig2 = px.scatter(
    rfm_plot,
    x="Recency",
    y="Monetary",
    color="color_col",
    color_discrete_map=cmap,
    size="Frequency",
    size_max=20,
    opacity=0.75,
    hover_data={"CustomerID": True, "Segment": True, "color_col": False},
    labels={"color_col": "Segment", "Recency": "Recency (days)", "Monetary": "Monetary ($)"}
)
fig2.update_layout(
    height=500,
    legend_title="Segment",
    margin=dict(t=20, b=20)
)
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# --- Table ---
st.markdown("### 🔍 Customer Preview")
st.dataframe(
    filtered[["CustomerID", "Recency", "Frequency", "Monetary", "Segment"]]
    .sort_values("Monetary", ascending=False)
    .head(20)
    .reset_index(drop=True),
    use_container_width=True
)

st.markdown("---")
st.caption("Built with Python · scikit-learn · Streamlit · Plotly | Anupam Gajbhiye · SIIB MBA-IB")

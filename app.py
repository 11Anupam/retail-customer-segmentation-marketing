import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# --- Page Config ---
st.set_page_config(page_title="Customer Segmentation", page_icon="🛍️", layout="wide")

# --- Load Data ---
rfm = pd.read_csv("rfm.csv")

# ✅ FIX #1 — Strip whitespace & normalize segment names to avoid KeyError crashes
rfm["Segment"] = rfm["Segment"].astype(str).str.strip()

# ✅ FIX #3 — Clip Frequency to min 1 to avoid plotly scatter size=0 crash
rfm["Frequency"] = rfm["Frequency"].clip(lower=1)

# ✅ FIX #4 — Cast CustomerID to int to avoid ugly 14911.0 in table
rfm["CustomerID"] = rfm["CustomerID"].astype(int)

# --- Config Dicts ---
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

# --- Dropdown at Top ---
segment_options = ["All Segments"] + sorted(rfm["Segment"].unique().tolist())
segment = st.selectbox("🎛️ Select a Customer Segment to Explore", segment_options)

st.markdown("---")

# --- Full summary always computed on ENTIRE dataset (never filtered) ---
full_summary = rfm.groupby("Segment").agg(
    Recency=("Recency", "mean"),
    Frequency=("Frequency", "mean"),
    Monetary=("Monetary", "mean"),
    Count=("CustomerID", "count")
).round(1).reset_index()

# --- Filter ---
filtered = rfm if segment == "All Segments" else rfm[rfm["Segment"] == segment]

# --- Banner ---
if segment != "All Segments":
    color = colors.get(segment, "#888888")
    icon = icons.get(segment, "📊")
    rec = recommendations.get(segment, "")
    st.markdown(
        f"""
        <div style='background-color:{color}22; border-left: 5px solid {color};
        padding: 15px 20px; border-radius: 0 10px 10px 0; margin-bottom: 20px;'>
        <h3 style='color:{color}; margin:0 0 6px 0'>{icon} {segment}</h3>
        <p style='margin:0; font-size:15px'>📋 <b>Marketing Recommendation:</b> {rec}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# --- Metrics ---
st.markdown("### 📊 Segment Metrics")
col1, col2, col3, col4 = st.columns(4)

# ✅ FIX #2 — Guard against empty filtered df to avoid NaN format crash
if filtered.empty:
    col1.metric("👥 Total Customers", "0")
    col2.metric("🕐 Avg Recency (days)", "N/A")
    col3.metric("🔁 Avg Frequency", "N/A")
    col4.metric("💰 Avg Monetary ($)", "N/A")
else:
    col1.metric("👥 Total Customers", f"{filtered.shape[0]:,}")
    col2.metric("🕐 Avg Recency (days)", round(filtered["Recency"].mean(), 1))
    col3.metric("🔁 Avg Frequency", round(filtered["Frequency"].mean(), 1))
    col4.metric("💰 Avg Monetary ($)", f"${filtered['Monetary'].mean():,.1f}")

st.markdown("---")

# ============================================================
# CHART ROW 1 — Donut + Scatter
# ============================================================
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### 🍩 Customer Distribution")

    donut_data = full_summary[["Segment", "Count"]].copy()
    donut_data.columns = ["Segment", "Customer Count"]

    # ✅ FIX #6 — Build pull_values from donut_data order, not external list
    donut_data["pull"] = donut_data["Segment"].apply(
        lambda x: 0.1 if x == segment else 0
    )

    fig1 = px.pie(
        donut_data,
        values="Customer Count",
        names="Segment",
        hole=0.5,
        color="Segment",
        color_discrete_map=colors
    )
    fig1.update_traces(
        textposition="outside",
        textinfo="percent+label",
        pull=donut_data["pull"].tolist()
    )
    fig1.update_layout(
        showlegend=True,
        margin=dict(t=30, b=30, l=10, r=10),
        height=350
    )
    st.plotly_chart(fig1, use_container_width=True)

with col_right:
    st.markdown("### 🫧 Recency vs Monetary Value")

    rfm_plot = rfm.copy()
    if segment != "All Segments":
        rfm_plot["display_color"] = rfm_plot["Segment"].apply(
            lambda x: x if x == segment else "Other"
        )
        color_map = {segment: colors.get(segment, "#888888"), "Other": "#444455"}
    else:
        rfm_plot["display_color"] = rfm_plot["Segment"]
        color_map = colors

    fig3 = px.scatter(
        rfm_plot,
        x="Recency",
        y="Monetary",
        color="display_color",
        color_discrete_map=color_map,
        size="Frequency",
        size_max=18,
        hover_data=["CustomerID", "Segment"],
        opacity=0.75,
        labels={"display_color": "Segment"}
    )
    fig3.update_layout(
        margin=dict(t=30, b=30),
        height=350,
        legend_title="Segment"
    )
    st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# ============================================================
# CHART ROW 2 — Bar Chart + Radar
# ============================================================
col_left2, col_right2 = st.columns(2)

with col_left2:
    st.markdown("### 📈 RFM Metrics by Segment")

    # ✅ FIX #7 — Use local bar_colors list, don't mutate full_summary
    bar_colors = full_summary["Segment"].apply(
        lambda x: colors.get(x, "#888888") if (segment == "All Segments" or x == segment) else "#444455"
    ).tolist()

    fig2 = make_subplots(
        rows=1, cols=3,
        subplot_titles=("Avg Recency (days)", "Avg Frequency", "Avg Monetary ($)")
    )

    for i, metric in enumerate(["Recency", "Frequency", "Monetary"], 1):
        fig2.add_trace(
            go.Bar(
                x=full_summary["Segment"],
                y=full_summary[metric],
                marker_color=bar_colors,
                text=full_summary[metric],
                # ✅ FIX #5 — Use 'auto' instead of 'outside' to prevent clipping in subplots
                textposition="auto",
                showlegend=False
            ),
            row=1, col=i
        )

    fig2.update_layout(
        height=380,
        margin=dict(t=50, b=20),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig2, use_container_width=True)

with col_right2:
    st.markdown("### 🕸️ Segment Radar Chart")

    # Use a clean copy for radar — not mutated full_summary
    radar_df = full_summary[["Segment", "Recency", "Frequency", "Monetary"]].copy()
    radar_df["Freq_norm"] = radar_df["Frequency"] / radar_df["Frequency"].max()
    radar_df["Mon_norm"] = radar_df["Monetary"] / radar_df["Monetary"].max()
    radar_df["Rec_norm"] = 1 - (radar_df["Recency"] / radar_df["Recency"].max())

    categories = ["Recency Score", "Frequency", "Monetary Value"]
    fig4 = go.Figure()

    for _, row in radar_df.iterrows():
        is_selected = (segment == "All Segments" or row["Segment"] == segment)
        values = [row["Rec_norm"], row["Freq_norm"], row["Mon_norm"]]
        values += values[:1]

        fig4.add_trace(go.Scatterpolar(
            r=values,
            theta=categories + [categories[0]],
            fill="toself",
            name=row["Segment"],
            line_color=colors.get(row["Segment"], "#888888"),
            opacity=1.0 if is_selected else 0.15,
            fillcolor=colors.get(row["Segment"], "#888888") if is_selected else "#333333"
        ))

    fig4.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        height=380,
        margin=dict(t=30, b=30),
        showlegend=True
    )
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# ============================================================
# CUSTOMER TABLE
# ============================================================
st.markdown("### 🔍 Customer Data Preview")

if filtered.empty:
    st.warning("No customers found for this segment.")
else:
    st.dataframe(
        filtered[["CustomerID", "Recency", "Frequency", "Monetary", "Segment"]]
        .sort_values("Monetary", ascending=False)
        .head(20)
        .reset_index(drop=True),
        use_container_width=True
    )

st.markdown("---")
st.caption("Built with Python · scikit-learn · Streamlit · Plotly | Anupam Gajbhiye · SIIB MBA-IB")

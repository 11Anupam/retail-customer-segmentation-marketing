import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# --- Page Config ---
st.set_page_config(page_title="Customer Segmentation", page_icon="🛍️", layout="wide")

# --- Load Data ---
rfm = pd.read_csv("rfm.csv")

# --- Colors ---
colors = {
    "Champions": "#2ecc71",
    "Loyal Customers": "#3498db",
    "At-Risk": "#f39c12",
    "Lost": "#e74c3c"
}

icons = {
    "Champions": "🏆",
    "Loyal Customers": "💛",
    "At-Risk": "⚠️",
    "Lost": "💔"
}

recommendations = {
    "Champions": "Reward them with loyalty programs. Ask for reviews. Make them brand ambassadors.",
    "Loyal Customers": "Upsell premium products. Offer early access to new arrivals.",
    "At-Risk": "Send win-back emails. Offer a discount. Remind them what they're missing.",
    "Lost": "Last-chance campaign with a strong offer. If no response, deprioritize ad spend."
}

# --- Header ---
st.title("🛍️ Customer Segmentation Dashboard")
st.markdown("#### RFM Analysis + K-Means Clustering | Anupam Gajbhiye · SIIB MBA-IB")
st.markdown("---")

# --- DROPDOWN AT TOP ---
segment = st.selectbox(
    "🎛️ Select a Customer Segment to Explore",
    ["All Segments"] + list(rfm["Segment"].unique())
)

st.markdown("---")

# --- Filter Data ---
if segment == "All Segments":
    filtered = rfm
else:
    filtered = rfm[rfm["Segment"] == segment]

# --- Cluster Summary (dynamic) ---
cluster_summary = filtered.groupby("Segment").agg({
    "Recency": "mean",
    "Frequency": "mean",
    "Monetary": "mean",
    "CustomerID": "count"
}).round(1).reset_index()
cluster_summary.columns = ["Segment", "Avg Recency", "Avg Frequency", "Avg Monetary", "Customer Count"]
cluster_summary["Color"] = cluster_summary["Segment"].map(colors)

# --- Segment Banner ---
if segment != "All Segments":
    color = colors[segment]
    icon = icons[segment]
    rec = recommendations[segment]
    st.markdown(
        f"""
        <div style='background-color:{color}22; border-left: 5px solid {color};
        padding: 15px; border-radius: 8px; margin-bottom: 20px;'>
        <h3 style='color:{color}; margin:0'>{icon} {segment}</h3>
        <p style='margin:5px 0 0 0; font-size:16px'>📋 <b>Marketing Recommendation:</b> {rec}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# --- Top Metrics ---
st.markdown("### 📊 Segment Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("👥 Total Customers", f"{filtered.shape[0]:,}")
col2.metric("🕐 Avg Recency (days)", round(filtered["Recency"].mean(), 1))
col3.metric("🔁 Avg Frequency", round(filtered["Frequency"].mean(), 1))
col4.metric("💰 Avg Monetary ($)", f"${round(filtered['Monetary'].mean(), 1):,}")

st.markdown("---")

# --- Chart Row 1 ---
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### 🍩 Customer Distribution")
    all_summary = rfm.groupby("Segment").agg({"CustomerID": "count"}).reset_index()
    all_summary.columns = ["Segment", "Customer Count"]

    # Highlight selected segment
    if segment != "All Segments":
        all_summary["opacity"] = all_summary["Segment"].apply(
            lambda x: 1.0 if x == segment else 0.3
        )
    else:
        all_summary["opacity"] = 1.0

    fig1 = px.pie(all_summary,
                  values="Customer Count",
                  names="Segment",
                  hole=0.5,
                  color="Segment",
                  color_discrete_map=colors)
    fig1.update_traces(
        textposition="outside",
        textinfo="percent+label",
        pull=[0.1 if s == segment else 0 for s in all_summary["Segment"]]
    )
    fig1.update_layout(showlegend=False, margin=dict(t=20, b=20))
    st.plotly_chart(fig1, use_container_width=True)

with col_right:
    st.markdown("### 🫧 Recency vs Monetary Value")
    fig3 = px.scatter(
        rfm,
        x="Recency",
        y="Monetary",
        color="Segment",
        color_discrete_map={
            s: colors[s] if (segment == "All Segments" or s == segment) else "#dddddd"
            for s in rfm["Segment"].unique()
        },
        size="Frequency",
        hover_data=["CustomerID"],
        opacity=0.7,
        title=""
    )
    fig3.update_layout(margin=dict(t=20, b=20), height=380)
    st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# --- Chart Row 2 ---
col_left2, col_right2 = st.columns(2)

with col_left2:
    st.markdown("### 📈 RFM Metrics Comparison")
    all_cluster = rfm.groupby("Segment").agg({
        "Recency": "mean",
        "Frequency": "mean",
        "Monetary": "mean"
    }).round(1).reset_index()
    all_cluster["Color"] = all_cluster["Segment"].apply(
        lambda x: colors[x] if (segment == "All Segments" or x == segment) else "#dddddd"
    )

    fig2 = make_subplots(rows=1, cols=3,
                         subplot_titles=("Recency (days)", "Frequency", "Monetary ($)"))
    for i, metric in enumerate(["Recency", "Frequency", "Monetary"], 1):
        fig2.add_trace(
            go.Bar(
                x=all_cluster["Segment"],
                y=all_cluster[metric],
                marker_color=all_cluster["Color"],
                text=all_cluster[metric],
                textposition="outside",
                showlegend=False
            ),
            row=1, col=i
        )
    fig2.update_layout(height=380, margin=dict(t=40, b=20))
    st.plotly_chart(fig2, use_container_width=True)

with col_right2:
    st.markdown("### 🕸️ Segment Radar Chart")
    full_summary = rfm.groupby("Segment").agg({
        "Recency": "mean",
        "Frequency": "mean",
        "Monetary": "mean"
    }).round(1).reset_index()

    for m in ["Frequency", "Monetary"]:
        full_summary[m + "_norm"] = full_summary[m] / full_summary[m].max()
    full_summary["Recency_norm"] = 1 - (full_summary["Recency"] / full_summary["Recency"].max())

    categories = ["Recency Score", "Frequency", "Monetary Value"]
    fig4 = go.Figure()

    for _, row in full_summary.iterrows():
        opacity = 1.0 if (segment == "All Segments" or row["Segment"] == segment) else 0.15
        values = [row["Recency_norm"], row["Frequency_norm"], row["Monetary_norm"]]
        values += values[:1]
        fig4.add_trace(go.Scatterpolar(
            r=values,
            theta=categories + [categories[0]],
            fill="toself",
            name=row["Segment"],
            line_color=colors[row["Segment"]],
            opacity=opacity
        ))

    fig4.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        height=380,
        margin=dict(t=20, b=20)
    )
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# --- Individual Customer Table ---
st.markdown("### 🔍 Customer Data Preview")
st.dataframe(
    filtered[["CustomerID", "Recency", "Frequency", "Monetary", "Segment"]]
    .sort_values("Monetary", ascending=False)
    .head(20)
    .reset_index(drop=True),
    use_container_width=True
)

st.markdown("---")
st.caption("Built with Python · scikit-learn · Streamlit · Plotly | Anupam Gajbhiye · SIIB MBA-IB")

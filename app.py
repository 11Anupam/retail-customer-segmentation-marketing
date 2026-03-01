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

# --- Header ---
st.title("🛍️ Customer Segmentation Dashboard")
st.markdown("#### RFM Analysis + K-Means Clustering | by Anupam Gajbhiye")
st.markdown("---")

# --- Cluster Summary ---
cluster_summary = rfm.groupby("Segment").agg({
    "Recency": "mean",
    "Frequency": "mean",
    "Monetary": "mean",
    "CustomerID": "count"
}).round(1).reset_index()

cluster_summary.columns = ["Segment", "Avg Recency", "Avg Frequency", "Avg Monetary", "Customer Count"]
cluster_summary["Color"] = cluster_summary["Segment"].map(colors)

# --- Top Metrics ---
st.markdown("### 📊 Overall Segment Snapshot")
col1, col2, col3, col4 = st.columns(4)

segments = ["Champions", "Loyal Customers", "At-Risk", "Lost"]
icons = ["🏆", "💛", "⚠️", "💔"]

for col, seg, icon in zip([col1, col2, col3, col4], segments, icons):
    count = rfm[rfm["Segment"] == seg].shape[0]
    col.metric(f"{icon} {seg}", f"{count} customers")

st.markdown("---")

# --- Chart Row 1 ---
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### 🍩 Customer Distribution")
    fig1 = px.pie(cluster_summary, values="Customer Count", names="Segment",
                  hole=0.5,
                  color="Segment",
                  color_discrete_map=colors)
    fig1.update_traces(textposition="outside", textinfo="percent+label")
    fig1.update_layout(showlegend=False, margin=dict(t=20, b=20))
    st.plotly_chart(fig1, use_container_width=True)

with col_right:
    st.markdown("### 🫧 Recency vs Monetary Value")
    fig3 = px.scatter(cluster_summary,
                      x="Avg Recency",
                      y="Avg Monetary",
                      size="Customer Count",
                      color="Segment",
                      color_discrete_map=colors,
                      text="Segment",
                      size_max=80)
    fig3.update_traces(textposition="top center", textfont_size=11)
    fig3.update_layout(showlegend=False, margin=dict(t=20, b=20))
    st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# --- Chart Row 2 ---
col_left2, col_right2 = st.columns(2)

with col_left2:
    st.markdown("### 📈 RFM Metrics by Segment")
    fig2 = make_subplots(rows=1, cols=3,
                         subplot_titles=("Recency (days)", "Frequency", "Monetary ($)"))
    for i, metric in enumerate(["Avg Recency", "Avg Frequency", "Avg Monetary"], 1):
        fig2.add_trace(
            go.Bar(
                x=cluster_summary["Segment"],
                y=cluster_summary[metric],
                marker_color=cluster_summary["Color"],
                text=cluster_summary[metric],
                textposition="outside",
                showlegend=False
            ),
            row=1, col=i
        )
    fig2.update_layout(height=350, margin=dict(t=40, b=20))
    st.plotly_chart(fig2, use_container_width=True)

with col_right2:
    st.markdown("### 🕸️ Segment Radar Chart")
    for m in ["Avg Frequency", "Avg Monetary"]:
        cluster_summary[m + "_norm"] = cluster_summary[m] / cluster_summary[m].max()
    cluster_summary["Avg Recency_norm"] = 1 - (cluster_summary["Avg Recency"] / cluster_summary["Avg Recency"].max())

    categories = ["Recency Score", "Frequency", "Monetary Value"]
    fig4 = go.Figure()
    for _, row in cluster_summary.iterrows():
        values = [row["Avg Recency_norm"], row["Avg Frequency_norm"], row["Avg Monetary_norm"]]
        values += values[:1]
        fig4.add_trace(go.Scatterpolar(
            r=values,
            theta=categories + [categories[0]],
            fill="toself",
            name=row["Segment"],
            line_color=colors[row["Segment"]]
        ))
    fig4.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        height=350,
        margin=dict(t=20, b=20)
    )
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# --- Interactive Segment Explorer ---
st.markdown("### 🎛️ Explore a Segment")
segment = st.selectbox("Select a Customer Segment", rfm["Segment"].unique())
filtered = rfm[rfm["Segment"] == segment]

col1, col2, col3 = st.columns(3)
col1.metric("Avg Recency (days)", round(filtered["Recency"].mean()))
col2.metric("Avg Frequency", round(filtered["Frequency"].mean()))
col3.metric("Avg Monetary ($)", round(filtered["Monetary"].mean()))

recommendations = {
    "Champions": "🏆 Reward them with loyalty programs. Ask for reviews. Make them brand ambassadors.",
    "Loyal Customers": "💛 Upsell premium products. Offer early access to new arrivals.",
    "At-Risk": "⚠️ Send win-back emails. Offer a discount. Remind them what they're missing.",
    "Lost": "💔 Last-chance campaign with a strong offer. If no response, deprioritize ad spend."
}

st.info(f"**Marketing Recommendation:** {recommendations[segment]}")

st.markdown("---")
st.caption("Built with Python · scikit-learn · Streamlit · Plotly | Anupam Gajbhiye · SIIB MBA-IB")

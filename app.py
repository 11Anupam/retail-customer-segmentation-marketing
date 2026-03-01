
import streamlit as st
import plotly.express as px
import pandas as pd

rfm = pd.read_csv("rfm.csv")

st.title("🛍️ Customer Segmentation Dashboard")
st.subheader("RFM Analysis + K-Means Clustering")

segment = st.selectbox("Select a Customer Segment", rfm["Segment"].unique())
filtered = rfm[rfm["Segment"] == segment]

col1, col2, col3 = st.columns(3)
col1.metric("Avg Recency (days)", round(filtered["Recency"].mean()))
col2.metric("Avg Frequency", round(filtered["Frequency"].mean()))
col3.metric("Avg Monetary ($)", round(filtered["Monetary"].mean()))

fig = px.scatter(rfm, x="Recency", y="Monetary", color="Segment",
                 size="Frequency", hover_data=["CustomerID"],
                 title="Customer Segments Visualized")
st.plotly_chart(fig)

recommendations = {
    "Champions": "🏆 Reward them with loyalty programs. Ask for reviews. Make them brand ambassadors.",
    "Loyal Customers": "💛 Upsell premium products. Offer early access to new arrivals.",
    "At-Risk": "⚠️ Send win-back emails. Offer a discount. Remind them what they're missing.",
    "Lost": "💔 Last-chance campaign with a strong offer. If no response, deprioritize spend."
}

st.markdown("### 📋 Marketing Recommendation")
st.info(recommendations[segment])

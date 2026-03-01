import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(layout="wide")

rfm = pd.read_csv("rfm.csv")
rfm["Segment"] = rfm["Segment"].astype(str).str.strip()

colors = {
    "Champions": "#2ecc71",
    "Loyal Customers": "#3498db",
    "At-Risk": "#f39c12",
    "Lost": "#e74c3c"
}

counts = rfm["Segment"].value_counts().reset_index()
counts.columns = ["Segment", "Count"]

st.write("### Raw counts going into chart:")
st.write(counts)

fig = px.pie(counts, values="Count", names="Segment",
             hole=0.5, color="Segment", color_discrete_map=colors)
fig.update_traces(textinfo="label+value+percent", textposition="outside")
st.plotly_chart(fig, use_container_width=True)

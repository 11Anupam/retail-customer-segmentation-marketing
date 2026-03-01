import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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

# --- Always computed from full rfm ---
counts = rfm["Segment"].value_counts().reset_index()
counts.columns = ["Segment", "Count"]

full_summary = rfm.groupby("Segment").agg(
    Recency=("Recency", "mean"),
    Frequency=("Frequency", "mean"),
    Monetary=("Monetary", "mean"),
).round(1).reset_index()

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
c1.metric("👥 Customers",     f"{filtered.shape[0]:,}")
c2.metric("🕐 Avg Recency",   f"{filtered['Recency'].mean():.1f} days")
c3.metric("🔁 Avg Frequency", f"{filtered['Frequency'].mean():.1f}")
c4.metric("💰 Avg Monetary",  f"${filtered['Monetary'].mean():,.1f}")

st.markdown("---")

# ============================================================
# ROW 1 — Donut + Scatter
# ============================================================
st.markdown("### 🍩 Customer Distribution & Scatter")
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🍩 Customer Distribution by Segment")
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
        textinfo="label+value+percent",
        textposition="outside",
        pull=counts["Segment"].apply(lambda x: 0.1 if x == segment else 0).tolist()
    )
    fig1.update_layout(height=420, showlegend=True, margin=dict(t=60, b=40))
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("#### 🫧 Recency vs Monetary Value")
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
    fig2.update_layout(height=420, legend_title="Segment", margin=dict(t=20, b=20))
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ============================================================
# ROW 2 — Bar Chart (RFM Metrics)
# ============================================================
st.markdown("### 📊 Avg RFM Metrics by Segment")

bar_colors = full_summary["Segment"].apply(
    lambda x: colors.get(x, "#888") if (segment == "All Segments" or x == segment) else "#333344"
).tolist()

fig3 = make_subplots(
    rows=1, cols=3,
    subplot_titles=("Avg Recency (days) ↓ lower is better",
                    "Avg Frequency ↑ higher is better",
                    "Avg Monetary ($) ↑ higher is better")
)

for i, metric in enumerate(["Recency", "Frequency", "Monetary"], 1):
    fig3.add_trace(
        go.Bar(
            x=full_summary["Segment"],
            y=full_summary[metric],
            marker_color=bar_colors,
            text=full_summary[metric],
            textposition="auto",
            showlegend=False,
            hovertemplate="<b>%{x}</b><br>" + metric + ": %{y}<extra></extra>"
        ),
        row=1, col=i
    )

fig3.update_layout(
    height=420,
    margin=dict(t=60, b=20),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)"
)
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# ============================================================
# ROW 3 — Histogram + Box Plot
# ============================================================
st.markdown("### 📈 Recency Distribution & 📦 Monetary Spread")
col3, col4 = st.columns(2)

with col3:
    st.markdown("#### 📈 Recency Distribution by Segment")

    # Show only selected segment or all
    hist_data = filtered if segment != "All Segments" else rfm

    fig4 = px.histogram(
        hist_data,
        x="Recency",
        color="Segment",
        color_discrete_map=colors,
        nbins=40,
        barmode="overlay",
        opacity=0.75,
        labels={"Recency": "Recency (days)", "count": "Number of Customers"},
        title="How recently did customers purchase?"
    )
    fig4.update_layout(
        height=420,
        legend_title="Segment",
        margin=dict(t=60, b=20),
        bargap=0.05
    )
    st.plotly_chart(fig4, use_container_width=True)

with col4:
    st.markdown("#### 📦 Monetary Value Spread by Segment")

    # Always show all segments in box plot for comparison
    # Highlight selected by making others transparent
    fig5 = go.Figure()

    for seg in sorted(rfm["Segment"].unique()):
        seg_data = rfm[rfm["Segment"] == seg]["Monetary"]
        is_selected = (segment == "All Segments" or seg == segment)

        fig5.add_trace(go.Box(
            y=seg_data,
            name=seg,
            marker_color=colors.get(seg, "#888"),
            opacity=1.0 if is_selected else 0.2,
            boxmean=True,  # shows mean line inside box
            hovertemplate="<b>" + seg + "</b><br>Value: $%{y:,.0f}<extra></extra>"
        ))

    fig5.update_layout(
        height=420,
        yaxis_title="Monetary Value ($)",
        showlegend=True,
        margin=dict(t=40, b=20),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig5, use_container_width=True)

st.markdown("---")

# ============================================================
# Customer Table
# ============================================================
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

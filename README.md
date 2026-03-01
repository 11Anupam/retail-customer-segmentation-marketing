# 🛍️ Customer Segmentation Dashboard
### RFM Analysis + K-Means Clustering | Built by an MBA student who refused to just do case studies.

![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?style=flat&logo=streamlit)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-orange?style=flat&logo=scikit-learn)
![Plotly](https://img.shields.io/badge/Plotly-Visualization-lightblue?style=flat&logo=plotly)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

> 500,000+ transactions. 4 customer segments. 1 dashboard that tells you exactly where to spend your marketing budget.

🔗 **[Live Dashboard →](https://11anupam-customer-segmentation-rfm.streamlit.app)**

---

## 💡 Why I Built This

Marketing strategy without data is just expensive guessing.

As an MBA-IB student at SIIB, I wanted to go beyond theory and build something that solves a real business problem — so I took half a million retail transactions and turned them into a working segmentation engine, the kind that powers CRM tools at companies like Amazon and Nike.

No fluff. Just data → insight → strategy.

---

## 🎯 The Business Problem

Every brand has 4 types of customers hiding in their data:

| Segment | Who They Are | What Most Brands Do | What You *Should* Do |
|---|---|---|---|
| 🏆 Champions | Buy often, spend big, bought recently | Take them for granted | Reward them, make them advocates |
| 💛 Loyal | Consistent, reliable, mid-tier spend | Send generic emails | Upsell, give early access |
| ⚠️ At-Risk | Big spenders going quiet | Ignore them | Win them back — fast |
| 💔 Lost | Gone. Probably to a competitor | Keep spending on them anyway | Cut losses or last-chance offer |

This dashboard finds all four — automatically.

---

## 🧠 How It Works

**Step 1 — RFM Scoring**
Each customer gets scored on 3 dimensions:
- **Recency** — how recently did they buy?
- **Frequency** — how often do they buy?
- **Monetary** — how much have they spent?

**Step 2 — K-Means Clustering**
The algorithm groups customers by similarity across all 3 dimensions — no manual sorting, no bias.

**Step 3 — Strategy Layer**
Each segment gets a tailored marketing recommendation built into the dashboard.

---

## 📊 Dashboard Features

- 🎛️ Interactive segment selector
- 📈 Live RFM metrics per segment
- 🫧 Bubble chart — spend vs recency vs segment size
- 🕸️ Radar chart — full segment personality comparison
- 📋 Marketing recommendation card per segment

---

## 🛠️ Built With

`Python` `Pandas` `NumPy` `scikit-learn` `Plotly` `Streamlit`

---

## 🚀 Run It Yourself
```bash
git clone https://github.com/11Anupam/customer-segmentation-rfm.git
cd customer-segmentation-rfm
pip install -r requirements.txt
streamlit run app.py
```

---

## 📁 Structure
```
customer-segmentation-rfm/
├── app.py          # Streamlit dashboard
├── rfm.csv         # Processed RFM data
├── requirements.txt
└── README.md
```

---

## 💬 The Insight That Surprised Me

The **At-Risk segment** had the highest average lifetime spend of any group — yet they hadn't purchased in over 90 days. Most brands are actively ignoring their most valuable churning customers. A single targeted win-back campaign for this group could recover more revenue than acquiring 3x new customers.

That's the power of segmentation done right.

---

## 👤 Anupam Gajbhiye

MBA-IB | SIIB Pune | Marketing Analytics

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=flat&logo=linkedin)](https://linkedin.com/in/Anupam-Gajbhiye)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?style=flat&logo=github)](https://github.com/11Anupam)

---

⭐ Star this repo if it gave you ideas — it took way more Red Bull than expected.

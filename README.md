# 🛡️ CyberWatch SOC Services Pvt. Ltd.
### Case Study 94 — Security Operations Center Analysis
**B.Tech CSE 2024–28 | Semester IV | Business Studies**

---
## Important Links:

[![Streamlit App](https://img.shields.io/badge/Streamlit-Live%20App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://project-college-soc.streamlit.app/)
[![Google Colab](https://img.shields.io/badge/Colab-Notebook-F9AB00?style=for-the-badge&logo=googlecolab&logoColor=white)](https://colab.research.google.com/drive/14NOl6ZWOTsZz5dW4srhKQI9TuCFp1-08?usp=sharing)
[![CBA Sheet](https://img.shields.io/badge/Google%20Sheets-CBA%20Model-34A853?style=for-the-badge&logo=googlesheets&logoColor=white)](https://docs.google.com/spreadsheets/d/1NPxXCtya3yOMGMqTijXFiXe9D6kKXA14erGOMI1Mh2A/edit?gid=410792799#gid=410792799)
[![Google Docs](https://img.shields.io/badge/Google%20Docs-Project%20Document-4285F4?style=for-the-badge&logo=googledocs&logoColor=white)](https://docs.google.com/document/d/10z_mwrVkfPCBKKKWrn3AASTT6VqrXOdL_OeQ82l_C3Q/edit?usp=sharing)
---

## 📋 Table of Contents

1. [Business Problem Statement](#-business-problem-statement)
2. [Key Financial Parameters](#-key-financial-parameters)
3. [Economic Concepts Applied](#-economic-concepts-applied)
4. [AI Techniques Used](#-ai-techniques-used)
5. [Project Structure](#-project-structure)
6. [Answers to Case Study Questions](#-answers-to-case-study-questions)
7. [Model Results](#-model-results)
8. [How to Run](#-how-to-run)
9. [Final Recommendation](#-final-recommendation)

---

## 📌 Assignment Description

Students are required to analyze the assigned case study and evaluate the proposed business or technology solution. The task involves understanding the problem scenario, performing financial and technical analysis, and assessing the impact of the solution on business performance, efficiency, and customer satisfaction. Students should use logical reasoning, calculations, and data interpretation to support their conclusions.

### Expected Deliverables

| # | Deliverable | Description |
|---|---|---|
| 1 | **Problem Analysis** | Brief understanding of the case study scenario and objectives |
| 2 | **Financial Analysis** | Required calculations such as revenue, savings, or net benefit |
| 3 | **Technical/Data Analysis** | Identification of important data variables and explanation of their role in the system |
| 4 | **Business Impact Evaluation** | Explanation of how the solution affects efficiency, cost, customer satisfaction, or business growth |
| 5 | **Recommendation** | Final decision on whether the proposed solution should be implemented, supported with justification |

> All five deliverables are addressed in this project — see the sections below and the [Colab notebook](https://colab.research.google.com/drive/14NOl6ZWOTsZz5dW4srhKQI9TuCFp1-08?usp=sharing) for full implementation.

---

## 🏢 Business Problem Statement

**CyberWatch SOC Services Pvt. Ltd.** is a Hyderabad-based cybersecurity startup planning to establish a 24/7 **Security Operations Center (SOC)** to provide continuous threat monitoring and incident response for:

- 🏦 Banks & Financial Institutions
- 💻 IT Firms & Software Companies
- 🏪 Small & Medium Enterprises (SMEs)
- 🏛️ Government Agencies

With rising cyber threats such as **ransomware and phishing attacks**, most organizations lack the in-house expertise and infrastructure for continuous monitoring. CyberWatch aims to fill this gap through a managed SOC-as-a-Service subscription model.

The core question: **Is it financially viable and technically sustainable to invest ₹6 Crores in building this SOC?**

---

## 💰 Key Financial Parameters

| Parameter | Value |
|---|---|
| Initial Investment (SIEM, cloud, tools, analysts) | ₹6,00,00,000 (₹6 Crores) |
| Annual Operational Cost | ₹2,00,00,000 (₹2 Crores) |
| Year-1 Target Clients | 150 |
| Annual Subscription Fee per Client | ₹3,00,000 (₹3 Lakhs) |
| **Annual Revenue (Year 1)** | **₹4,50,00,000 (₹4.5 Crores)** |
| **Net Benefit (Year 1)** | **−₹3.5 Crores** *(one-time capex year)* |
| **Net Benefit (Year 2+)** | **+₹2.5 Crores/year** |
| **Payback Period** | **~2.4 Years** |

---

## 📚 Economic Concepts Applied

### 1. Cost–Benefit Analysis (CBA)

```
Net Benefit = Total Revenue − Annual Operational Cost − Initial Investment

Year 1:  ₹4.5 Cr − ₹2 Cr − ₹6 Cr  = −₹3.5 Crores  (loss due to one-time capex)
Year 2+: ₹4.5 Cr − ₹2 Cr           = +₹2.5 Crores/year

Total Benefits (5 yrs) = 150 × ₹3L × 5  = ₹22.5 Crores
Total Costs    (5 yrs) = ₹6 Cr + (₹2 Cr × 5) = ₹16.0 Crores

Cost-Benefit Ratio (CBR) = ₹22.5 Cr / ₹16 Cr = 1.41x  ✅ (> 1 = viable)
```

> 📊 Full CBA: [Google Sheets Model](https://docs.google.com/spreadsheets/d/1NPxXCtya3yOMGMqTijXFiXe9D6kKXA14erGOMI1Mh2A/edit?gid=410792799#gid=410792799)

### 2. Net Present Value (NPV)

Time value of money applied at a **10% discount rate** over 5 years.

```
PV Factor (Year t) = 1 / (1 + 0.10)^t

NPV = Σ [CIF_t × PV Factor_t]  −  Total PV of COFs (incl. initial investment)
```

NPV is positive — confirming the SOC generates value even after discounting future cash flows.

### 3. Payback Period

```
Payback Period = Initial Investment / Annual Net Benefit
              = ₹6 Crores / ₹2.5 Crores = 2.4 Years
```

The investment is fully recovered within the 5-year project lifespan.

### 4. Customer Lifetime Value (CLV)

CLV is derived from `client_satisfaction` scores using assumed retention thresholds. These are **business assumption thresholds coded in the notebook (Cell 30) — not data-derived**:

```python
def retention_from_sat(sat):
    if sat >= 8.0:   return 0.92
    elif sat >= 5.0: return 0.75
    else:            return 0.50

avg_lifetime_years = 1 / (1 - retention_rate)   # standard churn formula
clv = avg_lifetime_years × ₹3,00,000             # annual fee × lifetime
```

| Satisfaction Score | Retention Rate | Avg Lifetime | CLV |
|---|---|---|---|
| 8–10 (High) | 92% | 12.5 years | ₹37.5 Lakhs |
| 5–7 (Mid)   | 75% | 4.0 years  | ₹12.0 Lakhs |
| 1–4 (Low)   | 50% | 2.0 years  | ₹6.0 Lakhs  |

**Total Portfolio CLV (147 clients after cleaning): ₹21.47 Crores**

High-satisfaction clients generate a **6× CLV multiplier** over low-satisfaction clients — operational excellence directly translates to revenue.

### 5. Subscription Revenue Model

Recurring annual subscriptions provide **predictable, compounding revenue**. The 5-year projection models 20% annual client growth (150 → 180 → 216 → 259 → 311), growing revenue from ₹4.5 Cr in Year 1 to ₹9.3 Cr in Year 5.

---

## 🤖 AI Techniques Used

### 1. Synthetic Data Generation

150 client records generated using **NumPy** with segment-specific base values per client type (SME, IT Firm, Bank/Govt), with injected nulls (~4% per column), 5 duplicate rows, and 3 artificial outliers.

```python
np.random.seed(42)
client_types = np.random.choice([0, 1, 2], N, p=[0.45, 0.35, 0.20])
# Base detection rates: SME=89%, IT Firm=93%, Bank/Govt=96%
threat_detection_rate = np.clip(
    np.choose(client_types, [89, 93, 96]) + np.random.normal(0, 2.5, N),
    78, 99.9
)
```

### 2. Data Cleaning & Preprocessing

| Step | Method | Result |
|---|---|---|
| Duplicate removal | `drop_duplicates()` | 5 rows removed |
| Outlier removal | IQR method (1.5× fence) | 3 rows removed |
| Missing value imputation | Median imputation | 0 nulls remaining |
| **Final dataset** | — | **147 clients, 10 KPIs** |

**Engineered Features (Cell 13):**
```python
detection_efficiency = threat_detection_rate × (1 − false_positive_rate / 100)
response_quality     = system_uptime / incident_response_time
sla_score            = 0.35×detection + 0.30×(uptime−97)×10
                     + 0.20×(1−fpr/100)×100 + 0.15×(1−escalation/100)×100
client_type_code     = {'SME': 0, 'IT Firm': 1, 'Bank/Govt': 2}
```

### 3. K-Means Clustering (Unsupervised ML)

Clients segmented into **3 tiers** using K-Means (K=3), validated by Elbow Method and Silhouette Score analysis over K=2 to 9.

**Clustering features (7):** `threat_detection_rate`, `incident_response_time`, `system_uptime`, `false_positive_rate`, `client_satisfaction`, `patch_compliance_rate`, `escalation_rate`

```python
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=3, init='k-means++', n_init=20,
                max_iter=500, random_state=42)
```

**Results:**

| Cluster | Label | Clients | Avg Detection | Avg Response | Avg Satisfaction |
|---|---|---|---|---|---|
| 🟢 Premium | High-Performance | 33 | 96.4% | 8.2 min | 8.54 / 10 |
| 🟡 Standard | Mid-Tier | 40 | 92.8% | 12.9 min | 6.40 / 10 |
| 🔴 At-Risk | Low-Performance | 74 | 89.1% | 18.2 min | 4.43 / 10 |

**Silhouette Score: 0.2942** — confirms meaningful separation between tiers.

**Cluster Interpretation (from notebook Cell 31):**
- **Premium** — Bank/Govt dominated. Detection >95%, response <10 min. Priority SLA tier.
- **Standard** — Mid-range IT Firms. Upsell AI-enhanced monitoring opportunity.
- **At-Risk** — SME-heavy. Low detection, slow response, high FPR. Needs proactive intervention.

### 4. Linear Regression (Supervised ML)

Predicts `client_satisfaction` (1–10) from 8 SOC operational KPIs. Train-test split: 80/20, `random_state=42`.

**Features (8):** `threat_detection_rate`, `incident_response_time`, `system_uptime`, `false_positive_rate`, `patch_compliance_rate`, `escalation_rate`, `analyst_utilization`, `alerts_per_day`

**Model Performance:**

| Metric | Value |
|---|---|
| Training R² | 0.7609 |
| Test R²     | 0.7609 |
| MAE         | 0.6920 |
| RMSE        | 0.8976 |

The model explains **76.1% of the variance** in client satisfaction from SOC operational metrics alone.

**Key Drivers (from notebook Cell 31):**

| Direction | Features |
|---|---|
| ✅ Positive (raise satisfaction) | `threat_detection_rate`, `system_uptime`, `patch_compliance_rate` |
| ❌ Negative (lower satisfaction) | `incident_response_time`, `false_positive_rate`, `escalation_rate` |

### 5. What-If Scenario Analysis

Using the trained regression model to predict satisfaction under improvement scenarios (notebook Cell 28):

| Scenario | Predicted Satisfaction |
|---|---|
| Baseline | 5.73 / 10 |
| Improved Detection (+5%) | 6.39 / 10 |
| Faster Response (−5 min) | 6.76 / 10 |
| Lower FPR (−5%) | 6.27 / 10 |
| **All Improvements** | **7.91 / 10** |

### 6. Principal Component Analysis (PCA)

PCA reduces 7 clustering features to 2 dimensions for visual cluster separation. Used in both the notebook (Cell 23) and the Streamlit dashboard.

---

## 📁 Project Structure

```
CyberWatch-SOC-CaseStudy94/
│
├── Project_college_SOC.ipynb     # Main analysis notebook (Google Colab)
├── main.py                        # Streamlit dashboard application
├── CyberWatch_SOC_CBA.xlsx        # Cost-Benefit Analysis spreadsheet
└── README.md                      # This file
```

**Notebook Sections:**

| Section | Content |
|---|---|
| Section 1 | Business & Financial Analysis (Q1, Q2) + 5-Year Projection Chart |
| Section 2 | SOC Variables (Q3) + Synthetic Data Generation (Q4) |
| Section 3 | Data Cleaning & Preprocessing + Feature Engineering |
| Section 4 | Exploratory Data Analysis — distributions, heatmap, segment comparison |
| Section 5 | K-Means Clustering — Elbow, Silhouette, PCA, Radar Chart |
| Section 6 | Linear Regression — coefficients, diagnostics, What-If Analysis |
| Section 7 | CLV Analysis + Business Interpretation + Recommendation (Q5) |

---

## ❓ Answers to Case Study Questions

### Q1. Total Annual Subscription Revenue
```
Revenue = Number of Clients × Fee per Client
        = 150 × ₹3,00,000
        = ₹4,50,00,000 = ₹4.5 Crores
```

### Q2. Net Benefit
```
Net Benefit = Total Revenue − Annual Operational Cost − Initial Investment
            = ₹4.5 Cr − ₹2 Cr − ₹6 Cr
            = −₹3.5 Crores (Year 1)
```
Year 1 is negative only because ₹6 Cr is spent upfront. From Year 2: **+₹2.5 Crores/year**. Payback in **~2.4 years**.

### Q3. Key SOC Performance Variables

| Variable | Importance |
|---|---|
| `threat_detection_rate (%)` | % of actual threats correctly identified. Low rate = undetected breaches. Target: >95% |
| `incident_response_time (min)` | Time from detection to response. Lower MTTR reduces damage. Target: <15 min |
| `system_uptime (%)` | % SOC is operational. Downtime creates unprotected windows. Target: >99.9% |
| `false_positive_rate (%)` | Fraction of alerts that are not real threats. High FPR causes analyst alert fatigue |
| `alerts_per_day (count)` | Daily alert volume — requires AI triage to prioritize critical threats |
| `incidents_handled (count)` | Confirmed incidents resolved per month — reflects analyst capacity |
| `client_satisfaction (1–10)` | Drives retention rate and CLV |
| `escalation_rate (%)` | High escalation signals Tier-1 analyst skill gaps |
| `analyst_utilization (%)` | Target 65–80%. Too high = burnout; too low = wasted resources |
| `patch_compliance_rate (%)` | Unpatched systems are primary attack entry points |

### Q4. Synthetic Data Generation in Python
Synthetic data generated with `numpy` using segment-specific distributions per client type (SME/IT Firm/Bank/Govt), then quality issues (nulls, duplicates, outliers) were injected and cleaned. Full implementation in [Section 2–3 of the notebook](https://colab.research.google.com/drive/14NOl6ZWOTsZz5dW4srhKQI9TuCFp1-08?usp=sharing).

### Q5. CRM, Retention & Long-Term Business Growth

**Fast Threat Detection →** Reduces time-to-detect breaches and minimises client financial damage. `threat_detection_rate` is a positive driver of client satisfaction in the regression model.

**Quick Incident Response →** Reduces Mean-Time-To-Respond (MTTR) and prevents SLA violations. `incident_response_time` is the strongest negative driver of satisfaction — the single biggest operational lever.

**Reliable Monitoring (High Uptime) →** Ensures zero unprotected windows and builds long-term client confidence. `system_uptime` positively predicts satisfaction.

**Business Impact Chain:**
```
Better SOC Operations
  → Higher Client Satisfaction
    → Higher Retention (50% → 75% → 92%)
      → Higher CLV (₹6L → ₹12L → ₹37.5L)
        → More Revenue & Referrals
          → Reinvest in AI & Analysts
            → Better SOC Operations ↑  (growth flywheel)
```

---

## 📊 Model Results

### Financial Summary

| Metric | Value |
|---|---|
| Year-1 Annual Revenue | ₹4.5 Crores |
| Year-1 Net Benefit | −₹3.5 Crores |
| Year 2+ Annual Surplus | +₹2.5 Crores |
| Payback Period | ~2.4 Years |
| CBR (5-year) | 1.41x |
| Total Portfolio CLV (147 clients) | ₹21.47 Crores |

### Clustering Results

| Cluster | n | Avg Detection | Avg Response | Avg Satisfaction |
|---|---|---|---|---|
| 🟢 Premium | 33 | 96.4% | 8.2 min | 8.54 / 10 |
| 🟡 Standard | 40 | 92.8% | 12.9 min | 6.40 / 10 |
| 🔴 At-Risk | 74 | 89.1% | 18.2 min | 4.43 / 10 |
| **Silhouette Score** | — | — | — | **0.2942** |

### Regression Results

| Metric | Value |
|---|---|
| R² (Test) | 0.7609 |
| MAE       | 0.6920 |
| RMSE      | 0.8976 |

### Summary Table (from notebook Cell 33)

| Section | Method | Key Finding |
|---|---|---|
| Q1: Revenue | Formula | ₹4.5 Crores per year |
| Q2: Net Benefit | Formula | −₹3.5 Cr Year 1 / +₹2.5 Cr Year 2+ |
| Q3: Variables | Domain Analysis | 10 critical SOC KPIs defined |
| Q4: Data Gen | Python / NumPy | 150 synthetic client records |
| EDA | Plots & Heatmap | Detection rate and response time drive satisfaction |
| K-Means (K=3) | Clustering | Premium / Standard / At-Risk segments |
| Linear Regression | Predictive Model | SOC KPIs explain 76.1% of satisfaction variance |
| Q5: CRM Impact | CLV Analysis | High-satisfaction clients = 6× lifetime revenue |
| Recommendation | All evidence | ESTABLISH THE SOC |

---

## 🚀 How to Run

### Option 1: Streamlit App (Deployed)
**[project-college-soc.streamlit.app](https://project-college-soc.streamlit.app/)**

### Option 2: Run Locally
```bash
git clone https://github.com/<your-username>/CyberWatch-SOC-CaseStudy94.git
cd CyberWatch-SOC-CaseStudy94

pip install streamlit pandas numpy matplotlib seaborn scikit-learn scipy

streamlit run main.py
```

### Option 3: Google Colab
**[Open notebook →](https://colab.research.google.com/drive/14NOl6ZWOTsZz5dW4srhKQI9TuCFp1-08?usp=sharing)**

All dependencies install automatically via `!pip install` in the first cell.

---

## ✅ Final Recommendation

> **CyberWatch SOC Services Pvt. Ltd. SHOULD establish the Security Operations Center.**

| Evidence | Finding |
|---|---|
| CBR = 1.41x | Total benefits exceed total costs over 5 years |
| Payback = 2.4 years | Investment recovered well within project life |
| NPV positive | Project generates value after discounting at 10% |
| R² = 0.7609 | SOC KPIs strongly explain client satisfaction variance |
| CLV multiplier = 6× | High-satisfaction clients generate 6× more lifetime revenue |
| Subscription model | Recurring, predictable, scalable revenue stream |

**Priority Actions (from notebook Cell 31):**
1. Tiered SLA pricing — SME: ₹2L/yr | IT Firm: ₹3.5L/yr | Bank/Govt: ₹5L+/yr
2. Reduce `incident_response_time` for At-Risk cluster clients first
3. Invest in AI-assisted triage to lower `false_positive_rate`
4. Obtain ISO 27001 + SOC 2 Type II certifications in Year 1
5. Move Bank/Govt clients to ₹5L/yr pricing from Year 2

---

**B.Tech CSE 2024–28 | Semester IV | Business Studies | Case Study 94**

*Built with Python · NumPy · scikit-learn · Streamlit*

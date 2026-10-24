# InsightFlow | Industrial Data Engineering & Analytics Pipeline

## 📌 Executive Summary
**InsightFlow** is an end-to-end Data Engineering and Business Intelligence pipeline built to ingest, clean, transform, and analyze multi-region manufacturing and supply chain transactional data. The project automates data validation workflows, logs operational anomalies, generates SQL-aggregated metrics, and serves business-ready datasets for executive Power BI reporting.

---

## 🛠 Tech Stack
* **Language & ETL:** Python 3.11 (`pandas`, `faker`, `sqlite3`)
* **Storage & Querying:** SQLite Engine, Relational SQL Views
* **Business Intelligence:** Power BI Desktop
* **Version Control:** Git & GitHub

---

## 🏗 Architecture & Data Pipeline Workflow

```text
[Raw Multi-Region Transactions]
               │
               ▼
[Python Data Validation Engine] ──(Flagged Anomalies)──► error_log.csv
               │
      (Clean Transactions)
               │
               ▼
   [Feature Engineering Layer] ──► Calculates Revenue, Lead Times & Budget Variances
               │
               ▼
    [SQLite Data Warehouse]   ──► fact_transactions Table
               │
               ▼
   [SQL Analytical Views Layer]
       ├── v_monthly_operations_summary
       └── v_financial_variance_analysis
               │
               ▼
  [Power BI Ready Export Layer] ──► Automated CSV Exports for Visual Reporting
```
---

## 🚀 Key Features

### 1. Data Ingestion & Synthetic Generation (`generator.py`)
Generates high-volume transactional data mimicking manufacturing logistics across multiple regions (*APAC, Europe, North America, LATAM*) and product categories (*Electronics, Hydraulics, Industrial Automation*), intentionally injecting real-world data anomalies (e.g., negative quantities, invalid dates, missing customer IDs).

### 2. Automated ETL & Data Validation (`etl_pipeline.py`)
* **Validation Workflows:** Isolates and logs bad records dynamically into `data/processed/error_log.csv` without halting pipeline execution.
* **Feature Engineering:** Computes operational KPIs including:
  * `total_revenue`: Transacted order value.
  * `lead_time_days`: Fulfillment duration between order placement and shipping.
  * `revenue_variance`: Actual revenue vs. target budget.
  * `variance_status`: Categorical classification (*Favorable*, *Unfavorable*, *On Target*).

### 3. Analytics SQL Views Layer (`create_views.py`)
* **`v_monthly_operations_summary`**: Aggregates monthly revenue, total volume sold, and average fulfillment lead time grouped by region and product line.
* **`v_financial_variance_analysis`**: Exposes granular budget vs. actual financial performance metrics for operational cost control.

---

## 📊 Business Intelligence & Visualizations
The transformed analytical views are connected to Power BI Desktop to deliver an executive-level operational dashboard tracking:

* Executive KPIs: Total Revenue, Total Units Shipped, and Average Fulfillment Lead Time.

* Operational Performance: Monthly Revenue Trends and Supply Chain Lead Time by Region.

* Financial Governance: Budget vs. Actual Revenue Variance distribution for cost tracking.


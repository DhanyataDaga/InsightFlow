import sqlite3
import os


def create_sql_views():
    print("[START] Creating SQL Analytical Views in SQLite...")

    db_path = 'data/processed/insightflow.db'
    if not os.path.exists(db_path):
        print(
            f"[ERROR] Database not found at {db_path}. Run etl_pipeline.py first!")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # View 1: Monthly Operations Summary (Lead times, volume, revenue by region & category)
    cursor.execute("DROP VIEW IF EXISTS v_monthly_operations_summary;")
    cursor.execute("""
        CREATE VIEW v_monthly_operations_summary AS
        SELECT 
            strftime('%Y-%m', order_date) AS order_month,
            region,
            category,
            COUNT(order_id) AS total_orders,
            SUM(quantity) AS total_units_sold,
            ROUND(SUM(total_revenue), 2) AS total_revenue,
            ROUND(AVG(lead_time_days), 1) AS avg_lead_time_days
        FROM fact_transactions
        GROUP BY strftime('%Y-%m', order_date), region, category;
    """)
    print("   -> Created View: v_monthly_operations_summary")

    # View 2: Financial Variance Analysis (Favorable vs Unfavorable budget tracking)
    cursor.execute("DROP VIEW IF EXISTS v_financial_variance_analysis;")
    cursor.execute("""
        CREATE VIEW v_financial_variance_analysis AS
        SELECT 
            order_id,
            order_date,
            customer_type,
            region,
            category,
            total_revenue,
            target_budget,
            revenue_variance,
            variance_status
        FROM fact_transactions;
    """)
    print("   -> Created View: v_financial_variance_analysis")

    conn.commit()
    conn.close()
    print("[SUCCESS] All SQL analytical views successfully created inside 'insightflow.db'!")


if __name__ == "__main__":
    create_sql_views()

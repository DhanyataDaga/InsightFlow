import sqlite3
import pandas as pd
import os


def export_views():
    print("[START] Exporting analytical views for Power BI...")

    db_path = 'data/processed/insightflow.db'
    conn = sqlite3.connect(db_path)

    # Output directory for Power BI datasets
    output_dir = 'data/powerbi_ready'
    os.makedirs(output_dir, exist_ok=True)

    # Export View 1
    df_summary = pd.read_sql(
        "SELECT * FROM v_monthly_operations_summary", conn)
    summary_path = os.path.join(output_dir, 'monthly_operations_summary.csv')
    df_summary.to_csv(summary_path, index=False)
    print(f"   -> Exported: {summary_path} ({len(df_summary)} rows)")

    # Export View 2
    df_variance = pd.read_sql(
        "SELECT * FROM v_financial_variance_analysis", conn)
    variance_path = os.path.join(output_dir, 'financial_variance_analysis.csv')
    df_variance.to_csv(variance_path, index=False)
    print(f"   -> Exported: {variance_path} ({len(df_variance)} rows)")

    conn.close()
    print("[SUCCESS] All datasets ready for Power BI import in 'data/powerbi_ready/'!")


if __name__ == "__main__":
    export_views()

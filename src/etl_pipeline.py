import os
import sqlite3
import pandas as pd


def run_etl_pipeline():
    print("[START] Starting InsightFlow ETL Pipeline...")

    # ==========================================
    # PHASE 1: EXTRACT
    # ==========================================
    raw_file_path = 'data/raw/raw_transactions.csv'
    if not os.path.exists(raw_file_path):
        print(
            f"[ERROR] Raw data file not found at {raw_file_path}. Run generator.py first!")
        return

    print("[Extract] Reading raw transactions dataset...")
    df = pd.read_csv(raw_file_path)
    print(f"   -> Extracted {len(df)} raw records.")

    # Convert date columns back to datetime objects
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['ship_date'] = pd.to_datetime(df['ship_date'])

    # ==========================================
    # PHASE 2: DATA VALIDATION & ERROR HANDLING
    # ==========================================
    print("[Validate] Running data validation workflows...")

    # Rule 1: Quantity must be greater than 0
    # Rule 2: customer_id must not be null
    # Rule 3: ship_date must be on or after order_date

    is_valid_quantity = df['quantity'] > 0
    is_not_null_customer = df['customer_id'].notna()
    is_valid_dates = df['ship_date'] >= df['order_date']

    # Combine all validation rules
    valid_mask = is_valid_quantity & is_not_null_customer & is_valid_dates

    # Separate clean data from error data
    df_clean = df[valid_mask].copy()
    df_errors = df[~valid_mask].copy()

    # Save error log for tracking anomalies
    os.makedirs('data/processed', exist_ok=True)
    df_errors.to_csv('data/processed/error_log.csv', index=False)

    print(f"   -> Validation Complete: {len(df_clean)} valid records passed.")
    print(
        f"   -> Flagged & isolated {len(df_errors)} invalid records into 'data/processed/error_log.csv'.")

    # ==========================================
    # PHASE 3: TRANSFORM & FEATURE ENGINEERING
    # ==========================================
    print("[Transform] Engineering analytics features & metrics...")

    # 1. Calculate Total Revenue per transaction
    df_clean['total_revenue'] = round(
        df_clean['quantity'] * df_clean['unit_price'], 2)

    # 2. Calculate Logistics Lead Time (Days between order and shipping)
    df_clean['lead_time_days'] = (
        df_clean['ship_date'] - df_clean['order_date']).dt.days

    # 3. Calculate Financial Variance (Actual Revenue vs Target Budget)
    df_clean['revenue_variance'] = round(
        df_clean['total_revenue'] - df_clean['target_budget'], 2)

    # 4. Categorize Variance Status for operational tracking
    def get_variance_status(var):
        if var > 0:
            return 'Favorable'
        elif var < 0:
            return 'Unfavorable'
        else:
            return 'On Target'

    df_clean['variance_status'] = df_clean['revenue_variance'].apply(
        get_variance_status)

    print("   -> Feature engineering complete (Revenue, Lead Times, Variances calculated).")

    # ==========================================
    # PHASE 4: LOAD INTO SQL DATABASE
    # ==========================================
    print("[Load] Loading processed dataset into SQLite database...")

    db_path = 'data/processed/insightflow.db'
    conn = sqlite3.connect(db_path)

    # Write clean dataframe to a SQL table named 'fact_transactions'
    df_clean.to_sql('fact_transactions', conn,
                    if_exists='replace', index=False)

    conn.close()
    print(
        f"[SUCCESS] Loaded {len(df_clean)} structured records into SQLite table 'fact_transactions' at '{db_path}'!")
    print("[DONE] ETL Pipeline execution completed successfully!")


if __name__ == "__main__":
    run_etl_pipeline()

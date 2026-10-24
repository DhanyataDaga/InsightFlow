import os
import random
import numpy as np
import pandas as pd
from faker import Faker

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)
fake = Faker()


def generate_raw_transactions(num_records=2500):
    categories = {
        'Electronics': ['Power Drives', 'Sensors', 'Control Panels', 'Inverters'],
        'Hydraulics': ['Pumps', 'Valves', 'Motors', 'Hoses'],
        'Industrial Automation': ['PLC Units', 'Relays', 'Transmitters']
    }

    data = []

    for i in range(1, num_records + 1):
        order_id = f"ORD-{10000 + i}"
        order_date = fake.date_between(start_date='-1y', end_date='today')
        customer_id = f"CUST-{random.randint(100, 250)}"
        customer_type = random.choice(['Enterprise', 'SMB', 'Distributor'])
        region = random.choice(['North America', 'Europe', 'APAC', 'LATAM'])

        category = random.choice(list(categories.keys()))
        product = random.choice(categories[category])

        quantity = random.randint(1, 50)
        base_price = round(random.uniform(50.0, 1500.0), 2)
        target_budget = round(base_price * quantity *
                              random.uniform(0.90, 1.10), 2)

        # Calculate delivery dates
        shipping_days = random.randint(1, 14)
        ship_date = order_date + pd.Timedelta(days=shipping_days)

        data.append({
            'order_id': order_id,
            'order_date': order_date,
            'ship_date': ship_date,
            'customer_id': customer_id,
            'customer_type': customer_type,
            'region': region,
            'category': category,
            'product': product,
            'quantity': quantity,
            'unit_price': base_price,
            'target_budget': target_budget
        })

    df = pd.DataFrame(data)

    # Inject intentional "dirty" data anomalies to test our validation & cleaning pipeline!
    # 1. Negative quantity error (invalid transaction)
    df.loc[15, 'quantity'] = -5

    # 2. Missing customer_id (null value)
    df.loc[42, 'customer_id'] = None

    # 3. Ship date before order date (invalid logic)
    df.loc[88, 'ship_date'] = df.loc[88, 'order_date'] - pd.Timedelta(days=3)

    # Save to data/raw/
    os.makedirs('data/raw', exist_ok=True)
    file_path = 'data/raw/raw_transactions.csv'
    df.to_csv(file_path, index=False)
    print(
        f" Successfully generated {num_records} raw transactions at '{file_path}'!")


if __name__ == "__main__":
    generate_raw_transactions()

# generate_fake_inventory.py
"""
Creates data/inventory_raw.csv with columns:
SKU, Description, Location, OnHandQty, ReorderPoint, UnitCost
    ***Imported from assignment 3**
"""

import pandas as pd
from faker import Faker
from random import randint, choice, uniform
from pathlib import Path

fake = Faker()
SKUS = [f"SKU{str(i).zfill(5)}" for i in range(1, 501)]
LOCATIONS = ["WH1", "WH2", "WH3"]

def make_row(sku):
    return {
        "SKU": sku,
        "Description": fake.word().capitalize(),
        "Location": choice(LOCATIONS),
        "OnHandQty": randint(0, 500),
        "ReorderPoint": randint(20, 100),
        "UnitCost": round(uniform(2.5, 50.0), 2),
    }

Path("data").mkdir(exist_ok=True)
df = pd.DataFrame([make_row(s) for s in SKUS])
df.to_csv("data/inventory_raw.csv", index=False)
print("✅  Fake inventory written to data/inventory_raw.csv")


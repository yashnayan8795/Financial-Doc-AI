from faker import Faker
from jinja2 import Template
import os
import random
from datetime import datetime, timedelta

fake = Faker()
os.makedirs("financial-doc-ai/data/synthetic_documents", exist_ok=True)

with open("financial-doc-ai/templates/trade_confirmation_template.txt") as f:
    template = Template(f.read())

instruments = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN", "META"]
sides = ["Buy", "Sell"]
counterparties = ["Morgan Stanley", "Goldman Sachs", "JPMorgan", "UBS", "Citadel"]

for i in range(10):  # generate 10 trade confirmations
    trade_date = fake.date_between(start_date="-2y", end_date="today")
    settlement_date = trade_date + timedelta(days=2)

    doc = template.render(
        trade_id=f"TRD{fake.random_int(10000, 99999)}",
        trade_date=trade_date.strftime("%Y-%m-%d"),
        instrument=random.choice(instruments),
        side=random.choice(sides),
        quantity=random.randint(100, 5000),
        price=round(random.uniform(100.0, 500.0), 2),
        counterparty=random.choice(counterparties),
        settlement_date=settlement_date.strftime("%Y-%m-%d")
    )

    with open(f"financial-doc-ai/data/synthetic_documents/trade_confirmation_{i}.txt", "w") as out:
        out.write(doc)

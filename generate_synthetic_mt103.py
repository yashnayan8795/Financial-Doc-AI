from faker import Faker
from jinja2 import Template
import os

fake = Faker()
os.makedirs("financial-doc-ai/data/synthetic_documents", exist_ok=True)

with open("financial-doc-ai/templates/mt103_template.txt") as f:
    template = Template(f.read())

for i in range(10):  # generate 10 documents
    doc = template.render(
        sender_bic="BANKUS33XXX",
        receiver_bic="BANKDEFFXXX",
        transaction_ref=fake.uuid4()[:10].upper(),
        time="1030",
        date="250530",
        value_date="250530",
        currency="USD",
        amount=str(round(fake.pyfloat(left_digits=5, right_digits=2, positive=True), 2)),
        sender_account=fake.bban(),
        sender_name=fake.name(),
        sender_address=fake.address().replace('\n', ' '),
        receiver_account=fake.bban(),
        receiver_name=fake.name(),
        receiver_address=fake.address().replace('\n', ' ')
    )

    with open(f"financial-doc-ai/data/synthetic_documents/mt103_{i}.txt", "w") as out:
        out.write(doc)

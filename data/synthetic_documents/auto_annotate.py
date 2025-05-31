import os
import re
import json

# --- Entity Extractors ---

def annotate_mt103(text):
    entities = []
    if match := re.search(r"20:([A-Z0-9]+)", text):
        start = match.start(1)
        end = match.end(1)
        entities.append((start, end, "TRANSACTION_REF"))

    if match := re.search(r"32A:\d{6}([A-Z]{3})(\d+),", text):
        currency, amount = match.group(1), match.group(2)
        start_currency = text.index(currency)
        start_amount = text.index(amount, start_currency + len(currency))
        entities.append((start_currency, start_currency + len(currency), "CURRENCY"))
        entities.append((start_amount, start_amount + len(amount), "AMOUNT"))

    if match := re.search(r"50K:/(\d+)\n(.+)", text):
        acc_num, sender = match.group(1), match.group(2).strip()
        start_acc = text.index(acc_num)
        start_sender = text.index(sender, start_acc + len(acc_num))
        entities.append((start_acc, start_acc + len(acc_num), "ACCOUNT_NO"))
        entities.append((start_sender, start_sender + len(sender), "SENDER_NAME"))

    return (text, {"entities": entities})


def annotate_trade_confirmation(text):
    entities = []

    def extract(field, label):
        pattern = rf"{field}:\s*([^\n]+)"
        match = re.search(pattern, text)
        if match:
            value = match.group(1).strip()
            start = text.index(value)
            end = start + len(value)
            entities.append((start, end, label))

    extract("TradeID", "TRADE_ID")
    extract("TradeDate", "TRADE_DATE")
    extract("Instrument", "INSTRUMENT")
    extract("Buy/Sell", "SIDE")
    extract("Quantity", "QUANTITY")
    extract("Price", "PRICE")
    extract("Counterparty", "COUNTERPARTY")
    extract("SettlementDate", "SETTLEMENT_DATE")

    return (text, {"entities": entities})


# --- Load and Annotate ---

train_data = []
base_dir = "financial-doc-ai/data/synthetic_documents"

for filename in os.listdir(base_dir):
    if filename.endswith(".txt"):
        filepath = os.path.join(base_dir, filename)
        with open(filepath, "r") as f:
            text = f.read()

        if filename.startswith("mt103"):
            annotated = annotate_mt103(text)
        elif filename.startswith("trade_confirmation"):
            annotated = annotate_trade_confirmation(text)
        else:
            continue  # skip unknown formats

        train_data.append(annotated)

# --- Save to JSON ---
out_path = "financial-doc-ai/data/ner_training/train_data_auto.json"
os.makedirs(os.path.dirname(out_path), exist_ok=True)

with open(out_path, "w") as f:
    json.dump(train_data, f, indent=2)

print(f"✅ Saved {len(train_data)} annotated examples to {out_path}")

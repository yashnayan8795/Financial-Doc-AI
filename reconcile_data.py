# reconcile_data.py
import json
import csv

def reconcile(extracted, golden):
    result = []

    for key in golden:
        extracted_value = extracted.get(key, "MISSING")
        golden_value = golden[key]

        status = "MATCH" if extracted_value == golden_value else "MISMATCH"
        result.append({
            "Field": key,
            "Extracted": extracted_value,
            "Golden": golden_value,
            "Status": status
        })

    return result

# Load data
with open("data/workflow_output/extracted_data.json") as f1, open("data/golden_source/golden_source.json") as f2:
    extracted = json.load(f1)
    golden = json.load(f2)

# Reconcile
report = reconcile(extracted, golden)

# Save to CSV (Alteryx-readable)
with open("data/reports/reconciliation_report.csv", "w", newline="") as csvfile:
    fieldnames = ["Field", "Extracted", "Golden", "Status"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(report)

print("✅ Reconciliation report saved to data/reports/reconciliation_report.csv")

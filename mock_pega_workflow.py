import json
import os

def validate_entities(entities):
    errors = []

    if not entities.get("TRADE_ID") or not entities["TRADE_ID"].isalnum():
        errors.append("Invalid or missing TRADE_ID.")

    if entities.get("CURRENCY") not in ["USD", "EUR", "INR", "GBP"]:
        errors.append("Unsupported currency.")

    try:
        amount = float(entities.get("AMOUNT", 0))
        if amount <= 0:
            errors.append("Amount must be greater than 0.")
    except ValueError:
        errors.append("Amount is not a valid number.")

    if not entities.get("ACCOUNT_NO") or not entities["ACCOUNT_NO"].isdigit() or not (9 <= len(entities["ACCOUNT_NO"]) <= 12):
        errors.append("Invalid account number.")

    if not entities.get("SENDER_NAME"):
        errors.append("Sender name missing.")

    return errors

def route_workflow(entities):
    errors = validate_entities(entities)

    if errors:
        return {
            "status": "Manual Review",
            "errors": errors,
            "data": entities
        }
    else:
        return {
            "status": "Auto Approved",
            "data": entities
        }

# ✅ Test run
if __name__ == "__main__":
    extracted = {
        "TRADE_ID": "XYZ9998887",
        "CURRENCY": "EUR",
        "AMOUNT": "750000",
        "ACCOUNT_NO": "987654321",
        "SENDER_NAME": "ACME CORP"
    }

    result = route_workflow(extracted)

    # Show result
    print(result)

    # ✅ Write extracted data to JSON for reconciliation
    output_dir = "data/workflow_output"
    os.makedirs(output_dir, exist_ok=True)

    with open(os.path.join(output_dir, "extracted_data.json"), "w") as f:
        json.dump(result["data"], f, indent=2)
    print(f"✅ Extracted data saved to {os.path.join(output_dir, 'extracted_data.json')}")
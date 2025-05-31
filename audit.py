import json
import os

# Ensure the audit_logs folder exists
os.makedirs("data/audit_logs", exist_ok=True)

def compute_match_score(extracted, golden):
    matched = 0
    total = len(golden)
    mismatches = {}

    for key in golden:
        if key in extracted and str(extracted[key]).strip() == str(golden[key]).strip():
            matched += 1
        else:
            mismatches[key] = {
                "expected": golden.get(key),
                "found": extracted.get(key)
            }

    score = round((matched / total) * 100, 2)
    return score, mismatches

if __name__ == "__main__":
    with open("data/workflow_output/extracted_data.json") as f1, open("data/golden_source/golden_source.json") as f2:
        extracted = json.load(f1)
        golden = json.load(f2)

    score, mismatches = compute_match_score(extracted, golden)

    audit_log = {
        "match_score": score,
        "mismatches": mismatches,
        "extracted": extracted,
        "golden_source": golden
    }

    with open("data/audit_logs/audit_result.json", "w") as out:
        json.dump(audit_log, out, indent=2)

    print(f"Match Score: {score}%")
    if mismatches:
        print("Mismatches found:")
        for k, v in mismatches.items():
            print(f"- {k}: expected {v['expected']}, found {v['found']}")
    else:
        print("All fields match.")
    print("Audit log saved to data/audit_logs/audit_result.json")

def write_audit_log(result, output_path="data/audit_logs/audit_result.json"):
    with open(output_path, "w") as out:
        json.dump(result, out, indent=4)

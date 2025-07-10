import csv
import os
import json

def log_review(result: dict):
    # CSV
    file_path = "review_log.csv"
    file_exists = os.path.exists(file_path)

    with open(file_path, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "review_type", "code_type", "logic_result", "optimization_score", "summary"])
        writer.writerow([
            result["timestamp"],
            result["review_type"],
            result["code_type"],
            result["logic_result"],
            result["optimization_score"],
            result["summary"][:100].replace("\n", " ")
        ])

    # Optional: JSON file log
    with open("review_result.json", "w") as jf:
        json.dump(result, jf, indent=2)

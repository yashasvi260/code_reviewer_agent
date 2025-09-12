import sys
import os
from datetime import datetime
from dotenv import load_dotenv
from agent import review_code
from logger import log_review

# Load environment variables from .env
load_dotenv()

def read_file(path):
    try:
        with open(path, 'r') as file:
            return file.read()
    except Exception as e:
        print(f" ERROR reading file '{path}': {e}")
        sys.exit(1)

def main():
    ci_mode = "--ci-mode" in sys.argv
    json_mode = "--json-output" in sys.argv

    print(f"\n📁 Current directory: {os.getcwd()}")
    print(f"🛠️  ci_mode={ci_mode}, json_mode={json_mode}")

    # Get API Key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print(" ERROR: OPENAI_API_KEY is not set. Please define it in a .env file or export it as an environment variable.")
        sys.exit(1)
    else:
        print("API KEY:  Loaded")

    # Load file paths
    if ci_mode:
        print("Running in CI Mode with default files")
        business_path = "sample_business.txt"
        code_path = "sample_code_pyspark.py"
        code_type = "pyspark"
        review_type = "both"
    else:
        print("\n Code Review Agent — INTERACTIVE MODE\n")
        business_path = input(" Enter path to business logic: ").strip()
        code_path = input("Enter path to code (SQL or PySpark): ").strip()
        code_type = input("Enter code type (sql or pyspark): ").lower().strip()
        review_type = input("What do you want to review? (logic / optimization / both): ").lower().strip()

    # Load contents
    business_logic = read_file(business_path)
    code = read_file(code_path)

    print("\n Running agent...\n")
    try:
        result = review_code(
            business_logic=business_logic,
            code=code,
            code_type=code_type,
            review_type=review_type,
            return_json=json_mode,
            api_key=api_key
        )
    except Exception as e:
        print(f"ERROR during agent execution: {e}")
        sys.exit(1)

    # Output result
    if json_mode:
        print("\n🧾 JSON Output:\n")
        print(result)
    else:
        print("\n Review Summary:\n")
        print(result["summary"])

    #  Log result
    log_review(result)
    print("\n📦 Result logged to review_log.csv and review_result.json\n")

if __name__ == "__main__":
    main()

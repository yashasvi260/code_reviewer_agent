# Code Reviewer with LLMs

A lightweight code review agent that uses **OpenAI GPT-4** to evaluate **SQL** or **PySpark** code against provided business logic and optimization standards. Ideal for data engineers and analysts who want automated validation of their data transformation logic.


## Features

- Compares SQL or PySpark code against business logic
- Suggests optimization improvements
- Returns logic match result, optimization score, and summary
- Toggle review mode: logic only, optimization only, or both
- OpenAI API integration with `.env` file support
- Includes both real and mocked unit tests
- Test coverage reporting with `pytest-cov`


## Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/YOUR_USERNAME/code_reviewer.git
cd code_reviewer
```

### 2. Create and Activate Virtual Environment
bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

### 3. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt

### 4 . Set Up OpenAI API Key
Create a .env file in the project root:

ini
Copy
Edit
OPENAI_API_KEY=sk-xxxxx...



### Running the App
To start a review from terminal:

bash
Copy
Edit
python app.py
You’ll be prompted for:

Business Logic

Code (SQL or PySpark)

Code type

Review type (logic, optimization, both)


### Unit Testing
Run all tests:
bash
Copy
Edit
pytest --cov=agent --cov-report=term-missing

### Run only mocked tests (for CI/CD):
bash
Copy
Edit
pytest -m "not integration"

### Run real tests that call OpenAI API:
bash
Copy
Edit
pytest -m integration
## Real tests require valid OpenAI credentials in .env.

## Example Output
json
Copy
Edit
{
  "logic_result": "PASS",
  "optimization_score": "Score: 8/10 - Consider indexing filters.",
  "summary": "Logic is correct and performance is acceptable."
}

### Example Usage in Code
python
Copy
Edit
from agent import review_code

result = review_code(
    business_logic="List all active users created after 2020",
    code="SELECT * FROM users WHERE status = 'active' AND created_at > '2020-01-01'",
    code_type="sql",
    review_type="both",
    return_json=True
)
print(result)

## Test Coverage Report
bash
Copy
Edit
pytest --cov=agent --cov-report=html
open htmlcov/index.html


## Security
Your API key is never committed to source control. The .env file is included in .gitignore.

## Requirements
Python 3.10+

OpenAI account with API access

## Contributing
Contributions are welcome! Please open issues or submit pull requests for enhancements, bug fixes, or ideas.

## License
MIT License. See LICENSE file.

## Acknowledgements
LangChain

OpenAI GPT
 



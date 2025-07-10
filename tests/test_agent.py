import os
import sys
import pytest
from dotenv import load_dotenv

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent import review_code

load_dotenv()

@pytest.mark.integration
def test_review_code_returns_valid_structure():
    """
    Real-world integration test that checks OpenAI response structure.
    Requires a valid OPENAI_API_KEY in .env or environment.
    """

    api_key = os.getenv("OPENAI_API_KEY")
    assert api_key is not None, "OPENAI_API_KEY not found. Please set it in .env or your environment."

    dummy_logic = "Sum total payments by user where status is 'Paid'"
    dummy_code = "SELECT user_id, SUM(payment_amount) FROM payments WHERE status = 'Paid' GROUP BY user_id"

    result = review_code(
        business_logic=dummy_logic,
        code=dummy_code,
        code_type="sql",
        review_type="both",
        return_json=True,
        api_key=api_key
    )

    # Assertions on structure
    assert result is not None, "review_code returned None"
    assert isinstance(result, dict), "Result is not a dictionary"
    assert "logic_result" in result, "Missing logic_result"
    assert "optimization_score" in result, "Missing optimization_score"
    assert "summary" in result, "Missing summary"

    # Optional content checks
    assert result["logic_result"] in ["PASS", "FAIL", "UNKNOWN"]
    assert isinstance(result["optimization_score"], int) or "UNKNOWN" in str(result["optimization_score"])

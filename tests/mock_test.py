import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Ensure the agent module is discoverable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent import review_code


@patch("agent.LLMChain")
@patch("agent.ChatOpenAI")
def test_review_code_returns_valid_structure(mock_chat_openai, mock_llm_chain):
    # Mock ChatOpenAI instance
    mock_chat_openai.return_value = MagicMock()

    # Mock LLMChain instance and its invoke return
    mock_chain_instance = MagicMock()
    mock_chain_instance.invoke.side_effect = [
        {"text": "PASS: The SQL matches the business logic."},
        {"text": "8 - Efficient use of indexing and filters."}
    ]
    mock_llm_chain.return_value = mock_chain_instance

    # Inputs
    dummy_logic = "Sum total payments by user where status is 'Paid'"
    dummy_code = "SELECT user_id, SUM(payment_amount FROM payments WHERE status = 'Paid' GROUP BY user_id"

    result = review_code(
        business_logic=dummy_logic,
        code=dummy_code,
        code_type="sql",
        review_type="both",
        return_json=True,
        api_key="fake-key"
    )

    # Assertions
    assert result is not None, "Returned None"
    assert isinstance(result, dict), "Result is not a dict"
    assert "logic_result" in result
    assert "optimization_score" in result
    assert "summary" in result
    assert "timestamp" in result
    assert result["logic_result"] == "PASS"
    assert result["optimization_score"] == 8

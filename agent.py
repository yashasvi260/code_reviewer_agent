from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from datetime import datetime


def review_code(business_logic, code, code_type="sql", review_type="both", return_json=False, api_key=None):
    if code_type not in ["sql", "pyspark"]:
        raise ValueError("code_type must be 'sql' or 'pyspark'")
    if review_type not in ["logic", "optimization", "both"]:
        raise ValueError("review_type must be 'logic', 'optimization', or 'both'")

    # Initialize LLM
    llm = ChatOpenAI(model="gpt-4o", temperature=0, api_key=api_key)

    logic_result = None
    optimization_score = None
    summary = ""

    # Logic Review
    if review_type in ["logic", "both"]:
        prompt_logic = PromptTemplate(
            input_variables=["business_logic", "code", "code_type"],
            template=(
                "You are a senior data engineer. Given the following business logic:\n\n"
                "{business_logic}\n\nReview the following {code_type} code and tell me if it correctly implements "
                "the business logic. Return only PASS or FAIL with a short reason.\n\n"
                "Code:\n{code}"
            )
        )

        chain = LLMChain(llm=llm, prompt=prompt_logic)
        logic_response = chain.invoke({
            "business_logic": business_logic,
            "code": code,
            "code_type": code_type
        })

        response_text = logic_response.get("text", "")
        logic_result = (
            "PASS" if "PASS" in response_text.upper()
            else "FAIL" if "FAIL" in response_text.upper()
            else "UNKNOWN"
        )
        summary += f"\n🧠 Logic Review: {response_text.strip()}\n"

    # Optimization Review
    if review_type in ["optimization", "both"]:
        prompt_opt = PromptTemplate(
            input_variables=["code", "code_type"],
            template=(
                "You're an expert in {code_type} performance tuning. Review the following code and give it a score "
                "from 1 to 10 on optimization, followed by a one-line justification:\n\n{code}"
            )
        )

        chain = LLMChain(llm=llm, prompt=prompt_opt)
        opt_response = chain.invoke({
            "code": code,
            "code_type": code_type
        })

        opt_text = opt_response.get("text", "")
        optimization_score = None
        for token in opt_text.split():
            try:
                optimization_score = int(token)
                break
            except ValueError:
                continue

        summary += f"\n⚙️ Optimization Review: {opt_text.strip()}\n"

    # JSON or Human Output
    if return_json:
        return {
            "logic_result": logic_result,
            "optimization_score": optimization_score,
            "summary": summary.strip(),
            "timestamp": datetime.utcnow().isoformat()
        }
    else:
        return summary.strip()

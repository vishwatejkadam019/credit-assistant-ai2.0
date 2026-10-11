import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def generate_credit_advice(financial_data: dict) -> dict:
    if not GEMINI_API_KEY:
        # Fallback tailored advice engine if no API key present
        return _generate_fallback_advice(financial_data)

    try:
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"""
        Act as a senior Indian credit counselor and financial expert. Analyze the following user metrics:
        - CIBIL Score: {financial_data['credit_score']}
        - Monthly Income: ₹{financial_data['monthly_income']}
        - Monthly Debt/Expenses: ₹{financial_data['monthly_expenses']}
        - Total Debt: ₹{financial_data['total_debt']}
        - Total Credit Limit: ₹{financial_data['credit_limit']}
        - Credit Utilization: {financial_data['credit_utilization']:.1f}%
        - DTI Ratio: {financial_data['dti_ratio']:.1f}%

        Respond ONLY in raw valid JSON format matching this exact JSON schema:
        {{
          "analysis": "Poor|Fair|Good|Excellent",
          "summary": "Brief 2-3 sentence overview of credit status in Indian banking context.",
          "action_plan": [
            "Step 1: Specific actionable advice...",
            "Step 2: Specific actionable advice...",
            "Step 3: Specific actionable advice...",
            "Step 4: Specific actionable advice...",
            "Step 5: Specific actionable advice..."
          ]
        }}
        Do not include markdown markdown backticks (like ```json). Return pure JSON.
        """
        
        response = model.generate_content(prompt)
        text = response.text.strip()
        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()
        
        parsed = json.loads(text)
        return {
            "analysis": parsed.get("analysis", "Fair"),
            "action_plan": parsed.get("action_plan", [])
        }
    except Exception as e:
        return _generate_fallback_advice(financial_data)

def _generate_fallback_advice(data: dict) -> dict:
    score = data['credit_score']
    utilization = data['credit_utilization']
    dti = data['dti_ratio']

    if score < 600:
        category = "Poor"
    elif score < 750:
        category = "Fair"
    elif score < 800:
        category = "Good"
    else:
        category = "Excellent"

    plan = []
    if utilization > 30:
        plan.append("Pay down active credit card balances to bring your overall utilization below RBI-recommended 30%.")
    else:
        plan.append("Maintain credit utilization strictly below 30% across all card accounts.")

    if dti > 40:
        plan.append("Reduce monthly EMI commitments or boost secondary income to bring Debt-To-Income (DTI) under 40%.")
    else:
        plan.append("Keep monthly debt obligations well below 40% of net monthly income.")

    plan.append("Opt for secured credit cards against fixed deposits (FD) to establish a clean payment track record without hard inquiries.")
    plan.append("Enable auto-pay for all credit card and loan dues via UPI / NACH mandates to prevent any accidental delayed payment flags on CIBIL.")
    plan.append("Periodically review your full CIBIL/Experian credit report once every 3 months to detect and dispute potential errors or unauthorized inquiries.")

    return {
        "analysis": category,
        "action_plan": plan[:5]
    }
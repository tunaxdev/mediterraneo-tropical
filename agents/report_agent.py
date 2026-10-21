# agents/report_agent.py

"""
Business / report agent.

Acts as a restaurant consultant and summarizes:
- concept
- operational feasibility
- pricing strategy
"""

from services.llm_service import call_llm
from config import BRAND_NAME


def generate_business_report(
    style: str,
    main_dish_recipe: str,
    drink_recipe: str,
    cost_text: str,
    target_profit_margin: float,
) -> str:
    """
    Ask the LLM to produce a short owner-oriented recommendation.
    """

    system_prompt = f"""
You are a restaurant & bar business consultant helping the owners of "{BRAND_NAME}".
The concept is a fusion between Turkish Mediterranean cuisine and Colombian / Latin
tropical flavors.

Your job is to:
- Evaluate if the proposed dish and drink fit the concept
- Comment on menu positioning and target customers
- Interpret the pricing & profit margin in simple language
- Suggest next steps for experimentation and A/B testing
"""

    user_prompt = f"""
Fusion style: {style}
Target profit margin: {int(target_profit_margin * 100)}%

Main dish recipe:
{main_dish_recipe}

Drink pairing:
{drink_recipe}

Cost and pricing summary:
{cost_text}

Write a concise business recommendation (around 3–6 paragraphs) that a restaurant
owner can quickly read before a menu meeting. Highlight:
- menu positioning (e.g. signature dish, special, seasonal)
- perceived value vs. price
- risks or operational challenges
- 1–3 concrete next actions.
"""

    return call_llm(system_prompt, user_prompt)

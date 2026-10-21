# services/cost_service.py

import textwrap
from services.llm_service import call_llm


def estimate_cost_and_price(
    food_recipe_text: str,
    drink_recipe_text: str,
    target_profit_margin: float,
) -> str:
    """
    Cost & price estimator used by the orchestrator.

    Called from services.orchestrator.run_pipeline() as:
        estimate_cost_and_price(food_recipe, drink_recipe, margin)
    """

    system_prompt = textwrap.dedent(
        """
        You are a restaurant financial consultant specializing in menu engineering.
        Your job is to estimate realistic food & beverage cost percentages,
        ingredient cost breakdowns, recommended menu prices, and profit margins.
        Be concise but structured.
        """
    )

    user_prompt = textwrap.dedent(
        f"""
        Food recipe:
        {food_recipe_text}

        Drink recipe:
        {drink_recipe_text}

        Target profit margin: {target_profit_margin:.2f}

        Please provide a short analysis including:
        - Estimated ingredient cost for the main dish (approximate)
        - Estimated ingredient cost for the drink (approximate)
        - Recommended menu price for each
        - Approximate profit margin vs target
        - One actionable suggestion to improve profitability

        Answer in English, in a bullet-point or short paragraph style,
        suitable for showing directly in a business report.
        """
    )

    return call_llm(system_prompt, user_prompt)


def format_cost_info(cost_analysis_text: str) -> str:
    """
    Small helper that cleans up LLM response for app display.
    """
    if not cost_analysis_text:
        return "⚠️ No cost analysis generated."

    return cost_analysis_text.strip()

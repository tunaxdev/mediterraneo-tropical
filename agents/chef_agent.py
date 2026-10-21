# agents/chef_agent.py

import textwrap
from services.llm_service import call_llm


def generate_food_recipe(
    ingredients: str,
    style: str,
    target_profit_margin: float,
) -> str:
    """
    Main entry point for the Chef agent.
    Called from services.orchestrator.run_pipeline() as:

        generate_food_recipe(ingredients, style, margin)

    Parameters
    ----------
    ingredients : str
        Comma-separated list from the UI.
    style : str
        Fusion style (e.g. "Mediterranean–Tropical fusion").
    target_profit_margin : float
        0–1 between (0.25 = 25% etc.)

    Returns
    -------
    str
        Formatted recipe text for the UI.
    """

    system_prompt = textwrap.dedent(
        """
        You are the head chef of Mediterraneo Tropical, a fusion bar & kitchen
        combining Mediterranean and tropical Latin American flavors.

        You design realistic, kitchen-ready main course recipes for a busy
        restaurant environment. Recipes must:
        - Use mainly the available ingredients when possible.
        - Fit the requested fusion style.
        - Be clear and step-by-step for line cooks.
        - Be suitable for a bar / casual-dining setting.
        """
    )

    user_prompt = textwrap.dedent(
        f"""
        Available ingredients: {ingredients}
        Preferred style: {style}
        Target profit margin (0–1): {target_profit_margin:.2f}

        Please create ONE main course recipe that could be served at
        Mediterraneo Tropical.

        In your answer include:
        - Dish name
        - Yields (servings) and estimated prep / cook time
        - Ingredients list with quantities
        - Equipment
        - Step-by-step instructions
        - Chef's notes / variations that keep cost under control

        Write the answer in English, formatted nicely for a restaurant report.
        """
    )

    response = call_llm(system_prompt, user_prompt)
    return response


"""
Orchestrator: connects all domain agents and services.

Pipeline:
1) Chef agent -> main dish recipe
2) Mixologist agent -> cocktail pairing
3) Cost service -> numeric cost & recommended prices
4) Business/report agent -> narrative recommendation
"""

from agents.chef_agent import generate_food_recipe
from agents.mixologist_agent import generate_drink_pairing
from agents.report_agent import generate_business_report
from services.cost_service import estimate_cost_and_price, format_cost_info


def run_pipeline(user_request: dict) -> dict:
    """
    Main orchestration entry point used by the Streamlit UI.

    Parameters
    ----------
    user_request : dict
        {
            "ingredients": str,
            "style": str,
            "target_profit_margin": float,  # 0.25 for 25%
        }

    Returns
    -------
    dict
        {
            "food_recipe": str,
            "drink_recipe": str,
            "cost_info": str,
            "business_report": str,
            "image_url": None  # visual tab uses only text explanation for now
        }
    """
    ingredients = user_request.get("ingredients", "")
    style = user_request.get("style", "Mediterranean–Tropical fusion")
    margin = float(user_request.get("target_profit_margin", 0.25))

    # 1) Chef
    food_recipe = generate_food_recipe(ingredients, style, margin)

    # 2) Mixologist
    drink_recipe = generate_drink_pairing(ingredients, style, food_recipe)

    # 3) Cost service (rule-based, non-LLM)
    cost_summary = estimate_cost_and_price(food_recipe, drink_recipe, margin)
    cost_info_text = format_cost_info(cost_summary)


    # 4) Business / report agent
    business_report = generate_business_report(
        style=style,
        main_dish_recipe=food_recipe,
        drink_recipe=drink_recipe,
        cost_text=cost_info_text,
        target_profit_margin=margin,
    )
    
    # 🔸 For now we do not use any image generation.
    image_url = None

    return {
        "food_recipe": food_recipe,
        "drink_recipe": drink_recipe,
        "cost_info": cost_info_text,
        "business_report": business_report,
        "image_url": image_url,
    }

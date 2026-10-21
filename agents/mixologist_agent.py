# agents/mixologist_agent.py

"""
Mixologist agent

Generates a signature cocktail or mocktail that pairs with the main dish.
"""

from services.llm_service import call_llm
from config import BRAND_NAME


def generate_drink_pairing(
    ingredients: str,
    style: str,
    main_dish_recipe: str,
    is_alcoholic: bool = True,
) -> str:
    """
    Ask the LLM (as Head Bartender) to design a drink that pairs with the main dish.
    """

    system_prompt = f"""
You are the Head Bartender at "{BRAND_NAME}", a fusion restaurant and bar
combining Mediterranean and tropical Latin American influences.

You design creative, profitable cocktails / mocktails that:
- Match the flavor profile of the main dish
- Use ingredients that can realistically exist in a bar inventory
- Are visually appealing and easy to explain to guests
"""

    drink_type = "cocktail (with alcohol)" if is_alcoholic else "mocktail (non-alcoholic)"

    user_prompt = f"""
Here is the main dish recipe you are pairing with:

{main_dish_recipe}

Available bar & kitchen ingredients: {ingredients}
Fusion style: {style}

Create ONE signature {drink_type} that pairs well with this dish.

Output format:
- Drink name
- 1–2 sentence flavor description
- Ingredients list with measurements
- Shake / build / stir instructions step by step
- Glassware & garnish suggestions
"""

    return call_llm(system_prompt, user_prompt)

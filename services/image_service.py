# services/image_service.py

"""
Image service stub for Mediterraneo Tropical.

For the current prototype, we do NOT generate or load any images.
The UI only shows text explaining how multimodal could work in the future.

Later, this module can be extended to call a real text-to-image API and
return a URL or local file path.
"""

from typing import Optional


def generate_image_concept(
    ingredients: str,
    style: str,
    main_dish_recipe: str,
    drink_recipe: str,
) -> Optional[str]:
    """
    Placeholder function. Always returns None so that the UI knows
    there is no image available.
    """
    return None

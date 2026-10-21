# services/storage_service.py

import os
import json
from datetime import datetime
from typing import Any, Dict, List

# Proje kök klasörü
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# data klasörü ve json dosya yolu
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
os.makedirs(DATA_DIR, exist_ok=True)

MENUS_PATH = os.path.join(DATA_DIR, "saved_menus.json")


def _load_all() -> List[Dict[str, Any]]:
    """Internal helper – tüm kayıtları JSON'dan yükler."""
    if not os.path.exists(MENUS_PATH):
        return []

    try:
        with open(MENUS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except Exception:
        # Dosya bozulursa vs. uygulama patlamasın
        return []


def load_menu_concepts() -> List[Dict[str, Any]]:
    """Saved_Menus sayfasının kullandığı public fonksiyon."""
    return _load_all()


def save_menu_concept(entry: Dict[str, Any]) -> None:
    """
    Yeni bir menu concept kaydeder.
    entry içinde örnek alanlar:
      - ingredients
      - style
      - target_profit_margin
      - food_recipe
      - drink_recipe
      - cost_info
      - business_report
    """
    items = _load_all()

    # created_at ekle (yoksa)
    entry = dict(entry)  # kopya
    entry.setdefault(
        "created_at",
        datetime.now().strftime("%Y-%m-%d %H:%M"),
    )

    items.append(entry)

    with open(MENUS_PATH, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

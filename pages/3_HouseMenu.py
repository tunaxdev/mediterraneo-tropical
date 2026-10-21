# pages/3_HouseMenu.py

import os
import sys
import json
import html

# ---- Python path ayarı ----
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

import streamlit as st
from config import BRAND_NAME

# AI hizmeti (opsiyonel)
try:
    from services.llm_service import call_llm
except Exception:
    call_llm = None


# ---------- CSS (Aegean Coastal Fire vibe) ----------
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top left, #E0F7FA 0%, #FFF5E1 40%, #FFE4E1 80%);
    background-size: 160% 160%;
    animation: medtGradientShift 18s ease infinite;
    color: #222222;
}

@keyframes medtGradientShift {
    0% { background-position: 0% 0%; }
    50% { background-position: 100% 100%; }
    100% { background-position: 0% 0%; }
}

/* Header */
.medt-header {
    background: linear-gradient(120deg, #0277BD 0%, #00ACC1 40%, #FF6F00 80%);
    color: #FFFFFF;
    border-radius: 1.5rem;
    padding: 1.6rem 1.7rem;
    box-shadow: 0 12px 30px rgba(2, 119, 189, 0.35);
    margin-bottom: 1.2rem;
}

/* Kart */
.medt-house-card {
    background: rgba(255, 255, 255, 0.92);
    border-radius: 1.4rem;
    padding: 1.1rem 1.3rem;
    border: 1px solid rgba(255, 183, 77, 0.9);
    box-shadow:
        0 16px 32px rgba(0, 0, 0, 0.06),
        0 2px 8px rgba(0, 0, 0, 0.04);
    margin-bottom: 1.1rem;
}

/* Kart başlığı */
.medt-card-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #1F2933;
    margin-bottom: 0.25rem;
}

/* Küçük meta */
.medt-meta {
    font-size: 0.8rem;
    color: #6B7280;
}

/* Kategori etiketleri */
.medt-tag-drink {
    display:inline-block;
    padding: 0.18rem 0.6rem;
    border-radius: 999px;
    background: rgba(33, 150, 243, 0.1);
    color: #1565C0;
    font-size: 0.75rem;
    margin-right: 0.35rem;
}

/* Food tag */
.medt-tag-food {
    display:inline-block;
    padding: 0.18rem 0.6rem;
    border-radius: 999px;
    background: rgba(165, 151, 184, 0.25);
    color: #40305E;
    font-size: 0.75rem;
    margin-right: 0.35rem;
}

/* Signature etiketi */
.medt-tag-signature {
    display:inline-block;
    padding: 0.18rem 0.65rem;
    border-radius: 999px;
    background: linear-gradient(120deg, #FF6F00, #FFB300);
    color: #FFFFFF;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
}

/* Görsel kutusu */
.medt-thumb {
    border-radius: 1.1rem;
    overflow: hidden;
    width: 220px;
    height: 140px;
    background: linear-gradient(135deg, #FFE0B2, #FFCC80);
    display:flex;
    align-items:center;
    justify-content:center;
    color:#BF360C;
    font-weight:600;
    font-size:0.78rem;
    text-align:center;
}

/* Açıklama */
.medt-desc {
    font-size: 0.9rem;
    color: #374151;
    margin-bottom: 0.55rem;
}

/* Buton satırı */
.medt-btn-row {
    display:flex;
    gap:0.4rem;
    flex-wrap:wrap;
    margin-top:0.4rem;
}

/* AI cevap kutusu */
.medt-ai-box {
    margin-top:0.35rem;
    padding:0.6rem 0.75rem;
    border-radius:0.9rem;
    background:rgba(224, 242, 241, 0.92);
    border:1px solid rgba(0, 150, 136, 0.5);
    font-size:0.88rem;
}

/* AI button styling */
div.stButton > button[kind="secondary"], 
div.stButton > button {
    background: linear-gradient(120deg, #FF6F00, #FFB300);
    color: white !important;
    border-radius: 12px;
    padding: 0.45rem 1rem;
    border: none;
    font-weight: 600;
    transition: 0.2s ease;
}

div.stButton > button:hover {
    background: linear-gradient(120deg, #FF8F00, #FFC233);
    transform: translateY(-1px);
}

/* ===== RADIO TEXT COLOR FULL FIX ===== */

/* Radio header (Filter items) */
.stRadio > label,
.stRadio label,
div[role="radiogroup"] > label,
div[role="radiogroup"] > span,
div[role="radiogroup"] > p {
    color: #000 !important;
}

/* Radio option labels */
div[role="radiogroup"] label,
div[role="radiogroup"] span,
div[role="radiogroup"] p,
.stRadio > div > div,
.stRadio label > div div {
    color: #000 !important;
}

</style>
"""


# ---------- Yardımcılar ----------

def load_house_menu():
    json_path = os.path.join(PROJECT_ROOT, "data", "house_menu.json")
    if not os.path.exists(json_path):
        return []
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading house_menu.json: {e}")
        return []


def generate_ai_pairing(name: str, style: str, category: str) -> str:
    """
    category: 'food' or 'drink' (string) - used to tailor the prompt
    Returns a short bulleted list suitable for display.
    """
    if call_llm is None:
        return "AI service is not available in this environment."

    # Use neutral "Item" label and pass the category explicitly so model doesn't assume 'cocktail'
    system_prompt = (
        "You are an expert Mediterraneo Tropical bar & menu consultant. "
        "Given an item name, category (food or drink) and style, suggest 2–3 concise pairing ideas "
        "(bar snacks, meze, side bites) that fit the concept. Answer in short bullets only."
    )

    # Make the user prompt explicit and neutral
    user_prompt = (
        f"Item name: {name}\n"
        f"Category: {category}\n"
        f"Style: {style}\n\n"
        "Give 2-3 short bullet points suitable as quick pairing suggestions. Keep each bullet 1-2 short sentences."
    )

    try:
        return call_llm(system_prompt, user_prompt)
    except TypeError:
        # if call_llm expects a single string, join them
        return call_llm(system_prompt + "\n\n" + user_prompt)
    except Exception as e:
        return f"LLM ERROR: {e}"



# ---------- Ana Sayfa ----------

def main():
    st.set_page_config(
        page_title=f"{BRAND_NAME} – House Menu",
        layout="wide",
        page_icon="🍹",
    )

    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="medt-header">
            <h2 style="margin:0; font-size:1.9rem;">🏠 House Menu – Signature & Fusion Cocktails</h2>
            <p style="margin:0.4rem 0 0; font-size:0.95rem;">
                Aegean breeze meets tropical fire: curated house cocktails of <strong>{BRAND_NAME}</strong>, 
                blending Turkish sherbets, Colombian fruits and Latin spirits. Use this page to present 
                your fixed menu alongside AI-powered pairing suggestions.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    items = load_house_menu()
    if not items:
        st.info("No house menu items found. Please fill data/house_menu.json first.")
        return

    # ---- Filtre seçenekleri ----
    col_filter, _ = st.columns([1, 3])
    with col_filter:
        filter_choice = st.radio(
            "Filter items",
            options=["All", "Signature only", "Food", "Beverage"],
            index=0,
            horizontal=True,
        )

    # Orijinal listeyi bozmamak için
    filtered_items = items

    if filter_choice == "Signature only":
        filtered_items = [i for i in items if i.get("signature")]
    elif filter_choice == "Food":
        filtered_items = [i for i in items if i.get("category") == "food"]
    elif filter_choice == "Beverage":
        filtered_items = [i for i in items if i.get("category") == "drink"]

    st.write("")

    # Kartlar (filtrelenmiş listeyi kullan)
    for idx, entry in enumerate(filtered_items, start=1):
        name = entry.get("name", "Item")
        style = entry.get("style", "")
        description = entry.get("description", "")
        ingredients = entry.get("ingredients", [])
        preparation = entry.get("preparation", [])
        taste_profile = entry.get("taste_profile", [])
        signature = bool(entry.get("signature", False))
        image_rel = entry.get("image", "")
        category = entry.get("category", "drink")  # "food" / "drink"

        is_food = category == "food"

        # Kategori etiketi
        if is_food:
            category_tag_html = "<span class='medt-tag-food'>Food</span>"
        else:
            category_tag_html = "<span class='medt-tag-drink'>Cocktail</span>"

        # Signature etiketi: Dish vs Cocktail
        if signature:
            sig_label = "Signature Dish" if is_food else "Signature Cocktail"
            sig_html = f"<span class='medt-tag-signature'>{sig_label}</span>"
        else:
            sig_html = ""

        image_path = os.path.join(PROJECT_ROOT, image_rel) if image_rel else None

        with st.container():
            st.markdown('<div class="medt-house-card">', unsafe_allow_html=True)

            cols = st.columns([2, 3])

            # SOL TARAF: başlık + görsel
            with cols[0]:
                st.markdown(
                    f"<div class='medt-card-title'>{idx}. {name}</div>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"{category_tag_html} "
                    f"<span class='medt-meta'>{style}</span> &nbsp; {sig_html}",
                    unsafe_allow_html=True,
                )

                st.write("")

                if image_path and os.path.exists(image_path):
                    # Kartın içinde tek bir görsel
                    st.image(image_path, width=500)
                else:
                    # Görsel yoksa sadece placeholder kutu
                    st.markdown(
                        "<div class='medt-thumb'>Add image<br/>in house_menu.json</div>",
                        unsafe_allow_html=True,
                    )

            # SAĞ TARAF: açıklama + açılır sekmeler + AI
            with cols[1]:
                if description:
                    st.markdown(
                        f"<div class='medt-desc'>{description}</div>",
                        unsafe_allow_html=True,
                    )

                # Açılır sekmeler
                with st.expander("🧾 Ingredients", expanded=False):
                    if ingredients:
                        for ing in ingredients:
                            st.write(f"- {ing}")
                    else:
                        st.write("No ingredients defined.")

                with st.expander("🧊 Preparation / Method", expanded=False):
                    if preparation:
                        for step_no, step in enumerate(preparation, start=1):
                            st.write(f"{step_no}. {step}")
                    else:
                        st.write("No preparation steps defined.")

                with st.expander("🎨 Taste profile", expanded=False):
                    if isinstance(taste_profile, list) and taste_profile:
                        for line in taste_profile:
                            st.write(f"- {line}")
                    elif isinstance(taste_profile, str) and taste_profile.strip():
                        st.write(taste_profile)
                    else:
                        st.write("No taste profile description yet.")

                # AI eşleştirme önerisi
                ai_key = f"ai_pair_{idx}"
                btn_label = "✨ AI pairing suggestions (snacks / meze)"

                # Make button text slightly different if it's a food or drink (optional)
                if is_food:
                    btn_label = "✨ AI pairing suggestions (snacks / meze)"
                else:
                    btn_label = "✨ AI pairing suggestions (snacks / meze)"

                if st.button(btn_label, key=ai_key):
                    with st.spinner("Asking the AI for pairing ideas..."):
                        # pass category so the model won't assume "cocktail"
                        suggestion = generate_ai_pairing(name, style, category)
                        # Normalize result a bit: we'll store raw text (model returns bullets)
                        st.session_state[ai_key + "_text"] = suggestion

                # Show result with a clear header so model's internal "Cocktail:" wording (if any) isn't prominent
                if st.session_state.get(ai_key + "_text"):
                    ai_text = st.session_state[ai_key + "_text"]
                    # build a neat HTML box with our own small header
                    # escape model output so it can't inject HTML into the page
                    ai_text_safe = html.escape(ai_text).replace("\n", "<br/>")
                    safe_html = (
                        f"<div style='font-weight:700; margin-bottom:6px;'>Pairing suggestions for <em>{html.escape(name)}</em></div>"
                        f"<div class='medt-ai-box'>{ai_text_safe}</div>"
                    )
                    st.markdown(safe_html, unsafe_allow_html=True)


            st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()

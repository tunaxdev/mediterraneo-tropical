# pages/2_SavedRecipes.py  (dosya adın farklıysa aynı içeriği oraya yapıştır)

import os
import html
import sys

# --- Python path ayarı (projeyi import edebilmek için) ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

import streamlit as st
from config import BRAND_NAME
from services.storage_service import load_menu_concepts

# --- CSS: Generate sayfasıyla uyumlu, ama split-card tasarımı ile ---
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #FFF5E1 0%, #FFE4E1 25%, #E0F7FA 50%, #FFF8DC 75%, #FFE4B5 100%);
    background-size: 400% 400%;
    animation: medtGradientShift 15s ease infinite;
    color: #222222;
}

@keyframes medtGradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Genel kart */
.medt-card {
    background: rgba(255, 255, 255, 0.96);
    border-radius: 1.5rem;
    padding: 1.4rem 1.6rem;
    border: 1px solid rgba(255, 183, 77, 0.45);
    box-shadow:
        0 10px 30px rgba(0, 0, 0, 0.06),
        0 2px 8px rgba(0, 0, 0, 0.03);
    margin-bottom: 1rem;
}

/* Header */
.medt-header {
    background: linear-gradient(120deg, #D32F2F 0%, #FF6F00 35%, #0097A7 65%, #FFB300 100%);
    color: #FFFFFF;
    border-radius: 1.5rem;
    padding: 1.6rem 1.7rem;
    box-shadow: 0 12px 30px rgba(211, 47, 47, 0.3);
    margin-bottom: 1.2rem;
}

/* Küçük başlık */
.medt-section-title {
    font-size: 1.05rem;
    font-weight: 700;
    letter-spacing: 0.03em;
    text-transform: uppercase;
    color: #E65100;
    margin-bottom: 0.6rem;
}

/* Küçük bilgi yazısı */
.medt-note {
    font-size: 0.85rem;
    color: #4B5563;
}

/* Tag / pill */
.medt-tag {
    display: inline-block;
    padding: 0.15rem 0.7rem;
    border-radius: 999px;
    font-size: 0.75rem;
    background: rgba(255, 111, 0, 0.12);
    color: #E65100;
    margin-left: 0.4rem;
}

/* ID / tarih satırı */
.medt-meta {
    font-size: 0.8rem;
    color: #6B7280;
}

/* Split card layout */
.medt-card-split {
    padding: 1.2rem 1.3rem;
}

.medt-card-title {
    font-size: 1.05rem;
    font-weight: 800;
    color: #111827;
    margin-bottom: 0.35rem;
}

/* Sol kolon: başlık + görsel */
.medt-card-left {
    display: flex;
    flex-direction: column;
    gap: 0.55rem;
    height: 100%;
}

.medt-card-image {
    border-radius: 1.05rem;
    overflow: hidden;
    border: 1px solid rgba(209, 213, 219, 0.7);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
}

/* Sağ kolon: expanders */
.medt-card-right {
    padding-left: 0.75rem;
}

/* Expanders arasında boşluk */
.medt-expander + .medt-expander {
    margin-top: 0.45rem;
}

/* Küçük dikdörtgen görsel */
.medt-card-image-small {
    width: 240px;        /* istediğinde değiştirilebilir */
    height: 320px;       /* dikey dikdörtgen */
    border-radius: 1rem;
    overflow: hidden;
    border: 1px solid rgba(209,213,219,0.65);
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    margin-top: 0.5rem;
}

.medt-card-image-small img {
    width: 100%;
    height: 100%;
    object-fit: cover;  /* crop değil, şık görünüm */
}

/* Saved menu cards */
.saved-card {
    background: rgba(255, 255, 255, 0.88);
    border-radius: 1.3rem;
    border: 1px solid rgba(255, 183, 77, 0.9);
    box-shadow: 0 10px 24px rgba(0, 0, 0, 0.06);
    padding: 1.2rem 1.4rem;
    margin-bottom: 1.2rem;
    backdrop-filter: blur(3px);
}

.saved-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.6rem;
    gap: 0.75rem;
}

.saved-title {
    font-weight: 700;
    font-size: 1rem;
    color: #1F2933;
}

.saved-meta {
    font-size: 0.78rem;
    color: #6B7280;
}

.saved-tag {
    display: inline-flex;
    align-items: center;
    padding: 0.2rem 0.7rem;
    border-radius: 999px;
    background: rgba(255, 111, 0, 0.14);
    color: #C05621;
    font-size: 0.72rem;
}

/* Küçük afiş / thumbnail kutusu */
.saved-thumb-box {
    width: 220px;          /* burada 220x130 civarı küçük dikdörtgen */
    height: 130px;
    border-radius: 0.9rem;
    background: linear-gradient(135deg,#FFFDE7,#FFE0B2);
    border: 1px solid rgba(255,183,77,0.7);
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:0.75rem;
    color:#C05621;
    margin-top:0.4rem;
    text-align:center;
}



</style>
"""


def main():
    st.set_page_config(
        page_title=f"{BRAND_NAME} – Saved Menus",
        layout="wide",
        page_icon="💾",
    )

    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    # --- Header ---
    st.markdown(
        """
        <div class="medt-header">
            <h2 style="margin:0; font-size:1.8rem;">💾 Saved Menu Concepts</h2>
            <p style="margin:0.4rem 0 0; font-size:0.95rem;">
                Here you can review all <strong>Mediterraneo Tropical</strong> menu & cocktail ideas 
                that were generated on the <em>Menu Designer</em> page and saved for later.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- Veriyi oku ---
    items = load_menu_concepts()

    if not items:
        st.info(
            "No saved concepts yet. Go to the **Menu Designer** page, generate a menu and "
            "click **Save this menu concept**."
        )
        return

    # Küçük özet alanı
    st.markdown(
        f"""
        <div class="medt-card">
            <div class="medt-section-title">Overview</div>
            <p class="medt-note">
                Total saved concepts: <strong>{len(items)}</strong><br>
                Use this page during your presentation to show how the system can keep a history
                of successful menu and drink ideas for future reference.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Sıralama: en yeni en üstte olsun
    items = sorted(items, key=lambda x: x.get("created_at", ""), reverse=True)

    # --- Her kayıt için kart göster ---
    default_thumb = os.path.join(PROJECT_ROOT, "assets", "menu_placeholder.jpg")

    # --- Her kayıt için kart göster (yeni tasarım) ---
    for idx, entry in enumerate(items, start=1):
        ingredients = entry.get("ingredients", "")
        style = entry.get("style", "")
        margin = entry.get("target_profit_margin", 0.0)
        food_text = entry.get("food_recipe", "")
        drink_text = entry.get("drink_recipe", "")
        cost_text = entry.get("cost_info", "")
        business_text = entry.get("business_report", "")
        created_at = entry.get("created_at", "n/a")

        # Başlık olarak food_recipe'nin ilk satırını kullan
        title_line = food_text.splitlines()[0].strip() if food_text else "Menu Concept"

        # Kartın dış kabuğu
        st.markdown('<div class="saved-card">', unsafe_allow_html=True)

        # -------- ÜST SATIR (başlık + meta) --------
        head_left, head_right = st.columns([3, 1])

        with head_left:
            st.markdown(
                f'<div class="saved-header">'
                f'<div class="saved-title">{idx}. {html.escape(str(title_line))}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="saved-meta">Created: {created_at}</div>',
                unsafe_allow_html=True,
            )

        with head_right:
            st.markdown(
                f'<span class="saved-tag">Target margin: {round(margin * 100)}%</span>',
                unsafe_allow_html=True,
            )

        
        # -------- ALT KISIM: SOL = özet & görsel, SAĞ = detay sekmeleri --------
        left_col, right_col = st.columns([1.4, 2.1])

        # SOL TARAF: malzemeler + stil + küçük afiş
        with left_col:
            st.markdown("**Ingredients snapshot:**")
            st.write(ingredients)

            st.markdown("**Fusion style:**")
            st.write(style)

            # Küçük afiş / thumbnail (şu anlık placeholder)
            thumb_path = entry.get("image_path")  # ileride gerçek path eklersen buradan gelecek

            if thumb_path and os.path.exists(thumb_path):
                # Gerçek görsel varsa küçük boyda göster
                st.image(thumb_path, width=220)
            else:
                # Şimdilik stok / placeholder kutusu
                st.markdown(
                    '<div class="saved-thumb-box">'
                    'No image saved for this menu yet.<br/>'
                    'Later this can show the generated dish photo.'
                    '</div>',
                    unsafe_allow_html=True,
                )

        # SAĞ TARAF: expanders
        with right_col:
            with st.expander("🍽️ Food recipe details", expanded=False):
                st.write(food_text)

            with st.expander("🍸 Drink pairing details", expanded=False):
                st.write(drink_text)

            with st.expander("💰 Cost & profit notes", expanded=False):
                st.write(cost_text)

            with st.expander("📊 Business recommendation", expanded=False):
                st.write(business_text)

        st.markdown("</div>", unsafe_allow_html=True)  # saved-card kapanış




if __name__ == "__main__":
    main()

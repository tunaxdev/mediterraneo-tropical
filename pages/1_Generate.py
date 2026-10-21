# pages/1_Generate.py
from services.storage_service import save_menu_concept  # NEW


import os
import sys
import streamlit as st

# --- PYTHON PATH FIX ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from services.orchestrator import run_pipeline
from config import BRAND_NAME

# ---------- Custom Styling (same as app.py) ----------
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

/* App background */
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

/* Card-like containers */
.medt-card {
    background: rgba(255, 255, 255, 0.96);
    border-radius: 1.5rem;
    padding: 1.5rem 1.7rem;
    border: 1px solid rgba(255, 183, 77, 0.45);
    box-shadow:
        0 10px 30px rgba(0, 0, 0, 0.06),
        0 2px 8px rgba(0, 0, 0, 0.03);
}

/* Section headers */
.medt-section-title {
    font-size: 1.05rem;
    font-weight: 700;
    letter-spacing: 0.03em;
    text-transform: uppercase;
    color: #E65100;
    margin-bottom: 0.6rem;
}

/* Small pill/badge */
.medt-badge {
    display: inline-flex;
    align-items: center;
    padding: 0.2rem 0.7rem;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.25);
    border: 1px solid rgba(255, 255, 255, 0.6);
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: #FFFDE7;
}

/* Brand gradient text */
.medt-brand {
    background: linear-gradient(120deg, #D32F2F, #FF6F00, #0097A7, #FFB300);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Header / hero */
.medt-hero {
    background: linear-gradient(120deg, #D32F2F 0%, #FF6F00 35%, #0097A7 65%, #FFB300 100%);
    color: #FFFFFF;
    border-radius: 1.5rem;
    padding: 1.8rem 1.7rem 1.6rem 1.7rem;
    box-shadow: 0 12px 30px rgba(211, 47, 47, 0.3);
}

/* Info banner (how to demo) */
.medt-hero-banner {
    background: linear-gradient(90deg, rgba(255,255,255,0.9), rgba(255,255,255,0.95));
    border-radius: 1rem;
    border: 1px solid rgba(255, 183, 77, 0.55);
    padding: 0.9rem 1.2rem;
    margin-top: 0.9rem;
    color: #4B5563;
}

/* Input panel labels */
.medt-input-label {
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.16em;
    color: #FF6F00;
    font-weight: 600;
    margin-bottom: 0.2rem;
}

.medt-input-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #D32F2F;
    margin-bottom: 0.3rem;
}

/* Inputs */
.stTextArea textarea, .stTextInput input {
    border-radius: 16px !important;
    border: 2px solid #FFE0B2 !important;
    padding: 0.9rem !important;
    font-size: 0.95rem !important;
    transition: all 0.25s ease !important;
}

.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: #FF6F00 !important;
    box-shadow: 0 0 0 3px rgba(255, 111, 0, 0.12) !important;
}

/* Slider */
.stSlider { padding-top: 0.4rem; }

/* Buttons */
.stButton > button {
    border-radius: 999px !important;
    background: linear-gradient(120deg, #D32F2F, #FF6F00, #0097A7) !important;
    border: none !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    padding: 0.6rem 1rem !important;
    letter-spacing: 0.03em;
    box-shadow: 0 10px 26px rgba(211, 47, 47, 0.35);
    text-transform: uppercase;
    font-size: 0.9rem !important;
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 14px 32px rgba(211, 47, 47, 0.45);
}

/* Tabs styling */
[data-baseweb="tab-list"] {
    gap: 0.35rem;
    background: rgba(255, 255, 255, 0.95);
    padding: 0.4rem;
    border-radius: 999px;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.06);
}

[data-baseweb="tab"] {
    border-radius: 999px !important;
    padding: 0.35rem 0.9rem !important;
    font-size: 0.9rem !important;
    color: #6B7280 !important;
}

/* Selected tab */
[data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(120deg, #D32F2F, #FF6F00) !important;
    color: #FFFFFF !important;
}

/* Info / note text */
.medt-note {
    font-size: 0.85rem;
    color: #4B5563;
}

.stAlert { border-radius: 1rem !important; }

/* ---------- Input Label Colors ---------- */

/* All Streamlit widget labels */
.stTextInput label,
.stTextArea label,
.stSlider label {
    color: #000000 !important;   /* Kırmızı ton */
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.5px;
}

/* Gradient stroke around the brand text */
.medt-brand {
    font-weight: 900 !important;
    font-size: 2.3rem !important;

    /* White main text */
    color: #FFFFFF !important;

    /* Transparent text fill (allows stroke to show clean) */
    -webkit-text-fill-color: #FFFFFF !important;

    /* Stroke around text (thin outline) */
    -webkit-text-stroke: 2px transparent;

    /* Gradient border effect */
    background: linear-gradient(120deg, #ff6f00, #ffb300, #00acc1, #d32f2f);
    background-clip: text;
    -webkit-background-clip: text;

    /* Glow effect for emphasis */
    text-shadow:
        0 0 6px rgba(255, 111, 0, 0.6),
        0 0 12px rgba(255, 179, 0, 0.5),
        0 0 18px rgba(0, 150, 136, 0.4);
}


</style>
"""


def main():
    st.set_page_config(
        page_title=f"{BRAND_NAME} – Menu Generator",
        layout="wide",
        page_icon="🌴",
    )

    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    # --- HEADER ---
    st.markdown(
        f"""
        <div class="medt-hero" style="margin-bottom: 1rem;">
            <div class="medt-badge">Generative AI Final Project</div>
            <h1 style="margin-top: 0.6rem; margin-bottom: 0.25rem; font-size: 2.2rem; line-height:1.2;">
                🌴 <span class="medt-brand">{BRAND_NAME}</span>
            </h1>
            <p style="font-size: 0.98rem; color: #FFFDF7; max-width: 720px; margin-bottom:0;">
                AI-powered fusion menu &amp; bar assistant that blends Mediterranean cuisine
                with tropical Latin American flavors.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="medt-hero-banner">
            <strong>How to demo:</strong> Enter realistic ingredients in the input panel below, choose a style,
            then click <em>Generate Menu Proposal</em>. The system will act as a multi-agent team:
            a head chef, a mixologist, and a business consultant.
        </div>
        """,
        unsafe_allow_html=True,
    )



    # --- INPUT PANEL ---
    
    st.markdown(
        """
        <br>
        <div class="medt-input-label">Input Panel</div>
        <div class="medt-input-title">Menu Generator</div>
        <p style="font-size:0.87rem; color:#4B5563; margin-bottom:0.8rem;">
            Define your inventory and fusion concept, then let the AI design the experience.
        </p>
        """,
        unsafe_allow_html=True,
    )

    col_left, col_right = st.columns([2, 1])

    with col_left:
        ingredients = st.text_area(
            "Available ingredients (comma-separated)",
            value="chicken, rice, lime, cilantro, rum, mint, sugar",
            height=110,
        )

        style = st.text_input(
            "Preferred style",
            value="Mediterranean–Tropical fusion",
        )

        target_profit = st.slider(
            "Target profit margin (%)",
            min_value=10,
            max_value=60,
            value=25,
            step=5,
        )

    with col_right:
        st.markdown(
            """
            <p class="medt-note" style="margin-top:0.3rem; line-height:1.6;">
                💡 <strong>Demo tip</strong><br>
                • Use a real restaurant or bar inventory.<br>
                • Change the profit margin live to show dynamic updates.<br>
                • Emphasize that each suggestion is cost- and concept-aware.
            </p>
            """,
            unsafe_allow_html=True,
        )

    generate_button = st.button("Generate Menu Proposal")
    st.markdown("</div>", unsafe_allow_html=True)
    

    # ---- STATE: last result ----
    if "last_result" not in st.session_state:
        st.session_state["last_result"] = None

    # ---- WHEN BUTTON CLICKED ----
    if generate_button:
        with st.spinner(
            "👨‍🍳 Chef is designing your dish...\n"
            "🍸 Mixologist is crafting your cocktail...\n"
            "📊 Consultant is calculating profit margin..."
        ):
            user_request = {
                "ingredients": ingredients,
                "style": style,
                "target_profit_margin": target_profit / 100.0,
            }

            try:
                result = run_pipeline(user_request)
            except Exception as e:
                st.error("Something went wrong while generating the menu proposal.")
                st.exception(e)
                return
        
        st.session_state["last_request"] = user_request
        st.session_state["last_result"] = result


    # ---- DISPLAY RESULT (if we have one) ----
    result = st.session_state.get("last_result")

    if result:
        tab_recipes, tab_business, tab_visual = st.tabs(
            ["🍽️ Recipes", "💰 Business Insights", "📷 Visual Concept"]
        )

        with tab_recipes:
            st.markdown('<div class="medt-card">', unsafe_allow_html=True)
            st.markdown(
                '<div class="medt-section-title">Generated Recipes</div>',
                unsafe_allow_html=True,
            )

            st.markdown("#### 🍽️ Food Recipe")
            food_recipe = result.get("food_recipe", "")
            if food_recipe:
                st.write(food_recipe)
            else:
                st.info("No food recipe generated.")

            st.markdown("---")
            st.markdown("#### 🍸 Drink Pairing")
            drink_recipe = result.get("drink_recipe", "")
            if drink_recipe:
                st.write(drink_recipe)
            else:
                st.info("No drink pairing generated.")

            st.markdown("</div>", unsafe_allow_html=True)

        with tab_business:
            st.markdown('<div class="medt-card">', unsafe_allow_html=True)
            st.markdown(
                '<div class="medt-section-title">Cost & Profit Overview</div>',
                unsafe_allow_html=True,
            )

            cost_info = result.get("cost_info", "")
            if cost_info:
                st.write(cost_info)
            else:
                st.info("No cost information available.")

            st.markdown("---")
            st.markdown(
                '<div class="medt-section-title">Owner Recommendation</div>',
                unsafe_allow_html=True,
            )

            business_report = result.get("business_report", "")
            if business_report:
                st.write(business_report)
            else:
                st.info("No business recommendation generated.")

            st.markdown("</div>", unsafe_allow_html=True)

        # ----- Visual Concept Tab (text + banner) -----
        with tab_visual:
            st.markdown('<div class="medt-card">', unsafe_allow_html=True)

            st.markdown(
                """
                <div class="medt-section-title">Visual Concept (Prototype)</div>
                <p>
                In this prototype, we focus on the <strong>multi-agent reasoning</strong> and 
                <strong>business logic</strong> of Mediterraneo Tropical.<br><br>
                The visual concept tab explains how a future version of the system could integrate 
                with multimodal models:
                </p>

                <ul>
                    <li>Generate food photography based on the dish description</li>
                    <li>Create cocktail images consistent with the brand</li>
                    <li>Produce marketing visuals for social media and digital signage</li>
                </ul>

                <p>
                For this course project, we intentionally keep image generation out of the critical path 
                to keep the demo stable, fast, and free.
                </p>
                """,
                unsafe_allow_html=True,
            )



        # ----------------------------------------
        # KAYDETME & LİBRARY BÖLÜMÜ
        # ----------------------------------------
        st.markdown("---")
        st.markdown("### 💾 Save & Library")

        # Son üretilen sonucu session_state’ten çek
        last_request = st.session_state.get("last_request")
        last_result = st.session_state.get("last_result")

        if not last_result or not last_request:
            st.info("First generate a menu proposal above, then you can save it here.")
        else:
            col_save, col_go = st.columns([1, 1])

            with col_save:
                if st.button("💾 Save this menu concept"):
                    payload = {
                        "ingredients": last_request.get("ingredients", ""),
                        "style": last_request.get("style", ""),
                        "target_profit_margin": last_request.get("target_profit_margin", 0.0),
                        "food_recipe": last_result.get("food_recipe", ""),
                        "drink_recipe": last_result.get("drink_recipe", ""),
                        "cost_info": last_result.get("cost_info", ""),
                        "business_report": last_result.get("business_report", ""),
                    }

                    try:
                        save_menu_concept(payload)
                        st.success("Menu concept saved to the library (Saved Menus page).")
                    except Exception as e:
                        st.error("Could not save this concept.")
                        st.exception(e)

            with col_go:
                if st.button("📚 Open Saved Menu Concepts"):
                    st.switch_page("pages/2_SavedRecipes.py")


            




if __name__ == "__main__":
    main()

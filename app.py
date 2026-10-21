import streamlit as st
from config import BRAND_NAME

# ---------- SAYFA AYARLARI ----------
st.set_page_config(
    page_title=f"{BRAND_NAME} – Mediterraneo Tropical",
    layout="wide",
    page_icon="🌴",
)

# ---------- CUSTOM CSS ----------
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

/* Arka plan gradyan (diğer sayfalarla uyumlu) */
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

/* HERO */
.landing-hero {
    background: linear-gradient(120deg, #D32F2F 0%, #FF6F00 35%, #0097A7 65%, #FFB300 100%);
    color: #FFFFFF;
    border-radius: 1.4rem;
    padding: 1.4rem 1.7rem;
    box-shadow: 0 12px 26px rgba(211, 47, 47, 0.32);
    margin-bottom: 1.0rem;
}

/* Küçük badge */
.landing-badge {
    display: inline-flex;
    align-items: center;
    padding: 0.18rem 0.7rem;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.16);
    border: 1px solid rgba(255, 255, 255, 0.4);
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.16em;
}

/* Marka metni */
.medt-brand {
    font-weight: 900 !important;
    font-size: 2.3rem !important;

    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    -webkit-text-stroke: 2px transparent;

    background: linear-gradient(120deg, #ff6f00, #ffb300, #00acc1, #d32f2f);
    background-clip: text;
    -webkit-background-clip: text;

    text-shadow:
        0 0 6px rgba(255, 111, 0, 0.6),
        0 0 12px rgba(255, 179, 0, 0.5),
        0 0 18px rgba(0, 150, 136, 0.4);
}

/* Hero alt metinleri */
.landing-subtitle {
    font-size: 0.92rem;
    color: #FFFDF5;
    max-width: 620px;
    margin-top: 0.35rem;
    margin-bottom: 0.2rem;
}

.landing-info {
    font-size: 0.78rem;
    color: #FDEFD0;
}

/* Ana içerik (Hero altı) */
.landing-section-title {
    font-size: 0.95rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #E65100;
    margin-bottom: 0.35rem;
    margin-top: 0.3rem;
}

.landing-text-block {
    font-size: 0.9rem;
    color: #374151;
    max-width: 520px;
}

/* Tek dikey afiş */
.poster-vertical {
    width: 100%;
    aspect-ratio: 9 / 16;
    border-radius: 1.1rem;
    background: linear-gradient(145deg, #E0F7FA, #FFE4E1);
    border: 1px solid rgba(2, 136, 209, 0.45);
    box-shadow: 0 10px 24px rgba(2, 119, 189, 0.22);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.82rem;
    color: #0D47A1;
    text-align: center;
    padding: 0.7rem;
}

/* CTA buton */
.stButton > button {
    border-radius: 999px !important;
    background: linear-gradient(120deg, #D32F2F, #FF6F00, #0097A7) !important;
    border: none !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    padding: 0.45rem 1.0rem !important;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    font-size: 0.8rem !important;
    box-shadow: 0 10px 22px rgba(211, 47, 47, 0.35);
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 14px 28px rgba(211, 47, 47, 0.45);
}

</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ---------- HERO ----------
st.markdown(
    f"""
    <div class="landing-hero">
        <div class="landing-badge">Mediterranean • Tropical • Latin</div>
        <h1 style="margin-top:0.55rem; margin-bottom:0.1rem; line-height:1.2;">
            🌴 <span class="medt-brand">{BRAND_NAME}</span>
        </h1>
        <p class="landing-subtitle">
            A fusion restaurant & cocktail bar where Aegean meze, Latin spirits 
            and Colombian fruits meet in one concept.
        </p>
        <p class="landing-info">
            This homepage is Generative AI final project welcome screen – 
            from here guests can discover the AI-powered menu, house cocktails 
            and saved concepts via the sidebar.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- HERO ALTINDAKİ SATIR: SOL METİN + SAĞ DİKEY AFİŞ ----------
col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown(
        """
        <div class="landing-section-title">Tonight at Mediterraneo Tropical</div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="landing-text-block">
            • Design a <strong>fusion menu</strong> with our AI Menu Designer.<br/>
            • Browse the curated <strong>House Menu</strong> of signature cocktails & dishes.<br/>
            • Revisit <strong>Saved Concepts</strong> that worked well in previous runs.<br/><br/>
            Use the sidebar to move between pages, or start directly with the AI Menu Designer below.
            <br>
            <br
        </div>
        """,
        unsafe_allow_html=True,
    )

    
    # Tek ana CTA buton 
    if st.button("Start AI Menu Designer"):
        st.switch_page("pages/1_Generate.py")

    st.image("assets/menu_placeholder.jpg", width=720   )

with col_right:
    st.image("assets/banner.jpg", use_container_width=True,caption="Tonight's Special – Signature Cocktail & Tasting Menu")



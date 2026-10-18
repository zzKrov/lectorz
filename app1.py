import streamlit as st
import cv2
import numpy as np
import pytesseract
from PIL import Image

# ============================================================
# CONFIGURACIÓN GENERAL (SIN SIDEBAR)
# ============================================================
st.set_page_config(
    page_title="Reconocimiento Óptico // Krov Industries",
    page_icon="▣",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# RENDERIZADOR SEGURO
# ============================================================
def render_clean_html(html_str: str):
    clean = "".join(line.strip() for line in html_str.splitlines() if line.strip())
    st.markdown(clean, unsafe_allow_html=True)

# ============================================================
# ESTILOS VISUALES: FONDO LÍQUIDO KROV, BRILLO INTEGRAL Y CONTROLES
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500;700&display=swap');

:root {
    --black: #040207;
    --red: #ff174f;
    --pink: #ff3c91;
    --purple: #7928ca;
    --violet: #9b42ff;
    --white: #f3edf2;
    --soft: #b9afb8;
}

/* Supresión absoluta de cualquier elemento residual de sidebar */
[data-testid="stSidebar"], section[data-testid="stSidebar"] {
    display: none !important;
}

html, body, [data-testid="stAppViewContainer"], .stApp {
    background-color: var(--black) !important;
    color: var(--white) !important;
    font-family: 'Inter', sans-serif !important;
    overflow-x: hidden;
}

[data-testid="stHeader"] { background: transparent !important; }

/* ============================================================
   1. FONDO FLUIDO LÍQUIDO ACELERADO POR GPU (SIN PUNTOS / CERO LAG)
============================================================ */
.krov-fluid-canvas {
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;
    overflow: hidden;
    background: radial-gradient(circle at 50% 50%, #0a0314 0%, #040207 100%);
}

.krov-orb {
    position: absolute;
    border-radius: 50%;
    filter: blur(85px);
    opacity: 0.44;
    will-change: transform;
}

.krov-orb-1 {
    width: 620px;
    height: 620px;
    background: radial-gradient(circle, var(--red) 0%, var(--purple) 55%, transparent 75%);
    top: -12%;
    left: -6%;
    animation: krovDrift1 16s ease-in-out infinite alternate;
}

.krov-orb-2 {
    width: 660px;
    height: 660px;
    background: radial-gradient(circle, var(--purple) 0%, var(--pink) 50%, transparent 75%);
    bottom: -16%;
    right: -8%;
    animation: krovDrift2 20s ease-in-out infinite alternate;
}

.krov-orb-3 {
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, var(--violet) 0%, var(--red) 50%, transparent 70%);
    top: 40%;
    left: 45%;
    transform: translate(-50%, -50%);
    animation: krovDrift3 24s ease-in-out infinite alternate;
}

@keyframes krovDrift1 {
    0% { transform: translate3d(0, 0, 0) scale(1); }
    50% { transform: translate3d(90px, 70px, 0) scale(1.15); }
    100% { transform: translate3d(-50px, 120px, 0) scale(0.92); }
}

@keyframes krovDrift2 {
    0% { transform: translate3d(0, 0, 0) scale(1); }
    50% { transform: translate3d(-100px, -80px, 0) scale(1.12); }
    100% { transform: translate3d(70px, -60px, 0) scale(0.9); }
}

@keyframes krovDrift3 {
    0% { transform: translate(-50%, -50%) scale(0.9); }
    50% { transform: translate(-35%, -65%) scale(1.2); }
    100% { transform: translate(-65%, -35%) scale(0.95); }
}

/* ============================================================
   2. TIPOGRAFÍA Y ESTRUCTURA KROV INDUSTRIES
============================================================ */
.block-container {
    position: relative;
    z-index: 10;
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

.brand-signature {
    text-align: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--red);
    margin-bottom: 2px;
}

h1 {
    font-family: "Cormorant Garamond", serif !important;
    font-size: clamp(2.8rem, 5.5vw, 4.8rem) !important;
    font-weight: 500 !important;
    letter-spacing: 0.025em;
    text-align: center;
    color: var(--white) !important;
    line-height: 0.95 !important;
    text-shadow: 0 0 25px rgba(255,23,79,0.35), 0 0 60px rgba(121,40,202,0.25);
    animation: titlePulse 5s ease-in-out infinite alternate;
}

@keyframes titlePulse {
    0% { text-shadow: 0 0 15px rgba(255,23,79,0.25), 0 0 35px rgba(121,40,202,0.15); }
    100% { text-shadow: 0 0 30px rgba(255,23,79,0.5), 0 0 70px rgba(121,40,202,0.35); }
}

.header-subtitle {
    text-align: center;
    font-size: 0.72rem;
    letter-spacing: 0.28em;
    text-transform: uppercase;
    color: #a998a4;
    margin-top: 0.6rem;
    margin-bottom: 1.4rem;
}

.header-line {
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--red), var(--purple), var(--pink), transparent);
    background-size: 250% 100%;
    box-shadow: 0 0 15px rgba(255,23,79,0.6);
    animation: lineFlow 5s linear infinite;
    margin-bottom: 1.8rem;
}

@keyframes lineFlow {
    0% { background-position: 0% 50%; }
    100% { background-position: 250% 50%; }
}

/* ============================================================
   3. BARRA DE CONTROL INTEGRADA EN EL SITIO
============================================================ */
.control-bar {
    background: linear-gradient(145deg, rgba(18, 5, 26, 0.9), rgba(8, 2, 14, 0.95));
    border: 1px solid rgba(255, 23, 79, 0.28);
    border-radius: 8px;
    padding: 12px 20px;
    margin-bottom: 1.6rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    backdrop-filter: blur(14px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.6), inset 0 0 15px rgba(255,23,79,0.06);
}

/* ============================================================
   4. CÁMARA Y CONTENEDOR DE TEXTO
============================================================ */
[data-testid="stCameraInput"] {
    position: relative;
    z-index: 20;
    background: rgba(18, 5, 24, 0.85);
    border: 1px solid rgba(255, 23, 79, 0.3);
    padding: 10px;
    border-radius: 8px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.6), 0 0 25px rgba(255,23,79,0.12);
    transition: all 0.35s ease;
}

[data-testid="stCameraInput"]:hover {
    transform: translateY(-3px);
    border-color: rgba(255, 60, 145, 0.7);
    box-shadow: 0 25px 75px rgba(0,0,0,0.7), 0 0 35px rgba(255,23,79,0.25);
}

.result-container {
    position: relative;
    z-index: 20;
    background: linear-gradient(145deg, rgba(22, 6, 30, 0.9), rgba(8, 2, 14, 0.96));
    border: 1px solid rgba(255, 23, 79, 0.3);
    border-left: 4px solid var(--red);
    padding: 1.8rem 2rem;
    min-height: 160px;
    border-radius: 8px;
    backdrop-filter: blur(16px);
    box-shadow: 0 20px 60px rgba(0,0,0,0.55), inset 0 0 25px rgba(255,23,79,0.08);
    transition: all 0.3s ease;
}

.result-container:hover {
    border-color: rgba(255, 60, 145, 0.7);
    box-shadow: 0 25px 65px rgba(0, 0, 0, 0.75), 0 0 35px rgba(255, 23, 79, 0.25);
}

.result-text {
    font-family: "Cormorant Garamond", serif;
    font-size: 1.45rem;
    line-height: 1.6;
    color: #eee5e6;
    white-space: pre-wrap;
    text-shadow: 0 0 15px rgba(255,255,255,0.08);
}

.status-badge {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 0.9rem;
    font-size: 0.68rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #a58d98;
}

.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--red);
    box-shadow: 0 0 10px var(--red), 0 0 22px rgba(255,23,79,0.9);
    animation: statusPulse 1.4s ease-in-out infinite;
}

@keyframes statusPulse {
    0%, 100% { transform: scale(0.75); opacity: 0.6; }
    50% { transform: scale(1.35); opacity: 1; }
}

/* ============================================================
   5. TARJETAS INFERIORES: BRILLO INTEGRAL EN TODA LA SUPERFICIE (SHINE HOVER)
============================================================ */
.info-card {
    position: relative;
    background: linear-gradient(145deg, rgba(20, 7, 28, 0.88), rgba(9, 3, 15, 0.95));
    border: 1px solid rgba(255, 23, 79, 0.28);
    border-top: 2px solid var(--red);
    padding: 1.5rem 1rem;
    text-align: center;
    border-radius: 8px;
    backdrop-filter: blur(16px);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.7), inset 0 0 20px rgba(255, 23, 79, 0.06);
    overflow: hidden;
    transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}

/* Haz de luz especular diagonal que barre toda la superficie de la tarjeta al interactuar */
.info-card::before {
    content: "";
    position: absolute;
    top: -60%;
    left: -160%;
    width: 220%;
    height: 220%;
    background: linear-gradient(
        115deg,
        transparent 25%,
        rgba(255, 255, 255, 0.05) 45%,
        rgba(255, 23, 79, 0.28) 52%,
        rgba(175, 80, 255, 0.3) 60%,
        transparent 72%
    );
    transform: rotate(25deg);
    transition: transform 0.75s ease;
    pointer-events: none;
    z-index: 1;
}

.info-card:hover::before {
    transform: rotate(25deg) translate3d(95%, 45%, 0);
}

.info-card:hover {
    transform: translateY(-5px);
    border-color: rgba(255, 60, 145, 0.85);
    box-shadow:
        0 20px 50px rgba(0, 0, 0, 0.85),
        0 0 35px rgba(255, 23, 79, 0.45),
        inset 0 0 25px rgba(255, 23, 79, 0.22),
        inset 0 1px 0 rgba(255, 255, 255, 0.35);
}

.info-number {
    position: relative;
    z-index: 5;
    font-family: "Cormorant Garamond", serif;
    font-size: 2.4rem;
    font-weight: 600;
    color: #ffffff;
    line-height: 1.1;
    text-shadow: 0 0 18px rgba(255, 23, 79, 0.5);
}

.info-label {
    position: relative;
    z-index: 5;
    font-size: 0.68rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #a4919b;
    margin-top: 6px;
    font-family: 'JetBrains Mono', monospace;
}
</style>

<!-- Atmósfera fluida continua Krov Industries (GPU) -->
<div class="krov-fluid-canvas">
    <div class="krov-orb krov-orb-1"></div>
    <div class="krov-orb krov-orb-2"></div>
    <div class="krov-orb krov-orb-3"></div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# CABECERA KROV INDUSTRIES
# ============================================================
render_clean_html(
    """
    <div class="brand-signature">Krov Industries · Óptica</div>
    """
)

st.title("Reconocimiento óptico de caracteres")

render_clean_html(
    """
    <div class="header-subtitle">
        Análisis óptico continuo · Procesamiento de matriz y extracción de texto
    </div>
    <div class="header-line"></div>
    """
)

# ============================================================
# PANEL DE CONTROL INTEGRADO EN EL SITIO (SIN SIDEBAR)
# ============================================================
col_ctrl1, col_ctrl2 = st.columns([1.5, 1], gap="medium")

with col_ctrl1:
    filtro = st.radio(
        "Filtro óptico de contraste:",
        ("Sin Filtro (Original)", "Con Filtro (Inversión negativa)"),
        horizontal=True
    )

with col_ctrl2:
    render_clean_html(
        """
        <div style="font-family:'JetBrains Mono'; font-size:0.75rem; color:#a4919b; padding-top:8px;">
            ESTADO: <span style="color:#ff174f; font-weight:700;">CANAL ÓPTICO DISPONIBLE</span>
        </div>
        """
    )

st.write("")

# ============================================================
# ENTRADA DE CÁMARA Y SALIDA DE TEXTO
# ============================================================
col_cam, col_res = st.columns([1, 1.2], gap="large")

with col_cam:
    render_clean_html('<div class="section-label">Captura en Vivo</div>')
    img_file_buffer = st.camera_input("Toma una Foto", label_visibility="collapsed")

with col_res:
    render_clean_html('<div class="section-label">Texto Reconocido</div>')

    if img_file_buffer is not None:
        bytes_data = img_file_buffer.getvalue()
        cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

        if "Con Filtro" in filtro:
            cv2_img = cv2.bitwise_not(cv2_img)

        img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)

        try:
            text = pytesseract.image_to_string(img_rgb)
        except Exception:
            text = ""

        clean_text = text.strip()
        character_count = len(clean_text)
        word_count = len(text.split())

        status_text = "Texto detectado" if character_count > 0 else "No se detectó texto reconocible"

        render_clean_html(
            f"""
            <div class="status-badge">
                <div class="status-dot"></div>
                <span>{status_text}</span>
            </div>
            """
        )

        safe_text = (
            text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
        )
        display_text = safe_text if clean_text else "No se encontró texto legible en la captura realizada."

        render_clean_html(
            f"""
            <div class="result-container">
                <div class="result-text">{display_text}</div>
            </div>
            """
        )

        st.write("")
        col1, col2, col3 = st.columns(3)

        with col1:
            render_clean_html(
                f"""
                <div class="info-card">
                    <div class="info-number">{word_count}</div>
                    <div class="info-label">Palabras</div>
                </div>
                """
            )

        with col2:
            render_clean_html(
                f"""
                <div class="info-card">
                    <div class="info-number">{character_count}</div>
                    <div class="info-label">Caracteres</div>
                </div>
                """
            )

        with col3:
            method = "Invertido" if "Con Filtro" in filtro else "Original"
            render_clean_html(
                f"""
                <div class="info-card">
                    <div class="info-number">{method}</div>
                    <div class="info-label">Modo</div>
                </div>
                """
            )
    else:
        render_clean_html(
            """
            <div class="result-container" style="display:flex; justify-content:center; align-items:center; text-align:center; color:#94a3b8;">
                Captura una imagen con la cámara web para analizar los caracteres.
            </div>
            """
        )

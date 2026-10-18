import streamlit as st
import cv2
import numpy as np
import pytesseract
from PIL import Image

# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================
st.set_page_config(
    page_title="Reconocimiento óptico de caracteres",
    page_icon="▣",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# FUNCIÓN DE RENDERIZADO SEGURO (SIN FILTRACIONES DE TEXTO HTML)
# ============================================================
def render_clean_html(html_str: str):
    clean = "".join(line.strip() for line in html_str.splitlines() if line.strip())
    st.markdown(clean, unsafe_allow_html=True)

# ============================================================
# ESTILOS VISUALES: FLUIDO LÍQUIDO LIVIANO Y RESPLANDOR REAL
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');

:root {
    --black: #040207;
    --red: #ff174f;
    --pink: #ff3c91;
    --purple: #7928ca;
    --violet: #9b42ff;
    --blue: #2563eb;
    --white: #f3edf2;
    --soft: #b9afb8;
}

/* ============================================================
   FONDO FLUIDO LÍQUIDO ULTRA-RÁPIDO (SIN PUNTOS NI LAG)
============================================================ */
html, body, [data-testid="stAppViewContainer"], .stApp {
    background-color: var(--black) !important;
    color: var(--white) !important;
    font-family: 'Inter', sans-serif !important;
    overflow-x: hidden;
}

[data-testid="stHeader"] { background: transparent !important; }

/* Contenedor fijo de los orbes fluidos */
.fluid-background {
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;
    overflow: hidden;
    background: radial-gradient(circle at 50% 50%, #080310 0%, #040207 100%);
}

.fluid-orb {
    position: absolute;
    border-radius: 50%;
    filter: blur(85px);
    opacity: 0.38;
    will-change: transform;
}

.fluid-orb-1 {
    width: 600px;
    height: 600px;
    background: radial-gradient(circle, var(--red) 0%, var(--purple) 65%, transparent 80%);
    top: -15%;
    left: -5%;
    animation: orbDrift1 18s ease-in-out infinite alternate;
}

.fluid-orb-2 {
    width: 650px;
    height: 650px;
    background: radial-gradient(circle, var(--purple) 0%, var(--pink) 55%, transparent 80%);
    bottom: -20%;
    right: -10%;
    animation: orbDrift2 22s ease-in-out infinite alternate;
}

.fluid-orb-3 {
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, var(--blue) 0%, var(--red) 50%, transparent 75%);
    top: 35%;
    left: 45%;
    transform: translate(-50%, -50%);
    animation: orbDrift3 25s ease-in-out infinite alternate;
}

@keyframes orbDrift1 {
    0% { transform: translate3d(0, 0, 0) scale(1); }
    50% { transform: translate3d(80px, 60px, 0) scale(1.15); }
    100% { transform: translate3d(-40px, 110px, 0) scale(0.95); }
}

@keyframes orbDrift2 {
    0% { transform: translate3d(0, 0, 0) scale(1); }
    50% { transform: translate3d(-90px, -70px, 0) scale(1.12); }
    100% { transform: translate3d(60px, -50px, 0) scale(0.92); }
}

@keyframes orbDrift3 {
    0% { transform: translate(-50%, -50%) scale(0.9); }
    50% { transform: translate(-40%, -60%) scale(1.18); }
    100% { transform: translate(-60%, -40%) scale(1); }
}

/* ============================================================
   ESTRUCTURA Y TIPOGRAFÍA
============================================================ */
.block-container {
    position: relative;
    z-index: 10;
    max-width: 1100px;
    padding-top: 2.5rem;
    padding-bottom: 5rem;
}

h1 {
    font-family: "Cormorant Garamond", serif !important;
    font-size: clamp(3.2rem, 6.5vw, 5.5rem) !important;
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
    margin-top: 0.8rem;
    margin-bottom: 1.8rem;
}

.header-line {
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--red), var(--purple), var(--pink), transparent);
    background-size: 250% 100%;
    box-shadow: 0 0 15px rgba(255,23,79,0.6);
    animation: lineFlow 5s linear infinite;
    margin-bottom: 2rem;
}

@keyframes lineFlow {
    0% { background-position: 0% 50%; }
    100% { background-position: 250% 50%; }
}

/* ============================================================
   BARRA LATERAL
============================================================ */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(6,2,11,0.98), rgba(14,3,22,0.97), rgba(6,2,11,0.98)) !important;
    border-right: 1px solid rgba(255,23,79,0.25) !important;
    box-shadow: 12px 0 60px rgba(0,0,0,0.5) !important;
}

.section-label {
    font-size: 0.65rem;
    letter-spacing: 0.24em;
    text-transform: uppercase;
    color: #c47791;
    margin-bottom: 0.7rem;
}

/* ============================================================
   CÁMARA
============================================================ */
[data-testid="stCameraInput"] {
    position: relative;
    z-index: 20;
    background: rgba(18, 5, 24, 0.85);
    border: 1px solid rgba(255, 23, 79, 0.3);
    padding: 12px;
    border-radius: 8px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.6), 0 0 25px rgba(255,23,79,0.12);
    transition: all 0.35s ease;
}

[data-testid="stCameraInput"]:hover {
    transform: translateY(-4px);
    border-color: rgba(255, 60, 145, 0.7);
    box-shadow: 0 25px 75px rgba(0,0,0,0.7), 0 0 35px rgba(255,23,79,0.25);
}

/* ============================================================
   CONTENEDOR DE RESULTADO (TEXTO RECONOCIDO)
============================================================ */
.result-container {
    position: relative;
    z-index: 20;
    background: rgba(18, 5, 24, 0.88);
    border: 1px solid rgba(255, 23, 79, 0.3);
    border-left: 4px solid var(--red);
    padding: 2rem 2.2rem;
    min-height: 150px;
    border-radius: 8px;
    backdrop-filter: blur(14px);
    box-shadow: 0 20px 60px rgba(0,0,0,0.55), 0 0 30px rgba(255,23,79,0.12);
}

.result-text {
    position: relative;
    z-index: 5;
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
   TARJETAS INFERIORES: RESPLANDOR REAL (SIN CONIC GRADIENTS CORTADOS)
============================================================ */
.info-card {
    position: relative;
    background: rgba(16, 6, 24, 0.88);
    border: 1px solid rgba(255, 23, 79, 0.25);
    border-top: 2px solid var(--red);
    padding: 1.4rem 1rem;
    text-align: center;
    border-radius: 8px;
    backdrop-filter: blur(14px);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6), 0 0 20px rgba(255, 23, 79, 0.08);
    transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
}

.info-card:hover {
    transform: translateY(-5px);
    border-color: rgba(255, 60, 145, 0.85);
    box-shadow:
        0 15px 45px rgba(0, 0, 0, 0.8),
        0 0 35px rgba(255, 23, 79, 0.55),
        inset 0 0 20px rgba(255, 23, 79, 0.18);
}

.info-number {
    font-family: "Cormorant Garamond", serif;
    font-size: 2.3rem;
    font-weight: 600;
    color: #ffffff;
    line-height: 1.1;
    text-shadow: 0 0 18px rgba(255, 23, 79, 0.5);
}

.info-label {
    font-size: 0.68rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #a4919b;
    margin-top: 6px;
    font-family: 'Inter', sans-serif;
}
</style>

<!-- Fondo líquido de orbes orgánicos acelerados por GPU -->
<div class="fluid-background">
    <div class="fluid-orb fluid-orb-1"></div>
    <div class="fluid-orb fluid-orb-2"></div>
    <div class="fluid-orb fluid-orb-3"></div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# CABECERA
# ============================================================
st.title("Reconocimiento óptico de caracteres")

render_clean_html(
    """
    <div class="header-subtitle">
        Krov Industries · Análisis de imagen · Reconocimiento óptico de caracteres
    </div>
    <div class="header-line"></div>
    """
)

# ============================================================
# BARRA LATERAL
# ============================================================
with st.sidebar:
    render_clean_html('<div class="section-label">Configuración</div>')

    filtro = st.radio(
        "Aplicar Filtro:",
        ("Sin Filtro", "Con Filtro (Inversión de contraste)"),
        index=0
    )

    st.markdown("---")

    render_clean_html(
        """
        <div class="section-label">Método</div>
        <p style="font-size: 0.85rem; color: #b9afb8; line-height: 1.6;">
            Captura una imagen mediante la cámara web. El sistema procesa la matriz óptica,
            aplica el realce seleccionado y extrae los caracteres presentes en el documento.
        </p>
        """
    )

# ============================================================
# CÁMARA
# ============================================================
render_clean_html('<div class="section-label">Captura Óptica</div>')
img_file_buffer = st.camera_input("Toma una Foto", label_visibility="collapsed")

# ============================================================
# INFERENCIA OCR Y PRESENTACIÓN
# ============================================================
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

    st.markdown("---")
    render_clean_html('<div class="section-label">Resultado de Extracción</div>')

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
        method = "Filtrado" if "Con Filtro" in filtro else "Original"
        render_clean_html(
            f"""
            <div class="info-card">
                <div class="info-number">{method}</div>
                <div class="info-label">Modo Procesamiento</div>
            </div>
            """
        )

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
# FUNCIÓN DE RENDERIZADO SEGURO (ELIMINA FUGAS DE HTML)
# ============================================================
def render_clean_html(html_str: str):
    clean = "".join(line.strip() for line in html_str.splitlines() if line.strip())
    st.markdown(clean, unsafe_allow_html=True)

# ============================================================
# DISEÑO VISUAL ORIGINAL RESTAURADO (GPU ACCELERATED)
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');

:root {
    --black: #030207;
    --deep-purple: #0b0315;
    --purple: #6326ff;
    --violet: #9b42ff;
    --red: #ff174f;
    --pink: #ff3c91;
    --blue: #3155ff;
    --white: #f2edf1;
    --soft: #b9afb8;
    --dim: #817680;
}

/* ============================================================
   FONDO GLOBAL ATMOSFÉRICO EN MOVIMIENTO
============================================================ */
.stApp {
    min-height: 100vh;
    overflow-x: hidden;
    color: var(--white);
    background-color: var(--black);
    background-image:
        radial-gradient(ellipse 40% 35% at 5% 10%, rgba(105, 25, 255, 0.30), transparent 70%),
        radial-gradient(ellipse 45% 40% at 95% 15%, rgba(255, 15, 85, 0.25), transparent 70%),
        radial-gradient(ellipse 50% 45% at 80% 90%, rgba(65, 40, 255, 0.25), transparent 70%),
        radial-gradient(ellipse 40% 40% at 10% 85%, rgba(255, 20, 100, 0.18), transparent 70%),
        linear-gradient(135deg, #030207 0%, #100419 32%, #18040e 58%, #07040f 100%);
    background-size: 170% 170%, 180% 180%, 180% 180%, 170% 170%, 100% 100%;
    animation: atmosphere 16s ease-in-out infinite alternate;
}

/* ============================================================
   ORBE DE LUZ ORBITAL EN SEGUNDO PLANO
============================================================ */
.stApp::after {
    content: "";
    position: fixed;
    width: 55vw;
    height: 55vw;
    left: -20vw;
    top: -15vw;
    pointer-events: none;
    z-index: 0;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(255, 30, 110, 0.09), rgba(115, 30, 255, 0.05), transparent 70%);
    filter: blur(20px);
    animation: lightOrbit 14s ease-in-out infinite alternate;
}

/* ============================================================
   CAMPO DE PARTÍCULAS ERRÁTICAS (CAPA 1)
============================================================ */
.stApp > div::before {
    content: "";
    position: fixed;
    inset: -30%;
    pointer-events: none;
    z-index: 1;
    opacity: 0.9;
    background-image:
        radial-gradient(circle, rgba(255, 70, 150, 0.95) 0 2px, transparent 4px),
        radial-gradient(circle, rgba(130, 65, 255, 0.95) 0 2px, transparent 4px),
        radial-gradient(circle, rgba(255, 45, 110, 0.9) 0 1.5px, transparent 4px),
        radial-gradient(circle, rgba(70, 105, 255, 0.9) 0 2px, transparent 4px),
        radial-gradient(circle, rgba(255, 150, 210, 0.8) 0 1px, transparent 3px),
        radial-gradient(circle, rgba(170, 100, 255, 0.85) 0 1.5px, transparent 4px);
    background-size: 105px 125px, 145px 170px, 190px 145px, 230px 190px, 125px 210px, 270px 160px;
    animation: particleChaos1 7s linear infinite, particleChaos2 11s ease-in-out infinite alternate;
    filter: drop-shadow(0 0 5px rgba(255,50,130,0.7)) drop-shadow(0 0 12px rgba(100,50,255,0.35));
}

/* ============================================================
   CAMPO DE PARTÍCULAS ERRÁTICAS (CAPA 2)
============================================================ */
.stApp > div::after {
    content: "";
    position: fixed;
    inset: -40%;
    pointer-events: none;
    z-index: 2;
    opacity: 0.55;
    background-image:
        radial-gradient(circle, rgba(255, 80, 160, 0.9) 0 2px, transparent 5px),
        radial-gradient(circle, rgba(100, 80, 255, 0.9) 0 2px, transparent 5px),
        radial-gradient(circle, rgba(255, 40, 100, 0.8) 0 1px, transparent 4px);
    background-size: 180px 230px, 260px 190px, 150px 310px;
    animation: particleChaos3 5s linear infinite, particleChaos4 8s ease-in-out infinite alternate;
    filter: drop-shadow(0 0 8px rgba(255,40,130,0.7));
}

/* ============================================================
   ANIMACIONES DE PARTÍCULAS Y ATMÓSFERA
============================================================ */
@keyframes particleChaos1 {
    0% { transform: translate3d(-4%, -5%, 0) rotate(0deg); }
    31% { transform: translate3d(-9%, 4%, 0) rotate(-2deg); }
    64% { transform: translate3d(2%, -15%, 0) rotate(-1deg); }
    100% { transform: translate3d(5%, 14%, 0) rotate(-3deg); }
}

@keyframes particleChaos2 {
    0% { transform: scale(0.9) skewX(-2deg); }
    53% { transform: scale(0.82) skewX(-4deg); }
    100% { transform: scale(0.95) skewX(-3deg); }
}

@keyframes particleChaos3 {
    0% { transform: translate3d(8%, 10%, 0) rotate(0deg); }
    55% { transform: translate3d(-5%, 16%, 0) rotate(-2deg); }
    100% { transform: translate3d(11%, 12%, 0) rotate(-4deg); }
}

@keyframes particleChaos4 {
    0% { opacity: 0.35; transform: scale(0.8); }
    50% { opacity: 0.45; transform: scale(0.9); }
    100% { opacity: 0.5; transform: scale(0.85); }
}

@keyframes atmosphere {
    0% { background-position: 0% 0%, 100% 0%, 100% 100%, 0% 100%, center; filter: saturate(1) brightness(0.90); }
    50% { filter: saturate(1.4) brightness(1.05); }
    100% { background-position: 20% 20%, 80% 15%, 80% 80%, 15% 85%, center; filter: saturate(1.2) brightness(0.98); }
}

@keyframes lightOrbit {
    0% { transform: translate(0, 0) scale(0.9); }
    50% { transform: translate(45vw, 20vh) scale(1.2); }
    100% { transform: translate(70vw, 55vh) scale(0.85); }
}

/* ============================================================
   ESTRUCTURA Y TIPOGRAFÍA
============================================================ */
.block-container {
    position: relative;
    z-index: 10;
    max-width: 1150px;
    padding-top: 2.5rem;
    padding-bottom: 5rem;
}

h1 {
    font-family: "Cormorant Garamond", serif !important;
    font-size: clamp(3.5rem, 7vw, 6rem) !important;
    font-weight: 500 !important;
    letter-spacing: 0.025em;
    text-align: center;
    color: var(--white) !important;
    line-height: 0.95 !important;
    text-shadow: 0 0 15px rgba(255,255,255,0.12), 0 0 35px rgba(255,30,110,0.25), 0 0 70px rgba(120,40,255,0.18);
    animation: titlePulse 5s ease-in-out infinite alternate;
}

@keyframes titlePulse {
    0% { text-shadow: 0 0 12px rgba(255,30,110,0.20), 0 0 30px rgba(110,40,255,0.10); }
    100% { text-shadow: 0 0 22px rgba(255,40,120,0.42), 0 0 60px rgba(120,40,255,0.25); }
}

.header-subtitle {
    text-align: center;
    font-size: 0.72rem;
    letter-spacing: 0.28em;
    text-transform: uppercase;
    color: #a998a4;
    margin-top: 0.8rem;
    margin-bottom: 2rem;
}

.header-line {
    height: 2px;
    background: linear-gradient(90deg, transparent, #ff174f, #8b35ff, #ff3d91, #3155ff, transparent);
    background-size: 250% 100%;
    box-shadow: 0 0 15px rgba(255,25,100,0.65), 0 0 35px rgba(120,30,255,0.25);
    animation: lineFlow 4s linear infinite;
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
    background: linear-gradient(180deg, rgba(4,2,9,0.98), rgba(14,3,20,0.97), rgba(4,3,12,0.98)) !important;
    border-right: 1px solid rgba(255,35,110,0.25) !important;
    box-shadow: 12px 0 80px rgba(100,20,150,0.18) !important;
}

.section-label {
    font-size: 0.65rem;
    letter-spacing: 0.24em;
    text-transform: uppercase;
    color: #c47791;
    margin-bottom: 0.7rem;
}

/* ============================================================
   CÁMARA Y RECUADRO DE ENTRADA
============================================================ */
[data-testid="stCameraInput"] {
    position: relative;
    z-index: 20;
    background: linear-gradient(145deg, rgba(18,4,20,0.94), rgba(5,5,18,0.96));
    border: 1px solid rgba(255,40,110,0.25);
    padding: 12px;
    border-radius: 6px;
    box-shadow: 0 25px 90px rgba(0,0,0,0.6), 0 0 45px rgba(150,20,100,0.10);
    transition: all 0.4s cubic-bezier(.2,.8,.2,1);
}

[data-testid="stCameraInput"]:hover {
    transform: translateY(-5px);
    border-color: rgba(255,70,140,0.75);
    box-shadow: 0 35px 110px rgba(0,0,0,0.7), 0 0 45px rgba(255,25,100,0.25);
}

/* ============================================================
   TARJETA DE RESULTADO CON BARRIDO DE LUZ REFLECTANTE
============================================================ */
.result-container {
    position: relative;
    z-index: 20;
    overflow: hidden;
    background: linear-gradient(135deg, rgba(27,5,23,0.94), rgba(5,6,20,0.97));
    border: 1px solid rgba(255,45,115,0.25);
    border-left: 4px solid #ff285f;
    padding: 2rem 2.2rem;
    min-height: 160px;
    border-radius: 6px;
    box-shadow: 0 25px 80px rgba(0,0,0,0.55), 0 0 50px rgba(150,20,100,0.10);
}

.result-container::before {
    content: "";
    position: absolute;
    top: -60%;
    left: -80%;
    width: 45%;
    height: 220%;
    transform: rotate(20deg);
    pointer-events: none;
    background: linear-gradient(90deg, transparent, rgba(255,50,130,0.16), rgba(120,50,255,0.14), transparent);
    animation: reflection 5s ease-in-out infinite;
}

@keyframes reflection {
    0% { left: -80%; opacity: 0; }
    20%, 70% { opacity: 1; }
    100% { left: 130%; opacity: 0; }
}

.result-container::after {
    content: "";
    position: absolute;
    right: -40px;
    top: -40px;
    width: 130px;
    height: 130px;
    border-radius: 50%;
    pointer-events: none;
    background: radial-gradient(circle, rgba(255,35,120,0.2), transparent 70%);
    filter: blur(6px);
    animation: cornerGlow 3s ease-in-out infinite alternate;
}

@keyframes cornerGlow {
    from { opacity: 0.4; transform: scale(0.8); }
    to { opacity: 1; transform: scale(1.2); }
}

.result-text {
    position: relative;
    z-index: 5;
    font-family: "Cormorant Garamond", serif;
    font-size: 1.4rem;
    line-height: 1.6;
    color: #eee5e6;
    white-space: pre-wrap;
    text-shadow: 0 0 15px rgba(255,255,255,0.07);
}

/* ============================================================
   ESTADO Y PUNTO PULSANTE
============================================================ */
.status-badge {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 1rem;
    font-size: 0.68rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #a58d98;
}

.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #ff285f;
    box-shadow: 0 0 8px #ff285f, 0 0 20px rgba(255,30,100,0.9);
    animation: statusPulse 1.4s ease-in-out infinite;
}

@keyframes statusPulse {
    0%, 100% { transform: scale(0.7); opacity: 0.5; }
    50% { transform: scale(1.4); opacity: 1; }
}

/* ============================================================
   TARJETAS ESTADÍSTICAS CON BORDE ROTATORIO (CONIC)
============================================================ */
.info-card {
    position: relative;
    overflow: hidden;
    z-index: 20;
    background: linear-gradient(145deg, rgba(20,5,21,0.94), rgba(5,7,19,0.96));
    border: 1px solid rgba(255,40,110,0.2);
    padding: 1.3rem;
    text-align: center;
    border-radius: 6px;
    box-shadow: 0 18px 55px rgba(0,0,0,0.35);
    transition: all 0.35s ease;
}

.info-card:hover {
    transform: translateY(-6px) scale(1.02);
    border-color: rgba(255,65,135,0.7);
    box-shadow: 0 25px 80px rgba(0,0,0,0.55), 0 0 35px rgba(255,30,100,0.25);
}

.info-card::before {
    content: "";
    position: absolute;
    inset: -2px;
    z-index: -1;
    background: conic-gradient(from 0deg, transparent, #ff174f, transparent, #873cff, transparent);
    animation: borderRotate 4s linear infinite;
    opacity: 0;
    transition: opacity 0.3s ease;
}

.info-card:hover::before {
    opacity: 1;
}

@keyframes borderRotate {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

.info-number {
    position: relative;
    z-index: 5;
    font-family: "Cormorant Garamond", serif;
    font-size: 2.1rem;
    font-weight: 600;
    color: #f2dfe7;
    text-shadow: 0 0 15px rgba(255,40,120,0.4);
}

.info-label {
    position: relative;
    z-index: 5;
    font-size: 0.65rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #917f89;
    margin-top: 2px;
}
</style>
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
# BARRA LATERAL (ORIGINAL RESTAURADA)
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
            aplica el realce seleccionado y extrae los caracteres de forma continua.
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

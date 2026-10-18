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
# ESTILOS VISUALES: DERIVA FLUIDA VISIBLE, CÁMARA +50% Y SHINE TOTAL
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500;700&display=swap');

:root {
    --black: #05020a;
    --red: #ff174f;
    --pink: #ff3c91;
    --purple: #7928ca;
    --violet: #9b42ff;
    --blue: #2563eb;
    --white: #f3edf2;
    --soft: #b9afb8;
}

[data-testid="stSidebar"], section[data-testid="stSidebar"] {
    display: none !important;
}

/* Transparencia total en Streamlit para que los orbes en movimiento sean 100% visibles */
html, body, [data-testid="stAppViewContainer"], .stApp, section.main, .block-container {
    background: transparent !important;
    background-color: transparent !important;
    color: var(--white) !important;
    font-family: 'Inter', sans-serif !important;
    overflow-x: hidden;
}

body {
    background-color: #040207 !important;
}

[data-testid="stHeader"] { background: transparent !important; }

/* ============================================================
   1. ORBES LÍQUIDOS EN DERIVA CONTINUA VISIBLE (ACELERADOS POR GPU)
============================================================ */
.krov-fluid-canvas {
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;
    overflow: hidden;
    background: radial-gradient(circle at 50% 50%, #090314 0%, #040207 100%);
}

.krov-drift-orb {
    position: absolute;
    border-radius: 50%;
    filter: blur(80px);
    opacity: 0.52;
    will-change: transform;
    pointer-events: none;
}

.orb-1 {
    width: 600px;
    height: 600px;
    background: radial-gradient(circle, var(--red) 0%, var(--purple) 60%, transparent 75%);
    top: -10%;
    left: 5%;
    animation: driftMotion1 20s cubic-bezier(0.4, 0, 0.2, 1) infinite alternate;
}

.orb-2 {
    width: 640px;
    height: 640px;
    background: radial-gradient(circle, var(--violet) 0%, var(--pink) 55%, transparent 75%);
    bottom: -15%;
    right: 5%;
    animation: driftMotion2 24s cubic-bezier(0.4, 0, 0.2, 1) infinite alternate;
}

.orb-3 {
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, var(--blue) 0%, var(--red) 50%, transparent 75%);
    top: 35%;
    right: 30%;
    animation: driftMotion3 28s cubic-bezier(0.4, 0, 0.2, 1) infinite alternate;
}

.orb-4 {
    width: 450px;
    height: 450px;
    background: radial-gradient(circle, var(--pink) 0%, var(--purple) 50%, transparent 75%);
    bottom: 20%;
    left: 10%;
    animation: driftMotion4 22s cubic-bezier(0.4, 0, 0.2, 1) infinite alternate;
}

@keyframes driftMotion1 {
    0% { transform: translate3d(0, 0, 0) scale(1); }
    33% { transform: translate3d(180px, -60px, 0) scale(1.18); }
    66% { transform: translate3d(240px, 140px, 0) scale(0.92); }
    100% { transform: translate3d(-80px, 120px, 0) scale(1.05); }
}

@keyframes driftMotion2 {
    0% { transform: translate3d(0, 0, 0) scale(1.05); }
    33% { transform: translate3d(-190px, 110px, 0) scale(0.95); }
    66% { transform: translate3d(-110px, -160px, 0) scale(1.22); }
    100% { transform: translate3d(130px, -80px, 0) scale(1); }
}

@keyframes driftMotion3 {
    0% { transform: translate3d(0, 0, 0) scale(0.92); }
    33% { transform: translate3d(-160px, 170px, 0) scale(1.15); }
    66% { transform: translate3d(180px, -120px, 0) scale(1.08); }
    100% { transform: translate3d(-70px, -80px, 0) scale(0.95); }
}

@keyframes driftMotion4 {
    0% { transform: translate3d(0, 0, 0) scale(1); }
    33% { transform: translate3d(140px, 150px, 0) scale(1.16); }
    66% { transform: translate3d(-130px, -140px, 0) scale(0.88); }
    100% { transform: translate3d(70px, -50px, 0) scale(1.06); }
}

/* ============================================================
   2. TIPOGRAFÍA Y ESTRUCTURA KROV
============================================================ */
.block-container {
    position: relative;
    z-index: 10;
    max-width: 1250px;
    padding-top: 1.8rem;
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
    font-size: clamp(2.8rem, 5.5vw, 4.6rem) !important;
    font-weight: 500 !important;
    letter-spacing: 0.025em;
    text-align: center;
    color: var(--white) !important;
    line-height: 0.95 !important;
    text-shadow: 0 0 25px rgba(255,23,79,0.4), 0 0 60px rgba(121,40,202,0.3);
    animation: titlePulse 5s ease-in-out infinite alternate;
}

@keyframes titlePulse {
    0% { text-shadow: 0 0 15px rgba(255,23,79,0.3), 0 0 35px rgba(121,40,202,0.2); }
    100% { text-shadow: 0 0 30px rgba(255,23,79,0.6), 0 0 70px rgba(121,40,202,0.4); }
}

.header-subtitle {
    text-align: center;
    font-size: 0.72rem;
    letter-spacing: 0.28em;
    text-transform: uppercase;
    color: #a998a4;
    margin-top: 0.6rem;
    margin-bottom: 1.2rem;
}

.header-line {
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--red), var(--purple), var(--pink), transparent);
    background-size: 250% 100%;
    box-shadow: 0 0 15px rgba(255,23,79,0.6);
    animation: lineFlow 5s linear infinite;
    margin-bottom: 1.6rem;
}

@keyframes lineFlow {
    0% { background-position: 0% 50%; }
    100% { background-position: 250% 50%; }
}

/* ============================================================
   3. CÁMARA 50% MÁS GRANDE (AMPLIADA A 720x420px)
============================================================ */
[data-testid="stCameraInput"] {
    position: relative;
    z-index: 20;
    background: rgba(18, 5, 26, 0.88);
    border: 1px solid rgba(255, 23, 79, 0.35);
    padding: 12px;
    border-radius: 10px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.7), 0 0 25px rgba(255,23,79,0.15);
    max-width: 720px !important;
    width: 100% !important;
    margin: 0 auto;
    transition: all 0.35s ease;
}

[data-testid="stCameraInput"]:hover {
    transform: translateY(-3px);
    border-color: rgba(255, 60, 145, 0.75);
    box-shadow: 0 25px 75px rgba(0,0,0,0.8), 0 0 35px rgba(255,23,79,0.3);
}

[data-testid="stCameraInput"] video {
    max-height: 420px !important;
    height: 400px !important;
    object-fit: cover !important;
    border-radius: 8px !important;
}

/* ============================================================
   4. CAJA DE RESULTADO Y ESTADO
============================================================ */
.result-container {
    position: relative;
    z-index: 20;
    background: linear-gradient(145deg, rgba(22, 6, 32, 0.92), rgba(8, 2, 14, 0.96));
    border: 1px solid rgba(255, 23, 79, 0.3);
    border-left: 4px solid var(--red);
    padding: 1.6rem 2rem;
    min-height: 180px;
    border-radius: 8px;
    backdrop-filter: blur(16px);
    box-shadow: 0 20px 60px rgba(0,0,0,0.6), inset 0 0 25px rgba(255,23,79,0.08);
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
   5. TARJETAS CON BRILLO INTEGRAL EN TODA LA SUPERFICIE (SHINE HOVER)
============================================================ */
.info-card {
    position: relative;
    background: linear-gradient(145deg, rgba(20, 7, 30, 0.9), rgba(9, 3, 16, 0.96));
    border: 1px solid rgba(255, 23, 79, 0.28);
    border-top: 2px solid var(--red);
    padding: 1.5rem 1rem;
    text-align: center;
    border-radius: 8px;
    backdrop-filter: blur(16px);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.7), inset 0 0 20px rgba(255, 23, 79, 0.08);
    overflow: hidden;
    transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}

/* Haz especular diagonal que cruza toda la cara interna de la tarjeta */
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
        inset 0 0 25px rgba(255, 23, 79, 0.25),
        inset 0 1px 0 rgba(255, 255, 255, 0.4);
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

<!-- Orbes líquidos en deriva continua asimétrica -->
<div class="krov-fluid-canvas">
    <div class="krov-drift-orb orb-1"></div>
    <div class="krov-drift-orb orb-2"></div>
    <div class="krov-drift-orb orb-3"></div>
    <div class="krov-drift-orb orb-4"></div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# CABECERA
# ============================================================
render_clean_html('<div class="brand-signature">Krov Industries · Óptica</div>')
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
# CONTROLES INTEGRADOS EN LA PÁGINA (SIN SIDEBAR)
# ============================================================
col_ctrl1, col_ctrl2 = st.columns([1.6, 1], gap="medium")

with col_ctrl1:
    filtro = st.radio(
        "Modo de preprocesamiento:",
        ("Automático (detecta fondos oscuros)", "Original", "Inversión forzada"),
        horizontal=True
    )

with col_ctrl2:
    render_clean_html(
        """
        <div style="font-family:'JetBrains Mono'; font-size:0.75rem; color:#a4919b; padding-top:10px;">
            CANAL ÓPTICO: <span style="color:#ff174f; font-weight:700;">ALTA PRECISIÓN 2× CLAHE</span>
        </div>
        """
    )

st.write("")

# ============================================================
# PIPELINE DE PROCESAMIENTO OCR ROBUSTO
# ============================================================
def procesar_ocr_avanzado(cv_image, modo_filtro):
    # 1. Escalado 2x cúbico para elevar el tamaño del texto capturado por webcam
    h, w = cv_image.shape[:2]
    scaled = cv2.resize(cv_image, (int(w * 2.0), int(h * 2.0)), interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(scaled, cv2.COLOR_BGR2GRAY)

    # 2. Detección automática de pantallas en modo oscuro (letras claras sobre fondo negro)
    brillo_medio = np.mean(gray)
    es_fondo_oscuro = brillo_medio < 120

    if modo_filtro == "Inversión forzada" or (modo_filtro.startswith("Automático") and es_fondo_oscuro):
        # Tesseract requiere texto oscuro sobre fondo claro
        invertido = cv2.bitwise_not(gray)
    else:
        invertido = gray

    # 3. Filtrado bilateral para preservar bordes tipográficos reduciendo ruido
    denoised = cv2.bilateralFilter(invertido, 7, 50, 50)

    # 4. Ecualización adaptativa de contraste (CLAHE)
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    enhanced = clahe.apply(denoised)

    # 5. Doble pasada de OCR (PSM 3 automático y PSM 6 bloque uniforme)
    try:
        t1 = pytesseract.image_to_string(enhanced, config="--psm 3").strip()
    except Exception:
        t1 = ""

    try:
        t2 = pytesseract.image_to_string(enhanced, config="--psm 6").strip()
    except Exception:
        t2 = ""

    # Se selecciona la pasada con mayor información válida
    resultado = t2 if len(t2.split()) > len(t1.split()) else t1
    return resultado

# ============================================================
# CÁMARA (AMPLIADA 50%) Y SALIDA
# ============================================================
col_cam, col_res = st.columns([1.35, 1], gap="large")

with col_cam:
    render_clean_html('<div class="section-label">Visor de Captura (720px)</div>')
    img_file_buffer = st.camera_input("Toma una Foto", label_visibility="collapsed")

with col_res:
    render_clean_html('<div class="section-label">Texto Extraído</div>')

    if img_file_buffer is not None:
        bytes_data = img_file_buffer.getvalue()
        cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

        with st.spinner("Decodificando caracteres con CLAHE y 2× de resolución..."):
            text = procesar_ocr_avanzado(cv2_img, filtro)

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
        display_text = safe_text if clean_text else "No se encontró texto legible. Ajusta el ángulo o enfoca con mayor claridad."

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
            modo_etiqueta = "Auto CLAHE" if filtro.startswith("Automático") else ("Invertido" if "Inversión" in filtro else "Original")
            render_clean_html(
                f"""
                <div class="info-card">
                    <div class="info-number">{modo_etiqueta}</div>
                    <div class="info-label">Procesamiento</div>
                </div>
                """
            )
    else:
        render_clean_html(
            """
            <div class="result-container" style="display:flex; justify-content:center; align-items:center; text-align:center; color:#94a3b8;">
                Apunta la cámara a un texto o pantalla para procesar los caracteres.
            </div>
            """
        )

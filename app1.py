import streamlit as st
import cv2
import numpy as np
import pytesseract
from PIL import Image

# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================
st.set_page_config(
    page_title="Reconocimiento Óptico // Krov Industries",
    page_icon="▣",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def render_clean_html(html_str: str):
    clean = "".join(line.strip() for line in html_str.splitlines() if line.strip())
    st.markdown(clean, unsafe_allow_html=True)

# ============================================================
# ESTILOS VISUALES KROV
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500;700&display=swap');

:root {
    --black: #05020a;
    --red: #ff174f;
    --pink: #ff3c91;
    --purple: #7928ca;
    --white: #f3edf2;
}

[data-testid="stSidebar"], section[data-testid="stSidebar"] { display: none !important; }

html, body, [data-testid="stAppViewContainer"], .stApp, section.main, .block-container {
    background: transparent !important;
    background-color: transparent !important;
    color: var(--white) !important;
    font-family: 'Inter', sans-serif !important;
    overflow-x: hidden;
}

body { background-color: #040207 !important; }
[data-testid="stHeader"] { background: transparent !important; }

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
    opacity: 0.45;
    will-change: transform;
    pointer-events: none;
}

.orb-1 { width: 600px; height: 600px; background: radial-gradient(circle, var(--red) 0%, var(--purple) 60%, transparent 75%); top: -10%; left: 5%; }
.orb-2 { width: 640px; height: 640px; background: radial-gradient(circle, var(--purple) 0%, var(--pink) 55%, transparent 75%); bottom: -15%; right: 5%; }

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
    font-size: clamp(2.6rem, 5vw, 4.2rem) !important;
    font-weight: 500 !important;
    text-align: center;
    color: var(--white) !important;
    line-height: 0.95 !important;
    text-shadow: 0 0 25px rgba(255,23,79,0.4);
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
    margin-bottom: 1.6rem;
}

[data-testid="stCameraInput"] {
    background: rgba(18, 5, 26, 0.88);
    border: 1px solid rgba(255, 23, 79, 0.35);
    padding: 12px;
    border-radius: 10px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.7);
    max-width: 720px !important;
    margin: 0 auto;
}

[data-testid="stCameraInput"] video {
    max-height: 420px !important;
    height: 400px !important;
    object-fit: cover !important;
    border-radius: 8px !important;
}

.result-container {
    background: linear-gradient(145deg, rgba(22, 6, 32, 0.92), rgba(8, 2, 14, 0.96));
    border: 1px solid rgba(255, 23, 79, 0.3);
    border-left: 4px solid var(--red);
    padding: 1.6rem 2rem;
    min-height: 180px;
    border-radius: 8px;
    backdrop-filter: blur(16px);
    box-shadow: 0 20px 60px rgba(0,0,0,0.6);
}

.result-text {
    font-family: "JetBrains Mono", monospace;
    font-size: 1.15rem;
    line-height: 1.6;
    color: #00ff88;
    white-space: pre-wrap;
}

.info-card {
    background: linear-gradient(145deg, rgba(20, 7, 30, 0.9), rgba(9, 3, 16, 0.96));
    border: 1px solid rgba(255, 23, 79, 0.28);
    border-top: 2px solid var(--red);
    padding: 1.2rem 1rem;
    text-align: center;
    border-radius: 8px;
}

.info-number {
    font-family: "Cormorant Garamond", serif;
    font-size: 2.2rem;
    font-weight: 600;
    color: #ffffff;
}

.info-label {
    font-size: 0.68rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #a4919b;
    font-family: 'JetBrains Mono', monospace;
}
</style>

<div class="krov-fluid-canvas">
    <div class="krov-drift-orb orb-1"></div>
    <div class="krov-drift-orb orb-2"></div>
</div>
""", unsafe_allow_html=True)

render_clean_html('<div class="brand-signature">Krov Industries · Óptica Pura</div>')
st.title("Reconocimiento óptico de caracteres")
render_clean_html('<div class="header-subtitle">Motor Local de Inferencia Óptica Directa</div><div class="header-line"></div>')

# ============================================================
# CONTROL DIRECTO
# ============================================================
c_opt1, c_opt2 = st.columns([1.5, 1])
with c_opt1:
    enfocar_centro = st.checkbox("Recortar enfoque central al 75% (Ignora el fondo y la habitación)", value=True)
with c_opt2:
    ver_recorte = st.checkbox("Ver imagen que lee el motor", value=False)

st.write("")

# ============================================================
# MOTOR OCR LIMPIO (SIN FILTROS DESTRUCTIVOS)
# ============================================================
def ejecutar_ocr_limpio(cv_image, crop_center=True):
    # 1. Recorte opcional del área de interés (elimina techo, cabeza y fondo)
    if crop_center:
        h, w = cv_image.shape[:2]
        y1, y2 = int(h * 0.12), int(h * 0.88)
        x1, x2 = int(w * 0.12), int(w * 0.88)
        img = cv_image[y1:y2, x1:x2]
    else:
        img = cv_image

    # 2. Conversión a escala de grises
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 3. Normalización Min-Max de contraste (estira el rango dinámico sin binarizar ni pixelar)
    norm = cv2.normalize(gray, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)

    # 4. Tesseract con PSM 3 (detección automática real de bloques) y OEM 3 (LSTM moderno)
    cfg = "--oem 3 --psm 3"
    
    # Pasada A: Normal (texto oscuro sobre fondo claro, como páginas web o documentos)
    texto_a = pytesseract.image_to_string(norm, lang="spa+eng", config=cfg).strip()

    # Pasada B: Invertida (texto claro sobre fondo oscuro, como el reloj del teléfono)
    norm_inv = cv2.bitwise_not(norm)
    texto_b = pytesseract.image_to_string(norm_inv, lang="spa+eng", config=cfg).strip()

    # Criterio de selección: mayor densidad de caracteres alfanuméricos válidos
    score_a = sum(1 for c in texto_a if c.isalnum())
    score_b = sum(1 for c in texto_b if c.isalnum())

    if score_a >= score_b:
        resultado = texto_a
        preview = norm
    else:
        resultado = texto_b
        preview = norm_inv

    return resultado, preview

# ============================================================
# CAPTURA Y VISUALIZACIÓN
# ============================================================
col_cam, col_res = st.columns([1.3, 1], gap="large")

with col_cam:
    render_clean_html('<div class="section-label" style="font-family:JetBrains Mono; font-size:0.75rem; color:#a4919b; margin-bottom:8px;">VISOR DE CÁMARA</div>')
    img_file_buffer = st.camera_input("Capturar", label_visibility="collapsed")

with col_res:
    render_clean_html('<div class="section-label" style="font-family:JetBrains Mono; font-size:0.75rem; color:#a4919b; margin-bottom:8px;">TEXTO EXTRAÍDO</div>')

    if img_file_buffer is not None:
        bytes_data = img_file_buffer.getvalue()
        cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

        with st.spinner("Procesando matriz óptica..."):
            texto, preview_img = ejecutar_ocr_limpio(cv2_img, crop_center=enfocar_centro)

        clean_text = texto.strip()
        display_text = clean_text if clean_text else "No se detectó texto legible. Acerca un poco más el objetivo al centro."

        render_clean_html(
            f"""
            <div class="result-container">
                <div class="result-text">{display_text}</div>
            </div>
            """
        )

        st.write("")
        c1, c2 = st.columns(2)
        with c1:
            render_clean_html(f'<div class="info-card"><div class="info-number">{len(clean_text.split())}</div><div class="info-label">Palabras</div></div>')
        with c2:
            render_clean_html(f'<div class="info-card"><div class="info-number">{len(clean_text)}</div><div class="info-label">Caracteres</div></div>')

        if ver_recorte:
            st.write("")
            st.caption("Imagen entregada directamente al motor Tesseract:")
            st.image(preview_img, channels="GRAY", use_container_width=True)
    else:
        render_clean_html(
            """
            <div class="result-container" style="display:flex; justify-content:center; align-items:center; text-align:center; color:#94a3b8;">
                Centra el texto en el visor y pulsa "Toma una Foto".
            </div>
            """
        )

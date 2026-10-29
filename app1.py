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
    --violet: #9b42ff;
    --blue: #2563eb;
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
    opacity: 0.52;
    will-change: transform;
    pointer-events: none;
}

.orb-1 { width: 600px; height: 600px; background: radial-gradient(circle, var(--red) 0%, var(--purple) 60%, transparent 75%); top: -10%; left: 5%; }
.orb-2 { width: 640px; height: 640px; background: radial-gradient(circle, var(--violet) 0%, var(--pink) 55%, transparent 75%); bottom: -15%; right: 5%; }

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
    font-family: "Cormorant Garamond", serif;
    font-size: 1.45rem;
    line-height: 1.6;
    color: #eee5e6;
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

render_clean_html('<div class="brand-signature">Krov Industries · Óptica</div>')
st.title("Reconocimiento óptico de caracteres")
render_clean_html('<div class="header-subtitle">Pipeline Adaptativo Multi-Estrategia · OCR Optimizado</div><div class="header-line"></div>')

# ============================================================
# CONTROLES
# ============================================================
col_ctrl1, col_ctrl2 = st.columns([1.5, 1], gap="medium")

with col_ctrl1:
    idioma = st.selectbox("Idiomas de reconocimiento:", ["spa+eng (Español + Inglés)", "spa (Sólo Español)", "eng (Sólo Inglés)"])
    lang_code = "spa+eng" if "spa+eng" in idioma else ("spa" if "spa" in idioma else "eng")

with col_ctrl2:
    ver_debug = st.checkbox("Mostrar imagen preprocesada (Diagnóstico)", value=False)

st.write("")

# ============================================================
# PIPELINE MULTI-ESTRATEGIA ROBUSTO PARA FOTOS
# ============================================================
def pipeline_ocr_robusto(cv_image, lang="spa+eng"):
    # 1. Escalar 1.5x para aumentar definición de fuentes pequeñas
    h, w = cv_image.shape[:2]
    interp = cv2.INTER_CUBIC if (w < 1200) else cv2.INTER_AREA
    img_scaled = cv2.resize(cv_image, (int(w * 1.5), int(h * 1.5)), interpolation=interp)
    gray = cv2.cvtColor(img_scaled, cv2.COLOR_BGR2GRAY)

    # 2. Corrección de iluminación por morfología Top-Hat (elimina sombras y brillos)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))
    tophat = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, kernel)
    blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, kernel)
    norm = cv2.add(gray, tophat)
    norm = cv2.subtract(norm, blackhat)

    # 3. Denoising suave
    blurred = cv2.GaussianBlur(norm, (3, 3), 0)

    # 4. Estrategia A: Umbral adaptativo de Gauss (especial para fotos con sombras irregulares)
    bin_adaptive = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 11
    )

    # 5. Estrategia B: Otsu Binarization (especial para texto con iluminación uniforme)
    _, bin_otsu = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Invertir si el fondo quedó negro en lugar de blanco
    if np.mean(bin_adaptive) < 127:
        bin_adaptive = cv2.bitwise_not(bin_adaptive)
    if np.mean(bin_otsu) < 127:
        bin_otsu = cv2.bitwise_not(bin_otsu)

    candidatos = []
    configs = [
        ("--oem 3 --psm 3", bin_adaptive),
        ("--oem 3 --psm 6", bin_adaptive),
        ("--oem 3 --psm 11", bin_adaptive),
        ("--oem 3 --psm 6", bin_otsu),
    ]

    for cfg, img_target in configs:
        try:
            texto = pytesseract.image_to_string(img_target, lang=lang, config=cfg).strip()
            if len(texto) > 0:
                candidatos.append(texto)
        except Exception:
            pass

    # Seleccionar la inferencia con mayor cantidad de palabras válidas
    if candidatos:
        candidatos.sort(key=lambda t: len(t.split()), reverse=True)
        resultado = candidatos[0]
    else:
        resultado = ""

    return resultado, bin_adaptive

# ============================================================
# CÁMARA Y RESULTADOS
# ============================================================
col_cam, col_res = st.columns([1.35, 1], gap="large")

with col_cam:
    render_clean_html('<div class="section-label" style="font-family:JetBrains Mono; font-size:0.75rem; color:#a4919b; margin-bottom:8px;">VISOR ÓPTICO</div>')
    img_file_buffer = st.camera_input("Capturar", label_visibility="collapsed")

with col_res:
    render_clean_html('<div class="section-label" style="font-family:JetBrains Mono; font-size:0.75rem; color:#a4919b; margin-bottom:8px;">TEXTO EXTRAÍDO</div>')

    if img_file_buffer is not None:
        bytes_data = img_file_buffer.getvalue()
        cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

        with st.spinner("Procesando imagen con umbralización adaptativa y diccionario multilingüe..."):
            text, processed_preview = pipeline_ocr_robusto(cv2_img, lang=lang_code)

        clean_text = text.strip()
        word_count = len(clean_text.split())
        char_count = len(clean_text)

        safe_text = (
            text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
        )
        display_text = safe_text if clean_text else "No se detectaron caracteres legibles. Asegura buena iluminación y enfoca el texto de frente."

        render_clean_html(
            f"""
            <div class="result-container">
                <div class="result-text">{display_text}</div>
            </div>
            """
        )

        st.write("")
        c1, c2, c3 = st.columns(3)
        with c1:
            render_clean_html(f'<div class="info-card"><div class="info-number">{word_count}</div><div class="info-label">Palabras</div></div>')
        with c2:
            render_clean_html(f'<div class="info-card"><div class="info-number">{char_count}</div><div class="info-label">Caracteres</div></div>')
        with c3:
            render_clean_html(f'<div class="info-card"><div class="info-number" style="font-size:1.3rem;">{lang_code}</div><div class="info-label">Idiomas</div></div>')

        if ver_debug:
            st.write("")
            st.caption("Visión interna de Tesseract (después de eliminar sombras y binarizar):")
            st.image(processed_preview, channels="GRAY", use_container_width=True)
    else:
        render_clean_html(
            """
            <div class="result-container" style="display:flex; justify-content:center; align-items:center; text-align:center; color:#94a3b8;">
                Apunta la cámara a un texto impreso o pantalla y captura la foto.
            </div>
            """
        )

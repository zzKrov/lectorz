import streamlit as st
import cv2
import numpy as np
from PIL import Image

# Verificación de motores locales instalados
try:
    import easyocr
    EASYOCR_INSTALADO = True
except ImportError:
    EASYOCR_INSTALADO = False

try:
    import pytesseract
    TESSERACT_INSTALADO = True
except ImportError:
    TESSERACT_INSTALADO = False

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
# ESTILOS VISUALES MONOLÍTICOS KROV
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
    margin-bottom: 1.6rem;
}

.header-line {
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--red), var(--purple), var(--pink), transparent);
    margin-bottom: 2rem;
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
    padding: 1.8rem 2rem;
    min-height: 220px;
    border-radius: 8px;
    backdrop-filter: blur(16px);
    box-shadow: 0 20px 60px rgba(0,0,0,0.6);
}

.result-text {
    font-family: "JetBrains Mono", monospace;
    font-size: 1.15rem;
    line-height: 1.7;
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
render_clean_html('<div class="header-subtitle">Motor Monolítico Local · Sin Dependencias Externas</div><div class="header-line"></div>')

# ============================================================
# MOTOR LOCAL MONOLÍTICO
# ============================================================
@st.cache_resource
def get_easyocr_reader():
    if EASYOCR_INSTALADO:
        return easyocr.Reader(['es', 'en'], gpu=False)
    return None

def motor_ocr_monolitico(cv_image):
    """
    Procesamiento transparente: si EasyOCR está instalado se usa como motor primario;
    de lo contrario, se ejecuta Tesseract optimizado dimensionalmente.
    """
    # 1. INTENTO CON MOTOR NEURONAL (Si easyocr está en requirements.txt)
    reader = get_easyocr_reader()
    if reader is not None:
        try:
            rgb = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
            resultados = reader.readtext(rgb, detail=0, paragraph=True)
            if resultados:
                return "\n".join(resultados).strip()
        except Exception:
            pass

    # 2. MOTOR TESSERACT AUTO-ADAPTATIVO
    if not TESSERACT_INSTALADO:
        return "Error: No se encontró un motor de OCR instalado en el sistema."

    # Corrección dimensional: elevar la altura de las letras minúsculas (de 6px a ~20px)
    h, w = cv_image.shape[:2]
    target_dim = 1600.0
    if max(h, w) < target_dim:
        factor = target_dim / float(max(h, w))
        img_proc = cv2.resize(cv_image, (int(w * factor), int(h * factor)), interpolation=cv2.INTER_CUBIC)
    else:
        img_proc = cv_image

    gray = cv2.cvtColor(img_proc, cv2.COLOR_BGR2GRAY)

    # Enfoque óptico unsharp (recupera nitidez en bordes degradados por la lente webcam)
    gaussian = cv2.GaussianBlur(gray, (0, 0), 2.0)
    sharp = cv2.addWeighted(gray, 1.6, gaussian, -0.6, 0)

    # Modos de segmentación para escenas y pantallas
    configs = ["--oem 3 --psm 11", "--oem 3 --psm 3"]
    sharp_inv = cv2.bitwise_not(sharp)

    mejor_texto = ""
    max_score = 0

    # Doble pasada automática: polaridad normal e invertida
    for img_variante in (sharp, sharp_inv):
        for cfg in configs:
            try:
                raw = pytesseract.image_to_string(img_variante, lang="spa+eng", config=cfg).strip()
                # Filtrar líneas vacías y evaluar densidad alfanumérica real
                lineas = [l.strip() for l in raw.splitlines() if any(c.isalnum() for c in l)]
                texto_candidato = "\n".join(lineas)
                score = sum(1 for c in texto_candidato if c.isalnum())

                if score > max_score:
                    max_score = score
                    mejor_texto = texto_candidato
            except Exception:
                pass

    return mejor_texto

# ============================================================
# CAPTURA Y SALIDA
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

        with st.spinner("Decodificando texto en matriz local..."):
            texto_extraido = motor_ocr_monolitico(cv2_img)

        clean_text = texto_extraido.strip()
        display_text = clean_text if clean_text else "No se detectó texto con suficiente nitidez."

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
    else:
        render_clean_html(
            """
            <div class="result-container" style="display:flex; justify-content:center; align-items:center; text-align:center; color:#94a3b8;">
                Apunta la cámara a un texto o pantalla y pulsa "Toma una Foto".
            </div>
            """
        )

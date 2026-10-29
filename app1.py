import os
import io
import base64
import streamlit as st
import cv2
import numpy as np
from PIL import Image

# Intentar importar pytesseract (opcional si se usa Visión IA)
try:
    import pytesseract
    TESSERACT_DISPONIBLE = True
except ImportError:
    TESSERACT_DISPONIBLE = False

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

render_clean_html('<div class="brand-signature">Krov Industries · Reconocimiento Óptico</div>')
st.title("Reconocimiento de caracteres")
render_clean_html('<div class="header-subtitle">Extracción Óptica de Alta Fidelidad en Escenas Reales</div><div class="header-line"></div>')

# ============================================================
# SELECCIÓN DE MOTOR
# ============================================================
c_ctrl1, c_ctrl2 = st.columns([1.4, 1], gap="medium")

with c_ctrl1:
    motor = st.radio(
        "Motor de Inferencia Óptica:",
        ["⚡ Visión Neuronal IA (GPT-4o-mini · Recomendado para pantallas/fotos)", "▣ Tesseract Local con Filtro Antirruido"],
        horizontal=True
    )

with c_ctrl2:
    api_key_input = st.text_input(
        "Clave de API de OpenAI (para Visión Neuronal):",
        type="password",
        value=os.environ.get("OPENAI_API_KEY", ""),
        placeholder="sk-..."
    )
    if api_key_input:
        os.environ["OPENAI_API_KEY"] = api_key_input

st.write("")

# ============================================================
# MOTORES DE RECONOCIMIENTO
# ============================================================
def ocr_vision_ia(cv_image, api_key):
    """Reconoce texto en imágenes complejas mediante el modelo de visión."""
    from openai import OpenAI
    client = OpenAI(api_key=api_key)

    _, buffer = cv2.imencode(".jpg", cv_image, [cv2.IMWRITE_JPEG_QUALITY, 90])
    b64_image = base64.b64encode(buffer).decode("utf-8")

    prompt = (
        "Transcribe de forma exacta y literal todo el texto visible en esta imagen (incluyendo números, "
        "fechas, horas, nombres de red o marcas). "
        "No agregues comentarios ni explicaciones, responde únicamente con el texto transcrito exactamente como aparece."
    )

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_image}"}}
            ]
        }],
        max_tokens=300,
        temperature=0.0
    )
    return resp.choices[0].message.content.strip()

def ocr_tesseract_limpio(cv_image):
    """Ejecuta Tesseract filtrando estrictamente el ruido y artefactos."""
    if not TESSERACT_DISPONIBLE:
        return "Tesseract no está instalado en este entorno."

    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

    # Detección de fondo oscuro usando solo el cuadrante central
    h, w = gray.shape
    centro = gray[int(h*0.2):int(h*0.8), int(w*0.2):int(w*0.8)]
    if np.mean(centro) < 120:
        gray = cv2.bitwise_not(gray)

    # Filtro Otsu directo (evita la estática del filtro adaptativo)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Filtrar mediante image_to_data: descartar palabras con confianza menor a 60%
    data = pytesseract.image_to_data(thresh, lang="spa+eng", config="--psm 6", output_type=pytesseract.Output.DICT)

    palabras_validas = []
    for i in range(len(data["text"])):
        conf = int(data["conf"][i])
        palabra = data["text"][i].strip()
        # Se descarta cualquier predicción dudosa que genere caracteres aleatorios
        if conf > 60 and len(palabra) > 1:
            palabras_validas.append(palabra)

    return " ".join(palabras_validas)

# ============================================================
# CÁMARA Y PROCESAMIENTO
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

        texto_resultado = ""

        if "Visión" in motor:
            key_actual = os.environ.get("OPENAI_API_KEY", "").strip()
            if not key_actual:
                st.warning("Introduce tu clave de API de OpenAI para usar el reconocimiento neuronal.")
            else:
                with st.spinner("Decodificando texto mediante red de visión neural..."):
                    try:
                        texto_resultado = ocr_vision_ia(cv2_img, key_actual)
                    except Exception as e:
                        st.error(f"Error con la API de Visión: {e}")
        else:
            with st.spinner("Procesando con Tesseract y filtro de confianza > 60%..."):
                try:
                    texto_resultado = ocr_tesseract_limpio(cv2_img)
                except Exception as e:
                    st.error(f"Error en Tesseract: {e}")

        clean_text = texto_resultado.strip()
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

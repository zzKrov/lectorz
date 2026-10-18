import streamlit as st
import cv2
import numpy as np
import pytesseract

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
# ESTILOS VISUALES: FONDO LÍQUIDO GPU, RESPLANDOR Y SIN HTML EXPUESTO
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [data-testid="stAppViewContainer"], .stApp {
    background-color: #06020c !important;
    color: #f1f5f9 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    overflow-x: hidden;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { display: none !important; }

/* 1. Malla continua líquida acelerada por GPU */
.stApp {
    background:
        radial-gradient(circle at 20% 20%, rgba(255, 23, 79, 0.16) 0%, transparent 40%),
        radial-gradient(circle at 80% 30%, rgba(155, 66, 255, 0.18) 0%, transparent 45%),
        radial-gradient(circle at 50% 80%, rgba(255, 60, 145, 0.12) 0%, transparent 40%),
        linear-gradient(135deg, #06020c 0%, #13031e 50%, #06020c 100%) !important;
    background-size: 200% 200% !important;
    animation: liquidMove 14s ease infinite alternate !important;
}

@keyframes liquidMove {
    0% { background-position: 0% 0%; }
    50% { background-position: 100% 100%; }
    100% { background-position: 0% 100%; }
}

.brand-signature {
    text-align: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.18em;
    color: #ff174f;
    text-transform: uppercase;
}

.main-title {
    font-size: 2.2rem;
    font-weight: 700;
    text-align: center;
    background: linear-gradient(90deg, #ffffff 0%, #ff174f 50%, #9b42ff 100%);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: titleShine 8s linear infinite;
    margin-bottom: 0.2rem;
}

@keyframes titleShine {
    to { background-position: 200% center; }
}

.sub-lead {
    text-align: center;
    color: #94a3b8;
    font-size: 0.95rem;
    margin-bottom: 1.8rem;
}

/* Visor óptico acotado y centrado */
[data-testid="stCameraInput"] {
    max-width: 480px;
    margin: 0 auto;
}
[data-testid="stCameraInput"] video {
    max-height: 280px !important;
    border-radius: 8px !important;
    border: 2px solid rgba(255, 23, 79, 0.4) !important;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.8), 0 0 20px rgba(255, 23, 79, 0.2) !important;
}

/* Tarjetas y botones con resplandor en hover */
.ocr-box {
    background: rgba(16, 6, 24, 0.82);
    border: 1px solid rgba(255, 23, 79, 0.3);
    border-left: 4px solid #ff174f;
    border-radius: 8px;
    padding: 1.4rem;
    backdrop-filter: blur(14px);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
    min-height: 180px;
    font-size: 1.05rem;
    line-height: 1.6;
    color: #f8fafc;
}

div.stButton > button {
    border-radius: 6px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.85rem !important;
    background: linear-gradient(135deg, #ff174f 0%, #9b42ff 100%) !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    border: none !important;
    padding: 0.75rem 1.6rem !important;
    box-shadow: 0 0 20px rgba(255, 23, 79, 0.35) !important;
    transition: all 0.25s ease !important;
}

div.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 0 35px rgba(255, 23, 79, 0.7) !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="brand-signature">Krov Industries · Óptica</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">Reconocimiento Óptico</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-lead">Extracción de texto en tiempo real con preprocesamiento de contraste</div>', unsafe_allow_html=True)

col_cam, col_out = st.columns([1, 1.2], gap="large")

with col_cam:
    st.markdown("#### 1. Captura de imagen")
    img_buffer = st.camera_input("Captura", label_visibility="collapsed")
    filtro = st.radio("Filtro:", ["Original", "Inversión de Contraste"], horizontal=True)

with col_out:
    st.markdown("#### 2. Texto extraído")
    if img_buffer:
        bytes_data = img_buffer.getvalue()
        cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

        if filtro == "Inversión de Contraste":
            cv2_img = cv2.bitwise_not(cv2_img)

        img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)

        with st.spinner("Procesando caracteres..."):
            try:
                texto = pytesseract.image_to_string(img_rgb).strip()
            except Exception:
                texto = ""

        if texto:
            st.markdown(f'<div class="ocr-box">{texto}</div>', unsafe_allow_html=True)
            st.write("")
            m1, m2, m3 = st.columns(3)
            m1.metric("Palabras", len(texto.split()))
            m2.metric("Caracteres", len(texto))
            m3.metric("Filtro", filtro)
        else:
            st.warning("No se detectó texto reconocible. Intenta mejorar el enfoque o la iluminación.")
    else:
        st.markdown(
            '<div class="ocr-box" style="display:flex; justify-content:center; align-items:center; text-align:center; color:#94a3b8;">'
            'Toma una fotografía con la cámara para iniciar la extracción.'
            '</div>',
            unsafe_allow_html=True
        )

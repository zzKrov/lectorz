import streamlit as st
import cv2
import numpy as np
import pytesseract
from PIL import Image


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Reconocimiento óptico de caracteres",
    page_icon="▣",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# VISUAL DESIGN
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');


/* ============================================================
   GLOBAL
============================================================ */

.stApp {

    background:
        radial-gradient(
            circle at 50% 0%,
            rgba(100, 15, 30, 0.12),
            transparent 35%
        ),
        linear-gradient(
            135deg,
            #080708 0%,
            #0d0c0d 45%,
            #080708 100%
        );

    color: #ded9d0;

}


/* subtle architectural lines */

.stApp::before {

    content: "";

    position: fixed;

    inset: 0;

    pointer-events: none;

    background-image:
        linear-gradient(
            90deg,
            transparent 49.95%,
            rgba(255,255,255,0.025) 50%,
            transparent 50.05%
        );

    opacity: 0.25;

}


/* ============================================================
   MAIN
============================================================ */

.block-container {

    max-width: 1150px;

    padding-top: 3rem;
    padding-bottom: 5rem;

}


/* ============================================================
   TYPOGRAPHY
============================================================ */

html,
body,
[class*="css"] {

    font-family: "Inter", sans-serif;

}

h1 {

    font-family: "Cormorant Garamond", serif !important;

    font-size: clamp(4rem, 8vw, 7rem) !important;

    font-weight: 500 !important;

    letter-spacing: 0.03em;

    text-align: center;

    color: #e7e1d7 !important;

    line-height: 0.9 !important;

    margin-bottom: 0.2rem !important;

}


h2,
h3 {

    font-family: "Cormorant Garamond", serif !important;

    font-weight: 600 !important;

    color: #ded8ce !important;

}


.stApp p {

    color: #aaa49b;

}


/* ============================================================
   HEADER
============================================================ */

.header-subtitle {

    text-align: center;

    font-family: "Inter", sans-serif;

    font-size: 0.72rem;

    font-weight: 400;

    letter-spacing: 0.28em;

    text-transform: uppercase;

    color: #827c75;

    margin-top: 0.8rem;

    margin-bottom: 3rem;

}


.header-line {

    height: 1px;

    width: 100%;

    background:
        linear-gradient(
            90deg,
            transparent,
            #63202d,
            transparent
        );

    margin-bottom: 2.5rem;

}


/* ============================================================
   SIDEBAR
============================================================ */

section[data-testid="stSidebar"] {

    background:
        linear-gradient(
            180deg,
            #090809,
            #0d0b0d
        );

    border-right:
        1px solid rgba(180, 170, 160, 0.08);

}


section[data-testid="stSidebar"] h3 {

    font-size: 1.7rem !important;

    letter-spacing: 0.02em;

}


section[data-testid="stSidebar"] p {

    font-size: 0.8rem;

    line-height: 1.7;

    color: #858078;

}


/* ============================================================
   RADIO
============================================================ */

div[data-testid="stRadio"] label {

    color: #aaa49b !important;

    transition:
        color 0.2s ease,
        transform 0.2s ease;

}


div[data-testid="stRadio"] label:hover {

    color: #c9c0b5 !important;

    transform: translateX(3px);

}


/* ============================================================
   CAMERA CONTAINER
============================================================ */

[data-testid="stCameraInput"] {

    background:
        #0b0a0b;

    border:
        1px solid rgba(190, 180, 165, 0.13);

    padding: 12px;

    box-shadow:
        0 20px 70px rgba(0,0,0,0.35);

    transition:
        border-color 0.3s ease,
        box-shadow 0.3s ease;

}


[data-testid="stCameraInput"]:hover {

    border-color:
        rgba(140, 30, 50, 0.45);

    box-shadow:
        0 20px 80px rgba(0,0,0,0.55),
        0 0 30px rgba(100,20,35,0.06);

}


/* ============================================================
   CAMERA BUTTON
============================================================ */

[data-testid="stCameraInput"] button {

    background:
        #121012 !important;

    color:
        #d8d1c7 !important;

    border:
        1px solid rgba(180,170,160,0.18) !important;

    border-radius:
        2px !important;

    font-family:
        "Inter", sans-serif !important;

    transition:
        all 0.25s ease !important;

}


[data-testid="stCameraInput"] button:hover {

    background:
        #191417 !important;

    border-color:
        rgba(160,35,55,0.6) !important;

    box-shadow:
        0 0 20px rgba(120,20,40,0.12);

}


/* ============================================================
   SECTION LABELS
============================================================ */

.section-label {

    font-family:
        "Inter", sans-serif;

    font-size:
        0.65rem;

    letter-spacing:
        0.24em;

    text-transform:
        uppercase;

    color:
        #766f67;

    margin-bottom:
        0.7rem;

}


/* ============================================================
   RESULT
============================================================ */

.result-container {

    position:
        relative;

    background:
        #0c0b0d;

    border:
        1px solid rgba(190,180,165,0.12);

    border-left:
        2px solid #712638;

    padding:
        2rem 2.2rem;

    min-height:
        170px;

    box-shadow:
        0 15px 50px rgba(0,0,0,0.3);

}


.result-container::after {

    content:
        "";

    position:
        absolute;

    top:
        0;

    right:
        0;

    width:
        80px;

    height:
        80px;

    border-top:
        1px solid rgba(150,30,50,0.25);

    border-right:
        1px solid rgba(150,30,50,0.25);

}


.result-text {

    font-family:
        "Cormorant Garamond",
        serif;

    font-size:
        1.35rem;

    line-height:
        1.65;

    color:
        #d6d0c6;

    white-space:
        pre-wrap;

}


/* ============================================================
   INFORMATION CARDS
============================================================ */

.info-card {

    background:
        rgba(15,13,15,0.8);

    border:
        1px solid rgba(180,170,160,0.09);

    padding:
        1.2rem;

    text-align:
        center;

    transition:
        transform 0.25s ease,
        border-color 0.25s ease,
        background 0.25s ease;

}


.info-card:hover {

    transform:
        translateY(-3px);

    background:
        rgba(24,19,22,0.9);

    border-color:
        rgba(140,30,50,0.3);

}


.info-number {

    font-family:
        "Cormorant Garamond",
        serif;

    font-size:
        2rem;

    color:
        #c5bdb1;

}


.info-label {

    font-size:
        0.6rem;

    letter-spacing:
        0.18em;

    text-transform:
        uppercase;

    color:
        #706a63;

}


/* ============================================================
   STATUS
============================================================ */

.status {

    display:
        flex;

    align-items:
        center;

    gap:
        10px;

    margin-top:
        1.5rem;

    font-size:
        0.68rem;

    letter-spacing:
        0.15em;

    text-transform:
        uppercase;

    color:
        #766f68;

}


.status-dot {

    width:
        6px;

    height:
        6px;

    border-radius:
        50%;

    background:
        #8d2940;

    box-shadow:
        0 0 12px rgba(160,35,60,0.55);

}


/* ============================================================
   DIVIDERS
============================================================ */

hr {

    border:
        none !important;

    height:
        1px !important;

    background:
        linear-gradient(
            90deg,
            transparent,
            rgba(160,150,140,0.12),
            transparent
        ) !important;

    margin:
        2.5rem 0 !important;

}


/* ============================================================
   RESPONSIVE
============================================================ */

@media (max-width: 768px) {

    .block-container {

        padding-left: 1rem;
        padding-right: 1rem;

    }

    h1 {

        font-size:
            4rem !important;

    }

    .header-subtitle {

        font-size:
            0.58rem;

        letter-spacing:
            0.18em;

    }

    .result-container {

        padding:
            1.3rem;

    }

    .result-text {

        font-size:
            1.15rem;

    }

}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

st.title("Reconocimiento óptico de caracteres")

st.markdown(
    '<div class="header-subtitle">Image analysis · Optical character recognition</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="header-line"></div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="section-label">Configuración</div>',
        unsafe_allow_html=True
    )

    filtro = st.radio(
        "Aplicar Filtro",
        (
            "Con Filtro",
            "Sin Filtro"
        )
    )

    st.markdown("---")

    st.markdown(
        """
        <div class="section-label">
            Método
        </div>

        <p>
        Captura una imagen mediante la cámara.
        El sistema procesa la imagen y utiliza
        reconocimiento óptico de caracteres para
        identificar el texto.
        </p>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# CAMERA
# ============================================================

st.markdown(
    '<div class="section-label">Captura</div>',
    unsafe_allow_html=True
)

img_file_buffer = st.camera_input("Toma una Foto")


# ============================================================
# OCR
# ============================================================

if img_file_buffer is not None:

    # --------------------------------------------------------
    # READ IMAGE
    # --------------------------------------------------------

    bytes_data = img_file_buffer.getvalue()

    cv2_img = cv2.imdecode(
        np.frombuffer(
            bytes_data,
            np.uint8
        ),
        cv2.IMREAD_COLOR
    )


    # --------------------------------------------------------
    # FILTER
    # --------------------------------------------------------

    if filtro == "Con Filtro":

        cv2_img = cv2.bitwise_not(
            cv2_img
        )

    else:

        cv2_img = cv2_img


    # --------------------------------------------------------
    # RGB
    # --------------------------------------------------------

    img_rgb = cv2.cvtColor(
        cv2_img,
        cv2.COLOR_BGR2RGB
    )


    # --------------------------------------------------------
    # OCR
    # --------------------------------------------------------

    text = pytesseract.image_to_string(
        img_rgb
    )


    # --------------------------------------------------------
    # STATISTICS
    # --------------------------------------------------------

    clean_text = text.strip()

    character_count = len(clean_text)

    word_count = len(text.split())


    # ========================================================
    # RESULT HEADER
    # ========================================================

    st.markdown("---")

    st.markdown(
        '<div class="section-label">Resultado</div>',
        unsafe_allow_html=True
    )


    if character_count > 0:

        status_text = "Texto detectado"

    else:

        status_text = "No se detectó texto"


    st.markdown(
        f"""
        <div class="status">

            <div class="status-dot"></div>

            <span>{status_text}</span>

        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # TEXT
    # ========================================================

    # Escape HTML characters so OCR text cannot
    # accidentally be interpreted as HTML.

    safe_text = (
        text
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


    if clean_text:

        display_text = safe_text

    else:

        display_text = "No se encontró texto reconocible."


    st.markdown(
        f"""
        <div class="result-container">

            <div class="result-text">
                {display_text}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # STATISTICS
    # ========================================================

    st.markdown(
        "<br>",
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)


    with col1:

        st.markdown(
            f"""
            <div class="info-card">

                <div class="info-number">
                    {word_count}
                </div>

                <div class="info-label">
                    Palabras
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with col2:

        st.markdown(
            f"""
            <div class="info-card">

                <div class="info-number">
                    {character_count}
                </div>

                <div class="info-label">
                    Caracteres
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with col3:

        method = (
            "Filtrado"
            if filtro == "Con Filtro"
            else "Original"
        )

        st.markdown(
            f"""
            <div class="info-card">

                <div class="info-number">
                    {method}
                </div>

                <div class="info-label">
                    Procesamiento
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )
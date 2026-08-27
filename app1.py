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

/* ============================================================
   FONTS
============================================================ */

@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');


/* ============================================================
   ROOT
============================================================ */

:root {

    --bg-black: #040208;
    --bg-purple: #10051c;
    --bg-red: #21040f;

    --red: #ff174f;
    --pink: #ff3b91;
    --violet: #8a3ffc;
    --blue: #394cff;

    --text-main: #f0e9e5;
    --text-soft: #b8afb4;
    --text-dim: #82777e;

}


/* ============================================================
   GLOBAL APPLICATION
============================================================ */

.stApp {

    min-height: 100vh;

    overflow-x: hidden;

    color: var(--text-main);

    background-color: var(--bg-black);

    background-image:

        /* atmospheric light */
        radial-gradient(
            ellipse 45% 35% at 15% 15%,
            rgba(76, 20, 190, 0.30),
            transparent 70%
        ),

        radial-gradient(
            ellipse 50% 40% at 85% 20%,
            rgba(255, 20, 80, 0.22),
            transparent 70%
        ),

        radial-gradient(
            ellipse 45% 45% at 75% 85%,
            rgba(90, 20, 210, 0.24),
            transparent 70%
        ),

        radial-gradient(
            ellipse 35% 40% at 20% 80%,
            rgba(210, 15, 70, 0.16),
            transparent 70%
        ),

        /* irregular particles */
        radial-gradient(
            circle at 7% 18%,
            rgba(255, 55, 130, 0.8) 0 1px,
            transparent 2px
        ),

        radial-gradient(
            circle at 17% 73%,
            rgba(130, 80, 255, 0.75) 0 1px,
            transparent 2px
        ),

        radial-gradient(
            circle at 28% 31%,
            rgba(255, 60, 140, 0.65) 0 2px,
            transparent 3px
        ),

        radial-gradient(
            circle at 39% 87%,
            rgba(110, 100, 255, 0.7) 0 1px,
            transparent 2px
        ),

        radial-gradient(
            circle at 52% 14%,
            rgba(255, 50, 120, 0.75) 0 1px,
            transparent 2px
        ),

        radial-gradient(
            circle at 63% 62%,
            rgba(170, 70, 255, 0.65) 0 2px,
            transparent 3px
        ),

        radial-gradient(
            circle at 76% 38%,
            rgba(255, 50, 110, 0.7) 0 1px,
            transparent 2px
        ),

        radial-gradient(
            circle at 88% 79%,
            rgba(100, 100, 255, 0.7) 0 1px,
            transparent 2px
        ),

        radial-gradient(
            circle at 93% 12%,
            rgba(255, 60, 130, 0.7) 0 2px,
            transparent 3px
        ),

        /* base */
        linear-gradient(
            135deg,
            #040208 0%,
            #0d0414 35%,
            #17040d 58%,
            #07040f 100%
        );

    background-size:
        180% 180%,
        170% 170%,
        180% 180%,
        160% 160%,
        100% 100%,
        100% 100%,
        100% 100%,
        100% 100%,
        100% 100%,
        100% 100%,
        100% 100%,
        100% 100%,
        100% 100%,
        100% 100%,
        100% 100%;

    background-position:
        0% 0%,
        100% 0%,
        100% 100%,
        0% 100%,
        center,
        center,
        center,
        center,
        center,
        center,
        center,
        center,
        center,
        center,
        center;

    animation:
        atmosphereMovement 18s ease-in-out infinite alternate;

}


/* ============================================================
   FULL PAGE SCAN
   PART OF THE BACKGROUND ITSELF
============================================================ */

.stApp {

    background-image:

        linear-gradient(
            to bottom,
            transparent 0%,
            transparent 44%,
            rgba(255, 20, 85, 0.015) 46%,
            rgba(255, 35, 105, 0.10) 49%,
            rgba(145, 40, 255, 0.15) 50%,
            rgba(255, 30, 90, 0.06) 51%,
            transparent 56%,
            transparent 100%
        ),

        radial-gradient(
            ellipse 45% 35% at 15% 15%,
            rgba(76, 20, 190, 0.30),
            transparent 70%
        ),

        radial-gradient(
            ellipse 50% 40% at 85% 20%,
            rgba(255, 20, 80, 0.22),
            transparent 70%
        ),

        radial-gradient(
            ellipse 45% 45% at 75% 85%,
            rgba(90, 20, 210, 0.24),
            transparent 70%
        ),

        radial-gradient(
            ellipse 35% 40% at 20% 80%,
            rgba(210, 15, 70, 0.16),
            transparent 70%
        ),

        radial-gradient(circle at 7% 18%, rgba(255,55,130,0.8) 0 1px, transparent 2px),
        radial-gradient(circle at 17% 73%, rgba(130,80,255,0.75) 0 1px, transparent 2px),
        radial-gradient(circle at 28% 31%, rgba(255,60,140,0.65) 0 2px, transparent 3px),
        radial-gradient(circle at 39% 87%, rgba(110,100,255,0.7) 0 1px, transparent 2px),
        radial-gradient(circle at 52% 14%, rgba(255,50,120,0.75) 0 1px, transparent 2px),
        radial-gradient(circle at 63% 62%, rgba(170,70,255,0.65) 0 2px, transparent 3px),
        radial-gradient(circle at 76% 38%, rgba(255,50,110,0.7) 0 1px, transparent 2px),
        radial-gradient(circle at 88% 79%, rgba(100,100,255,0.7) 0 1px, transparent 2px),
        radial-gradient(circle at 93% 12%, rgba(255,60,130,0.7) 0 2px, transparent 3px),

        linear-gradient(
            135deg,
            #040208 0%,
            #0d0414 35%,
            #17040d 58%,
            #07040f 100%
        );

    background-size:
        100% 220%,
        180% 180%,
        170% 170%,
        180% 180%,
        160% 160%,
        100% 100%,
        100% 100%,
        100% 100%,
        100% 100%,
        100% 100%,
        100% 100%,
        100% 100%,
        100% 100%,
        100% 100%;

    background-position:
        0 -120vh,
        0% 0%,
        100% 0%,
        100% 100%,
        0% 100%,
        center,
        center,
        center,
        center,
        center,
        center,
        center,
        center,
        center;

    animation:
        pageScan 7s linear infinite,
        atmosphereMovement 20s ease-in-out infinite alternate;

}


/* ============================================================
   AMBIENT VIGNETTE
============================================================ */

.stApp > div {

    position: relative;

}


.stApp > div::before {

    content: "";

    position: fixed;

    inset: 0;

    pointer-events: none;

    z-index: 0;

    background:
        radial-gradient(
            ellipse at center,
            transparent 35%,
            rgba(0,0,0,0.30) 100%
        );

}


/* ============================================================
   CONTENT
============================================================ */

.block-container {

    position: relative;

    z-index: 10;

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

    font-family:
        "Inter",
        sans-serif;

}


h1 {

    font-family:
        "Cormorant Garamond",
        serif !important;

    font-size:
        clamp(4rem, 8vw, 7rem) !important;

    font-weight:
        500 !important;

    letter-spacing:
        0.025em;

    text-align:
        center;

    color:
        #f4edf0 !important;

    line-height:
        0.9 !important;

    margin-bottom:
        0.3rem !important;

    text-shadow:
        0 0 12px rgba(255,50,120,0.25),
        0 0 40px rgba(130,40,255,0.18),
        0 0 80px rgba(255,20,80,0.08);

    animation:
        titleGlow 4s ease-in-out infinite alternate;

}


h2,
h3 {

    font-family:
        "Cormorant Garamond",
        serif !important;

    color:
        #eee5e2 !important;

}


.stApp p {

    color:
        var(--text-soft);

}


/* ============================================================
   HEADER
============================================================ */

.header-subtitle {

    text-align:
        center;

    font-size:
        0.72rem;

    font-weight:
        400;

    letter-spacing:
        0.28em;

    text-transform:
        uppercase;

    color:
        #9d929a;

    margin-top:
        0.8rem;

    margin-bottom:
        3rem;

}


.header-line {

    height:
        2px;

    width:
        100%;

    margin-bottom:
        2.5rem;

    background:
        linear-gradient(
            90deg,
            transparent,
            #ff164f,
            #933cff,
            #ff3b91,
            #ff164f,
            transparent
        );

    background-size:
        300% 100%;

    box-shadow:
        0 0 15px rgba(255,30,100,0.5),
        0 0 40px rgba(120,40,255,0.25);

    animation:
        lineMovement 4s linear infinite;

}


/* ============================================================
   SIDEBAR
============================================================ */

section[data-testid="stSidebar"] {

    background:
        linear-gradient(
            180deg,
            rgba(5,2,9,0.98),
            rgba(15,3,16,0.97),
            rgba(5,4,14,0.98)
        );

    border-right:
        1px solid rgba(255,35,100,0.20);

    box-shadow:
        10px 0 70px rgba(100,0,80,0.20);

}


section[data-testid="stSidebar"] h3 {

    font-family:
        "Cormorant Garamond",
        serif !important;

    font-size:
        1.8rem !important;

    color:
        #eee4e5 !important;

}


section[data-testid="stSidebar"] p {

    font-size:
        0.8rem;

    line-height:
        1.7;

    color:
        #92878f;

}


/* ============================================================
   SECTION LABEL
============================================================ */

.section-label {

    font-size:
        0.65rem;

    letter-spacing:
        0.24em;

    text-transform:
        uppercase;

    color:
        #bd7188;

    margin-bottom:
        0.7rem;

}


/* ============================================================
   RADIO
============================================================ */

div[data-testid="stRadio"] label {

    color:
        #bcb1b8 !important;

    transition:
        all 0.25s ease;

}


div[data-testid="stRadio"] label:hover {

    color:
        #ff7197 !important;

    transform:
        translateX(5px);

    text-shadow:
        0 0 12px rgba(255,40,110,0.65);

}


/* ============================================================
   CAMERA
============================================================ */

[data-testid="stCameraInput"] {

    position:
        relative;

    z-index:
        20;

    background:
        linear-gradient(
            145deg,
            rgba(16,5,18,0.94),
            rgba(5,6,17,0.96)
        );

    border:
        1px solid rgba(255,40,105,0.25);

    padding:
        12px;

    border-radius:
        5px;

    box-shadow:
        0 25px 80px rgba(0,0,0,0.55),
        0 0 45px rgba(130,20,100,0.10);

    transition:
        transform 0.35s ease,
        border-color 0.35s ease,
        box-shadow 0.35s ease;

}


[data-testid="stCameraInput"]:hover {

    transform:
        translateY(-5px);

    border-color:
        rgba(255,55,125,0.65);

    box-shadow:
        0 30px 100px rgba(0,0,0,0.65),
        0 0 45px rgba(255,20,100,0.20),
        0 0 90px rgba(100,40,255,0.12);

}


/* ============================================================
   CAMERA BUTTON
============================================================ */

[data-testid="stCameraInput"] button {

    background:
        linear-gradient(
            110deg,
            #100711,
            #1b0716,
            #10071c
        ) !important;

    color:
        #eee6e7 !important;

    border:
        1px solid rgba(255,55,120,0.25) !important;

    border-radius:
        4px !important;

    transition:
        all 0.3s ease !important;

}


[data-testid="stCameraInput"] button:hover {

    background:
        linear-gradient(
            110deg,
            #270918,
            #190b2d,
            #270817
        ) !important;

    border-color:
        rgba(255,65,135,0.8) !important;

    box-shadow:
        0 0 25px rgba(255,20,90,0.25),
        0 0 45px rgba(100,40,255,0.15);

    transform:
        translateY(-2px);

}


/* ============================================================
   RESULT CONTAINER
============================================================ */

.result-container {

    position:
        relative;

    z-index:
        20;

    overflow:
        hidden;

    background:
        linear-gradient(
            135deg,
            rgba(25,5,20,0.94),
            rgba(6,6,19,0.96)
        );

    border:
        1px solid rgba(255,40,110,0.20);

    border-left:
        3px solid #ff285f;

    padding:
        2rem 2.2rem;

    min-height:
        170px;

    border-radius:
        3px;

    box-shadow:
        0 25px 80px rgba(0,0,0,0.50),
        0 0 40px rgba(150,20,90,0.10);

    transition:
        all 0.4s cubic-bezier(.2,.8,.2,1);

}


.result-container:hover {

    transform:
        translateY(-5px);

    border-color:
        rgba(255,55,125,0.55);

    box-shadow:
        0 30px 100px rgba(0,0,0,0.65),
        0 0 50px rgba(255,30,100,0.14),
        0 0 90px rgba(110,40,255,0.10);

}


/* moving light through result */

.result-container::before {

    content:
        "";

    position:
        absolute;

    width:
        45%;

    height:
        200%;

    top:
        -50%;

    left:
        -60%;

    pointer-events:
        none;

    background:
        linear-gradient(
            90deg,
            transparent,
            rgba(255,50,130,0.10),
            rgba(140,60,255,0.08),
            transparent
        );

    transform:
        rotate(18deg);

    animation:
        resultLight 5s ease-in-out infinite;

}


/* corner illumination */

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
        120px;

    height:
        120px;

    pointer-events:
        none;

    background:
        radial-gradient(
            circle at top right,
            rgba(255,40,120,0.13),
            transparent 70%
        );

}


/* ============================================================
   RESULT TEXT
============================================================ */

.result-text {

    position:
        relative;

    z-index:
        5;

    font-family:
        "Cormorant Garamond",
        serif;

    font-size:
        1.35rem;

    line-height:
        1.65;

    color:
        #eee4e0;

    white-space:
        pre-wrap;

    text-shadow:
        0 0 15px rgba(255,255,255,0.06);

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
        #a18a93;

}


.status-dot {

    width:
        7px;

    height:
        7px;

    border-radius:
        50%;

    background:
        #ff285f;

    box-shadow:
        0 0 8px #ff285f,
        0 0 20px rgba(255,30,100,0.8),
        0 0 40px rgba(255,20,80,0.35);

    animation:
        statusPulse 1.5s ease-in-out infinite;

}


/* ============================================================
   INFORMATION CARDS
============================================================ */

.info-card {

    position:
        relative;

    overflow:
        hidden;

    z-index:
        20;

    background:
        linear-gradient(
            145deg,
            rgba(20,5,20,0.92),
            rgba(6,7,18,0.94)
        );

    border:
        1px solid rgba(255,40,105,0.14);

    padding:
        1.2rem;

    text-align:
        center;

    border-radius:
        3px;

    box-shadow:
        0 15px 50px rgba(0,0,0,0.30);

    transition:
        all 0.35s cubic-bezier(.2,.8,.2,1);

}


.info-card::before {

    content:
        "";

    position:
        absolute;

    width:
        180%;

    height:
        2px;

    left:
        -40%;

    top:
        0;

    background:
        linear-gradient(
            90deg,
            transparent,
            #ff286b,
            #8c3cff,
            transparent
        );

    animation:
        cardScan 4s linear infinite;

}


.info-card:hover {

    transform:
        translateY(-8px)
        scale(1.025);

    border-color:
        rgba(255,55,125,0.45);

    box-shadow:
        0 25px 70px rgba(0,0,0,0.55),
        0 0 35px rgba(255,30,100,0.13),
        0 0 70px rgba(100,40,255,0.08);

}


.info-number {

    font-family:
        "Cormorant Garamond",
        serif;

    font-size:
        2rem;

    color:
        #f1dce4;

    text-shadow:
        0 0 15px rgba(255,40,120,0.35);

}


.info-label {

    font-size:
        0.6rem;

    letter-spacing:
        0.18em;

    text-transform:
        uppercase;

    color:
        #8c7c84;

}


/* ============================================================
   DIVIDER
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
            rgba(255,35,100,0.35),
            rgba(110,50,255,0.30),
            transparent
        ) !important;

    margin:
        2.5rem 0 !important;

}


/* ============================================================
   ANIMATIONS
============================================================ */

@keyframes pageScan {

    0% {

        background-position:
            0 -120vh,
            0% 0%,
            100% 0%,
            100% 100%,
            0% 100%,
            center,
            center,
            center,
            center,
            center,
            center,
            center,
            center,
            center;

    }

    100% {

        background-position:
            0 220vh,
            20% 10%,
            80% 15%,
            80% 90%,
            10% 90%,
            center,
            center,
            center,
            center,
            center,
            center,
            center,
            center,
            center;

    }

}


@keyframes atmosphereMovement {

    0% {

        filter:
            saturate(1)
            brightness(0.92);

    }

    50% {

        filter:
            saturate(1.35)
            brightness(1.05);

    }

    100% {

        filter:
            saturate(1.15)
            brightness(0.96);

    }

}


@keyframes titleGlow {

    from {

        text-shadow:
            0 0 10px rgba(255,40,110,0.20),
            0 0 35px rgba(120,40,255,0.12);

    }

    to {

        text-shadow:
            0 0 20px rgba(255,40,110,0.40),
            0 0 55px rgba(120,40,255,0.25);

    }

}


@keyframes lineMovement {

    0% {

        background-position:
            0% 50%;

    }

    100% {

        background-position:
            300% 50%;

    }

}


@keyframes resultLight {

    0% {

        left:
            -60%;

        opacity:
            0;

    }

    25% {

        opacity:
            1;

    }

    75% {

        opacity:
            1;

    }

    100% {

        left:
            120%;

        opacity:
            0;

    }

}


@keyframes cardScan {

    0% {

        transform:
            translateX(-60%);

    }

    100% {

        transform:
            translateX(60%);

    }

}


@keyframes statusPulse {

    0%,
    100% {

        transform:
            scale(0.75);

        opacity:
            0.55;

    }

    50% {

        transform:
            scale(1.4);

        opacity:
            1;

    }

}


/* ============================================================
   STREAMLIT BUTTONS
============================================================ */

.stButton > button {

    background:
        linear-gradient(
            110deg,
            #100611,
            #1c0718,
            #0e071c
        ) !important;

    color:
        #eee5e7 !important;

    border:
        1px solid rgba(255,45,115,0.25) !important;

    border-radius:
        4px !important;

    transition:
        all 0.25s ease !important;

}


.stButton > button:hover {

    transform:
        translateY(-3px);

    border-color:
        rgba(255,55,125,0.75) !important;

    box-shadow:
        0 0 25px rgba(255,30,100,0.20),
        0 0 50px rgba(100,40,255,0.10);

}


/* ============================================================
   FILE UPLOADER
============================================================ */

[data-testid="stFileUploader"] {

    position:
        relative;

    z-index:
        20;

}


[data-testid="stFileUploader"] section {

    background:
        linear-gradient(
            145deg,
            rgba(16,5,18,0.92),
            rgba(6,7,18,0.95)
        ) !important;

    border:
        1px solid rgba(255,40,110,0.20) !important;

    transition:
        all 0.3s ease;

}


[data-testid="stFileUploader"] section:hover {

    border-color:
        rgba(255,50,120,0.65) !important;

    box-shadow:
        0 0 35px rgba(255,30,100,0.12);

}


/* ============================================================
   CHECKBOX
============================================================ */

.stCheckbox label {

    color:
        #bcb0b7 !important;

}


.stCheckbox label:hover {

    color:
        #ff6d96 !important;

}


/* ============================================================
   RESPONSIVE
============================================================ */

@media (max-width: 768px) {

    .block-container {

        padding-left:
            1rem;

        padding-right:
            1rem;

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
    '<div class="header-subtitle">Análisis de imagen · Reconocimiento óptico de caracteres</div>',
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
        El sistema procesa la imagen y reconoce
        los caracteres presentes.
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
    # RESULT
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
    # SAFE OCR TEXT
    # ========================================================

    safe_text = (
        text
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


    if clean_text:

        display_text = safe_text

    else:

        display_text = (
            "No se encontró texto reconocible."
        )


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

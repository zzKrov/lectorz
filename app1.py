import streamlit as st
import streamlit.components.v1 as components
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
# GLOBAL VISUAL STYLE
# ============================================================

st.markdown("""
<style>

/* ============================================================
   IMPORTS
============================================================ */

@import url(
    'https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap'
);


/* ============================================================
   GLOBAL BACKGROUND
============================================================ */

.stApp {

    color: #eeeaf4;

    background:
        radial-gradient(
            circle at 8% 12%,
            rgba(255, 0, 91, 0.22),
            transparent 24%
        ),
        radial-gradient(
            circle at 92% 8%,
            rgba(111, 0, 255, 0.28),
            transparent 26%
        ),
        radial-gradient(
            circle at 82% 72%,
            rgba(0, 180, 255, 0.20),
            transparent 28%
        ),
        radial-gradient(
            circle at 15% 88%,
            rgba(255, 70, 0, 0.16),
            transparent 30%
        ),
        linear-gradient(
            125deg,
            #08020f,
            #12031a,
            #05091c,
            #16020f,
            #030710
        );

    background-size:
        180% 180%;

    animation:
        backgroundShift 18s ease-in-out infinite;

}


@keyframes backgroundShift {

    0% {
        background-position: 0% 20%;
    }

    25% {
        background-position: 70% 0%;
    }

    50% {
        background-position: 100% 80%;
    }

    75% {
        background-position: 20% 100%;
    }

    100% {
        background-position: 0% 20%;
    }

}


/* ============================================================
   AMBIENT LIGHTING
============================================================ */

.stApp::before {

    content: "";

    position: fixed;

    inset: -30%;

    pointer-events: none;

    z-index: 0;

    background:
        conic-gradient(
            from 0deg,
            transparent,
            rgba(255, 0, 110, 0.06),
            transparent 20%,
            rgba(100, 0, 255, 0.07),
            transparent 45%,
            rgba(0, 200, 255, 0.05),
            transparent 70%
        );

    filter: blur(55px);

    animation:
        ambientRotate 30s linear infinite;

}


@keyframes ambientRotate {

    from {
        transform: rotate(0deg) scale(1.1);
    }

    to {
        transform: rotate(360deg) scale(1.1);
    }

}


/* ============================================================
   CONTENT
============================================================ */

.block-container {

    position: relative;

    z-index: 2;

    max-width: 1250px;

    padding-top: 3rem;

    padding-bottom: 6rem;

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
        clamp(4rem, 9vw, 8rem) !important;

    font-weight:
        500 !important;

    letter-spacing:
        0.02em;

    text-align:
        center;

    line-height:
        0.82 !important;

    color:
        #fff5fc !important;

    margin-bottom:
        0.4rem !important;

    text-shadow:

        0 0 8px
        rgba(255,255,255,0.65),

        0 0 25px
        rgba(255,0,130,0.55),

        0 0 55px
        rgba(110,0,255,0.55),

        0 0 110px
        rgba(0,170,255,0.28);

    animation:
        titleGlow 4s ease-in-out infinite;

}


@keyframes titleGlow {

    0% {
        filter: brightness(0.92);
    }

    50% {
        filter: brightness(1.2);
    }

    100% {
        filter: brightness(0.92);
    }

}


h2,
h3 {

    font-family:
        "Cormorant Garamond",
        serif !important;

    color:
        #f0e8f2 !important;

}


.stApp p {

    color:
        #aaa4b7;

}


/* ============================================================
   HEADER
============================================================ */

.header-subtitle {

    text-align:
        center;

    font-size:
        0.72rem;

    letter-spacing:
        0.38em;

    text-transform:
        uppercase;

    color:
        #b3a5bd;

    margin-top:
        1rem;

    margin-bottom:
        2rem;

    text-shadow:
        0 0 18px
        rgba(210,130,255,0.55);

}


.header-line {

    height:
        2px;

    width:
        100%;

    margin-bottom:
        3rem;

    background:
        linear-gradient(
            90deg,
            transparent,
            #ff006e,
            #7a00ff,
            #00c8ff,
            #7a00ff,
            #ff006e,
            transparent
        );

    background-size:
        300% 100%;

    box-shadow:
        0 0 15px rgba(255,0,110,0.55),
        0 0 35px rgba(100,0,255,0.35);

    animation:
        lineFlow 5s linear infinite;

}


@keyframes lineFlow {

    from {
        background-position: 0% 50%;
    }

    to {
        background-position: 300% 50%;
    }

}


/* ============================================================
   SIDEBAR
============================================================ */

section[data-testid="stSidebar"] {

    background:
        linear-gradient(
            180deg,
            rgba(8,2,16,0.98),
            rgba(5,5,20,0.98)
        );

    border-right:
        1px solid
        rgba(190,80,255,0.22);

    box-shadow:
        15px 0 60px
        rgba(80,0,180,0.16);

}


section[data-testid="stSidebar"] h3 {

    color:
        #f3e9f7 !important;

    text-shadow:
        0 0 15px
        rgba(180,80,255,0.45);

}


section[data-testid="stSidebar"] p {

    color:
        #898197;

}


/* ============================================================
   SECTION LABELS
============================================================ */

.section-label {

    font-size:
        0.64rem;

    letter-spacing:
        0.30em;

    text-transform:
        uppercase;

    color:
        #a99ab5;

    margin-bottom:
        0.8rem;

}


/* ============================================================
   RADIO
============================================================ */

div[data-testid="stRadio"] label {

    color:
        #c7bdce !important;

    transition:
        all 0.25s ease;

}


div[data-testid="stRadio"] label:hover {

    color:
        #ffffff !important;

    transform:
        translateX(6px);

    text-shadow:
        0 0 15px
        rgba(255,0,130,0.7);

}


/* ============================================================
   CAMERA
============================================================ */

[data-testid="stCameraInput"] {

    position:
        relative;

    background:
        linear-gradient(
            135deg,
            rgba(20,4,30,0.95),
            rgba(4,10,28,0.95)
        );

    border:
        1px solid
        rgba(210,70,255,0.30);

    border-radius:
        10px;

    padding:
        12px;

    box-shadow:

        0 0 20px
        rgba(130,0,255,0.15),

        0 20px 70px
        rgba(0,0,0,0.45);

    transition:
        all 0.35s ease;

}


[data-testid="stCameraInput"]:hover {

    transform:
        translateY(-5px)
        scale(1.005);

    border-color:
        rgba(255,0,140,0.75);

    box-shadow:

        0 0 20px
        rgba(255,0,120,0.25),

        0 0 60px
        rgba(120,0,255,0.20),

        0 25px 80px
        rgba(0,0,0,0.60);

}


/* ============================================================
   CAMERA BUTTON
============================================================ */

[data-testid="stCameraInput"] button {

    background:
        linear-gradient(
            110deg,
            #17091f,
            #25103a,
            #09142e
        ) !important;

    color:
        #f0e9f3 !important;

    border:
        1px solid
        rgba(215,100,255,0.45) !important;

    border-radius:
        4px !important;

    transition:
        all 0.3s ease !important;

}


[data-testid="stCameraInput"] button:hover {

    transform:
        translateY(-2px);

    border-color:
        #ff3da2 !important;

    box-shadow:
        0 0 20px
        rgba(255,0,130,0.35) !important;

}


/* ============================================================
   RESULT
============================================================ */

.result-container {

    position:
        relative;

    overflow:
        hidden;

    background:
        linear-gradient(
            135deg,
            rgba(21,5,31,0.95),
            rgba(5,10,28,0.95)
        );

    border:
        1px solid
        rgba(180,80,255,0.24);

    border-left:
        3px solid
        #ff087e;

    padding:
        2rem 2.2rem;

    min-height:
        170px;

    border-radius:
        8px;

    box-shadow:

        0 0 25px
        rgba(130,0,255,0.12),

        0 20px 70px
        rgba(0,0,0,0.40);

    transition:
        all 0.35s ease;

}


.result-container:hover {

    transform:
        translateY(-5px);

    border-color:
        rgba(230,100,255,0.55);

    box-shadow:

        0 0 35px
        rgba(255,0,130,0.18),

        0 0 80px
        rgba(100,0,255,0.15),

        0 25px 80px
        rgba(0,0,0,0.55);

}


/* animated light crossing result */

.result-container::before {

    content:
        "";

    position:
        absolute;

    top:
        -100%;

    left:
        -20%;

    width:
        25%;

    height:
        300%;

    background:
        linear-gradient(
            90deg,
            transparent,
            rgba(255,255,255,0.08),
            transparent
        );

    transform:
        rotate(20deg);

    animation:
        resultSweep 6s ease-in-out infinite;

}


@keyframes resultSweep {

    0% {
        left: -30%;
    }

    55% {
        left: 120%;
    }

    100% {
        left: 120%;
    }

}


.result-container::after {

    content:
        "";

    position:
        absolute;

    right:
        0;

    top:
        0;

    width:
        120px;

    height:
        120px;

    border-top:
        1px solid
        rgba(255,0,110,0.45);

    border-right:
        1px solid
        rgba(100,0,255,0.45);

    box-shadow:
        8px -8px 35px
        rgba(255,0,130,0.10);

}


.result-text {

    position:
        relative;

    z-index:
        2;

    font-family:
        "Cormorant Garamond",
        serif;

    font-size:
        1.4rem;

    line-height:
        1.7;

    color:
        #eee7ef;

    white-space:
        pre-wrap;

    text-shadow:
        0 0 15px
        rgba(230,200,255,0.20);

}


/* ============================================================
   INFO CARDS
============================================================ */

.info-card {

    position:
        relative;

    overflow:
        hidden;

    background:
        linear-gradient(
            135deg,
            rgba(23,5,34,0.88),
            rgba(4,10,27,0.90)
        );

    border:
        1px solid
        rgba(175,80,255,0.20);

    padding:
        1.3rem;

    text-align:
        center;

    border-radius:
        7px;

    box-shadow:
        0 15px 45px
        rgba(0,0,0,0.25);

    transition:
        all 0.3s ease;

}


.info-card::before {

    content:
        "";

    position:
        absolute;

    width:
        150px;

    height:
        150px;

    left:
        50%;

    top:
        50%;

    transform:
        translate(-50%, -50%);

    background:
        radial-gradient(
            circle,
            rgba(255,0,130,0.12),
            transparent 70%
        );

    opacity:
        0;

    transition:
        opacity 0.3s ease;

}


.info-card:hover {

    transform:
        translateY(-7px)
        scale(1.02);

    border-color:
        rgba(255,70,170,0.55);

    box-shadow:

        0 0 25px
        rgba(255,0,130,0.18),

        0 20px 60px
        rgba(0,0,0,0.40);

}


.info-card:hover::before {

    opacity:
        1;

}


.info-number {

    position:
        relative;

    z-index:
        2;

    font-family:
        "Cormorant Garamond",
        serif;

    font-size:
        2.2rem;

    color:
        #eee7f2;

    text-shadow:
        0 0 20px
        rgba(200,120,255,0.50);

}


.info-label {

    position:
        relative;

    z-index:
        2;

    font-size:
        0.6rem;

    letter-spacing:
        0.2em;

    text-transform:
        uppercase;

    color:
        #84798e;

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
        #8e8299;

}


.status-dot {

    width:
        8px;

    height:
        8px;

    border-radius:
        50%;

    background:
        #ff087e;

    box-shadow:

        0 0 8px
        #ff087e,

        0 0 22px
        #ff087e,

        0 0 45px
        rgba(120,0,255,0.8);

    animation:
        statusPulse 1.5s ease-in-out infinite;

}


@keyframes statusPulse {

    0%,
    100% {
        transform: scale(0.8);
        opacity: 0.65;
    }

    50% {
        transform: scale(1.25);
        opacity: 1;
    }

}


/* ============================================================
   BUTTONS
============================================================ */

.stButton > button {

    position:
        relative;

    overflow:
        hidden;

    min-height:
        55px;

    background:
        linear-gradient(
            110deg,
            #1b0528,
            #470936,
            #130a3d,
            #06243b
        );

    background-size:
        300% 300%;

    color:
        #fff4fa;

    border:
        1px solid
        rgba(255,70,170,0.50);

    border-radius:
        5px;

    font-family:
        "Inter",
        sans-serif;

    letter-spacing:
        0.15em;

    transition:
        all 0.3s ease;

    animation:
        buttonGradient 7s ease infinite;

}


@keyframes buttonGradient {

    0% {
        background-position: 0% 50%;
    }

    50% {
        background-position: 100% 50%;
    }

    100% {
        background-position: 0% 50%;
    }

}


.stButton > button:hover {

    transform:
        translateY(-4px)
        scale(1.01);

    border-color:
        #ff51ad;

    box-shadow:

        0 0 20px
        rgba(255,0,130,0.35),

        0 0 60px
        rgba(100,0,255,0.20);

}


.stButton > button:active {

    transform:
        translateY(1px)
        scale(0.99);

}


/* ============================================================
   FILE UPLOADER
============================================================ */

[data-testid="stFileUploader"] {

    background:
        linear-gradient(
            135deg,
            rgba(15,4,25,0.85),
            rgba(4,10,26,0.85)
        );

    border:
        1px dashed
        rgba(190,80,255,0.35);

    border-radius:
        8px;

    transition:
        all 0.3s ease;

}


[data-testid="stFileUploader"]:hover {

    border-color:
        #ff3c9f;

    box-shadow:

        0 0 25px
        rgba(255,0,130,0.15),

        0 0 55px
        rgba(100,0,255,0.10);

}


/* ============================================================
   SELECT / INPUTS
============================================================ */

div[data-baseweb="select"] > div {

    background:
        rgba(8,5,17,0.95) !important;

    border:
        1px solid
        rgba(180,80,255,0.25) !important;

    transition:
        all 0.25s ease;

}


div[data-baseweb="select"] > div:hover {

    border-color:
        rgba(255,60,160,0.65) !important;

    box-shadow:
        0 0 20px
        rgba(180,0,255,0.15);

}


/* ============================================================
   DIVIDERS
============================================================ */

hr {

    border:
        none !important;

    height:
        2px !important;

    background:
        linear-gradient(
            90deg,
            transparent,
            rgba(255,0,110,0.45),
            rgba(100,0,255,0.45),
            rgba(0,190,255,0.40),
            transparent
        ) !important;

    box-shadow:
        0 0 15px
        rgba(130,0,255,0.18);

    margin:
        2.8rem 0 !important;

}


/* ============================================================
   IMAGE
============================================================ */

[data-testid="stImage"] img {

    border-radius:
        8px;

    border:
        1px solid
        rgba(180,70,255,0.25);

    box-shadow:

        0 0 25px
        rgba(130,0,255,0.18),

        0 25px 70px
        rgba(0,0,0,0.50);

    transition:
        all 0.35s ease;

}


[data-testid="stImage"] img:hover {

    transform:
        scale(1.01);

    border-color:
        rgba(255,60,160,0.60);

    box-shadow:

        0 0 30px
        rgba(255,0,130,0.25),

        0 0 70px
        rgba(100,0,255,0.20),

        0 30px 80px
        rgba(0,0,0,0.55);

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
            0.55rem;

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
# ANIMATED VISUAL HEADER
#
# This is isolated inside components.html() so none of the
# HTML/JavaScript can appear as visible Streamlit source.
# ============================================================

components.html(
    """
<!DOCTYPE html>
<html>
<head>

<style>

* {
    box-sizing: border-box;
}

html,
body {

    margin: 0;
    padding: 0;

    width: 100%;
    height: 100%;

    overflow: hidden;

    background: transparent;

}

.scene {

    position: relative;

    width: 100%;
    height: 190px;

    overflow: hidden;

    border-radius: 14px;

    background:
        radial-gradient(
            circle at 50% 50%,
            rgba(100,0,255,0.20),
            transparent 40%
        );

}


/* ============================================================
   LARGE MOVING BLOBS
============================================================ */

.blob {

    position: absolute;

    width: 260px;
    height: 260px;

    border-radius: 50%;

    filter: blur(35px);

    opacity: 0.35;

    pointer-events: none;

}


.blob.one {

    left: -100px;
    top: -140px;

    background:
        #ff006e;

    animation:
        blobOne 11s ease-in-out infinite;

}


.blob.two {

    right: -100px;
    top: -100px;

    background:
        #6200ff;

    animation:
        blobTwo 14s ease-in-out infinite;

}


.blob.three {

    left: 40%;
    bottom: -220px;

    background:
        #00c8ff;

    animation:
        blobThree 12s ease-in-out infinite;

}


@keyframes blobOne {

    0%,
    100% {
        transform: translate(0,0) scale(1);
    }

    50% {
        transform: translate(130px,80px) scale(1.25);
    }

}


@keyframes blobTwo {

    0%,
    100% {
        transform: translate(0,0) scale(1);
    }

    50% {
        transform: translate(-120px,70px) scale(1.2);
    }

}


@keyframes blobThree {

    0%,
    100% {
        transform: translate(0,0);
    }

    50% {
        transform: translate(-90px,-100px);
    }

}


/* ============================================================
   PARTICLES
============================================================ */

.particles {

    position: absolute;

    inset: 0;

    overflow: hidden;

    pointer-events: none;

}


.particle {

    position: absolute;

    border-radius: 50%;

    background:
        white;

    box-shadow:
        0 0 8px currentColor,
        0 0 20px currentColor;

    animation:
        particleFloat
        var(--duration)
        ease-in-out
        var(--delay)
        infinite;

}


@keyframes particleFloat {

    0% {

        transform:
            translate3d(
                0,
                30px,
                0
            )
            scale(0.1);

        opacity: 0;

    }

    15% {

        opacity: 0.9;

    }

    50% {

        transform:
            translate3d(
                var(--drift),
                -90px,
                0
            )
            scale(1);

        opacity: 0.75;

    }

    85% {

        opacity: 0.4;

    }

    100% {

        transform:
            translate3d(
                var(--drift2),
                -220px,
                0
            )
            scale(0.1);

        opacity: 0;

    }

}


/* ============================================================
   LIGHT RAYS
============================================================ */

.ray {

    position: absolute;

    left: 50%;
    top: 50%;

    width: 2px;
    height: 150%;

    transform-origin: center;

    background:
        linear-gradient(
            transparent,
            rgba(255,255,255,0.18),
            transparent
        );

    filter: blur(1px);

    opacity: 0.4;

    animation:
        raySpin
        15s linear infinite;

}


.ray:nth-child(2) {
    transform: rotate(35deg);
}

.ray:nth-child(3) {
    transform: rotate(85deg);
}

.ray:nth-child(4) {
    transform: rotate(140deg);
}

.ray:nth-child(5) {
    transform: rotate(210deg);
}

.ray:nth-child(6) {
    transform: rotate(275deg);
}


@keyframes raySpin {

    from {
        rotate: 0deg;
    }

    to {
        rotate: 360deg;
    }

}


/* ============================================================
   CENTRAL CORE
============================================================ */

.core {

    position: absolute;

    left: 50%;
    top: 50%;

    width: 110px;
    height: 110px;

    transform:
        translate(-50%,-50%);

    border-radius: 50%;

    background:
        radial-gradient(
            circle,
            rgba(255,255,255,0.30),
            rgba(200,80,255,0.16),
            transparent 70%
        );

    filter:
        blur(5px);

    box-shadow:

        0 0 30px
        rgba(255,0,130,0.35),

        0 0 70px
        rgba(100,0,255,0.30),

        0 0 120px
        rgba(0,190,255,0.20);

    animation:
        corePulse 3.5s ease-in-out infinite;

}


@keyframes corePulse {

    0%,
    100% {
        transform:
            translate(-50%,-50%)
            scale(0.85);
        opacity: 0.65;
    }

    50% {
        transform:
            translate(-50%,-50%)
            scale(1.2);
        opacity: 1;
    }

}


/* ============================================================
   MOUSE LIGHT
============================================================ */

.mouse-light {

    position: absolute;

    width: 180px;
    height: 180px;

    left: 50%;
    top: 50%;

    transform:
        translate(-50%,-50%);

    border-radius: 50%;

    background:
        radial-gradient(
            circle,
            rgba(255,255,255,0.16),
            rgba(160,0,255,0.08),
            transparent 70%
        );

    filter:
        blur(10px);

    pointer-events: none;

    transition:
        left 0.08s linear,
        top 0.08s linear;

}


/* ============================================================
   SCAN
============================================================ */

.scan {

    position: absolute;

    left: 0;
    right: 0;

    height: 2px;

    background:
        linear-gradient(
            90deg,
            transparent,
            rgba(255,0,130,0.8),
            rgba(120,0,255,1),
            rgba(0,200,255,0.8),
            transparent
        );

    box-shadow:

        0 0 10px
        rgba(255,0,130,0.9),

        0 0 35px
        rgba(100,0,255,0.8);

    animation:
        scanMove 4s ease-in-out infinite;

}


@keyframes scanMove {

    0% {
        top: -5%;
        opacity: 0;
    }

    10% {
        opacity: 1;
    }

    90% {
        opacity: 1;
    }

    100% {
        top: 105%;
        opacity: 0;
    }

}


/* ============================================================
   MOUSE TRAIL
============================================================ */

.trail {

    position: absolute;

    width: 7px;
    height: 7px;

    border-radius: 50%;

    pointer-events: none;

    background:
        white;

    box-shadow:

        0 0 8px
        #ff2a9d,

        0 0 20px
        #7d35ff;

    animation:
        trailFade 0.7s ease-out forwards;

}


@keyframes trailFade {

    0% {

        transform:
            scale(1);

        opacity:
            0.9;

    }

    100% {

        transform:
            scale(0);

        opacity:
            0;

    }

}

</style>

</head>

<body>

<div class="scene">

    <div class="blob one"></div>
    <div class="blob two"></div>
    <div class="blob three"></div>

    <div class="particles"></div>

    <div class="ray"></div>
    <div class="ray"></div>
    <div class="ray"></div>
    <div class="ray"></div>
    <div class="ray"></div>

    <div class="core"></div>

    <div class="mouse-light"></div>

    <div class="scan"></div>

</div>


<script>

/* ============================================================
   PARTICLES
============================================================ */

const particleContainer =
    document.querySelector(".particles");


const particleColors = [
    "#ff2a9d",
    "#9d4dff",
    "#35d9ff",
    "#ffffff",
    "#ff6a3d"
];


for (let i = 0; i < 90; i++) {

    const p =
        document.createElement("span");

    p.className =
        "particle";

    p.style.left =
        Math.random() * 100 + "%";

    p.style.top =
        45 + Math.random() * 65 + "%";

    p.style.width =
        (1 + Math.random() * 3.5) + "px";

    p.style.height =
        p.style.width;

    p.style.color =
        particleColors[
            Math.floor(
                Math.random() *
                particleColors.length
            )
        ];

    p.style.setProperty(
        "--duration",
        (5 + Math.random() * 12) + "s"
    );

    p.style.setProperty(
        "--delay",
        (-Math.random() * 12) + "s"
    );

    p.style.setProperty(
        "--drift",
        (-80 + Math.random() * 160) + "px"
    );

    p.style.setProperty(
        "--drift2",
        (-120 + Math.random() * 240) + "px"
    );

    particleContainer.appendChild(p);

}


/* ============================================================
   MOUSE TRACKING
============================================================ */

const scene =
    document.querySelector(".scene");

const mouseLight =
    document.querySelector(".mouse-light");


scene.addEventListener(
    "mousemove",
    function(event) {

        const rect =
            scene.getBoundingClientRect();

        const x =
            event.clientX - rect.left;

        const y =
            event.clientY - rect.top;

        mouseLight.style.left =
            x + "px";

        mouseLight.style.top =
            y + "px";


        /* Mouse trail */

        const trail =
            document.createElement("span");

        trail.className =
            "trail";

        trail.style.left =
            x + "px";

        trail.style.top =
            y + "px";

        scene.appendChild(trail);


        setTimeout(
            () => trail.remove(),
            700
        );

    }
);


/* ============================================================
   IDLE LIGHT MOVEMENT
============================================================ */

let idleX = 50;
let idleY = 50;

setInterval(
    function() {

        idleX =
            35 +
            Math.sin(
                Date.now() / 3000
            ) * 20;

        idleY =
            45 +
            Math.cos(
                Date.now() / 2500
            ) * 20;

        if (
            !scene.matches(":hover")
        ) {

            mouseLight.style.left =
                idleX + "%";

            mouseLight.style.top =
                idleY + "%";

        }

    },
    40
);

</script>

</body>
</html>
""",
    height=210,
    scrolling=False
)


# ============================================================
# HEADER
# ============================================================

st.title(
    "Reconocimiento óptico de caracteres"
)

st.markdown(
    '<div class="header-subtitle">'
    'IMAGE ANALYSIS · OPTICAL CHARACTER RECOGNITION'
    '</div>',
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
# CAPTURE
# ============================================================

st.markdown(
    '<div class="section-label">Captura</div>',
    unsafe_allow_html=True
)

img_file_buffer = st.camera_input(
    "Toma una Foto"
)


# ============================================================
# OCR
# ============================================================

if img_file_buffer is not None:

    bytes_data = (
        img_file_buffer
        .getvalue()
    )

    cv2_img = cv2.imdecode(
        np.frombuffer(
            bytes_data,
            np.uint8
        ),
        cv2.IMREAD_COLOR
    )

    if filtro == "Con Filtro":

        cv2_img = cv2.bitwise_not(
            cv2_img
        )

    else:

        cv2_img = cv2_img

    img_rgb = cv2.cvtColor(
        cv2_img,
        cv2.COLOR_BGR2RGB
    )

    text = pytesseract.image_to_string(
        img_rgb
    )

    clean_text = text.strip()

    character_count = len(
        clean_text
    )

    word_count = len(
        text.split()
    )


    # ========================================================
    # RESULT
    # ========================================================

    st.markdown("---")

    st.markdown(
        '<div class="section-label">Resultado</div>',
        unsafe_allow_html=True
    )


    if character_count > 0:

        status_text = (
            "Texto detectado"
        )

    else:

        status_text = (
            "No se detectó texto"
        )


    st.markdown(
        f"""
        <div class="status">

            <div class="status-dot"></div>

            <span>{status_text}</span>

        </div>
        """,
        unsafe_allow_html=True
    )


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

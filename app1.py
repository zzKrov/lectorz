import streamlit as st
import cv2
import numpy as np
import pytesseract
from PIL import Image

st.markdown("""
<style>

/* ============================================================
   GLOBAL LAYERS
============================================================ */

.stApp {
    position: relative;
    min-height: 100vh;
    overflow-x: hidden;

    background:
        radial-gradient(
            circle at var(--mouse-x, 50%) var(--mouse-y, 35%),
            rgba(180, 20, 80, 0.22),
            transparent 28%
        ),
        radial-gradient(
            circle at 15% 20%,
            rgba(70, 20, 190, 0.18),
            transparent 35%
        ),
        radial-gradient(
            circle at 85% 80%,
            rgba(220, 20, 60, 0.16),
            transparent 35%
        ),
        linear-gradient(
            135deg,
            #050309,
            #110510 40%,
            #08040e 70%,
            #03040a
        );

    color: #eee8df;
}


/* ============================================================
   BACKGROUND ATMOSPHERE
   ALWAYS BEHIND THE WEBSITE
============================================================ */

.stApp::before {

    content: "";

    position: fixed;
    inset: -50%;

    z-index: 0;
    pointer-events: none;

    background:
        conic-gradient(
            from 0deg,
            transparent,
            rgba(100, 20, 255, 0.08),
            transparent,
            rgba(255, 20, 80, 0.09),
            transparent
        );

    filter: blur(55px);

    animation:
        atmosphereSpin 30s linear infinite;
}


/* ============================================================
   PARTICLES
============================================================ */

.stApp .block-container::before {

    content:
        "✦     ·       ✧          ·     ✦       ·        ✧      ·     ✦";

    position: fixed;
    inset: 0;

    z-index: 1;
    pointer-events: none;

    color: rgba(255, 60, 140, 0.35);

    font-size: 16px;
    line-height: 120px;
    letter-spacing: 60px;

    white-space: pre-wrap;

    filter:
        drop-shadow(0 0 8px rgba(255,30,120,0.8));

    animation:
        particlesFloat 18s linear infinite;
}


.stApp .block-container::after {

    content:
        "·       ✦       ·       ✧       ·       ✦       ·       ✧";

    position: fixed;
    inset: -100px;

    z-index: 1;
    pointer-events: none;

    color: rgba(110, 90, 255, 0.30);

    font-size: 11px;
    line-height: 90px;
    letter-spacing: 100px;

    animation:
        particlesFloatReverse 25s linear infinite;

}


/* ============================================================
   ACTUAL STREAMLIT CONTENT
   ABOVE BACKGROUND EFFECTS
============================================================ */

.stApp > div {

    position: relative;
    z-index: 5;

}


/* Main content */

.block-container {

    position: relative;
    z-index: 10;

    max-width: 1150px;

    padding-top: 3rem;
    padding-bottom: 5rem;

}


/* ============================================================
   FULL PAGE SCANNER
   BEHIND CONTENT
============================================================ */

.stApp > div:first-child::before {

    content: "";

    position: fixed;

    left: 0;
    right: 0;

    top: -30vh;

    height: 30vh;

    z-index: 2;
    pointer-events: none;

    background:
        linear-gradient(
            to bottom,
            transparent 0%,
            rgba(255,20,80,0.015) 15%,
            rgba(255,30,100,0.07) 45%,
            rgba(140,40,255,0.10) 50%,
            rgba(255,30,100,0.025) 70%,
            transparent 100%
        );

    box-shadow:
        0 0 60px rgba(255,30,100,0.12);

    filter: blur(3px);

    animation:
        fullPageScan 8s linear infinite;

}


/* ============================================================
   SCANNER LINE
   ALSO BEHIND CONTENT
============================================================ */

.stApp > div:first-child::after {

    content: "";

    position: fixed;

    left: 0;
    right: 0;

    top: -3px;

    height: 2px;

    z-index: 3;
    pointer-events: none;

    background:
        linear-gradient(
            90deg,
            transparent,
            rgba(255,30,100,0.15),
            rgba(255,70,160,0.95),
            rgba(120,50,255,0.8),
            transparent
        );

    box-shadow:
        0 0 12px rgba(255,40,120,0.8),
        0 0 35px rgba(140,40,255,0.45);

    animation:
        scannerLine 8s linear infinite;

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

    text-align:
        center;

    color:
        #f2e9ed !important;

    text-shadow:
        0 0 15px rgba(255,40,120,0.25),
        0 0 40px rgba(120,40,255,0.15);

}


/* ============================================================
   CARDS
============================================================ */

.info-card,
.result-container,
[data-testid="stCameraInput"] {

    position: relative;
    z-index: 20;

}


/* ============================================================
   ANIMATIONS
============================================================ */

@keyframes fullPageScan {

    0% {
        transform: translateY(0);
    }

    100% {
        transform: translateY(440vh);
    }

}


@keyframes scannerLine {

    0% {
        top: -3px;
    }

    100% {
        top: 100vh;
    }

}


@keyframes atmosphereSpin {

    from {
        transform: rotate(0deg);
    }

    to {
        transform: rotate(360deg);
    }

}


@keyframes particlesFloat {

    0% {
        transform:
            translate3d(-30px, 0, 0);
    }

    50% {
        transform:
            translate3d(45px, -40px, 0);
    }

    100% {
        transform:
            translate3d(-30px, -80px, 0);
    }

}


@keyframes particlesFloatReverse {

    0% {
        transform:
            translate3d(40px, 30px, 0);
    }

    50% {
        transform:
            translate3d(-50px, -30px, 0);
    }

    100% {
        transform:
            translate3d(40px, -90px, 0);
    }

}


/* ============================================================
   MOBILE
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

}

</style>
""", unsafe_allow_html=True)

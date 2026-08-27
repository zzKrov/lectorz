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
   VARIABLES
============================================================ */

:root {

    --black: #030207;
    --deep-purple: #0b0315;
    --purple: #6326ff;
    --violet: #9b42ff;
    --red: #ff174f;
    --pink: #ff3c91;
    --blue: #3155ff;

    --white: #f2edf1;
    --soft: #b9afb8;
    --dim: #817680;

}


/* ============================================================
   GLOBAL BACKGROUND
============================================================ */

.stApp {

    min-height: 100vh;

    overflow-x: hidden;

    color: var(--white);

    background-color: var(--black);

    background-image:

        /* large moving atmospheric lights */

        radial-gradient(
            ellipse 40% 35% at 5% 10%,
            rgba(105, 25, 255, 0.30),
            transparent 70%
        ),

        radial-gradient(
            ellipse 45% 40% at 95% 15%,
            rgba(255, 15, 85, 0.25),
            transparent 70%
        ),

        radial-gradient(
            ellipse 50% 45% at 80% 90%,
            rgba(65, 40, 255, 0.25),
            transparent 70%
        ),

        radial-gradient(
            ellipse 40% 40% at 10% 85%,
            rgba(255, 20, 100, 0.18),
            transparent 70%
        ),

        /* glowing particles */

        radial-gradient(
            circle at 8% 18%,
            rgba(255, 40, 120, 0.95) 0 1px,
            transparent 3px
        ),

        radial-gradient(
            circle at 15% 67%,
            rgba(130, 70, 255, 0.9) 0 2px,
            transparent 4px
        ),

        radial-gradient(
            circle at 23% 38%,
            rgba(255, 70, 150, 0.85) 0 1px,
            transparent 3px
        ),

        radial-gradient(
            circle at 31% 82%,
            rgba(80, 100, 255, 0.9) 0 1px,
            transparent 3px
        ),

        radial-gradient(
            circle at 43% 12%,
            rgba(255, 40, 110, 0.9) 0 2px,
            transparent 4px
        ),

        radial-gradient(
            circle at 56% 73%,
            rgba(155, 60, 255, 0.9) 0 1px,
            transparent 3px
        ),

        radial-gradient(
            circle at 67% 27%,
            rgba(255, 45, 125, 0.9) 0 1px,
            transparent 3px
        ),

        radial-gradient(
            circle at 74% 65%,
            rgba(75, 100, 255, 0.9) 0 2px,
            transparent 4px
        ),

        radial-gradient(
            circle at 87% 42%,
            rgba(255, 45, 130, 0.85) 0 1px,
            transparent 3px
        ),

        radial-gradient(
            circle at 94% 82%,
            rgba(130, 65, 255, 0.9) 0 2px,
            transparent 4px
        ),

        /* base */

        linear-gradient(
            135deg,
            #030207 0%,
            #100419 32%,
            #18040e 58%,
            #07040f 100%
        );

    background-size:
        170% 170%,
        180% 180%,
        180% 180%,
        170% 170%,
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

    animation:
        atmosphere 16s ease-in-out infinite alternate;

}


/* ============================================================
   MOVING LIGHT
============================================================ */

.stApp::after {

    content: "";

    position: fixed;

    width: 55vw;

    height: 55vw;

    left: -20vw;

    top: -15vw;

    pointer-events: none;

    z-index: 0;

    border-radius: 50%;

    background:
        radial-gradient(
            circle,
            rgba(255, 30, 110, 0.09),
            rgba(115, 30, 255, 0.05),
            transparent 70%
        );

    filter:
        blur(20px);

    animation:
        lightOrbit 14s ease-in-out infinite alternate;

}


/* ============================================================
   ERRATIC PARTICLE FIELD
============================================================ */

.stApp > div::before {

    content: "";

    position: fixed;

    inset: -30%;

    pointer-events: none;

    z-index: 1;

    opacity: 0.9;

    background-image:

        radial-gradient(
            circle,
            rgba(255, 70, 150, 0.95) 0 2px,
            transparent 4px
        ),

        radial-gradient(
            circle,
            rgba(130, 65, 255, 0.95) 0 2px,
            transparent 4px
        ),

        radial-gradient(
            circle,
            rgba(255, 45, 110, 0.9) 0 1.5px,
            transparent 4px
        ),

        radial-gradient(
            circle,
            rgba(70, 105, 255, 0.9) 0 2px,
            transparent 4px
        ),

        radial-gradient(
            circle,
            rgba(255, 150, 210, 0.8) 0 1px,
            transparent 3px
        ),

        radial-gradient(
            circle,
            rgba(170, 100, 255, 0.85) 0 1.5px,
            transparent 4px
        ),

        radial-gradient(
            circle,
            rgba(255, 40, 130, 0.8) 0 2px,
            transparent 5px
        ),

        radial-gradient(
            circle,
            rgba(80, 130, 255, 0.8) 0 1.5px,
            transparent 4px
        );

    background-size:
        105px 125px,
        145px 170px,
        190px 145px,
        230px 190px,
        125px 210px,
        270px 160px,
        175px 260px,
        310px 220px;

    animation:
        particleChaos1 7s linear infinite,
        particleChaos2 11s ease-in-out infinite alternate;

    filter:
        drop-shadow(0 0 5px rgba(255,50,130,0.7))
        drop-shadow(0 0 12px rgba(100,50,255,0.35));

}


/* Second independent particle layer */

.stApp > div::after {

    content: "";

    position: fixed;

    inset: -40%;

    pointer-events: none;

    z-index: 2;

    opacity: 0.55;

    background-image:

        radial-gradient(
            circle,
            rgba(255, 80, 160, 0.9) 0 2px,
            transparent 5px
        ),

        radial-gradient(
            circle,
            rgba(100, 80, 255, 0.9) 0 2px,
            transparent 5px
        ),

        radial-gradient(
            circle,
            rgba(255, 40, 100, 0.8) 0 1px,
            transparent 4px
        ),

        radial-gradient(
            circle,
            rgba(130, 50, 255, 0.8) 0 1.5px,
            transparent 4px
        ),

        radial-gradient(
            circle,
            rgba(255, 180, 220, 0.75) 0 1px,
            transparent 3px
        );

    background-size:
        180px 230px,
        260px 190px,
        150px 310px,
        330px 240px,
        210px 170px;

    animation:
        particleChaos3 5s linear infinite,
        particleChaos4 8s ease-in-out infinite alternate;

    filter:
        blur(0.2px)
        drop-shadow(0 0 8px rgba(255,40,130,0.7));

}


/* ============================================================
   CHAOTIC MOTION
============================================================ */

@keyframes particleChaos1 {

    0% {
        transform:
            translate3d(-4%, -5%, 0)
            rotate(0deg);
    }

    17% {
        transform:
            translate3d(7%, -13%, 0)
            rotate(1deg);
    }

    31% {
        transform:
            translate3d(-9%, 4%, 0)
            rotate(-2deg);
    }

    48% {
        transform:
            translate3d(13%, 9%, 0)
            rotate(3deg);
    }

    64% {
        transform:
            translate3d(2%, -15%, 0)
            rotate(-1deg);
    }

    79% {
        transform:
            translate3d(-14%, 8%, 0)
            rotate(2deg);
    }

    100% {
        transform:
            translate3d(5%, 14%, 0)
            rotate(-3deg);
    }

}


@keyframes particleChaos2 {

    0% {
        transform:
            scale(0.9)
            skewX(-2deg);
    }

    27% {
        transform:
            scale(1.12)
            skewX(3deg);
    }

    53% {
        transform:
            scale(0.82)
            skewX(-4deg);
    }

    76% {
        transform:
            scale(1.2)
            skewX(2deg);
    }

    100% {
        transform:
            scale(0.95)
            skewX(-3deg);
    }

}


@keyframes particleChaos3 {

    0% {
        transform:
            translate3d(8%, 10%, 0)
            rotate(0deg);
    }

    19% {
        transform:
            translate3d(-12%, 2%, 0)
            rotate(-3deg);
    }

    37% {
        transform:
            translate3d(15%, -10%, 0)
            rotate(4deg);
    }

    55% {
        transform:
            translate3d(-5%, 16%, 0)
            rotate(-2deg);
    }

    73% {
        transform:
            translate3d(-17%, -7%, 0)
            rotate(3deg);
    }

    100% {
        transform:
            translate3d(11%, 12%, 0)
            rotate(-4deg);
    }

}


@keyframes particleChaos4 {

    0% {
        opacity: 0.35;
        transform: scale(0.8);
    }

    25% {
        opacity: 0.8;
        transform: scale(1.15);
    }

    50% {
        opacity: 0.45;
        transform: scale(0.9);
    }

    75% {
        opacity: 0.95;
        transform: scale(1.25);
    }

    100% {
        opacity: 0.5;
        transform: scale(0.85);
    }

}


/* ============================================================
   CONTENT LAYER
============================================================ */

.block-container {

    position: relative;

    z-index: 10;

    max-width: 1150px;

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
        clamp(4rem, 8vw, 7rem) !important;

    font-weight:
        500 !important;

    letter-spacing:
        0.025em;

    text-align:
        center;

    color:
        var(--white) !important;

    line-height:
        0.9 !important;

    text-shadow:
        0 0 15px rgba(255,255,255,0.12),
        0 0 35px rgba(255,30,110,0.25),
        0 0 70px rgba(120,40,255,0.18);

    animation:
        titlePulse 5s ease-in-out infinite alternate;

}


h2,
h3 {

    font-family:
        "Cormorant Garamond",
        serif !important;

    color:
        #eee7eb !important;

}


.stApp p {

    color:
        var(--soft);

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
        0.28em;

    text-transform:
        uppercase;

    color:
        #a998a4;

    margin-top:
        0.8rem;

    margin-bottom:
        3rem;

}


.header-line {

    height:
        2px;

    background:
        linear-gradient(
            90deg,
            transparent,
            #ff174f,
            #8b35ff,
            #ff3d91,
            #3155ff,
            transparent
        );

    background-size:
        250% 100%;

    box-shadow:
        0 0 15px rgba(255,25,100,0.65),
        0 0 35px rgba(120,30,255,0.25);

    animation:
        lineFlow 4s linear infinite;

}


/* ============================================================
   SIDEBAR
============================================================ */

section[data-testid="stSidebar"] {

    background:
        linear-gradient(
            180deg,
            rgba(4,2,9,0.98),
            rgba(14,3,20,0.97),
            rgba(4,3,12,0.98)
        );

    border-right:
        1px solid rgba(255,35,110,0.25);

    box-shadow:
        12px 0 80px rgba(100,20,150,0.18);

}


section[data-testid="stSidebar"] h3 {

    color:
        #eee6eb !important;

}


/* ============================================================
   LABELS
============================================================ */

.section-label {

    font-size:
        0.65rem;

    letter-spacing:
        0.24em;

    text-transform:
        uppercase;

    color:
        #c47791;

    margin-bottom:
        0.7rem;

}


/* ============================================================
   RADIO INTERACTION
============================================================ */

div[data-testid="stRadio"] label {

    color:
        #bfb2bb !important;

    transition:
        all 0.3s ease;

}


div[data-testid="stRadio"] label:hover {

    color:
        #ff6b96 !important;

    transform:
        translateX(7px);

    text-shadow:
        0 0 15px rgba(255,40,110,0.6);

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
            rgba(18,4,20,0.94),
            rgba(5,5,18,0.96)
        );

    border:
        1px solid rgba(255,40,110,0.25);

    padding:
        12px;

    border-radius:
        5px;

    box-shadow:
        0 25px 90px rgba(0,0,0,0.6),
        0 0 45px rgba(150,20,100,0.10);

    transition:
        all 0.4s cubic-bezier(.2,.8,.2,1);

}


[data-testid="stCameraInput"]:hover {

    transform:
        translateY(-7px)
        scale(1.01);

    border-color:
        rgba(255,70,140,0.75);

    box-shadow:
        0 35px 110px rgba(0,0,0,0.7),
        0 0 45px rgba(255,25,100,0.25),
        0 0 100px rgba(100,40,255,0.13);

}


/* ============================================================
   CAMERA BUTTON
============================================================ */

[data-testid="stCameraInput"] button {

    background:
        linear-gradient(
            110deg,
            #100611,
            #21071c,
            #100820
        ) !important;

    color:
        #f0e7eb !important;

    border:
        1px solid rgba(255,55,125,0.30) !important;

    border-radius:
        4px !important;

    transition:
        all 0.3s ease !important;

}


[data-testid="stCameraInput"] button:hover {

    transform:
        translateY(-2px);

    border-color:
        rgba(255,70,140,0.9) !important;

    box-shadow:
        0 0 25px rgba(255,30,100,0.35),
        0 0 60px rgba(100,40,255,0.16);

}


/* ============================================================
   RESULT
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
            rgba(27,5,23,0.94),
            rgba(5,6,20,0.97)
        );

    border:
        1px solid rgba(255,45,115,0.22);

    border-left:
        3px solid #ff285f;

    padding:
        2rem 2.2rem;

    min-height:
        170px;

    border-radius:
        4px;

    box-shadow:
        0 25px 80px rgba(0,0,0,0.55),
        0 0 50px rgba(150,20,100,0.10);

    transition:
        all 0.45s cubic-bezier(.2,.8,.2,1);

}


.result-container:hover {

    transform:
        translateY(-7px)
        scale(1.005);

    border-color:
        rgba(255,60,130,0.65);

    box-shadow:
        0 35px 110px rgba(0,0,0,0.70),
        0 0 55px rgba(255,25,100,0.20),
        0 0 110px rgba(100,40,255,0.13);

}


/* moving reflection */

.result-container::before {

    content:
        "";

    position:
        absolute;

    top:
        -60%;

    left:
        -80%;

    width:
        45%;

    height:
        220%;

    transform:
        rotate(20deg);

    pointer-events:
        none;

    background:
        linear-gradient(
            90deg,
            transparent,
            rgba(255,50,130,0.14),
            rgba(120,50,255,0.12),
            transparent
        );

    animation:
        reflection 5s ease-in-out infinite;

}


/* corner glow */

.result-container::after {

    content:
        "";

    position:
        absolute;

    right:
        -50px;

    top:
        -50px;

    width:
        150px;

    height:
        150px;

    border-radius:
        50%;

    pointer-events:
        none;

    background:
        radial-gradient(
            circle,
            rgba(255,35,120,0.16),
            transparent 70%
        );

    filter:
        blur(5px);

    animation:
        cornerGlow 3s ease-in-out infinite alternate;

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
        #eee5e6;

    white-space:
        pre-wrap;

    text-shadow:
        0 0 15px rgba(255,255,255,0.07);

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
        #a58d98;

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
        0 0 20px rgba(255,30,100,0.9),
        0 0 40px rgba(255,20,80,0.4);

    animation:
        statusPulse 1.4s ease-in-out infinite;

}


/* ============================================================
   INFO CARDS
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
            rgba(20,5,21,0.94),
            rgba(5,7,19,0.96)
        );

    border:
        1px solid rgba(255,40,110,0.17);

    padding:
        1.3rem;

    text-align:
        center;

    border-radius:
        4px;

    box-shadow:
        0 18px 55px rgba(0,0,0,0.35);

    transition:
        all 0.35s cubic-bezier(.2,.8,.2,1);

}


.info-card:hover {

    transform:
        translateY(-9px)
        scale(1.035);

    border-color:
        rgba(255,65,135,0.65);

    box-shadow:
        0 25px 80px rgba(0,0,0,0.55),
        0 0 35px rgba(255,30,100,0.20),
        0 0 75px rgba(100,40,255,0.13);

}


/* animated border */

.info-card::before {

    content:
        "";

    position:
        absolute;

    inset:
        -2px;

    z-index:
        -1;

    background:
        conic-gradient(
            from 0deg,
            transparent,
            #ff174f,
            transparent,
            #873cff,
            transparent
        );

    animation:
        borderRotate 4s linear infinite;

    opacity:
        0;

    transition:
        opacity 0.3s ease;

}


.info-card:hover::before {

    opacity:
        1;

}


/* card light */

.info-card::after {

    content:
        "";

    position:
        absolute;

    width:
        80px;

    height:
        80px;

    left:
        50%;

    top:
        50%;

    transform:
        translate(-50%, -50%);

    background:
        radial-gradient(
            circle,
            rgba(255,35,120,0.12),
            transparent 70%
        );

    pointer-events:
        none;

    animation:
        cardPulse 3s ease-in-out infinite;

}


.info-number {

    position:
        relative;

    z-index:
        5;

    font-family:
        "Cormorant Garamond",
        serif;

    font-size:
        2rem;

    color:
        #f2dfe7;

    text-shadow:
        0 0 15px rgba(255,40,120,0.4);

}


.info-label {

    position:
        relative;

    z-index:
        5;

    font-size:
        0.6rem;

    letter-spacing:
        0.18em;

    text-transform:
        uppercase;

    color:
        #917f89;

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
            rgba(255,30,100,0.4),
            rgba(100,50,255,0.4),
            transparent
        ) !important;

    box-shadow:
        0 0 10px rgba(255,30,100,0.12);

}


/* ============================================================
   ANIMATIONS
============================================================ */

@keyframes atmosphere {

    0% {

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

        filter:
            saturate(1)
            brightness(0.90);

    }

    50% {

        filter:
            saturate(1.4)
            brightness(1.05);

    }

    100% {

        background-position:
            20% 20%,
            80% 15%,
            80% 80%,
            15% 85%,
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

        filter:
            saturate(1.2)
            brightness(0.98);

    }

}


@keyframes lightOrbit {

    0% {

        transform:
            translate(0, 0)
            scale(0.9);

    }

    50% {

        transform:
            translate(45vw, 20vh)
            scale(1.2);

    }

    100% {

        transform:
            translate(70vw, 55vh)
            scale(0.85);

    }

}


@keyframes particlesDrift {

    0% {

        transform:
            translate3d(-2%, -2%, 0)
            rotate(0deg);

    }

    50% {

        transform:
            translate3d(3%, -5%, 0)
            rotate(2deg);

    }

    100% {

        transform:
            translate3d(-4%, 4%, 0)
            rotate(-2deg);

    }

}


@keyframes titlePulse {

    0% {

        text-shadow:
            0 0 12px rgba(255,30,110,0.20),
            0 0 30px rgba(110,40,255,0.10);

    }

    100% {

        text-shadow:
            0 0 22px rgba(255,40,120,0.42),
            0 0 60px rgba(120,40,255,0.25);

    }

}


@keyframes lineFlow {

    0% {

        background-position:
            0% 50%;

    }

    100% {

        background-position:
            250% 50%;

    }

}


@keyframes reflection {

    0% {

        left:
            -80%;

        opacity:
            0;

    }

    20% {

        opacity:
            1;

    }

    70% {

        opacity:
            1;

    }

    100% {

        left:
            130%;

        opacity:
            0;

    }

}


@keyframes cornerGlow {

    from {

        opacity:
            0.4;

        transform:
            scale(0.8);

    }

    to {

        opacity:
            1;

        transform:
            scale(1.25);

    }

}


@keyframes statusPulse {

    0%,
    100% {

        transform:
            scale(0.7);

        opacity:
            0.5;

    }

    50% {

        transform:
            scale(1.5);

        opacity:
            1;

    }

}


@keyframes borderRotate {

    from {

        transform:
            rotate(0deg);

    }

    to {

        transform:
            rotate(360deg);

    }

}


@keyframes cardPulse {

    0%,
    100% {

        opacity:
            0.2;

        transform:
            translate(-50%, -50%)
            scale(0.7);

    }

    50% {

        opacity:
            0.7;

        transform:
            translate(-50%, -50%)
            scale(1.8);

    }

}


/* ============================================================
   BUTTONS
============================================================ */

.stButton > button {

    background:
        linear-gradient(
            110deg,
            #100611,
            #23081c,
            #0d0820
        ) !important;

    color:
        #f0e7eb !important;

    border:
        1px solid rgba(255,45,115,0.30) !important;

    border-radius:
        4px !important;

    transition:
        all 0.3s ease !important;

}


.stButton > button:hover {

    transform:
        translateY(-3px)
        scale(1.015);

    border-color:
        rgba(255,70,140,0.85) !important;

    box-shadow:
        0 0 25px rgba(255,30,100,0.28),
        0 0 60px rgba(100,40,255,0.15);

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
            rgba(18,5,20,0.94),
            rgba(5,6,18,0.96)
        ) !important;

    border:
        1px solid rgba(255,40,110,0.22) !important;

    transition:
        all 0.35s ease;

}


[data-testid="stFileUploader"] section:hover {

    transform:
        translateY(-5px);

    border-color:
        rgba(255,65,135,0.75) !important;

    box-shadow:
        0 20px 70px rgba(0,0,0,0.55),
        0 0 35px rgba(255,30,100,0.15);

}


/* ============================================================
   CHECKBOX
============================================================ */

.stCheckbox label {

    color:
        #bcb0b8 !important;

    transition:
        all 0.25s ease;

}


.stCheckbox label:hover {

    color:
        #ff6d96 !important;

}


/* ============================================================
   MOBILE
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

    bytes_data = img_file_buffer.getvalue()

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


    img_rgb = cv2.cvtColor(
        cv2_img,
        cv2.COLOR_BGR2RGB
    )


    text = pytesseract.image_to_string(
        img_rgb
    )


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
    # SAFE TEXT
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

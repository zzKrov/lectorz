import streamlit as st
import cv2
import numpy as np
import pytesseract
from PIL import Image
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');


/* ============================================================
   GLOBAL
============================================================ */

html, body, [class*="css"] {
    font-family: "Inter", sans-serif;
}

.stApp {
    position: relative;
    min-height: 100vh;
    overflow-x: hidden;

    background:
        radial-gradient(
            circle at var(--mouse-x, 50%) var(--mouse-y, 30%),
            rgba(150, 15, 65, 0.25),
            transparent 24%
        ),
        radial-gradient(
            circle at 15% 20%,
            rgba(50, 20, 180, 0.20),
            transparent 32%
        ),
        radial-gradient(
            circle at 85% 75%,
            rgba(190, 20, 45, 0.20),
            transparent 35%
        ),
        linear-gradient(
            125deg,
            #050309,
            #10050e 35%,
            #09040e 65%,
            #03040a
        );

    color: #eee8df;
}


/* ============================================================
   FULL PAGE ATMOSPHERE
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
            rgba(110, 0, 255, 0.08),
            transparent,
            rgba(255, 0, 90, 0.08),
            transparent
        );

    animation:
        atmosphereSpin 28s linear infinite;

    filter: blur(45px);

}


.stApp::after {

    content: "";

    position: fixed;

    inset: 0;

    z-index: 1;

    pointer-events: none;

    background:

        repeating-linear-gradient(
            0deg,
            transparent 0px,
            transparent 5px,
            rgba(255,255,255,0.012) 6px
        ),

        linear-gradient(
            90deg,
            transparent,
            rgba(255,255,255,0.018),
            transparent
        );

    mix-blend-mode: screen;

}


/* ============================================================
   FULL SCREEN SCANNER
============================================================ */

.stApp > div:first-child::before {

    content: "";

    position: fixed;

    left: 0;
    right: 0;

    height: 25vh;

    top: -25vh;

    z-index: 2;

    pointer-events: none;

    background:
        linear-gradient(
            to bottom,
            transparent,
            rgba(255, 20, 90, 0.015) 10%,
            rgba(255, 40, 110, 0.12) 45%,
            rgba(120, 20, 255, 0.16) 50%,
            rgba(255, 20, 90, 0.04) 70%,
            transparent
        );

    filter: blur(4px);

    box-shadow:
        0 0 60px rgba(255, 20, 90, 0.12);

    animation:
        pageScanner 7s linear infinite;

}


/* ============================================================
   MOVING LASER LINE
============================================================ */

.stApp > div:first-child::after {

    content: "";

    position: fixed;

    left: 0;
    right: 0;

    height: 2px;

    top: -5px;

    z-index: 3;

    pointer-events: none;

    background:
        linear-gradient(
            90deg,
            transparent,
            rgba(255,30,110,0.15),
            rgba(255,80,170,0.95),
            rgba(130,50,255,0.8),
            transparent
        );

    box-shadow:
        0 0 12px rgba(255,40,120,0.9),
        0 0 35px rgba(150,30,255,0.5);

    animation:
        laserScan 7s linear infinite;

}


/* ============================================================
   PARTICLE FIELD
============================================================ */

.stApp .block-container {

    position: relative;

    z-index: 10;

}


.stApp .block-container::before {

    content:
        "✦   ·       ✧        ·   ✦        ·       ✧   ·       ✦        ·   ✧       ·       ✦";

    position: fixed;

    inset: 0;

    z-index: 2;

    pointer-events: none;

    font-size: 18px;

    line-height: 110px;

    letter-spacing: 75px;

    color: rgba(255, 70, 150, 0.28);

    white-space: pre-wrap;

    word-spacing: 50px;

    opacity: 0.65;

    animation:
        particleDrift 18s linear infinite;

    filter:
        drop-shadow(0 0 8px rgba(255,30,120,0.8))
        drop-shadow(0 0 15px rgba(100,50,255,0.4));

}


/* ============================================================
   PARTICLE SECONDARY LAYER
============================================================ */

.stApp .block-container::after {

    content:
        "·       ✦       ·    ✧       ·       ✦    ·       ✧       ·    ✦       ·";

    position: fixed;

    inset: -100px;

    z-index: 2;

    pointer-events: none;

    font-size: 11px;

    line-height: 85px;

    letter-spacing: 110px;

    color: rgba(100, 120, 255, 0.35);

    animation:
        particleDriftReverse 25s linear infinite;

    filter:
        blur(0.3px)
        drop-shadow(0 0 8px rgba(80,80,255,0.8));

}


/* ============================================================
   MAIN CONTAINER
============================================================ */

.block-container {

    max-width: 1150px;

    padding-top: 3rem;
    padding-bottom: 5rem;

}


/* ============================================================
   TYPOGRAPHY
============================================================ */

h1 {

    font-family:
        "Cormorant Garamond",
        serif !important;

    font-size:
        clamp(4rem, 8vw, 7rem) !important;

    font-weight:
        500 !important;

    letter-spacing:
        0.03em;

    text-align:
        center;

    color:
        #f4edf0 !important;

    line-height:
        0.9 !important;

    margin-bottom:
        0.2rem !important;

    text-shadow:
        0 0 10px rgba(255,60,130,0.25),
        0 0 35px rgba(130,30,255,0.15);

    animation:
        titlePulse 5s ease-in-out infinite;

}


h2,
h3 {

    font-family:
        "Cormorant Garamond",
        serif !important;

    font-weight:
        600 !important;

    color:
        #eee5e0 !important;

}


.stApp p {

    color:
        #b8afb3;

}


/* ============================================================
   HEADER
============================================================ */

.header-subtitle {

    text-align:
        center;

    font-family:
        "Inter",
        sans-serif;

    font-size:
        0.72rem;

    letter-spacing:
        0.28em;

    text-transform:
        uppercase;

    color:
        #a49aa2;

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

    background:
        linear-gradient(
            90deg,
            transparent,
            #ff174f,
            #8d35ff,
            #ff174f,
            transparent
        );

    background-size:
        300% 100%;

    box-shadow:
        0 0 15px rgba(255,30,90,0.45);

    animation:
        gradientMove 5s linear infinite;

    margin-bottom:
        2.5rem;

}


/* ============================================================
   SIDEBAR
============================================================ */

section[data-testid="stSidebar"] {

    background:
        linear-gradient(
            180deg,
            rgba(5,3,9,0.97),
            rgba(12,4,15,0.96)
        );

    border-right:
        1px solid rgba(255,40,100,0.18);

    box-shadow:
        10px 0 50px rgba(100,0,80,0.15);

}


section[data-testid="stSidebar"] h3 {

    font-size:
        1.7rem !important;

}


section[data-testid="stSidebar"] p {

    font-size:
        0.8rem;

    line-height:
        1.7;

    color:
        #91878e;

}


/* ============================================================
   RADIO
============================================================ */

div[data-testid="stRadio"] label {

    color:
        #b9afb5 !important;

    transition:
        all 0.25s ease;

}


div[data-testid="stRadio"] label:hover {

    color:
        #ff668f !important;

    transform:
        translateX(6px);

    text-shadow:
        0 0 10px rgba(255,30,90,0.6);

}


/* ============================================================
   CAMERA
============================================================ */

[data-testid="stCameraInput"] {

    position:
        relative;

    background:
        linear-gradient(
            145deg,
            rgba(15,5,15,0.95),
            rgba(7,7,18,0.95)
        );

    border:
        1px solid rgba(255,40,100,0.22);

    padding:
        12px;

    box-shadow:
        0 20px 70px rgba(0,0,0,0.55),
        0 0 40px rgba(130,20,100,0.12);

    transition:
        all 0.35s ease;

}


[data-testid="stCameraInput"]:hover {

    transform:
        translateY(-5px)
        scale(1.005);

    border-color:
        rgba(255,40,110,0.65);

    box-shadow:
        0 25px 90px rgba(0,0,0,0.7),
        0 0 45px rgba(255,20,90,0.18),
        0 0 90px rgba(100,20,255,0.12);

}


/* ============================================================
   CAMERA BUTTON
============================================================ */

[data-testid="stCameraInput"] button {

    background:
        linear-gradient(
            120deg,
            #100b13,
            #1b0713,
            #100b1b
        ) !important;

    color:
        #eee6e5 !important;

    border:
        1px solid rgba(255,60,120,0.25) !important;

    border-radius:
        4px !important;

    transition:
        all 0.3s ease !important;

}


[data-testid="stCameraInput"] button:hover {

    background:
        linear-gradient(
            120deg,
            #210b19,
            #180c29,
            #270915
        ) !important;

    border-color:
        rgba(255,60,130,0.8) !important;

    box-shadow:
        0 0 25px rgba(255,20,90,0.25),
        inset 0 0 15px rgba(130,30,255,0.12);

    transform:
        translateY(-2px);

}


/* ============================================================
   SECTION LABEL
============================================================ */

.section-label {

    font-family:
        "Inter",
        sans-serif;

    font-size:
        0.65rem;

    letter-spacing:
        0.24em;

    text-transform:
        uppercase;

    color:
        #a06a7b;

    margin-bottom:
        0.7rem;

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
            rgba(20,5,18,0.95),
            rgba(7,7,18,0.95)
        );

    border:
        1px solid rgba(255,40,100,0.18);

    border-left:
        3px solid #ff285f;

    padding:
        2rem 2.2rem;

    min-height:
        170px;

    box-shadow:
        0 20px 70px rgba(0,0,0,0.45),
        0 0 35px rgba(150,20,80,0.08);

    transition:
        all 0.4s ease;

}


.result-container:hover {

    transform:
        translateY(-4px);

    border-color:
        rgba(255,50,120,0.5);

    box-shadow:
        0 25px 90px rgba(0,0,0,0.65),
        0 0 50px rgba(255,30,100,0.13),
        0 0 90px rgba(100,40,255,0.08);

}


.result-container::before {

    content:
        "";

    position:
        absolute;

    width:
        150%;

    height:
        2px;

    left:
        -25%;

    top:
        0;

    background:
        linear-gradient(
            90deg,
            transparent,
            #ff2768,
            #8c3cff,
            transparent
        );

    animation:
        resultScan 4s linear infinite;

}


.result-container::after {

    content:
        "";

    position:
        absolute;

    inset:
        0;

    pointer-events:
        none;

    background:
        radial-gradient(
            circle at var(--mouse-x, 50%) var(--mouse-y, 50%),
            rgba(255,40,100,0.08),
            transparent 35%
        );

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
        1.35rem;

    line-height:
        1.65;

    color:
        #eee5e0;

    white-space:
        pre-wrap;

    text-shadow:
        0 0 10px rgba(255,255,255,0.05);

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
            145deg,
            rgba(18,7,18,0.9),
            rgba(7,8,18,0.9)
        );

    border:
        1px solid rgba(255,40,100,0.12);

    padding:
        1.2rem;

    text-align:
        center;

    transition:
        all 0.35s cubic-bezier(.2,.8,.2,1);

}


.info-card::before {

    content:
        "";

    position:
        absolute;

    inset:
        -100%;

    background:
        linear-gradient(
            120deg,
            transparent 40%,
            rgba(255,40,110,0.12),
            transparent 60%
        );

    transform:
        translateX(-50%);

    transition:
        transform 0.7s ease;

}


.info-card:hover::before {

    transform:
        translateX(50%);

}


.info-card:hover {

    transform:
        translateY(-8px)
        scale(1.025);

    background:
        linear-gradient(
            145deg,
            rgba(35,8,25,0.95),
            rgba(10,8,25,0.95)
        );

    border-color:
        rgba(255,50,120,0.45);

    box-shadow:
        0 15px 50px rgba(0,0,0,0.5),
        0 0 35px rgba(255,30,100,0.12);

}


.info-number {

    font-family:
        "Cormorant Garamond",
        serif;

    font-size:
        2rem;

    color:
        #f0dce2;

    text-shadow:
        0 0 15px rgba(255,50,120,0.3);

}


.info-label {

    font-size:
        0.6rem;

    letter-spacing:
        0.18em;

    text-transform:
        uppercase;

    color:
        #88777f;

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
        #9d858e;

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
        0 0 20px rgba(255,40,100,0.8);

    animation:
        statusPulse 1.5s ease-in-out infinite;

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
            rgba(255,40,100,0.3),
            rgba(100,50,255,0.3),
            transparent
        ) !important;

    margin:
        2.5rem 0 !important;

}


/* ============================================================
   ANIMATIONS
============================================================ */

@keyframes pageScanner {

    0% {
        transform: translateY(0);
    }

    100% {
        transform: translateY(500vh);
    }

}


@keyframes laserScan {

    0% {
        top: -5px;
    }

    100% {
        top: 100vh;
    }

}


@keyframes atmosphereSpin {

    0% {
        transform: rotate(0deg);
    }

    100% {
        transform: rotate(360deg);
    }

}


@keyframes particleDrift {

    0% {
        transform:
            translate3d(-30px, 0, 0)
            rotate(0deg);
    }

    50% {
        transform:
            translate3d(40px, -40px, 0)
            rotate(8deg);
    }

    100% {
        transform:
            translate3d(-30px, -80px, 0)
            rotate(0deg);
    }

}


@keyframes particleDriftReverse {

    0% {
        transform:
            translate3d(40px, 50px, 0);
    }

    50% {
        transform:
            translate3d(-50px, -20px, 0);
    }

    100% {
        transform:
            translate3d(40px, -90px, 0);
    }

}


@keyframes titlePulse {

    0%, 100% {
        text-shadow:
            0 0 10px rgba(255,60,130,0.2),
            0 0 35px rgba(130,30,255,0.1);
    }

    50% {
        text-shadow:
            0 0 18px rgba(255,60,130,0.35),
            0 0 55px rgba(130,30,255,0.22);
    }

}


@keyframes gradientMove {

    0% {
        background-position: 0% 50%;
    }

    100% {
        background-position: 300% 50%;
    }

}


@keyframes resultScan {

    0% {
        transform: translateX(-100%);
    }

    100% {
        transform: translateX(100%);
    }

}


@keyframes statusPulse {

    0%, 100% {
        transform: scale(0.8);
        opacity: 0.6;
    }

    50% {
        transform: scale(1.35);
        opacity: 1;
    }

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


<script>

(function() {

    const app = document.querySelector('.stApp');

    if (!app) return;


    /* ========================================================
       MOUSE POSITION
    ======================================================== */

    let mouseX = 50;
    let mouseY = 30;

    let targetX = 50;
    let targetY = 30;


    document.addEventListener('mousemove', function(e) {

        targetX = (e.clientX / window.innerWidth) * 100;
        targetY = (e.clientY / window.innerHeight) * 100;

    });


    function animateMouse() {

        mouseX += (targetX - mouseX) * 0.08;
        mouseY += (targetY - mouseY) * 0.08;

        app.style.setProperty(
            '--mouse-x',
            mouseX + '%'
        );

        app.style.setProperty(
            '--mouse-y',
            mouseY + '%'
        );

        requestAnimationFrame(animateMouse);

    }

    animateMouse();


    /* ========================================================
       MOUSE TRAIL
    ======================================================== */

    const trail = [];

    const TRAIL_LENGTH = 14;


    for (let i = 0; i < TRAIL_LENGTH; i++) {

        const dot = document.createElement('div');

        dot.style.position = 'fixed';
        dot.style.width = (4 - i * 0.18) + 'px';
        dot.style.height = (4 - i * 0.18) + 'px';
        dot.style.borderRadius = '50%';

        dot.style.pointerEvents = 'none';

        dot.style.zIndex = '999999';

        dot.style.background =
            i % 2 === 0
            ? 'rgba(255,45,110,0.9)'
            : 'rgba(130,70,255,0.9)';

        dot.style.boxShadow =
            '0 0 ' +
            (8 - i * 0.3) +
            'px rgba(255,30,120,0.8)';

        dot.style.transform =
            'translate(-50%, -50%)';

        document.body.appendChild(dot);

        trail.push({
            element: dot,
            x: 0,
            y: 0
        });

    }


    let cursorX = 0;
    let cursorY = 0;


    document.addEventListener('mousemove', function(e) {

        cursorX = e.clientX;
        cursorY = e.clientY;

    });


    function animateTrail() {

        let x = cursorX;
        let y = cursorY;


        trail.forEach(function(point, index) {

            point.x += (x - point.x) * (
                0.35 - index * 0.015
            );

            point.y += (y - point.y) * (
                0.35 - index * 0.015
            );


            point.element.style.left =
                point.x + 'px';

            point.element.style.top =
                point.y + 'px';


            x = point.x;
            y = point.y;

        });


        requestAnimationFrame(animateTrail);

    }

    animateTrail();


    /* ========================================================
       CLICK BURST
    ======================================================== */

    document.addEventListener('click', function(e) {

        for (let i = 0; i < 12; i++) {

            const particle =
                document.createElement('div');

            particle.style.position = 'fixed';

            particle.style.left =
                e.clientX + 'px';

            particle.style.top =
                e.clientY + 'px';

            particle.style.width = '5px';
            particle.style.height = '5px';

            particle.style.borderRadius = '50%';

            particle.style.pointerEvents =
                'none';

            particle.style.zIndex =
                '999999';

            particle.style.background =
                i % 2 === 0
                ? '#ff2868'
                : '#8d42ff';

            particle.style.boxShadow =
                '0 0 12px currentColor';

            const angle =
                Math.random() * Math.PI * 2;

            const distance =
                40 + Math.random() * 80;

            const dx =
                Math.cos(angle) * distance;

            const dy =
                Math.sin(angle) * distance;


            particle.animate(

                [
                    {
                        transform:
                            'translate(-50%, -50%) scale(1)',
                        opacity: 1
                    },

                    {
                        transform:
                            `translate(
                                ${dx - 50}px,
                                ${dy - 50}px
                            ) scale(0)`,
                        opacity: 0
                    }
                ],

                {
                    duration:
                        500 + Math.random() * 500,

                    easing:
                        'cubic-bezier(.2,.8,.2,1)'
                }

            );


            document.body.appendChild(
                particle
            );


            setTimeout(
                () => particle.remove(),
                1100
            );

        }

    });


})();

</script>
""", unsafe_allow_html=True)

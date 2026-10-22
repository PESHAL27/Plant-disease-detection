"""
AgroScan AI - Design System, Custom CSS & Smooth Motion Animations
Encapsulates all color tokens, typography, glassmorphism, responsive cards,
and buttery-smooth landing animations to achieve an exceptional commercial SaaS aesthetic.
"""

def get_custom_css():
    return """
<style>
/* ==========================================================================
   AGROSCAN AI - PREMIUM DESIGN SYSTEM & SMOOTH MOTION
   ========================================================================== */

@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700&display=swap');

:root {
    --forest-green: #173D2B;
    --primary-green: #28563B;
    --sage-green: #5F9668;
    --soft-leaf-green: #D8E7B8;
    --warm-ivory: #F5F4EC;
    --pure-white: #FFFFFF;
    --muted-gold: #D5A75A;
    --secondary-text: #617264;
    --card-border: #E5EADF;
    --border-dashed: #BFD3B7;
    --font-sans: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    --font-heading: 'Outfit', 'Plus Jakarta Sans', sans-serif;
    --ease-spring: cubic-bezier(0.16, 1, 0.3, 1);
}

/* Smooth HTML Scrolling */
html {
    scroll-behavior: smooth !important;
}

/* Base Body & App Container */
html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--warm-ivory) !important;
    font-family: var(--font-sans) !important;
    color: #173D2B !important;
    -webkit-font-smoothing: antialiased;
}

[data-testid="stHeader"] {
    background: transparent !important;
    height: 0px !important;
}

#MainMenu, header, footer, [data-testid="stDecoration"], [data-testid="stToolbar"] {
    display: none !important;
}

/* Global Content Landing Animation */
.block-container {
    padding-top: 1.2rem !important;
    padding-bottom: 2.5rem !important;
    max-width: 1180px !important;
    margin: 0 auto !important;
    animation: pageFadeIn 0.45s var(--ease-spring) both;
}

@keyframes pageFadeIn {
    0% {
        opacity: 0;
        transform: translateY(12px);
    }
    100% {
        opacity: 1;
        transform: translateY(0);
    }
}

/* ==========================================================================
   NAVBAR COMPONENT
   ========================================================================== */
.agroscan-navbar {
    background-color: var(--forest-green);
    border-radius: 16px;
    padding: 12px 28px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 4px 20px rgba(23, 61, 43, 0.12);
    margin-bottom: 24px;
    animation: navbarSlideDown 0.5s var(--ease-spring) both;
    transition: box-shadow 0.3s ease;
}

@keyframes navbarSlideDown {
    0% {
        opacity: 0;
        transform: translateY(-12px);
    }
    100% {
        opacity: 1;
        transform: translateY(0);
    }
}

.nav-brand {
    display: flex;
    align-items: center;
    gap: 10px;
    text-decoration: none !important;
    color: var(--pure-white) !important;
    font-size: 20px;
    font-weight: 800;
    letter-spacing: -0.3px;
    transition: transform 0.25s var(--ease-spring);
}

.nav-brand:hover {
    transform: scale(1.02);
}

.nav-brand svg {
    width: 24px;
    height: 24px;
    fill: var(--soft-leaf-green);
    transition: transform 0.3s var(--ease-spring);
}

.nav-brand:hover svg {
    transform: rotate(-8deg) scale(1.1);
}

.nav-links {
    display: flex;
    align-items: center;
    gap: 6px;
}

.agroscan-navbar a,
.agroscan-navbar a:link,
.agroscan-navbar a:visited,
.nav-link-item,
.nav-link-item:link,
.nav-link-item:visited {
    text-decoration: none !important;
    color: #CADBCF !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    padding: 7px 16px !important;
    border-radius: 20px !important;
    transition: all 0.25s var(--ease-spring) !important;
    display: inline-block !important;
}

.agroscan-navbar a:hover,
.nav-link-item:hover {
    color: #FFFFFF !important;
    background-color: rgba(255, 255, 255, 0.12) !important;
    text-decoration: none !important;
    transform: translateY(-1px);
}

.agroscan-navbar a.active,
.agroscan-navbar a.active:visited,
.nav-link-item.active,
.nav-link-item.active:visited {
    background-color: #28563B !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.25) !important;
    text-decoration: none !important;
    transform: none !important;
}

.nav-icon svg {
    width: 22px;
    height: 22px;
    fill: var(--sage-green);
    transition: transform 0.3s ease;
}

.nav-icon:hover svg {
    transform: rotate(45deg);
}

/* ==========================================================================
   HERO BANNER - SMOOTH ENTRANCE & BOTANICAL GLIDE
   ========================================================================== */
.hero-container {
    background: linear-gradient(135deg, #173D2B 0%, #1f4d36 100%);
    border-radius: 24px;
    padding: 44px 48px;
    color: var(--pure-white);
    position: relative;
    overflow: hidden;
    margin-bottom: 24px;
    box-shadow: 0 12px 36px rgba(23, 61, 43, 0.16);
    display: flex;
    align-items: center;
    justify-content: space-between;
    animation: heroReveal 0.65s var(--ease-spring) both;
}

@keyframes heroReveal {
    0% {
        opacity: 0;
        transform: translateY(18px) scale(0.99);
    }
    100% {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

.hero-content {
    max-width: 580px;
    z-index: 2;
    animation: heroContentFade 0.75s var(--ease-spring) 0.1s both;
}

@keyframes heroContentFade {
    0% {
        opacity: 0;
        transform: translateX(-16px);
    }
    100% {
        opacity: 1;
        transform: translateX(0);
    }
}

.hero-pill {
    display: inline-block;
    color: var(--muted-gold);
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 12px;
}

.hero-title {
    font-family: var(--font-heading);
    font-size: 42px;
    font-weight: 700;
    line-height: 1.15;
    letter-spacing: -0.8px;
    margin-bottom: 16px;
    color: var(--pure-white);
}

.hero-subtitle {
    font-size: 15px;
    line-height: 1.6;
    color: #BDD1C3;
    margin-bottom: 26px;
    max-width: 500px;
}

.hero-cta-btn {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background-color: var(--primary-green);
    color: var(--pure-white) !important;
    text-decoration: none !important;
    padding: 13px 26px;
    border-radius: 30px;
    font-weight: 600;
    font-size: 14px;
    border: 1px solid rgba(255, 255, 255, 0.18);
    transition: all 0.3s var(--ease-spring);
    cursor: pointer;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.18);
}

.hero-cta-btn:hover {
    background-color: #346c4b;
    transform: translateY(-2px) scale(1.02);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.28);
    color: var(--pure-white) !important;
}

.hero-image-wrapper {
    position: absolute;
    right: 0;
    top: 0;
    bottom: 0;
    width: 48%;
    height: 100%;
    overflow: hidden;
    z-index: 1;
}

.hero-image-wrapper img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center right;
    mask-image: linear-gradient(to right, transparent 0%, rgba(0, 0, 0, 0.5) 20%, black 65%);
    -webkit-mask-image: linear-gradient(to right, transparent 0%, rgba(0, 0, 0, 0.5) 20%, black 65%);
    animation: heroPhotoGlide 1s var(--ease-spring) both;
}

@keyframes heroPhotoGlide {
    0% {
        opacity: 0;
        transform: scale(1.06) translateX(12px);
    }
    100% {
        opacity: 1;
        transform: scale(1) translateX(0);
    }
}

/* ==========================================================================
   FEATURE CARDS - STAGGERED CASCADE LANDING
   ========================================================================= */
.feature-card {
    background-color: var(--pure-white);
    border: 1px solid var(--card-border);
    border-radius: 16px;
    padding: 18px 22px;
    display: flex;
    align-items: center;
    gap: 16px;
    box-shadow: 0 2px 10px rgba(23, 61, 43, 0.04);
    transition: transform 0.3s var(--ease-spring), box-shadow 0.3s var(--ease-spring), border-color 0.25s ease;
}

.feature-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(23, 61, 43, 0.09);
    border-color: #CDE0C8;
}

/* Staggered Landing */
.feature-card-1 {
    animation: cardLanding 0.55s var(--ease-spring) 0.08s both;
}
.feature-card-2 {
    animation: cardLanding 0.55s var(--ease-spring) 0.16s both;
}
.feature-card-3 {
    animation: cardLanding 0.55s var(--ease-spring) 0.24s both;
}

@keyframes cardLanding {
    0% {
        opacity: 0;
        transform: translateY(18px);
    }
    100% {
        opacity: 1;
        transform: translateY(0);
    }
}

.feature-icon-circle {
    width: 44px;
    height: 44px;
    border-radius: 50%;
    background-color: #EAF2E7;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--primary-green);
    flex-shrink: 0;
    transition: transform 0.3s var(--ease-spring), background-color 0.3s ease;
}

.feature-card:hover .feature-icon-circle {
    transform: scale(1.08);
    background-color: #DDEBD9;
}

.feature-title {
    font-size: 15px;
    font-weight: 700;
    color: var(--forest-green);
    margin-bottom: 2px;
}

.feature-subtitle {
    font-size: 13px;
    color: var(--secondary-text);
}

/* ==========================================================================
   SECTION HEADERS
   ========================================================================== */
.section-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-top: 14px;
    margin-bottom: 18px;
    animation: sectionHeaderSlide 0.5s var(--ease-spring) both;
}

@keyframes sectionHeaderSlide {
    0% {
        opacity: 0;
        transform: translateY(10px);
    }
    100% {
        opacity: 1;
        transform: translateY(0);
    }
}

.section-icon-badge {
    width: 36px;
    height: 36px;
    border-radius: 10px;
    background-color: #E6EFE2;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--primary-green);
    flex-shrink: 0;
    transition: transform 0.25s var(--ease-spring);
}

.section-header:hover .section-icon-badge {
    transform: scale(1.06);
}

.section-title {
    font-size: 22px;
    font-weight: 800;
    color: var(--forest-green);
    margin: 0;
    letter-spacing: -0.4px;
}

.section-desc {
    font-size: 14px;
    color: var(--secondary-text);
    margin-top: 2px;
    margin-bottom: 0;
}

/* ==========================================================================
   CARDS & CONTAINERS - SMOOTH ENTRANCE
   ========================================================================== */
.card-container {
    background-color: var(--pure-white);
    border: 1px solid var(--card-border);
    border-radius: 20px;
    padding: 26px;
    box-shadow: 0 4px 18px rgba(23, 61, 43, 0.04);
    animation: cardLanding 0.5s var(--ease-spring) 0.1s both;
    transition: transform 0.3s var(--ease-spring), box-shadow 0.3s var(--ease-spring);
}

.card-container:hover {
    box-shadow: 0 8px 26px rgba(23, 61, 43, 0.07);
}

/* ==========================================================================
   ACTIVE WORKING DROPZONE (STFILEUPLOADER)
   ========================================================================== */
[data-testid="stFileUploader"] {
    width: 100%;
    margin-bottom: 12px;
    animation: cardLanding 0.5s var(--ease-spring) 0.05s both;
}

[data-testid="stFileUploader"] > label {
    display: none !important;
}

[data-testid="stFileUploaderDropzone"] {
    border: 2px dashed #B8D1B4 !important;
    border-radius: 20px !important;
    padding: 38px 24px !important;
    text-align: center !important;
    background-color: #FAFCF8 !important;
    transition: all 0.3s var(--ease-spring) !important;
    cursor: pointer !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    min-height: 200px !important;
    box-shadow: 0 2px 10px rgba(23, 61, 43, 0.02) !important;
}

[data-testid="stFileUploaderDropzone"]:hover {
    border-color: #5F9668 !important;
    background-color: #F2F8EE !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(40, 86, 59, 0.08) !important;
}

/* Hide default small Upload button inside dropzone */
[data-testid="stFileUploaderDropzone"] button {
    display: none !important;
}

/* Upload Icon via CSS */
[data-testid="stFileUploaderDropzone"]::before {
    content: "";
    display: block;
    width: 48px;
    height: 48px;
    margin: 0 auto 12px auto;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%2328563B' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4'/%3E%3Cpolyline points='17 8 12 3 7 8'/%3E%3Cline x1='12' y1='3' x2='12' y2='15'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: center;
    background-size: contain;
    transition: transform 0.3s var(--ease-spring);
}

[data-testid="stFileUploaderDropzone"]:hover::before {
    transform: translateY(-3px) scale(1.08);
}

[data-testid="stFileUploaderDropzoneInstructions"] {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    text-align: center !important;
}

[data-testid="stFileUploaderDropzoneInstructions"]::before {
    content: "Drag and drop your image here\\A or click to browse";
    white-space: pre-wrap;
    font-size: 17px;
    font-weight: 700;
    color: #173D2B;
    line-height: 1.4;
    margin-bottom: 6px;
    display: block;
    font-family: inherit;
}

[data-testid="stFileUploaderDropzoneInstructions"] span {
    font-size: 13px !important;
    color: #7A8C7F !important;
}

.selected-leaf-card {
    background: #FFFFFF;
    border: 1.5px solid #C0D6BC;
    border-radius: 18px;
    padding: 16px 20px;
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 14px;
    box-shadow: 0 4px 16px rgba(23, 61, 43, 0.04);
    animation: cardLanding 0.4s var(--ease-spring) both;
}

/* Tips list */
.tip-item {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    margin-bottom: 16px;
    font-size: 14px;
    color: var(--forest-green);
    transition: transform 0.2s var(--ease-spring);
}

.tip-item:hover {
    transform: translateX(3px);
}

.tip-check {
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background-color: #E6EFE2;
    color: var(--primary-green);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    font-size: 11px;
    font-weight: 800;
    margin-top: 1px;
    transition: transform 0.2s ease, background-color 0.2s ease;
}

.tip-item:hover .tip-check {
    transform: scale(1.15);
    background-color: #D6E8D1;
}

/* ==========================================================================
   BUTTONS & INPUTS - SMOOTH PHYSICS
   ========================================================================== */
.stButton > button {
    background-color: var(--primary-green) !important;
    color: var(--pure-white) !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 10px 24px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    transition: all 0.25s var(--ease-spring) !important;
    box-shadow: 0 2px 8px rgba(40, 86, 59, 0.2) !important;
}

.stButton > button:hover {
    background-color: var(--forest-green) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 18px rgba(23, 61, 43, 0.3) !important;
}

.stButton > button:active {
    transform: translateY(0px) !important;
}

/* Secondary Button */
.secondary-btn > div > button {
    background-color: var(--pure-white) !important;
    color: var(--forest-green) !important;
    border: 1px solid #D1DDD0 !important;
    box-shadow: none !important;
}

.secondary-btn > div > button:hover {
    background-color: #F4F8F2 !important;
    border-color: var(--sage-green) !important;
    color: var(--forest-green) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(23, 61, 43, 0.08) !important;
}

/* Sample Quick Picker Buttons */
.sample-pill > div > button {
    background-color: #EDF3EB !important;
    color: var(--forest-green) !important;
    border: 1px solid #D6E4D1 !important;
    border-radius: 20px !important;
    font-size: 12px !important;
    padding: 6px 14px !important;
    box-shadow: none !important;
    transition: all 0.2s var(--ease-spring) !important;
}

.sample-pill > div > button:hover {
    background-color: #DDEBD9 !important;
    border-color: var(--sage-green) !important;
    transform: translateY(-2px) scale(1.02) !important;
    box-shadow: 0 3px 10px rgba(40, 86, 59, 0.12) !important;
}

/* ==========================================================================
   RESULTS DASHBOARD STYLING
   ========================================================================== */
.result-status-card {
    background: #FFFFFF;
    border: 1px solid var(--card-border);
    border-radius: 20px;
    padding: 28px;
    box-shadow: 0 4px 20px rgba(23, 61, 43, 0.05);
    animation: resultCardLanding 0.6s var(--ease-spring) both;
}

@keyframes resultCardLanding {
    0% {
        opacity: 0;
        transform: translateY(20px) scale(0.985);
    }
    100% {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

.prediction-badge-row {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 8px;
}

.badge-tag {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    transition: transform 0.2s ease;
}

.badge-tag:hover {
    transform: scale(1.04);
}

.badge-crop {
    background-color: #E7F1E4;
    color: var(--forest-green);
}

.badge-category {
    background-color: #F8EFE3;
    color: #94601A;
}

.prediction-title {
    font-size: 26px;
    font-weight: 800;
    color: var(--forest-green);
    letter-spacing: -0.5px;
    margin-bottom: 14px;
}

.diagnostic-box {
    background-color: #F3F8F1;
    border-left: 4px solid var(--sage-green);
    border-radius: 10px;
    padding: 16px 18px;
    margin-bottom: 22px;
    font-size: 14px;
    line-height: 1.55;
    color: #274D37;
    animation: pageFadeIn 0.5s var(--ease-spring) 0.15s both;
}

.confidence-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
    font-size: 14px;
    font-weight: 700;
    color: var(--forest-green);
}

.confidence-score {
    font-size: 18px;
    font-weight: 800;
    color: var(--forest-green);
}

.custom-progress-bar {
    width: 100%;
    height: 10px;
    background-color: #E2ECE0;
    border-radius: 10px;
    overflow: hidden;
    margin-bottom: 24px;
}

.custom-progress-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--sage-green), var(--primary-green));
    border-radius: 10px;
    animation: smoothProgressFill 0.9s var(--ease-spring) 0.1s both;
}

@keyframes smoothProgressFill {
    from {
        width: 0% !important;
    }
}

/* Top 3 Predictions List */
.top-prediction-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 0;
    border-bottom: 1px solid #EEF3EB;
    font-size: 14px;
    transition: transform 0.2s ease, background-color 0.2s ease;
}

.top-prediction-item:hover {
    transform: translateX(3px);
}

.top-prediction-item:last-child {
    border-bottom: none;
}

.top-prediction-name {
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: 600;
    color: var(--forest-green);
}

.top-prediction-rank {
    color: #8C9B90;
    font-weight: 500;
    width: 18px;
}

.top-prediction-bar-container {
    width: 120px;
    height: 6px;
    background: #EAF0E8;
    border-radius: 6px;
    overflow: hidden;
    margin: 0 12px;
}

.top-prediction-bar-fill {
    height: 100%;
    background: var(--sage-green);
    border-radius: 6px;
    animation: smoothProgressFill 0.8s var(--ease-spring) both;
}

.top-prediction-score {
    font-weight: 700;
    color: var(--forest-green);
    min-width: 45px;
    text-align: right;
}

/* ==========================================================================
   LOADING STATE
   ========================================================================== */
.loading-box {
    background-color: var(--pure-white);
    border: 1px solid var(--card-border);
    border-radius: 20px;
    padding: 50px 30px;
    text-align: center;
    box-shadow: 0 4px 20px rgba(23, 61, 43, 0.05);
    animation: cardLanding 0.45s var(--ease-spring) both;
}

.spinner-circle {
    width: 54px;
    height: 54px;
    border: 4px solid #E1EBE0;
    border-top: 4px solid var(--primary-green);
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin: 0 auto 20px auto;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.loading-step {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    margin: 12px 0;
    font-size: 14px;
    color: var(--forest-green);
    animation: pageFadeIn 0.4s var(--ease-spring) both;
}

/* ==========================================================================
   DISEASE GUIDE STYLES
   ========================================================================== */
.guide-card {
    background-color: var(--pure-white);
    border: 1px solid var(--card-border);
    border-radius: 18px;
    padding: 20px;
    margin-bottom: 16px;
    box-shadow: 0 2px 10px rgba(23, 61, 43, 0.03);
    animation: cardLanding 0.45s var(--ease-spring) both;
    transition: transform 0.25s var(--ease-spring), box-shadow 0.25s var(--ease-spring), border-color 0.2s ease;
}

.guide-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(23, 61, 43, 0.08);
    border-color: #CDE0C8;
}

.guide-thumb-box {
    position: relative;
    width: 92px;
    height: 92px;
    border-radius: 14px;
    overflow: hidden;
    flex-shrink: 0;
    border: 1px solid #E2E8DC;
    box-shadow: 0 2px 8px rgba(23, 61, 43, 0.06);
    background-color: #F1F5EE;
}

.guide-thumb-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.35s var(--ease-spring);
    display: block;
}

.guide-card:hover .guide-thumb-img {
    transform: scale(1.08);
}

/* ==========================================================================
   FOOTER
   ========================================================================== */
.agroscan-footer {
    margin-top: 48px;
    padding-top: 24px;
    border-top: 1px solid #E2E8DC;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 12px;
    color: var(--secondary-text);
    animation: pageFadeIn 0.5s var(--ease-spring) 0.2s both;
}

.footer-brand {
    font-weight: 600;
    color: var(--forest-green);
}

.footer-disclaimer {
    max-width: 600px;
    text-align: right;
    line-height: 1.4;
    color: #7A8C7F;
}
</style>
"""

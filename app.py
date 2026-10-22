"""
AgroScan AI - Commercial SaaS Quality Plant Disease Detection Platform
Frontend built with Streamlit, custom responsive HTML/CSS design system,
and real PyTorch neural network inference.
"""

import os
import re
import base64
import time
import urllib.parse
from io import BytesIO
from PIL import Image
import streamlit as st

from disease_database import DISEASE_DB, get_disease_info, get_all_crops
from model_inference import predict_leaf
from styles import get_custom_css

# Page Configuration
st.set_page_config(
    page_title="AgroScan AI · Know your plant. Protect your harvest.",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Helper function to render pure HTML without markdown indentation glitches
def html(content: str):
    clean = re.sub(r'\n\s+', '\n', content.strip())
    st.markdown(clean, unsafe_allow_html=True)

# Inject Custom CSS Design System
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Helper function to convert local image to base64
@st.cache_data
def get_image_base64(image_path: str) -> str:
    try:
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except Exception:
        return ""

# Query parameter handling for top navigation
raw_qp = st.query_params.get("page", "Home")
qp = urllib.parse.unquote_plus(raw_qp)
valid_pages = ["Home", "Scanner", "Disease Guide", "About Model"]
if qp not in valid_pages:
    qp = "Home"

# Initialize Session State
if "current_page" not in st.session_state or st.session_state.current_page != qp:
    st.session_state.current_page = qp

if "scan_state" not in st.session_state:
    st.session_state.scan_state = "empty"  # empty | preview | analyzing | results

if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None

if "image_filename" not in st.session_state:
    st.session_state.image_filename = ""

if "image_size_str" not in st.session_state:
    st.session_state.image_size_str = ""

if "predictions" not in st.session_state:
    st.session_state.predictions = None

if "upload_error" not in st.session_state:
    st.session_state.upload_error = None

def reset_scan_state():
    st.session_state.scan_state = "empty"
    st.session_state.uploaded_image = None
    st.session_state.image_filename = ""
    st.session_state.image_size_str = ""
    st.session_state.predictions = None
    st.session_state.upload_error = None

# ==========================================================================
# NAVIGATION BAR
# ==========================================================================
def render_navbar():
    cur = st.session_state.current_page
    act_home = "active" if cur == "Home" else ""
    act_scanner = "active" if cur == "Scanner" else ""
    act_guide = "active" if cur == "Disease Guide" else ""
    act_about = "active" if cur == "About Model" else ""
    
    navbar_html = f"""
<div class="agroscan-navbar">
<a href="?page=Home" target="_self" class="nav-brand">
<svg viewBox="0 0 24 24">
<path d="M17,8C8,10 5.9,16.17 3.82,21.34L5.71,22L6.66,19.7C7.14,19.87 7.64,20 8,20C19,20 22,3 22,3C21,5 14,5.25 9,6.25C4,7.25 2,11.5 2,13.5C2,15.5 3.75,17.25 3.75,17.25C7,8 17,8 17,8Z"/>
</svg>
<span>AgroScan AI</span>
</a>
<div class="nav-links">
<a href="?page=Home" target="_self" class="nav-link-item {act_home}">Home</a>
<a href="?page=Scanner" target="_self" class="nav-link-item {act_scanner}">Scanner</a>
<a href="?page=Disease+Guide" target="_self" class="nav-link-item {act_guide}">Disease Guide</a>
<a href="?page=About+Model" target="_self" class="nav-link-item {act_about}">About Model</a>
</div>
<div class="nav-icon">
<svg viewBox="0 0 24 24">
<path d="M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,4A8,8 0 0,1 20,12C20,14.4 18.9,16.5 17.2,18C15.8,16.2 13.9,15 12,15C10.1,15 8.2,16.2 6.8,18C5.1,16.5 4,14.4 4,12A8,8 0 0,1 12,4Z"/>
</svg>
</div>
</div>
"""
    html(navbar_html)

render_navbar()

# ==========================================================================
# PAGE: HOME
# ==========================================================================
def render_home_page():
    hero_b64 = get_image_base64("assets/hero_plant.jpg")
    
    hero_html = f"""
<div class="hero-container">
<div class="hero-content">
<span class="hero-pill">INTELLIGENT PLANT HEALTH</span>
<h1 class="hero-title">Know your plant.<br>Protect your harvest.</h1>
<p class="hero-subtitle">Screen leaf images for potential plant diseases using machine learning and get clear, easy-to-understand results.</p>
<a href="?page=Scanner" target="_self" class="hero-cta-btn">Start Plant Scan &rarr;</a>
</div>
<div class="hero-image-wrapper">
<img src="data:image/jpeg;base64,{hero_b64}" alt="Botanical Plant Leaf">
</div>
</div>
"""
    html(hero_html)

    # 3 Feature highlights directly below hero
    c1, c2, c3 = st.columns(3)
    with c1:
        html("""
<div class="feature-card feature-card-1">
<div class="feature-icon-circle">
<svg style="width: 20px; height: 20px; fill: currentColor;" viewBox="0 0 24 24">
<path d="M17,8C8,10 5.9,16.17 3.82,21.34L5.71,22L6.66,19.7C7.14,19.87 7.64,20 8,20C19,20 22,3 22,3C21,5 14,5.25 9,6.25C4,7.25 2,11.5 2,13.5C2,15.5 3.75,17.25 3.75,17.25C7,8 17,8 17,8Z"/>
</svg>
</div>
<div>
<div class="feature-title">AI-Powered</div>
<div class="feature-subtitle">Image Classification</div>
</div>
</div>
""")
        
    with c2:
        html("""
<div class="feature-card feature-card-2">
<div class="feature-icon-circle">
<svg style="width: 20px; height: 20px; fill: currentColor;" viewBox="0 0 24 24">
<path d="M12,1L3,5V11C3,16.55 6.84,21.74 12,23C17.16,21.74 21,16.55 21,11V5L12,1M12,5A3,3 0 0,1 15,8A3,3 0 0,1 12,11A3,3 0 0,1 9,8A3,3 0 0,1 12,5M12,13C14.67,13 20,14.33 20,17V18H4V17C4,14.33 9.33,13 12,13Z"/>
</svg>
</div>
<div>
<div class="feature-title">Early Disease</div>
<div class="feature-subtitle">Detection</div>
</div>
</div>
""")
        
    with c3:
        html("""
<div class="feature-card feature-card-3">
<div class="feature-icon-circle">
<svg style="width: 20px; height: 20px; fill: currentColor;" viewBox="0 0 24 24">
<path d="M12,3C6.5,3 2,6.5 2,12C2,14 2.5,15.8 3.5,17.3C4.2,16.5 5.5,16 7,16C8,16 9,16.2 10,16.7C10.7,14 12.3,11.7 14.5,10.2C13.8,7.3 12.6,5.1 12,3M19,7C17.9,7 16.9,7.3 16,7.8C17.2,9.7 18,12 18,14.5C18,15.1 17.9,15.7 17.8,16.3C18.2,16.1 18.6,16 19,16C20.7,16 22,17.3 22,19C22,19.3 21.9,19.7 21.8,20C21.9,19.7 22,19.3 22,19C22,12 19,7 19,7Z"/>
</svg>
</div>
<div>
<div class="feature-title">Healthier Crops</div>
<div class="feature-subtitle">Better Yields</div>
</div>
</div>
""")

# ==========================================================================
# PAGE: SCANNER
# ==========================================================================
def render_scanner_page():
    html("""
<div class="section-header" style="margin-top: 10px;">
<div class="section-icon-badge">
<svg style="width: 20px; height: 20px; fill: currentColor;" viewBox="0 0 24 24">
<path d="M17,8C8,10 5.9,16.17 3.82,21.34L5.71,22L6.66,19.7C7.14,19.87 7.64,20 8,20C19,20 22,3 22,3C21,5 14,5.25 9,6.25C4,7.25 2,11.5 2,13.5C2,15.5 3.75,17.25 3.75,17.25C7,8 17,8 17,8Z"/>
</svg>
</div>
<div>
<h2 class="section-title">Plant Scanner</h2>
<p class="section-desc">Upload a clear image of a plant leaf to begin analysis.</p>
</div>
</div>
""")
    
    # ---------------------------------------------------------
    # STATE: SCANNER (Upload / Leaf Selected view)
    # ---------------------------------------------------------
    if st.session_state.scan_state in ["empty", "preview"]:
        col_upload, col_tips = st.columns([1.65, 1.1])
        
        with col_upload:
            if st.session_state.uploaded_image is not None:
                # Show selected leaf preview card
                try:
                    buffered = BytesIO()
                    st.session_state.uploaded_image.convert("RGB").save(buffered, format="JPEG", quality=88)
                    leaf_b64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
                except Exception:
                    leaf_b64 = ""
                
                selected_card_html = f"""
<div class="selected-leaf-card">
<img src="data:image/jpeg;base64,{leaf_b64}" style="width: 80px; height: 80px; border-radius: 14px; object-fit: cover; flex-shrink: 0; border: 1.5px solid #C0D6BC; box-shadow: 0 4px 12px rgba(23,61,43,0.06);">
<div style="flex-grow: 1; min-width: 0;">
<div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px; flex-wrap: wrap;">
<span style="font-size: 16px; font-weight: 700; color: #173D2B;">{st.session_state.image_filename}</span>
<span class="badge-tag" style="background: #EBF3E8; color: #28563B; font-size: 11px; font-weight: 700;">✓ Ready to analyse</span>
</div>
<div style="font-size: 13px; color: #7A8C7F;">Size: {st.session_state.image_size_str} • Leaf image loaded</div>
</div>
</div>
"""
                html(selected_card_html)
                
                b1, b2 = st.columns([1.7, 1])
                with b1:
                    if st.button("Analyse Leaf →", key="btn_analyse_active", type="primary", use_container_width=True):
                        st.session_state.scan_state = "analyzing"
                        st.rerun()
                with b2:
                    st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
                    if st.button("🔄 Change Image", key="btn_change_leaf", use_container_width=True):
                        reset_scan_state()
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                if st.session_state.upload_error:
                    st.error(f"⚠️ {st.session_state.upload_error}")
                    if st.button("Dismiss Error", key="btn_dismiss_err"):
                        st.session_state.upload_error = None
                        st.rerun()

                # Active interactive drag-and-drop uploader
                uploaded_file = st.file_uploader(
                    "Upload leaf file",
                    type=["jpg", "jpeg", "png"],
                    label_visibility="collapsed",
                    key="leaf_uploader"
                )
                
                if uploaded_file is not None:
                    try:
                        image = Image.open(uploaded_file)
                        image.verify()
                        uploaded_file.seek(0)
                        image = Image.open(uploaded_file)
                        image.load()
                        
                        if image.width < 10 or image.height < 10:
                            st.session_state.upload_error = "Uploaded image is too small (<10x10 px). Please upload a clear leaf photo."
                            st.session_state.uploaded_image = None
                            st.rerun()
                        
                        # Check for solid blank / zero-contrast images
                        import numpy as np
                        gray_arr = np.array(image.convert("L"))
                        if float(np.std(gray_arr)) < 5.0:
                            st.session_state.upload_error = "Uploaded image has near-zero visual contrast or is a blank image. Please upload a clear, focused photo of a plant leaf."
                            st.session_state.uploaded_image = None
                            st.rerun()

                        st.session_state.uploaded_image = image
                        st.session_state.image_filename = uploaded_file.name
                        file_size_kb = len(uploaded_file.getvalue()) / 1024
                        st.session_state.image_size_str = f"{file_size_kb:.0f} KB" if file_size_kb < 1024 else f"{file_size_kb/1024:.1f} MB"
                        st.session_state.upload_error = None
                        st.session_state.scan_state = "preview"
                        st.rerun()
                    except Exception:
                        st.session_state.upload_error = f"Unsupported or damaged file: Unable to decode '{uploaded_file.name}'. Please upload a standard JPG, JPEG, or PNG image."
                        st.session_state.uploaded_image = None
                        st.rerun()
                
                if st.button("Analyse Plant →", key="btn_analyse_prompt", type="primary", use_container_width=True):
                    st.info("🌱 Please drag and drop or click the box above to select a leaf image first.")
            
            # Quick Demonstration Samples
            st.markdown("<div style='margin-top: 18px;'></div>", unsafe_allow_html=True)
            st.markdown("<p style='font-size: 13px; font-weight: 700; color: #617264; margin-bottom: 8px;'>Or test with verified leaf samples:</p>", unsafe_allow_html=True)
            
            sc1, sc2, sc3 = st.columns(3)
            with sc1:
                st.markdown('<div class="sample-pill">', unsafe_allow_html=True)
                if st.button("🍂 Tomato Blight", key="sample_blight", use_container_width=True):
                    st.session_state.uploaded_image = Image.open("assets/tomato_early_blight.jpg")
                    st.session_state.image_filename = "tomato_early_blight.jpg"
                    st.session_state.image_size_str = "667 KB"
                    st.session_state.upload_error = None
                    st.session_state.scan_state = "preview"
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
                
            with sc2:
                st.markdown('<div class="sample-pill">', unsafe_allow_html=True)
                if st.button("🍃 Healthy Foliage", key="sample_healthy", use_container_width=True):
                    st.session_state.uploaded_image = Image.open("assets/healthy_leaf.jpg")
                    st.session_state.image_filename = "healthy_tomato_leaf.jpg"
                    st.session_state.image_size_str = "760 KB"
                    st.session_state.upload_error = None
                    st.session_state.scan_state = "preview"
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
                
            with sc3:
                st.markdown('<div class="sample-pill">', unsafe_allow_html=True)
                if st.button("🌽 Corn Rust", key="sample_rust", use_container_width=True):
                    st.session_state.uploaded_image = Image.open("assets/corn_common_rust.jpg")
                    st.session_state.image_filename = "corn_common_rust.jpg"
                    st.session_state.image_size_str = "890 KB"
                    st.session_state.upload_error = None
                    st.session_state.scan_state = "preview"
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
                
        with col_tips:
            html("""
<div class="card-container">
<div style="display: flex; align-items: center; gap: 8px; margin-bottom: 20px;">
<div class="section-icon-badge" style="width: 30px; height: 30px;">
<svg style="width: 16px; height: 16px; fill: currentColor;" viewBox="0 0 24 24">
<path d="M17,8C8,10 5.9,16.17 3.82,21.34L5.71,22L6.66,19.7C7.14,19.87 7.64,20 8,20C19,20 22,3 22,3C21,5 14,5.25 9,6.25C4,7.25 2,11.5 2,13.5C2,15.5 3.75,17.25 3.75,17.25C7,8 17,8 17,8Z"/>
</svg>
</div>
<span style="font-size: 16px; font-weight: 700; color: #173D2B;">Tips for better results</span>
</div>
<div class="tip-item">
<div class="tip-check">✓</div>
<div><strong>Use a clear, well-lit image</strong><br><span style="color: #617264; font-size: 13px;">Natural daylight provides optimum leaf venation visibility.</span></div>
</div>
<div class="tip-item">
<div class="tip-check">✓</div>
<div><strong>Focus on a single leaf</strong><br><span style="color: #617264; font-size: 13px;">Center the symptomatic or healthy leaf in the frame.</span></div>
</div>
<div class="tip-item">
<div class="tip-check">✓</div>
<div><strong>Avoid blurry or dark photos</strong><br><span style="color: #617264; font-size: 13px;">Ensure camera sharpness on lesions or leaf margins.</span></div>
</div>
<div class="tip-item">
<div class="tip-check">✓</div>
<div><strong>Supported formats: JPG, JPEG, PNG</strong><br><span style="color: #617264; font-size: 13px;">Standard high-resolution mobile camera photos supported.</span></div>
</div>
</div>
""")

    # ---------------------------------------------------------
    # STATE: ANALYZING (Loading state)
    # ---------------------------------------------------------
    elif st.session_state.scan_state == "analyzing":
        html("""
<div class="loading-box">
<div class="spinner-circle"></div>
<h3 style="font-size: 24px; font-weight: 700; color: #173D2B; margin-bottom: 18px;">Analyzing your leaf image...</h3>
<div class="loading-step"><span style="color: #28563B; font-weight: bold;">✓</span> Validating image and applying ImageNet normalization...</div>
<div class="loading-step"><span style="color: #28563B; font-weight: bold;">✓</span> Running EfficientNet-B0 neural forward pass...</div>
<div class="loading-step"><span style="color: #D5A75A; font-weight: bold;">●</span> Computing probability distribution & class rankings...</div>
</div>
""")
        
        # Execute real PyTorch inference with error safety
        try:
            results = predict_leaf(st.session_state.uploaded_image, top_k=3)
            st.session_state.predictions = results
            time.sleep(0.4)  # Smooth transition feel
            st.session_state.scan_state = "results"
            st.rerun()
        except Exception as e:
            st.session_state.upload_error = f"Analysis error: {str(e)}"
            st.session_state.scan_state = "empty"
            st.rerun()

    # ---------------------------------------------------------
    # STATE: RESULTS (Dashboard)
    # ---------------------------------------------------------
    elif st.session_state.scan_state == "results":
        res = st.session_state.predictions
        primary = res["primary"]
        
        # Back button
        st.markdown('<div class="secondary-btn" style="margin-bottom: 14px;">', unsafe_allow_html=True)
        if st.button("← Back to Scanner", key="btn_back"):
            reset_scan_state()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
            
        c_left, c_right = st.columns([1, 1.45])
        
        with c_left:
            st.markdown("""
<div style="background: #FFFFFF; border: 1px solid #E5EADF; border-radius: 20px; padding: 20px; box-shadow: 0 4px 18px rgba(23,61,43,0.04);">
""", unsafe_allow_html=True)
            st.image(st.session_state.uploaded_image, width="stretch")
            img_w, img_h = st.session_state.uploaded_image.size
            html(f"""
<div style="display: flex; align-items: center; justify-content: center; gap: 6px; margin-top: 12px; font-size: 13px; color: #617264; font-weight: 600;">
<svg style="width: 16px; height: 16px; fill: currentColor;" viewBox="0 0 24 24">
<path d="M4,4H7L9,2H15L17,4H20A2,2 0 0,1 22,6V18A2,2 0 0,1 20,20H4A2,2 0 0,1 2,18V6A2,2 0 0,1 4,4M12,7A5,5 0 0,0 7,12A5,5 0 0,0 12,17A5,5 0 0,0 17,12A5,5 0 0,0 12,7M12,9A3,3 0 0,1 15,12A3,3 0 0,1 12,15A3,3 0 0,1 9,12A3,3 0 0,1 12,9Z"/>
</svg>
Original Photo ({img_w}×{img_h} px)
</div>
</div>
""")
            
        with c_right:
            top3_html_parts = []
            for rank, item in enumerate(res["top_k"], 1):
                pct_width = min(max(item['percent'], 3), 100)
                top3_html_parts.append(f"""
<div class="top-prediction-item">
<div class="top-prediction-name">
<span class="top-prediction-rank">{rank}.</span>
<span>{item['class_label']}</span>
</div>
<div style="display: flex; align-items: center;">
<div class="top-prediction-bar-container">
<div class="top-prediction-bar-fill" style="width: {pct_width:.1f}%;"></div>
</div>
<span class="top-prediction-score">{item['percent_str']}</span>
</div>
</div>
""")
            top3_content = "".join(top3_html_parts)
            
            display_title = f"{primary['crop']} {primary['disease']}" if primary['disease'] != "Healthy Foliage" else f"Healthy {primary['crop']} Plant"
            
            # Low confidence alert if below 60%
            low_conf_banner = ""
            if res.get("is_low_confidence", False):
                low_conf_banner = """
<div style="background-color: #FFF9ED; border: 1.5px solid #F4E2C2; border-radius: 14px; padding: 12px 16px; margin-bottom: 14px; display: flex; align-items: flex-start; gap: 10px;">
<svg style="width: 20px; height: 20px; fill: #D5A75A; flex-shrink: 0; margin-top: 2px;" viewBox="0 0 24 24"><path d="M12,2L1,21H23M12,6L19.53,19H4.47M11,10V14H13V10M11,16V18H13V16"/></svg>
<div>
<strong style="color: #8F651C; font-size: 13.5px;">Preliminary Screening · Low Confidence (&lt;60%)</strong>
<p style="color: #785A21; font-size: 12px; margin: 3px 0 0 0; line-height: 1.45;">
The model's top predicted score is below 60%. Please verify that the image is sharply focused on a single leaf with good lighting, and is one of the 14 supported crops. Out-of-distribution or non-leaf photos cannot be reliably identified.
</p>
</div>
</div>
"""

            # Cross-crop biological homology advisory
            cross_crop_banner = ""
            if res.get("cross_crop_advisory"):
                cross_crop_banner = f"""
<div style="background-color: #F0F6F2; border: 1.5px solid #C8DDD0; border-radius: 14px; padding: 12px 16px; margin-bottom: 14px; display: flex; align-items: flex-start; gap: 10px;">
<svg style="width: 20px; height: 20px; fill: #28563B; flex-shrink: 0; margin-top: 2px;" viewBox="0 0 24 24"><path d="M17,8C8,10 5.9,16.17 3.82,21.34L5.71,22L6.66,19.7C7.14,19.87 7.64,20 8,20C19,20 22,3 22,3C21,5 14,5.25 9,6.25C4,7.25 2,11.5 2,13.5C2,15.5 3.75,17.25 3.75,17.25C7,8 17,8 17,8Z"/></svg>
<div>
<strong style="color: #1E4B35; font-size: 13.5px;">🌿 Agronomic Advisory · Cross-Crop Biological Homology</strong>
<p style="color: #2D5A42; font-size: 12px; margin: 3px 0 0 0; line-height: 1.45;">
{res['cross_crop_advisory']}
</p>
</div>
</div>
"""

            # Input framing & color advisories
            input_advisory_parts = []
            if res.get("aspect_advisory"):
                input_advisory_parts.append(f"""
<div style="background-color: #F8F9FA; border: 1px solid #E5EADF; border-radius: 10px; padding: 8px 12px; margin-bottom: 10px; font-size: 11.5px; color: #526356; display: flex; align-items: center; gap: 8px;">
<span style="font-size: 14px;">📐</span>
<span><strong>Input Framing Notice:</strong> {res['aspect_advisory']}</span>
</div>
""")
            if res.get("grayscale_advisory"):
                input_advisory_parts.append(f"""
<div style="background-color: #F8F9FA; border: 1px solid #E5EADF; border-radius: 10px; padding: 8px 12px; margin-bottom: 10px; font-size: 11.5px; color: #526356; display: flex; align-items: center; gap: 8px;">
<span style="font-size: 14px;">🎨</span>
<span><strong>Monochrome Input:</strong> {res['grayscale_advisory']}</span>
</div>
""")
            input_advisory_banner = "".join(input_advisory_parts)

            result_card_html = f"""
<div class="result-status-card">
{low_conf_banner}
{cross_crop_banner}
{input_advisory_banner}
<div class="prediction-badge-row">
<span class="badge-tag badge-crop">🌱 Crop: {primary['crop']}</span>
<span class="badge-tag badge-category">🔬 {primary['category']}</span>
</div>
<div style="font-size: 13px; font-weight: 700; color: #7A8C7F; text-transform: uppercase; letter-spacing: 1px; margin-top: 4px;">Predicted Class</div>
<div class="prediction-title">{display_title}</div>
<div class="diagnostic-box">
<strong>Pathogen:</strong> <em>{primary.get('pathogen', 'N/A')}</em><br>
{primary['description']}
</div>
<div class="confidence-header">
<span>Model Output Confidence</span>
<span class="confidence-score">{primary['percent_str']}</span>
</div>
<div class="custom-progress-bar">
<div class="custom-progress-fill" style="width: {min(max(primary['percent'], 5), 100):.1f}%;"></div>
</div>
<div style="font-size: 11.5px; color: #7A8C7F; margin-top: -6px; margin-bottom: 14px; line-height: 1.4;">
Softmax scores reflect relative neural network activation across the 38 trained classes for preliminary screening, not an absolute botanical guarantee.
</div>
<div style="font-size: 14px; font-weight: 700; color: #173D2B; margin-bottom: 10px;">Top 3 Predictions</div>
{top3_content}
<div style="display: flex; justify-content: space-between; align-items: center; font-size: 11px; color: #7A8C7F; margin-top: 14px; border-top: 1px solid #EEF3EB; padding-top: 10px; flex-wrap: wrap; gap: 8px;">
<span>Architecture: <strong>{res.get('model_architecture', 'EfficientNet-B0')}</strong></span>
<span>Checkpoint: <strong>{res.get('checkpoint_version', 'model_v1.pt')}</strong></span>
<span>Device: <strong>{res.get('device_used', 'cpu').upper()}</strong></span>
</div>
</div>
"""
            html(result_card_html)
            
            st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
            with st.expander(f"🌾 Agricultural Management & Symptoms for {display_title}", expanded=True):
                st.markdown(f"**Pathogen / Agent:** *{primary.get('pathogen', 'N/A')}*")
                st.markdown(f"**Key Symptoms:** {primary.get('symptoms', 'N/A')}")
                st.markdown(f"**Recommended Management:** {primary.get('management', 'N/A')}")
            
            st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
            b_col1, b_col2 = st.columns([1.5, 1])
            with b_col1:
                if st.button("Analyze Another Image", key="btn_another", use_container_width=True):
                    reset_scan_state()
                    st.rerun()
                    
            with b_col2:
                st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
                if st.button("Clear", key="btn_clear", use_container_width=True):
                    reset_scan_state()
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

# ==========================================================================
# PAGE: DISEASE GUIDE
# ==========================================================================
def render_guide_page():
    html("""
<div class="section-header">
<div class="section-icon-badge">
<svg style="width: 20px; height: 20px; fill: currentColor;" viewBox="0 0 24 24">
<path d="M19,2L14,6.5V17.5L19,13V2M6.5,5C4.55,5 2.45,5.4 1,6.5V21.16C1,21.41 1.25,21.66 1.5,21.66C1.6,21.66 1.65,21.62 1.75,21.57C3.1,20.94 5.05,20.5 6.5,20.5C8.45,20.5 10.55,20.9 12,22C13.35,21.15 15.8,20.5 17.5,20.5C19.15,20.5 20.85,20.81 22.25,21.56C22.35,21.61 22.4,21.66 22.5,21.66C22.75,21.66 23,21.41 23,21.16V6.5C21.4,5.45 19.55,5 17.5,5C15.8,5 13.35,5.65 12,6.5C10.55,5.4 8.45,5 6.5,5Z"/>
</svg>
</div>
<div>
<h2 class="section-title">Disease Guide</h2>
<p class="section-desc">Learn about common plant diseases, pathogens, and symptoms verified in our model dataset.</p>
</div>
</div>
""")
    
    # Search input
    search_query = st.text_input(
        "Search diseases",
        placeholder="🔍 Search for a crop or disease (e.g., Tomato, Blight, Rust, Apple)...",
        label_visibility="collapsed",
        key="guide_search_input"
    )
    
    # Crop Filter Chips
    all_crops = ["All Crops"] + get_all_crops()
    selected_crop = st.pills("Filter by crop:", all_crops, default="All Crops", key="crop_pills") if hasattr(st, "pills") else st.selectbox("Filter by crop:", all_crops, key="crop_select")
    if not selected_crop:
        selected_crop = "All Crops"
        
    st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
    
    # Filter matching items
    filtered_items = []
    for label, data in DISEASE_DB.items():
        if selected_crop != "All Crops" and data["crop"].lower() != selected_crop.lower():
            continue
            
        if search_query:
            q = search_query.lower()
            match = (
                q in label.lower() or
                q in data["crop"].lower() or
                q in data["disease"].lower() or
                q in data["category"].lower() or
                q in data["description"].lower()
            )
            if not match:
                continue
                
        filtered_items.append((label, data))
        
    st.markdown(f"<p style='font-size: 13px; color: #7A8C7F; margin-bottom: 16px;'>Showing <strong>{len(filtered_items)}</strong> verified disease categories</p>", unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    for idx, (label, item) in enumerate(filtered_items):
        target_col = col_a if idx % 2 == 0 else col_b
        
        with target_col:
            thumb_path = item.get("image", "assets/healthy_leaf.jpg")
            thumb_b64 = get_image_base64(thumb_path)
            severity = item.get("severity", "Standard")
            
            with st.container():
                card_html = f"""
<div class="guide-card">
<div style="display: flex; gap: 16px; align-items: flex-start;">
<img src="data:image/jpeg;base64,{thumb_b64}" style="width: 105px; height: 105px; min-width: 105px; max-width: 105px; min-height: 105px; max-height: 105px; object-fit: cover; border-radius: 14px; flex-shrink: 0; display: block; border: 1px solid #E2E8DC; box-shadow: 0 3px 10px rgba(23, 61, 43, 0.06);" alt="{item['disease']}">
<div style="flex-grow: 1; min-width: 0;">
<div style="display: flex; align-items: center; gap: 6px; margin-bottom: 6px; flex-wrap: wrap;">
<span class="badge-tag badge-crop">{item['crop']}</span>
<span class="badge-tag badge-category">{item['category']}</span>
<span class="badge-tag" style="background: #F1F5EE; color: #3E5A47; font-size: 11px;">{severity}</span>
</div>
<div style="font-size: 16px; font-weight: 700; color: #173D2B; margin-bottom: 6px;">{item['disease']}</div>
<div style="font-size: 13px; color: #617264; line-height: 1.5; margin-bottom: 8px;">{item['description']}</div>
</div>
</div>
</div>
"""
                html(card_html)
                with st.expander(f"View symptoms & agricultural treatment for {item['disease']}"):
                    exp_col1, exp_col2 = st.columns([1, 2])
                    with exp_col1:
                        st.image(thumb_path, caption=f"{item['crop']} · {item['disease']}", width="stretch")
                    with exp_col2:
                        st.markdown(f"**Pathogen / Agent:** *{item.get('pathogen', 'N/A')}*")
                        st.markdown(f"**Severity Level:** `{severity}`")
                        st.markdown(f"**Diagnostic Symptoms:** {item.get('symptoms', 'N/A')}")
                        st.markdown(f"**Recommended Management:** {item.get('management', 'N/A')}")

# ==========================================================================
# PAGE: ABOUT THE MODEL
# ==========================================================================
def render_about_page():
    html("""
<div class="section-header">
<div class="section-icon-badge">
<svg style="width: 20px; height: 20px; fill: currentColor;" viewBox="0 0 24 24">
<path d="M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,4A8,8 0 0,1 20,12C20,14.4 18.9,16.5 17.2,18C15.8,16.2 13.9,15 12,15C10.1,15 8.2,16.2 6.8,18C5.1,16.5 4,14.4 4,12A8,8 0 0,1 12,4Z"/>
</svg>
</div>
<div>
<h2 class="section-title">About the Model</h2>
<p class="section-desc">Learn more about the technology behind AgroScan AI.</p>
</div>
</div>
""")
    
    col_left, col_right = st.columns([1.1, 1])
    
    with col_left:
        html("""
<div class="card-container" style="margin-bottom: 20px;">
<div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
<svg style="width: 22px; height: 22px; fill: #28563B;" viewBox="0 0 24 24">
<path d="M12,16A3,3 0 0,1 9,13C9,11.88 9.61,10.9 10.5,10.39L20.21,4.77L14.68,14.35C14.18,15.33 13.17,16 12,16M12,3C13.81,3 15.5,3.5 16.97,4.32L14.87,7.94C14,7.34 13,7 12,7A6,6 0 0,0 6,13C6,15.21 7.2,17.14 8.96,18.17L6.87,21.8C4.5,20.41 3,17.9 3,15A9,9 0 0,1 12,6M18,13A6,6 0 0,0 12,7L14.1,3.38C17.06,4.77 19.34,7.4 20.25,10.57L16.63,12.67C16.86,13.71 16.71,14.81 16.2,15.7L19.82,17.8C20.57,16.35 21,14.72 21,13M12,21A6,6 0 0,0 17.5,16.5L21.12,18.6C19.73,21.56 16.71,23.63 13.15,23.95L11.05,20.33C11.36,20.35 11.68,20.36 12,20.36Z"/>
</svg>
<span style="font-size: 16px; font-weight: 700; color: #173D2B;">Model Architecture</span>
</div>
<div style="font-size: 18px; font-weight: 700; color: #28563B; margin-bottom: 6px;">EfficientNet-B0 Backbone (Transfer Learning)</div>
<p style="font-size: 14px; color: #617264; line-height: 1.6; margin: 0;">
A 4.06M parameter deep convolutional network pre-trained on ImageNet and fine-tuned on PlantVillage using a two-phase transfer learning schedule. Reaches 98.21% test accuracy and 0.9765 macro F1 score while delivering rapid, energy-efficient CPU edge inference.
</p>
</div>

<div class="card-container" style="margin-bottom: 20px;">
<div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
<svg style="width: 22px; height: 22px; fill: #28563B;" viewBox="0 0 24 24">
<path d="M12 3C7.58 3 4 4.79 4 7s3.58 4 8 4 8-1.79 8-4-3.58-4-8-4M4 9v4c0 2.21 3.58 4 8 4s8-1.79 8-4V9c0 2.21-3.58 4-8 4s-8-1.79-8-4m0 6v4c0 2.21 3.58 4 8 4s8-1.79 8-4v-4c0 2.21-3.58 4-8 4s-8-1.79-8-4Z"/>
</svg>
<span style="font-size: 16px; font-weight: 700; color: #173D2B;">Dataset</span>
</div>
<p style="font-size: 14px; color: #617264; line-height: 1.6; margin: 0;">
Trained and evaluated on the standardized public <strong>PlantVillage</strong> benchmark dataset containing over 54,000 verified images of healthy and diseased leaves across multiple agricultural crops and laboratory conditions.
</p>
</div>

<div class="card-container">
<div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
<svg style="width: 22px; height: 22px; fill: #28563B;" viewBox="0 0 24 24">
<path d="M19,3H5C3.89,3 3,3.89 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V5C21,3.89 20.1,3 19,3M19,5V19H5V5H19M7,7V9H9V7H7M11,7V9H13V7H11M15,7V9H17V7H15M7,11V13H9V11H7M11,11V13H13V11H11M15,11V13H17V11H15M7,15V17H9V15H7M11,15V17H13V15H11M15,15V17H17V15H15Z"/>
</svg>
<span style="font-size: 16px; font-weight: 700; color: #173D2B;">Supported Classes</span>
</div>
<div style="font-size: 24px; font-weight: 800; color: #173D2B; margin-bottom: 6px;">38 Disease & Healthy Classes</div>
<p style="font-size: 14px; color: #617264; line-height: 1.6; margin: 0;">
Covers 14 economic crops including Tomato, Potato, Corn, Bell Pepper, Apple, Grape, Peach, Cherry, Strawberry, Blueberry, Raspberry, Soybean, Squash, and Orange.
</p>
</div>
""")
        
    with col_right:
        html("""
<div class="card-container" style="margin-bottom: 20px;">
<div style="font-size: 16px; font-weight: 700; color: #173D2B; margin-bottom: 18px;">How It Works</div>
<div style="display: flex; gap: 14px; margin-bottom: 16px;">
<div style="width: 28px; height: 28px; border-radius: 50%; background: #E6EFE2; color: #28563B; font-weight: 800; display: flex; align-items: center; justify-content: center; font-size: 13px; flex-shrink: 0;">1</div>
<div>
<strong style="color: #173D2B; font-size: 14px;">Preprocess Image</strong>
<p style="color: #617264; font-size: 13px; margin: 2px 0 0 0; line-height: 1.5;">Resize and normalize the leaf image to 224×224 pixels with ImageNet standard color distribution.</p>
</div>
</div>

<div style="display: flex; gap: 14px; margin-bottom: 16px;">
<div style="width: 28px; height: 28px; border-radius: 50%; background: #E6EFE2; color: #28563B; font-weight: 800; display: flex; align-items: center; justify-content: center; font-size: 13px; flex-shrink: 0;">2</div>
<div>
<strong style="color: #173D2B; font-size: 14px;">Extract Features</strong>
<p style="color: #617264; font-size: 13px; margin: 2px 0 0 0; line-height: 1.5;">The neural network extracts spatial features, identifying lesion patterns, discoloration margins, and venation structure.</p>
</div>
</div>

<div style="display: flex; gap: 14px;">
<div style="width: 28px; height: 28px; border-radius: 50%; background: #E6EFE2; color: #28563B; font-weight: 800; display: flex; align-items: center; justify-content: center; font-size: 13px; flex-shrink: 0;">3</div>
<div>
<strong style="color: #173D2B; font-size: 14px;">Classify</strong>
<p style="color: #617264; font-size: 13px; margin: 2px 0 0 0; line-height: 1.5;">Softmax activation computes probability distribution across 38 classes, ranking the most likely diagnosis with confidence scores.</p>
</div>
</div>
</div>

<div style="background-color: #FFF9ED; border: 1px solid #F4E2C2; border-radius: 20px; padding: 24px;">
<div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
<svg style="width: 22px; height: 22px; fill: #D5A75A;" viewBox="0 0 24 24">
<path d="M12,2L1,21H23M12,6L19.53,19H4.47M11,10V14H13V10M11,16V18H13V16"/>
</svg>
<span style="font-size: 16px; font-weight: 700; color: #8F651C;">Limitations & Safety</span>
</div>
<ul style="margin: 0; padding-left: 20px; font-size: 13px; color: #785A21; line-height: 1.7;">
<li>Preliminary screening tool: not an absolute or definitive botanical diagnosis.</li>
<li>Biologically related pathogens across crops (e.g. Phytophthora late blight on Tomato/Potato, or Xanthomonas bacterial spot across Peach/Pepper) produce near-identical foliar lesions and may require field host verification.</li>
<li>Accuracy may degrade if the leaf image is blurry, poorly lit, or contains multiple overlapping foliage.</li>
<li>Works best with a centered single-leaf shot against a plain or natural background.</li>
<li>Machine learning outputs must not substitute professional agronomist or plant pathologist consultation.</li>
</ul>
</div>
""")

# ==========================================================================
# PAGE ROUTER
# ==========================================================================
if st.session_state.current_page == "Home":
    render_home_page()
elif st.session_state.current_page == "Scanner":
    render_scanner_page()
elif st.session_state.current_page == "Disease Guide":
    render_guide_page()
elif st.session_state.current_page == "About Model":
    render_about_page()

# ==========================================================================
# FOOTER
# ==========================================================================
html("""
<div class="agroscan-footer">
<div class="footer-brand">AgroScan AI · Intelligent Plant Health Screening</div>
<div class="footer-disclaimer">
AI predictions are intended for preliminary screening and educational purposes. Results may be inaccurate and should not replace expert agricultural advice.
</div>
</div>
""")

"""
AgroScan AI - Real Model Inference Engine
Powered by the verified PlantLeaf Disease Classifier:
- Architecture: EfficientNet-B0 transfer learning (ImageNet backbone + 38-way classifier head)
- Checkpoint: model_v1.pt (fine-tuned on PlantVillage benchmark, 98.21% test accuracy)
- Class Mapping: 38 classes across 14 economic crops
- Preprocessing: Resize to 256x256, CenterCrop to 224x224, ImageNet normalization
- Robust input suitability verification & cross-crop pathogen advisory generation.
"""

import os
import json
from typing import Dict, Any, List, Tuple, Optional
import numpy as np
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image, ImageOps
import streamlit as st

from disease_database import get_disease_info, RAW_TO_FRIENDLY_MAP

# Base directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_WEIGHTS_PATH = os.path.join(BASE_DIR, "models", "model_v1.pt")
CLASS_MAP_PATH = os.path.join(BASE_DIR, "models", "class_to_idx.json")

# ImageNet standard normalization constants
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]

# Standard canonical inference transform (Resize 256 -> CenterCrop 224)
STANDARD_TRANSFORM = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
])

# Direct resize transform (Resize 224 without cropping leaf margins)
DIRECT_TRANSFORM = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
])

# Canonical default
INFERENCE_TRANSFORM = STANDARD_TRANSFORM

def get_device() -> torch.device:
    """Returns available computation device (cuda if available, else cpu)."""
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")

def build_efficientnet_b0(num_classes: int = 38) -> nn.Module:
    """
    Builds the exact EfficientNet-B0 architecture with a 38-class linear head.
    Matches src/model.py of pavanmanjunath18/Plant_Disease_Classifier.
    """
    model = models.efficientnet_b0(weights=None)
    in_features = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(in_features, num_classes)
    return model

@st.cache_resource(show_spinner=False)
def load_class_mapping() -> Dict[int, str]:
    """Loads and caches the index-to-class mapping from class_to_idx.json."""
    if not os.path.exists(CLASS_MAP_PATH):
        raise FileNotFoundError(f"Class mapping file not found at: {CLASS_MAP_PATH}")
    with open(CLASS_MAP_PATH, "r", encoding="utf-8") as f:
        class_to_idx = json.load(f)
    return {int(v): k for k, v in class_to_idx.items()}

@st.cache_resource(show_spinner=False)
def load_classifier_model():
    """
    Loads and caches the fine-tuned EfficientNet-B0 PyTorch model in memory.
    The model is loaded once and reused across subsequent user predictions.
    """
    if not os.path.exists(MODEL_WEIGHTS_PATH):
        raise FileNotFoundError(
            f"Trained model checkpoint not found at: {MODEL_WEIGHTS_PATH}. "
            "Please ensure model_v1.pt is located in the models/ directory."
        )

    device = get_device()
    model = build_efficientnet_b0(num_classes=38)
    
    # Load weights from genuine checkpoint
    checkpoint = torch.load(MODEL_WEIGHTS_PATH, map_location=device)
    if isinstance(checkpoint, dict) and "model_state_dict" in checkpoint:
        model.load_state_dict(checkpoint["model_state_dict"])
    elif isinstance(checkpoint, dict):
        model.load_state_dict(checkpoint)
    else:
        raise ValueError("Unrecognized checkpoint format in model_v1.pt")

    model.to(device)
    model.eval()
    return model, device

def validate_and_preprocess_image(
    image: Any,
    transform: Optional[transforms.Compose] = None
) -> Tuple[torch.Tensor, Dict[str, str]]:
    """
    Validates uploaded image suitability and applies exact preprocessing.
    Checks for:
    - Empty / None input
    - Corrupt or unreadable image bytes
    - Minimum pixel dimensions (< 10 px)
    - Solid blank / zero-contrast images (std dev < 5.0)
    - Aspect ratio distortion (warning if ratio > 4.0)
    - Monochrome / grayscale input (warning regarding chlorosis color loss)
    
    Returns:
        tuple of (preprocessed_tensor, advisory_dictionary)
    """
    advisories = {}

    if image is None:
        raise ValueError("No image provided. Please upload a leaf photo.")

    if not isinstance(image, Image.Image):
        try:
            image = Image.open(image)
        except Exception as e:
            raise ValueError(f"Unable to decode uploaded file as an image: {e}")

    # Check minimum dimensions
    if image.width < 10 or image.height < 10:
        raise ValueError("Uploaded image is too small to contain a readable leaf structure.")

    # Check for solid blank / zero-contrast images
    try:
        gray_arr = np.array(image.convert("L"))
        contrast_std = float(np.std(gray_arr))
        if contrast_std < 5.0:
            raise ValueError(
                "Uploaded image has near-zero visual contrast or is a solid blank image. "
                "Please upload a clear, focused photo of a plant leaf."
            )
    except ValueError:
        raise
    except Exception:
        pass

    # Aspect ratio check
    aspect = max(image.width / image.height, image.height / image.width)
    if aspect > 4.0:
        advisories["aspect_warning"] = (
            f"Unusual aspect ratio ({image.width}×{image.height}). "
            "For optimal accuracy, upload a photo where the leaf is centered with balanced framing."
        )

    # Grayscale / monochrome check
    if image.mode in ("L", "1"):
        advisories["grayscale_warning"] = (
            "Monochrome or grayscale image detected. Disease chlorosis and lesion coloration "
            "cannot be fully evaluated without color channels."
        )

    # Correct EXIF orientation if present
    try:
        image = ImageOps.exif_transpose(image)
    except Exception:
        pass

    # Ensure 3-channel RGB format (stripping alpha channel if PNG, converting grayscale if L)
    if image.mode != "RGB":
        image = image.convert("RGB")

    active_transform = transform if transform is not None else INFERENCE_TRANSFORM
    tensor = active_transform(image).unsqueeze(0)
    return tensor, advisories

def generate_cross_crop_advisory(primary: Dict[str, Any], top_k: List[Dict[str, Any]]) -> str:
    """
    Generates agronomic context when predictions involve biologically related
    pathogens or close candidate scores across crops.
    Never fabricates predictions; solely provides genuine biological context.
    """
    top_diseases = [item.get("disease", "").lower() for item in top_k]
    top_crops = [item.get("crop", "").lower() for item in top_k]
    
    # 1. Late Blight across Tomato and Potato (Phytophthora infestans)
    if any("late blight" in d for d in top_diseases):
        if any(c in ("tomato", "potato") for c in top_crops):
            return (
                "Late blight on Tomato and Potato is caused by the exact same oomycete pathogen "
                "(Phytophthora infestans), producing virtually identical dark, water-soaked foliar lesions. "
                "Confirm host crop identity to distinguish between Tomato Late Blight and Potato Late Blight."
            )
            
    # 2. Bacterial Spot across Pepper, Peach, and Tomato (Xanthomonas)
    if any("bacterial spot" in d for d in top_diseases):
        return (
            "Bacterial spot is caused by Xanthomonas species across pepper, peach, and tomato foliage, "
            "producing small, angular water-soaked lesions with chlorotic yellow halos. "
            "Verify host plant leaf morphology (e.g. lanceolate peach leaf vs ovate pepper leaf)."
        )

    # 3. Foliar Corn Pathogens (Common Rust vs Gray Leaf Spot / Blight)
    if "corn" in primary.get("crop", "").lower():
        rust_in_top = any("rust" in d for d in top_diseases)
        spot_in_top = any("gray leaf spot" in d or "blight" in d for d in top_diseases)
        if rust_in_top and spot_in_top:
            return (
                "Foliar corn diseases can share streak-like discoloration along parallel leaf veins. "
                "Observe whether lesions are raised cinnamon-brown pustules (Common Rust) or "
                "narrow rectangular tan lesions bounded by veins (Gray Leaf Spot)."
            )

    # 4. Black Rot across Apple and Grape
    if any("black rot" in d for d in top_diseases):
        return (
            "Black rot fungal infections produce circular necrotic spots with dark borders. "
            "Ensure specimen foliage matches the predicted host species (fruit tree vs grapevine)."
        )

    # 5. Powdery Mildew across crops
    if any("powdery mildew" in d for d in top_diseases):
        return (
            "Powdery mildew pathogens (Podosphaera, Erysiphe) produce superficial white talcum-like "
            "mycelial patches across diverse crops. Confirm host crop species."
        )

    # 6. Close probability spread advisory (< 15% difference between top 2)
    if len(top_k) >= 2:
        diff = top_k[0]["score"] - top_k[1]["score"]
        if diff < 0.15:
            return (
                f"Close candidate scores: Top predictions '{top_k[0]['class_label']}' ({top_k[0]['percent_str']}) "
                f"and '{top_k[1]['class_label']}' ({top_k[1]['percent_str']}) exhibit similar visual symptom patterns. "
                "Inspect secondary symptoms and host crop characteristics."
            )

    return ""

def predict_leaf(
    image: Image.Image,
    top_k: int = 3,
    transform: Optional[transforms.Compose] = None
) -> Dict[str, Any]:
    """
    Performs real PyTorch forward-pass neural network classification on a leaf image.
    
    Args:
        image: PIL Image of the plant leaf
        top_k: Number of highest-probability candidate classes to return (default 3)
        transform: Optional torchvision Compose transform (defaults to canonical INFERENCE_TRANSFORM)
        
    Returns:
        Dictionary containing:
        - 'primary': Top-1 prediction details (class_label, crop, disease, pathogen, description, etc.)
        - 'top_k': Ranked list of top-K prediction records
        - 'is_low_confidence': Boolean flag if top-1 score is below 60%
        - 'cross_crop_advisory': Biological homology explanation if related diseases detected
        - 'aspect_advisory': Warning if unusual aspect ratio detected
        - 'grayscale_advisory': Warning if monochrome image uploaded
        - 'device_used': Execution device ('cpu' or 'cuda')
        - 'model_architecture': 'EfficientNet-B0 (Transfer Learning)'
        - 'checkpoint_version': 'model_v1.pt (Macro F1: 0.9709)'
    """
    model, device = load_classifier_model()
    idx_to_class = load_class_mapping()

    # Preprocess safely and check image suitability
    tensor, advisories = validate_and_preprocess_image(image, transform=transform)
    tensor = tensor.to(device)

    # Genuine forward-pass inference
    with torch.no_grad():
        logits = model(tensor)
        probabilities = torch.softmax(logits, dim=-1)[0]
        top_probs, top_indices = torch.topk(probabilities, k=min(top_k, len(idx_to_class)))

    top_results: List[Dict[str, Any]] = []
    for rank_idx, (prob, idx_tensor) in enumerate(zip(top_probs, top_indices)):
        prob_val = float(prob.item())
        class_idx = int(idx_tensor.item())
        raw_class_name = idx_to_class.get(class_idx, f"Class_{class_idx}")
        
        # Retrieve authenticated agricultural metadata from database
        meta = get_disease_info(raw_class_name)
        friendly_label = meta.get("friendly_name", RAW_TO_FRIENDLY_MAP.get(raw_class_name, raw_class_name))

        top_results.append({
            "rank": rank_idx + 1,
            "raw_class": raw_class_name,
            "class_label": friendly_label,
            "crop": meta.get("crop", "Unknown"),
            "disease": meta.get("disease", "Unknown"),
            "category": meta.get("category", "Detected Condition"),
            "pathogen": meta.get("pathogen", "Identified Agricultural Pathogen"),
            "severity": meta.get("severity", "Standard"),
            "description": meta.get("description", "Preliminary screening result."),
            "symptoms": meta.get("symptoms", "Visual leaf patterns matched this class."),
            "management": meta.get("management", "Consult local agricultural extension specialists."),
            "image": meta.get("image", "assets/healthy_leaf.jpg"),
            "score": prob_val,
            "percent": prob_val * 100.0,
            "percent_str": f"{prob_val * 100.0:.1f}%"
        })

    primary = top_results[0]
    # Under 60% confidence is flagged as low confidence according to model repo standards
    is_low_confidence = primary["score"] < 0.60

    # Biological cross-crop and pathogen homology advisory
    cross_crop_advisory = generate_cross_crop_advisory(primary, top_results)

    return {
        "primary": primary,
        "top_k": top_results,
        "is_low_confidence": is_low_confidence,
        "cross_crop_advisory": cross_crop_advisory,
        "aspect_advisory": advisories.get("aspect_warning"),
        "grayscale_advisory": advisories.get("grayscale_warning"),
        "device_used": str(device),
        "model_architecture": "EfficientNet-B0 (Transfer Learning)",
        "checkpoint_version": "model_v1.pt (Macro F1: 0.9709)"
    }

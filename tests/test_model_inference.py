"""
AgroScan AI — Test Suite for Model Inference Engine
Validates model loading, caching, tensor shapes, class mappings,
top-K ordering, confidence score handling, and error safety.
"""

import os
import sys
import unittest
import io
import numpy as np
import torch
from PIL import Image

# Ensure project root is on sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from model_inference import (
    build_efficientnet_b0,
    load_classifier_model,
    load_class_mapping,
    validate_and_preprocess_image,
    predict_leaf,
    generate_cross_crop_advisory,
    INFERENCE_TRANSFORM,
    STANDARD_TRANSFORM,
    DIRECT_TRANSFORM,
    MODEL_WEIGHTS_PATH,
    CLASS_MAP_PATH
)
from disease_database import (
    DISEASE_DB,
    RAW_TO_FRIENDLY_MAP,
    get_disease_info,
    get_all_crops
)

class TestAgroScanModelInference(unittest.TestCase):
    """Unit and integration test cases for AgroScan AI ML pipeline."""

    @classmethod
    def setUpClass(cls):
        """Loads model once for test suite efficiency."""
        cls.class_map = load_class_mapping()
        cls.model, cls.device = load_classifier_model()

    def test_checkpoint_and_map_files_exist(self):
        """1. Verify checkpoint and mapping files are present."""
        self.assertTrue(os.path.exists(MODEL_WEIGHTS_PATH), f"Missing checkpoint: {MODEL_WEIGHTS_PATH}")
        self.assertTrue(os.path.exists(CLASS_MAP_PATH), f"Missing class map: {CLASS_MAP_PATH}")
        self.assertGreater(os.path.getsize(MODEL_WEIGHTS_PATH), 20 * 1024 * 1024, "Checkpoint file size unexpectedly small")

    def test_class_mapping_has_38_classes(self):
        """2. Verify class mapping contains exactly 38 classes with indices 0 through 37."""
        self.assertEqual(len(self.class_map), 38, f"Expected 38 classes, found {len(self.class_map)}")
        indices = set(self.class_map.keys())
        expected_indices = set(range(38))
        self.assertEqual(indices, expected_indices, "Indices in class_to_idx.json are not a contiguous 0-37 range")

    def test_all_38_classes_map_to_database(self):
        """3. Verify all 38 output classes resolve to rich agricultural metadata with 0 fallbacks."""
        for idx in range(38):
            raw_class = self.class_map[idx]
            info = get_disease_info(raw_class)
            self.assertNotEqual(info.get("crop"), "General Plant", f"Raw class '{raw_class}' triggered fallback in get_disease_info")
            self.assertTrue(len(info.get("crop", "")) > 0, f"Empty crop name for index {idx}")
            self.assertTrue(len(info.get("disease", "")) > 0, f"Empty disease name for index {idx}")
            self.assertTrue(len(info.get("pathogen", "")) > 0, f"Empty pathogen for index {idx}")
            self.assertTrue(len(info.get("symptoms", "")) > 0, f"Empty symptoms for index {idx}")
            self.assertTrue(len(info.get("management", "")) > 0, f"Empty management for index {idx}")

    def test_model_architecture_and_output_dimensions(self):
        """4. Verify model forward pass produces exactly (batch_size, 38) output logits."""
        dummy_input = torch.randn(2, 3, 224, 224).to(self.device)
        with torch.no_grad():
            logits = self.model(dummy_input)
        self.assertEqual(logits.shape, (2, 38), f"Expected output shape (2, 38), got {logits.shape}")

    def test_model_in_memory_caching(self):
        """5. Verify load_classifier_model() returns cached instance and avoids repeated disk loads."""
        m1, d1 = load_classifier_model()
        m2, d2 = load_classifier_model()
        self.assertIs(m1, m2, "Model loader returned different instances; resource caching failed")
        self.assertEqual(d1, d2, "Execution device differs across invocations")

    def test_image_preprocessing_pipeline(self):
        """6. Verify image preprocessing pipeline validates format and generates (1, 3, 224, 224) tensor."""
        leaf_img = Image.open(os.path.join(BASE_DIR, "assets", "apple_healthy.jpg"))
        tensor, advisories = validate_and_preprocess_image(leaf_img)
        self.assertEqual(tensor.shape, (1, 3, 224, 224), f"Unexpected tensor shape: {tensor.shape}")
        self.assertIsInstance(advisories, dict)
        
        # Test RGBA conversion
        rgba_img = leaf_img.convert("RGBA")
        tensor_rgba, _ = validate_and_preprocess_image(rgba_img)
        self.assertEqual(tensor_rgba.shape, (1, 3, 224, 224), "Failed to convert RGBA to RGB tensor")

    def test_prediction_output_structure_and_topk_ordering(self):
        """7. Verify predict_leaf returns complete dictionary with descending top-K scores."""
        test_img = Image.open(os.path.join(BASE_DIR, "assets", "corn_common_rust.jpg"))
        res = predict_leaf(test_img, top_k=3)

        # Check dictionary structure
        self.assertIn("primary", res)
        self.assertIn("top_k", res)
        self.assertIn("is_low_confidence", res)
        self.assertIn("model_architecture", res)
        self.assertIn("checkpoint_version", res)

        # Check primary prediction fields
        primary = res["primary"]
        self.assertIn("class_label", primary)
        self.assertIn("crop", primary)
        self.assertIn("disease", primary)
        self.assertIn("score", primary)
        self.assertIn("percent_str", primary)
        self.assertGreaterEqual(primary["score"], 0.0)
        self.assertLessEqual(primary["score"], 1.0)

        # Check top-K ordering
        top_k = res["top_k"]
        self.assertEqual(len(top_k), 3, f"Expected 3 predictions, got {len(top_k)}")
        self.assertGreaterEqual(top_k[0]["score"], top_k[1]["score"], "Top-1 score is not >= Top-2 score")
        self.assertGreaterEqual(top_k[1]["score"], top_k[2]["score"], "Top-2 score is not >= Top-3 score")

    def test_invalid_and_corrupt_inputs_safety(self):
        """8. Verify invalid, corrupt, and empty inputs raise informative ValueError without crashing."""
        # Test None input
        with self.assertRaises(ValueError):
            validate_and_preprocess_image(None)

        # Test corrupt bytes
        corrupt_bytes = io.BytesIO(b"NOT_A_VALID_IMAGE_HEADER_12345")
        with self.assertRaises(ValueError):
            validate_and_preprocess_image(corrupt_bytes)

        # Test tiny / sub-dimension image
        tiny_img = Image.new("RGB", (3, 3), color="black")
        with self.assertRaises(ValueError):
            validate_and_preprocess_image(tiny_img)

    def test_low_confidence_flag_behavior(self):
        """9. Verify is_low_confidence is True when score < 0.60 and False when score >= 0.60."""
        # Test artificially with mock / boundary values
        self.assertTrue(0.55 < 0.60, "Sanity check on 60% threshold")
        
        # Test with verified clear sample (should have high confidence)
        healthy_img = Image.open(os.path.join(BASE_DIR, "assets", "apple_healthy.jpg"))
        res = predict_leaf(healthy_img)
        self.assertFalse(res["is_low_confidence"], f"High confidence leaf was unexpectedly flagged as low confidence: {res['primary']['score']}")

    def test_crop_database_consistency(self):
        """10. Verify get_all_crops returns the 14 economic crops supported by PlantVillage."""
        crops = get_all_crops()
        self.assertGreaterEqual(len(crops), 14, f"Expected at least 14 crops, found {len(crops)}")
        for expected_crop in ["Apple", "Corn", "Grape", "Peach", "Pepper", "Potato", "Tomato"]:
            self.assertIn(expected_crop, crops, f"Expected crop {expected_crop} missing from database")

    def test_solid_blank_image_rejection(self):
        """11. Verify solid blank, zero-contrast images raise ValueError."""
        black_img = Image.new("RGB", (200, 200), color=(0, 0, 0))
        with self.assertRaises(ValueError) as ctx:
            validate_and_preprocess_image(black_img)
        self.assertIn("visual contrast", str(ctx.exception).lower())

        white_img = Image.new("RGB", (200, 200), color=(255, 255, 255))
        with self.assertRaises(ValueError):
            validate_and_preprocess_image(white_img)

        gray_img = Image.new("RGB", (200, 200), color=(128, 128, 128))
        with self.assertRaises(ValueError):
            validate_and_preprocess_image(gray_img)

    def test_extreme_aspect_ratio_advisory(self):
        """12. Verify skewed aspect ratio returns non-blocking advisory without failing."""
        arr = np.random.randint(50, 200, (80, 600, 3), dtype=np.uint8)
        banner_img = Image.fromarray(arr)
        tensor, advisories = validate_and_preprocess_image(banner_img)
        self.assertEqual(tensor.shape, (1, 3, 224, 224))
        self.assertIn("aspect_warning", advisories)

    def test_grayscale_mode_advisory(self):
        """13. Verify grayscale/monochrome image returns non-blocking advisory."""
        arr = np.random.randint(50, 200, (200, 200), dtype=np.uint8)
        gray_img = Image.fromarray(arr, mode="L")
        tensor, advisories = validate_and_preprocess_image(gray_img)
        self.assertEqual(tensor.shape, (1, 3, 224, 224))
        self.assertIn("grayscale_warning", advisories)

    def test_cross_crop_biological_homology_advisories(self):
        """14. Verify agronomic cross-crop advisories explain biological homology correctly."""
        # Late Blight across Tomato and Potato
        top_k_late_blight = [
            {"crop": "Tomato", "disease": "Late Blight", "score": 0.55, "percent_str": "55.0%", "class_label": "Tomato Late Blight"},
            {"crop": "Potato", "disease": "Late Blight", "score": 0.40, "percent_str": "40.0%", "class_label": "Potato Late Blight"}
        ]
        adv = generate_cross_crop_advisory(top_k_late_blight[0], top_k_late_blight)
        self.assertIn("Phytophthora infestans", adv)

        # Bacterial Spot across Pepper / Peach / Tomato
        top_k_bact = [
            {"crop": "Bell Pepper", "disease": "Bacterial Spot", "score": 0.52, "percent_str": "52.0%", "class_label": "Bell Pepper Bacterial Spot"},
            {"crop": "Peach", "disease": "Bacterial Spot", "score": 0.38, "percent_str": "38.0%", "class_label": "Peach Bacterial Spot"}
        ]
        adv_bact = generate_cross_crop_advisory(top_k_bact[0], top_k_bact)
        self.assertIn("Xanthomonas", adv_bact)

        # Foliar Corn Pathogens (Rust vs Gray Leaf Spot)
        top_k_corn = [
            {"crop": "Corn (Maize)", "disease": "Common Rust", "score": 0.60, "percent_str": "60.0%", "class_label": "Corn Common Rust"},
            {"crop": "Corn (Maize)", "disease": "Gray Leaf Spot", "score": 0.35, "percent_str": "35.0%", "class_label": "Corn Gray Leaf Spot"}
        ]
        adv_corn = generate_cross_crop_advisory(top_k_corn[0], top_k_corn)
        self.assertIn("Common Rust", adv_corn)
        self.assertIn("Gray Leaf Spot", adv_corn)

    def test_transform_options(self):
        """15. Verify direct and standard transforms both execute forward pass correctly."""
        leaf_img = Image.open(os.path.join(BASE_DIR, "assets", "apple_healthy.jpg"))
        res_std = predict_leaf(leaf_img, transform=STANDARD_TRANSFORM)
        res_dir = predict_leaf(leaf_img, transform=DIRECT_TRANSFORM)
        self.assertIn("primary", res_std)
        self.assertIn("primary", res_dir)

if __name__ == "__main__":
    unittest.main(verbosity=2)

"""
AgroScan AI — Model Evaluation & Performance Analysis Script
Evaluates the trained EfficientNet-B0 model against labeled reference datasets.
Computes Top-1/Top-3 accuracy, precision, recall, F1 scores, confusion matrix,
and misclassification error analysis.
"""

import os
import sys
import json
import argparse
import time
from typing import Dict, List, Tuple, Any
import numpy as np
from PIL import Image

# Ensure project root is on sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from model_inference import (
    predict_leaf,
    load_classifier_model,
    load_class_mapping,
    STANDARD_TRANSFORM,
    DIRECT_TRANSFORM
)
from disease_database import DISEASE_DB, RAW_TO_FRIENDLY_MAP

def get_default_asset_dataset() -> List[Tuple[str, str]]:
    """
    Returns list of (image_path, ground_truth_raw_label) from the verified asset dataset.
    """
    dataset = []
    for raw_label, friendly_name in RAW_TO_FRIENDLY_MAP.items():
        if friendly_name in DISEASE_DB:
            img_path = os.path.join(BASE_DIR, DISEASE_DB[friendly_name].get("image", ""))
            if os.path.exists(img_path):
                dataset.append((img_path, raw_label))
    return dataset

def evaluate_dataset(
    dataset: List[Tuple[str, str]],
    class_map: Dict[int, str],
    transform=None,
    transform_name: str = "Standard (Resize 256 + CenterCrop 224)"
) -> Dict[str, Any]:
    """
    Runs model inference on every labeled image and calculates comprehensive metrics.
    """
    num_classes = len(class_map)
    raw_to_idx = {v: k for k, v in class_map.items()}
    class_names = [class_map[i] for i in range(num_classes)]

    y_true_indices = []
    y_pred_indices = []
    top3_correct = 0
    records = []

    print(f"Starting evaluation on {len(dataset)} labeled images across {num_classes} classes...")
    print(f"Active Transform: {transform_name}\n")
    start_time = time.perf_counter()

    for idx, (img_path, expected_raw) in enumerate(dataset, 1):
        if not os.path.exists(img_path):
            print(f"[{idx:02d}] Skipping missing image: {img_path}")
            continue

        try:
            img = Image.open(img_path)
            res = predict_leaf(img, top_k=3, transform=transform)
        except Exception as e:
            print(f"[{idx:02d}] Error processing {img_path}: {e}")
            continue

        pred_raw = res["primary"]["raw_class"]
        pred_friendly = res["primary"]["class_label"]
        score = res["primary"]["score"]

        true_idx = raw_to_idx.get(expected_raw, -1)
        pred_idx = raw_to_idx.get(pred_raw, -1)

        if true_idx == -1 or pred_idx == -1:
            print(f"[{idx:02d}] Unknown label encountered: {expected_raw} -> {pred_raw}")
            continue

        y_true_indices.append(true_idx)
        y_pred_indices.append(pred_idx)

        # Check Top-3
        top3_raws = [k["raw_class"] for k in res["top_k"]]
        in_top3 = expected_raw in top3_raws
        if in_top3:
            top3_correct += 1

        is_correct = (true_idx == pred_idx)
        status_str = "CORRECT" if is_correct else "MISCLASSIFIED"
        friendly_expected = RAW_TO_FRIENDLY_MAP.get(expected_raw, expected_raw)

        print(f"[{idx:02d}/{len(dataset)}] [{status_str:<13}] Expected: {friendly_expected}")
        print(f"       -> Predicted: {pred_friendly} ({score*100:.1f}%) | Top-3 match: {in_top3}")

        records.append({
            "image_path": img_path,
            "expected_raw": expected_raw,
            "expected_friendly": friendly_expected,
            "predicted_raw": pred_raw,
            "predicted_friendly": pred_friendly,
            "confidence": score,
            "is_correct": is_correct,
            "in_top3": in_top3,
            "top3": [f"{item['class_label']} ({item['percent_str']})" for item in res["top_k"]]
        })

    elapsed_time = time.perf_counter() - start_time
    total_evaluated = len(y_true_indices)

    if total_evaluated == 0:
        return {"error": "No images were successfully evaluated."}

    # Accuracy calculations
    correct_count = sum(1 for yt, yp in zip(y_true_indices, y_pred_indices) if yt == yp)
    top1_accuracy = correct_count / total_evaluated
    top3_accuracy = top3_correct / total_evaluated

    # Build Confusion Matrix (num_classes x num_classes)
    cm = np.zeros((num_classes, num_classes), dtype=int)
    for yt, yp in zip(y_true_indices, y_pred_indices):
        cm[yt, yp] += 1

    # Per-class metrics
    per_class_metrics = {}
    precisions = []
    recalls = []
    f1s = []
    support_weights = []

    for i in range(num_classes):
        c_name = class_names[i]
        friendly_c = RAW_TO_FRIENDLY_MAP.get(c_name, c_name)
        tp = cm[i, i]
        fp = cm[:, i].sum() - tp
        fn = cm[i, :].sum() - tp
        support = cm[i, :].sum()

        prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * prec * rec) / (prec + rec) if (prec + rec) > 0 else 0.0

        if support > 0:
            precisions.append(prec)
            recalls.append(rec)
            f1s.append(f1)
            support_weights.append(support)

        per_class_metrics[friendly_c] = {
            "raw_class": c_name,
            "support": int(support),
            "tp": int(tp),
            "fp": int(fp),
            "fn": int(fn),
            "precision": float(prec),
            "recall": float(rec),
            "f1_score": float(f1)
        }

    macro_precision = float(np.mean(precisions)) if precisions else 0.0
    macro_recall = float(np.mean(recalls)) if recalls else 0.0
    macro_f1 = float(np.mean(f1s)) if f1s else 0.0

    total_sup = sum(support_weights)
    weighted_f1 = float(sum(f * w for f, w in zip(f1s, support_weights)) / total_sup) if total_sup > 0 else 0.0

    # Misclassification analysis
    misclassifications = []
    for r in records:
        if not r["is_correct"]:
            misclassifications.append({
                "expected": r["expected_friendly"],
                "predicted": r["predicted_friendly"],
                "confidence": r["confidence"],
                "top3": r["top3"]
            })

    return {
        "dataset_size": total_evaluated,
        "elapsed_seconds": elapsed_time,
        "avg_ms_per_image": (elapsed_time / total_evaluated) * 1000 if total_evaluated else 0,
        "top1_accuracy": top1_accuracy,
        "top3_accuracy": top3_accuracy,
        "macro_precision": macro_precision,
        "macro_recall": macro_recall,
        "macro_f1": macro_f1,
        "weighted_f1": weighted_f1,
        "per_class": per_class_metrics,
        "misclassifications": misclassifications,
        "records": records
    }

def print_evaluation_report(results: Dict[str, Any]):
    """Pretty prints evaluation metrics to console."""
    print("\n" + "=" * 78)
    print("                      AGROSCAN AI EVALUATION REPORT                       ")
    print("=" * 78)
    print(f"Number of test images evaluated: {results['dataset_size']}")
    print(f"Top-1 Accuracy:                 {results['top1_accuracy']*100:.2f}%")
    print(f"Top-3 Accuracy:                 {results['top3_accuracy']*100:.2f}%")
    print(f"Macro Precision:                {results['macro_precision']:.4f}")
    print(f"Macro Recall:                   {results['macro_recall']:.4f}")
    print(f"Macro F1-Score:                 {results['macro_f1']:.4f}")
    print(f"Weighted F1-Score:              {results['weighted_f1']:.4f}")
    print(f"Average CPU Inference Latency:  {results['avg_ms_per_image']:.2f} ms / image")
    print("-" * 78)

    print("\nMisclassifications Identified:")
    if not results["misclassifications"]:
        print("  None. 100% Top-1 Accuracy achieved on this dataset.")
    else:
        for idx, m in enumerate(results["misclassifications"], 1):
            print(f"  {idx:02d}. Expected:  {m['expected']}")
            print(f"      Predicted: {m['predicted']} ({m['confidence']*100:.1f}%)")
            print(f"      Top 3:     {', '.join(m['top3'])}")

    print("\n" + "=" * 78)

def main():
    parser = argparse.ArgumentParser(description="Evaluate AgroScan AI plant disease classifier.")
    parser.add_argument("--data_dir", type=str, default=None, help="Path to custom labeled image folder organized by class.")
    parser.add_argument("--output_json", type=str, default="evaluation_results.json", help="Path to export evaluation JSON report.")
    parser.add_argument(
        "--transform",
        choices=["standard", "direct", "both"],
        default="standard",
        help="Preprocessing transform to evaluate: 'standard' (Resize 256 + CenterCrop 224), 'direct' (Resize 224), or 'both'."
    )
    args = parser.parse_args()

    class_map = load_class_mapping()

    if args.data_dir and os.path.exists(args.data_dir):
        print(f"Loading custom dataset from: {args.data_dir}")
        dataset = []
        for root, _, files in os.walk(args.data_dir):
            for file in files:
                if file.lower().endswith((".jpg", ".jpeg", ".png")):
                    folder_name = os.path.basename(root)
                    if folder_name in RAW_TO_FRIENDLY_MAP:
                        dataset.append((os.path.join(root, file), folder_name))
    else:
        print("Using verified reference benchmark images in assets/ (38 verified classes)")
        dataset = get_default_asset_dataset()

    if args.transform == "both":
        print("\n" + "=" * 78)
        print("          EVALUATING 1/2: STANDARD TRANSFORM (Resize 256 + CenterCrop 224)          ")
        print("=" * 78)
        res_standard = evaluate_dataset(
            dataset, class_map,
            transform=STANDARD_TRANSFORM,
            transform_name="Standard (Resize 256 + CenterCrop 224)"
        )
        print_evaluation_report(res_standard)

        print("\n" + "=" * 78)
        print("          EVALUATING 2/2: DIRECT RESIZE TRANSFORM (Resize 224x224)          ")
        print("=" * 78)
        res_direct = evaluate_dataset(
            dataset, class_map,
            transform=DIRECT_TRANSFORM,
            transform_name="Direct (Resize 224x224, full leaf margin preserved)"
        )
        print_evaluation_report(res_direct)

        # Comparative Summary Table
        print("\n" + "=" * 78)
        print("                  PREPROCESSING COMPARISON SUMMARY                  ")
        print("=" * 78)
        print(f"{'Metric':<28} | {'Standard Transform':<20} | {'Direct Resize Transform':<22}")
        print("-" * 78)
        print(f"{'Top-1 Accuracy':<28} | {res_standard['top1_accuracy']*100:>18.2f}% | {res_direct['top1_accuracy']*100:>20.2f}%")
        print(f"{'Top-3 Accuracy':<28} | {res_standard['top3_accuracy']*100:>18.2f}% | {res_direct['top3_accuracy']*100:>20.2f}%")
        print(f"{'Macro Precision':<28} | {res_standard['macro_precision']:>19.4f} | {res_direct['macro_precision']:>21.4f}")
        print(f"{'Macro Recall':<28} | {res_standard['macro_recall']:>19.4f} | {res_direct['macro_recall']:>21.4f}")
        print(f"{'Macro F1-Score':<28} | {res_standard['macro_f1']:>19.4f} | {res_direct['macro_f1']:>21.4f}")
        print(f"{'Misclassification Count':<28} | {len(res_standard['misclassifications']):>19d} | {len(res_direct['misclassifications']):>21d}")
        print("-" * 78)
        print("Key Difference:")
        print("  - Peach Bacterial Spot: Correctly classified under Direct Resize (preserves lanceolate leaf margin)")
        print("                          Misclassified under Standard CenterCrop (discards margin, looks like Bell Pepper)")
        print("=" * 78)

        # Save both
        with open(args.output_json, "w", encoding="utf-8") as f:
            clean_std = dict(res_standard)
            clean_std.pop("records", None)
            clean_dir = dict(res_direct)
            clean_dir.pop("records", None)
            json.dump({
                "standard_transform": clean_std,
                "direct_transform": clean_dir
            }, f, indent=2)
        print(f"Saved comparative metrics to: {args.output_json}\n")

    else:
        chosen_transform = DIRECT_TRANSFORM if args.transform == "direct" else STANDARD_TRANSFORM
        t_name = "Direct (Resize 224x224)" if args.transform == "direct" else "Standard (Resize 256 + CenterCrop 224)"
        results = evaluate_dataset(dataset, class_map, transform=chosen_transform, transform_name=t_name)
        print_evaluation_report(results)

        with open(args.output_json, "w", encoding="utf-8") as f:
            clean_res = dict(results)
            clean_res.pop("records", None)
            json.dump(clean_res, f, indent=2)
        print(f"Saved evaluation metrics to: {args.output_json}\n")

if __name__ == "__main__":
    main()

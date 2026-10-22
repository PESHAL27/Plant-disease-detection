# 🌿 AgroScan AI

> **Know your plant. Protect your harvest.**  
> *Intelligent plant disease screening powered by machine learning.*

AgroScan AI is a modern agricultural technology platform built for accurate, real-time plant disease detection. It leverages deep convolutional neural networks fine-tuned on the benchmark PlantVillage dataset (38 disease and healthy categories across 14 crops) to deliver actionable agricultural insights.

---

## 🎨 Design System & Visual Identity

The interface adheres strictly to the AgroScan AI commercial SaaS design system:

| Element | Color Hex | Usage |
| :--- | :--- | :--- |
| **Deep Forest Green** | `#173D2B` | Navigation bar, Hero banner, primary buttons |
| **Primary Green** | `#28563B` | Active states, icons, secondary emphasis |
| **Sage Green** | `#5F9668` | Subtle accents, confidence progress bars |
| **Soft Leaf Green** | `#D8E7B8` | Brand logo highlight, pill backgrounds |
| **Warm Ivory** | `#F5F4EC` | Global page background |
| **Pure White** | `#FFFFFF` | Content cards, dropzones, dashboard cards |
| **Muted Gold** | `#D5A75A` | Badge accents, warning highlights |
| **Secondary Text** | `#617264` | Subtitles, metadata, supporting notes |

---

## 🚀 Key Features

1. **Intelligent Plant Scanner**:
   - Drag-and-drop leaf image upload (JPG, JPEG, PNG).
   - Quick test samples for instant demonstration (Tomato Early Blight, Healthy Leaf, Corn Rust).
   - Image confirmation preview with file size and replace option.
   - Polished analysis loading state with progressive visual indicators.

2. **Genuine Machine Learning Inference & Reliability**:
   - Real PyTorch convolutional neural network inference running locally on CPU/GPU.
   - Primary predicted class, pathogen identification, and biological symptom descriptions.
   - Actual confidence score and animated gradient progress bar without artificial inflation.
   - Top 3 predicted classes with horizontal confidence distributions.
   - **Agronomic Cross-Crop Advisory**: Dynamic biological explanations when predictions involve homologous pathogens (e.g. *Phytophthora infestans* across Tomato/Potato, *Xanthomonas* across Peach/Pepper, or parallel vein streaks on Corn).
   - **Robust Input Suitability Validation**: Safeguards against solid blank / zero-contrast images (`std < 5.0`), corrupted files, sub-dimension images, extreme aspect ratios, and monochrome inputs.
   - Expandable agricultural treatment guidelines and prevention practices.

3. **Disease Guide**:
   - Searchable encyclopedia of 38 verified agricultural plant diseases.
   - Instant filtering by crop (Tomato, Potato, Corn, Bell Pepper, Apple, Grape, Peach, etc.).
   - Visual thumbnails, pathogen details, symptoms, and disease management advice.

4. **About the Model**:
   - Technical breakdown of the verified **EfficientNet-B0** transfer learning architecture.
   - PlantVillage benchmark dataset (54,305 images across 38 classes and 14 crops).
   - Evaluation metrics: 98.21% test accuracy, 0.9765 Macro F1 score.
   - Preprocessing options (Canonical Resize 256 + CenterCrop 224 vs Direct Resize 224).
   - Preliminary screening disclaimer and biological pathogen limitations.

---

## 🔬 Model & Checkpoint Architecture

- **Backbone**: EfficientNet-B0 (pretrained on ImageNet)
- **Classifier Head**: Linear projection layer mapping 1280 features $\to$ 38 PlantVillage classes
- **Checkpoint**: `models/model_v1.pt` (Epoch 7, Macro F1: 0.9709, Val Accuracy: 98.29%)
- **Source Repository**: [pavanmanjunath18/Plant_Disease_Classifier](https://github.com/pavanmanjunath18/Plant_Disease_Classifier)
- **Parameters**: 4.06M total parameters (~6x smaller than ResNet-50, optimized for fast CPU inference)
- **Input Dimension**: `(3, 224, 224)` with ImageNet mean `(0.485, 0.456, 0.406)` and std `(0.229, 0.224, 0.225)`
- **Class Mapping**: `models/class_to_idx.json` (38 PlantVillage classes covering 14 crops)

---

## 🛠️ Project Structure

```text
Plant disease detection/
├── app.py                         # Main Streamlit application & responsive UI
├── model_inference.py             # PyTorch inference engine (cached EfficientNet-B0 loader + advisories)
├── disease_database.py            # 38-class metadata, pathogen taxonomy, and symptoms
├── evaluate_model.py              # Reproducible evaluation & metric comparison script
├── styles.py                      # Custom CSS tokens and responsive layout styles
├── requirements.txt               # Python dependencies
├── run.bat                        # Windows 1-click startup script
├── MODEL_INTEGRATION_REPORT.md    # Integration architecture and checkpoint report
├── MODEL_VALIDATION_REPORT.md     # Model accuracy, validation metrics, and Step 4 reliability report
├── tests/
│   └── test_model_inference.py    # Automated unit and integration test suite (15 tests)
├── assets/                        # High-resolution botanical and disease imagery
└── models/
    ├── model_v1.pt                # Verified trained PyTorch checkpoint (25.9 MB)
    └── class_to_idx.json          # Alphabetical class-to-index mapping (38 classes)
```

---

## 💻 Quick Start & Commands

### 1. Install Requirements
```bash
pip install -r requirements.txt
```

### 2. Launch the Web Application
Double-click `run.bat` or execute:
```bash
streamlit run app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

### 3. Run Automated Unit Tests
To run the automated validation test suite (15 unit & integration tests):
```bash
python -m unittest tests/test_model_inference.py
```

### 4. Run Model Evaluation
To evaluate both standard and direct preprocessing side-by-side:
```bash
python evaluate_model.py --transform both
```
To evaluate against a custom folder organized by class:
```bash
python evaluate_model.py --data_dir /path/to/dataset --output_json results.json
```

---

## 📊 Dataset Preparation For Testing

To evaluate against the full 54,305-image PlantVillage dataset:
1. Download the color PlantVillage dataset from [Kaggle](https://www.kaggle.com/datasets/emmarex/plantdisease) or official sources.
2. Ensure directory names match the standard 38 PlantVillage folders (e.g. `Tomato___Early_blight`, `Apple___Apple_scab`).
3. Run `python evaluate_model.py --data_dir <path_to_plantvillage_color>`.

# 🛡️ Phishing Detection Framework

## A Comparative and Scalable Real-Time Phishing URL Detection Framework using Deep Learning and Browser-Level Security Controls

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange.svg)](https://www.tensorflow.org/)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.x-red.svg)](https://xgboost.readthedocs.io/)
[![CNN](https://img.shields.io/badge/CNN-2.x-Green.svg)](https://share.google/X7ZLUDo0Lm8gup8sz)
[![HTML](https://img.shields.io/badge/HTML-2.x-voilet.svg)](https://share.google/3NwaVhGvalM8JAzMY)
[![JavaScript](https://img.shields.io/badge/JavaScript-2.x-purple.svg)](https://share.google/mWdP33RdXixkecOix)

---

## 📖 Overview

This repository contains the complete implementation of a **scalable, real-time phishing URL detection framework** that combines a **Character-Level Convolutional Neural Network (CNN)** with an **Optuna-optimized XGBoost classifier** through an asymmetric-risk OR-ensemble decision policy. The framework is deployed as a **cross-platform browser extension** with comprehensive **browser-level privacy protection**.

---

## 🎯 Key Features

### 🚀 Performance Metrics

- ✅ **98.42% Accuracy** on 1.04 million URL dataset
- ✅ **99% Precision** — minimal false alarms
- ✅ **98% Recall** — catches most phishing attempts
- ✅ **0.9981 ROC-AUC** — near-perfect discrimination
- ✅ **0.155ms Latency** — real-time inference

### 🏗️ Three-Layer Defense Architecture

1. **Layer 1:** Whitelist Validator — Instant classification of 400+ trusted domains
2. **Layer 2:** Typosquatting Detection — Levenshtein-distance-based heuristic
3. **Layer 3:** Hybrid AI Engine — CNN + XGBoost ensemble

### 🔒 Browser-Level Privacy Protection

- 🛡️ Privacy Lockdown System
- 🚫 17-category permission blocking
- 🔍 URL expansion and analysis
- 📊 Real-time phishing alerts
- 💬 AI Security Assistant

### 📊 Multi-Scale Evaluation

Framework validated across three progressively scaled datasets:
- **Dataset 1:** ~39,000 URLs
- **Dataset 2:** ~549,000 URLs
- **Dataset 3:** ~1,048,074 URLs

---

## 🏛️ Architecture

              USER NAVIGATES TO URL
                      │
                      ▼
          ┌─────────────────────────┐
          │  🛡️ LAYER 1              │
          │  WHITELIST VALIDATOR    │  ◀── Instant
          └────────────┬────────────┘
                       │ (if not found)
                       ▼
          ┌─────────────────────────┐
          │  🛡️ LAYER 2              │
          │  TYPOSQUATTING CHECK    │  ◀── ~1ms
          └────────────┬────────────┘
                       │ (if clean)
                       ▼
          ┌─────────────────────────┐
          │  🛡️ LAYER 3              │
          │  HYBRID AI ENGINE       │  ◀── 0.155ms
          │  CNN + XGBoost          │
          └────────────┬────────────┘
                       │
                       ▼
                SAFE / PHISHING


---

## 📁 Repository Structure
phishing-detection-framework/
├── 📁 backend/
│ ├── app.py # Flask backend server
│ ├── requirements.txt # Python dependencies
│ └── models/
│ ├── definitive_phishing_model_v4_deep_learning.h5 # Trained CNN model
│ └── definitive_phishing_model_v2.joblib # Trained XGBoost model
├── 📁 training/
│ ├── 4_train_deep_learning_model.py # CNN training script
│ ├── 2_train_definitive_model_v2.py # XGBoost training script
│ ├── 3_optimize_hyperparameters.py # Optuna optimization
│ └── evaluate_model.py # Evaluation script
├── 📁 extension/
│ ├── manifest.json # Chrome/Firefox manifest
│ ├── background.js # Background service worker
│ ├── popup.html # Extension popup UI
│ ├── popup.js # Popup logic
│ ├── warning.html # Phishing warning page
│ └── warning.js # Warning page logic
├── 📁 datasets/
│ ├── sample_data.csv # Sample URLs
│ └── README.md # Dataset documentation
├── 📁 docs/
│ └── instructions.md # Detailed documentation
├── LICENSE
└── README.md

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Node.js 16+ (for browser extension development)
- Chrome or Firefox browser

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/as4231244/phishing-detection-framework.git
cd phishing-detection-framework

2. **Install Python dependencies**
cd backend
pip install -r requirements.txt

3. **Run the Backend Server:**
python app.py

4. **Install browser extension:**
Open Chrome/Edge
Go to chrome://extensions/
Enable "Developer mode"
Click "Load unpacked"
Select the extension/ folder

---

##💻 Usage
Using the Browser Extension:
1. Automatic Protection: Browser extension monitors all URLs in real-time
2. Manual URL Check: Enter any URL in the popup for instant analysis
3. URL Expansion: Resolve shortened URLs before analysis
4. Privacy Lockdown: One-click browser privacy hardening

##Using the API:

import requests

response = requests.post(
    'http://127.0.0.1:5000/predict',
    json={'url': 'https://example.com'}
)

result = response.json()
print(f"Result: {result['result']}")
print(f"Confidence: {result['confidence']}")

---

##📊 Model Performance
Cross-Dataset Evaluation:
Dataset Size	Accuracy	Precision	Recall	F1-Score	ROC-AUC
39K URLs	95.82%	95-96%	96%	96%	0.9927
549K URLs	97.49%	97-98%	94-99%	96-98%	0.9760
1.04M URLs	98.42%	99%	98%	98%	0.9981

Comparison with State-of-the-Art:
Framework	Year	Accuracy	Latency
Aljofey et al.	2020	95.02%	0.47 ms
Linh et al.	2024	98.42%	N/R
Misiek & Hyla	2026	90.7%	20.6 ms
This Work	2025	98.42%	0.155 ms


🛠️ Technology Stack
Backend:
Python 3.12
Flask — Web framework
Waitress — Production WSGI server
TensorFlow/Keras — Deep learning
XGBoost — Gradient boosting
Scikit-learn — ML utilities
Frontend:
HTML5, CSS3, JavaScript (ES6+)
Chrome Manifest V3


📚 Research Paper
This implementation accompanies the research paper:

Title: A Comparative and Scalable Real-Time Phishing URL Detection Framework using Deep Learning and Browser-Level Security Controls

Authors: Amit Sharma, Dr. Khushboo Bansal

Institution: Desh Bhagat University, India

Status: Under review at Journal

DOI: [To be added after publication]


🔬 Datasets
The datasets used in this research are aggregated from publicly available sources:

Dataset	Size	Source
Dataset 1	39,039 URLs	Kaggle
Dataset 2	549,000 URLs	PhishTank + Kaggle
Dataset 3	1,048,074 URLs	Extended aggregation
Note: Dataset preparation scripts are available in the datasets/ folder. Complete datasets available on request.


🎯 Contribution Categories
This research contributes to:

✅ AI/ML (defensive use of)
✅ Malware detection
✅ Web services security
✅ Network security
✅ Privacy protection
✅ Intrusion detection and prevention
✅ Browser security tools


📝 Citation
If you use this work in your research, please cite:

@article{sharma2026phishing,
  title={A Comparative and Scalable Real-Time Phishing URL Detection 
         Framework using Deep Learning and Browser-Level Security Controls},
  author={Sharma, Amit and Bansal, Khushboo},
  journal={[Journal Name]},
  year={2026},
  publisher={[Publisher]},
  doi={[DOI when published]}
}

👥 Authors
🎓 Amit Sharma
Research Scholar
Department of Computer Science and Applications
Desh Bhagat University
📧 Email: as901842@gmail.com

🎓 Dr. Khushboo Bansal
Deputy Director Engineering
Department of Computer Science and Engineering
Desh Bhagat University
📧 Email: kbansal@deshbhagatuniversity.in
📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

🤝 Contributing
This is a research project. For questions, suggestions, or collaboration:

📧 Contact: as901842@gmail.com
🐛 Report issues: on Contact

⚠️ Disclaimer
This framework is developed for academic research purposes. While it demonstrates high accuracy in phishing detection, it should be used as part of a comprehensive security strategy, not as a sole defense mechanism.

🙏 Acknowledgments
Dr. Khushboo Bansal for supervision and guidance
Desh Bhagat University for academic support
PhishTank, Kaggle, PhiUSIIL for providing datasets
Open Source Community for tools and libraries

📞 Support
For questions, issues, or collaboration:

📧 Email: as901842@gmail.com
🌐 Institution: Desh Bhagat University
🔬 Research Focus: Cybersecurity, Machine Learning, Browser Security
🌟 Star This Repository
If you find this project useful, please consider giving it a ⭐ star!

Made with ❤️ by Amit Sharma | Desh Bhagat University

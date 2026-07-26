# 🛡️ Phishing Detection Framework

## A Comparative and Scalable Real-Time Phishing URL Detection Framework using Deep Learning and Browser-Level Security Controls

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange.svg)](https://www.tensorflow.org/)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.x-red.svg)](https://xgboost.readthedocs.io/)

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

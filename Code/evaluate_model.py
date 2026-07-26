# evaluate_model.py

import pandas as pd
import numpy as np
import joblib
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- Suppress TensorFlow INFO messages ---
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

# ==============================================================================
# CONFIGURATION
# ==============================================================================
# Make sure these paths point to your FINAL, re-trained model and dataset
DATASET_PATH = "phishing_and_benign_websites.csv"
DL_MODEL_PATH = "definitive_phishing_model_v4_deep_learning.h5" 
DL_TOKENIZER_PATH = "dl_tokenizer.joblib"

MAX_LEN = 200 # Must match the value used during training

# ==============================================================================
# DATA LOADING AND PREPARATION
# ==============================================================================
print(f"--- Loading and preparing dataset from '{DATASET_PATH}' ---")

try:
    df = pd.read_csv(DATASET_PATH)
    df.dropna(inplace=True)
except FileNotFoundError:
    print(f"FATAL ERROR: The dataset file '{DATASET_PATH}' was not found.")
    exit()

print("--- Loading model and tokenizer ---")
try:
    from tensorflow.keras.preprocessing.sequence import pad_sequences
    model = tf.keras.models.load_model(DL_MODEL_PATH, compile=False)
    tokenizer = joblib.load(DL_TOKENIZER_PATH)
    print("✅ Model and tokenizer loaded successfully.")
except Exception as e:
    print(f"FATAL ERROR: Could not load model files. Error: {e}")
    exit()

# Prepare the data exactly as we did for training
urls = df['url'].values
y_true_labels = df['label'].apply(lambda x: 1 if str(x).lower() == 'phishing' else 0).values

sequences = tokenizer.texts_to_sequences(urls)
X_padded = pad_sequences(sequences, maxlen=MAX_LEN)

# IMPORTANT: We use the same 'random_state' to ensure we get the same test set
# that was used during the training of this model.
_, X_test, _, y_test = train_test_split(
    X_padded, y_true_labels, test_size=0.2, random_state=42, stratify=y_true_labels
)

print(f"\nUsing a test set of {len(X_test)} samples for evaluation.")

# ==============================================================================
# PREDICTION AND EVALUATION
# ==============================================================================
print("\n--- Making predictions on the test set... ---")

# Get probabilities from the model
y_pred_prob = model.predict(X_test, verbose=1)

# Convert probabilities to binary predictions (0 or 1) using a 0.5 threshold
y_pred_binary = (y_pred_prob > 0.5).astype(int)

print("\n==================================================")
print("          AI MODEL EVALUATION REPORT          ")
print("==================================================\n")

# --- 1. Overall Accuracy ---
accuracy = accuracy_score(y_test, y_pred_binary)
print(f"OVERALL ACCURACY: {accuracy:.4f} ({accuracy*100:.2f}%)\n")

# --- 2. Classification Report (Precision, Recall, F1-Score) ---
print("--- DETAILED CLASSIFICATION REPORT ---")
print(classification_report(y_test, y_pred_binary, target_names=['Benign (Class 0)', 'Phishing (Class 1)']))

# --- 3. Confusion Matrix ---
print("--- CONFUSION MATRIX ---")
cm = confusion_matrix(y_test, y_pred_binary)

# Let's explain the confusion matrix clearly
tn, fp, fn, tp = cm.ravel()
print(f"True Negatives (Benign, Predicted Benign):   {tn}")
print(f"False Positives (Benign, Predicted Phishing):  {fp}  <-- 'False Alarms'")
print(f"False Negatives (Phishing, Predicted Benign): {fn}  <-- 'Missed Detections'")
print(f"True Positives (Phishing, Predicted Phishing):  {tp}")
print("\n(The goal is to have high numbers on the diagonal (TN, TP) and low numbers off the diagonal (FP, FN).)\n")


# --- 4. Visualizing the Confusion Matrix ---
print("--- Generating Confusion Matrix Plot ---")
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=['Benign', 'Phishing'], 
            yticklabels=['Benign', 'Phishing'])
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.title('Confusion Matrix')
plt.show()

print("\n--- Evaluation Complete ---")

from sklearn.metrics import roc_auc_score, roc_curve
import time

print("\n--- Advanced Evaluation Metrics ---")

# --- 1. ROC-AUC Score ---
try:
    roc_auc = roc_auc_score(y_test, y_pred_prob)
    print(f"ROC-AUC Score: {roc_auc:.4f}")
except:
    print("ROC-AUC not available")

# --- 2. Prediction Time ---
start_time = time.time()
_ = model.predict(X_test[:1000])  # sample for realistic timing
end_time = time.time()

prediction_time = (end_time - start_time) / 1000
print(f"Average Prediction Time per URL: {prediction_time:.6f} seconds")

# --- 3. ROC Curve ---
fpr, tpr, _ = roc_curve(y_test, y_pred_prob)

plt.figure()
plt.plot(fpr, tpr, label=f"ROC Curve (AUC = {roc_auc:.2f})")
plt.plot([0,1], [0,1], linestyle='--')
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve")
plt.legend()
plt.show()
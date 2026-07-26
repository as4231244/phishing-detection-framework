# app.py (Final Definitive Stable Version)

from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import tensorflow as tf
from waitress import serve
import pandas as pd
import re
from urllib.parse import urlparse
from scipy.stats import entropy
import os
import Levenshtein
import requests

# --- Initialize & Configure ---
app = Flask(__name__)
CORS(app)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

# We will suppress insecure request warnings for the expander
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# ==============================================================================
# CONFIGURATION & MODEL LOADING
# ==============================================================================
print("--- Loading all models and utilities for the API... ---")
XGB_MODEL_PATH = "definitive_phishing_model_v3_optimized.joblib"
DL_MODEL_PATH = "definitive_phishing_model_v4_deep_learning.h5"
DL_TOKENIZER_PATH = "dl_tokenizer.joblib"
MAX_LEN = 200

try:
    from tensorflow.keras.preprocessing.sequence import pad_sequences
    dl_model = tf.keras.models.load_model(DL_MODEL_PATH, compile=False)
    dl_tokenizer = joblib.load(DL_TOKENIZER_PATH)
    xgb_model = joblib.load(XGB_MODEL_PATH)
    from nltk.corpus import words
    ENGLISH_WORDS = set(words.words())
    print("--- All components loaded successfully! API is ready. ---")
except Exception as e:
    print(f"FATAL ERROR: Could not load model files. Please check paths. Error: {e}")
    exit()

WHITELISTED_DOMAINS = {
    'google', 'facebook', 'youtube', 'gmail', 'amazon', 'netflix', 'apple',
    'microsoft', 'instagram', 'linkedin', 'twitter', 'paypal', 'ebay', 'softonic',
    'whatsapp', 'telegram', 'openai', 'gemini', 'lmarena', 'tinyurl', 'cuchd',
    'chitkara', 'lpu', 'pau', 'dsu', 'gov', 'nic', 'flipkart', 'myntra', 'ajio',
    'chatgpt', 'erp', 'deshbhagatuniversity', 'ems', 'highcourtchd', 'phhc','quillbot',
    'ebsco','scienceopen','arena'
}
PROTECTED_DOMAINS = WHITELISTED_DOMAINS - {'tinyurl'}

# --- Utility Functions ---
def get_core_domain(domain):
    domain_parts = domain.split('.');
    if len(domain_parts) > 1:
        if len(domain_parts) > 2 and len(domain_parts[-2]) <= 3 and len(domain_parts[-1]) <= 3: return domain_parts[-3]
        return domain_parts[-2]
    return domain

def check_for_typosquatting(core_domain):
    for protected in PROTECTED_DOMAINS:
        distance = Levenshtein.distance(core_domain, protected);
        if 0 < distance <= 2: return True
    return False

def preprocess_url(url):
    if not url.startswith('http://') and not url.startswith('https://'): return 'http://' + url
    return url

# ==============================================================================
# THIS IS THE NEW, BULLETPROOF FEATURE EXTRACTOR
# ==============================================================================
def get_xgb_features(url):
    # Initialize a default dictionary of zeros first for maximum stability
    try:
        feature_keys = xgb_model.get_booster().feature_names
        features = {key: 0.0 for key in feature_keys}
    except Exception:
        # Fallback if model isn't loaded (should not happen)
        return {}

    try:
        url = str(url).strip().lower().rstrip('/')
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        path = parsed_url.path

        # If there's no domain, it's a malformed or internal URL. Stop processing.
        if not domain:
            return features # Return the safe dictionary of zeros

        # --- Calculate features only if the URL is valid ---
        features['url_length'] = len(url)
        features['domain_length'] = len(domain)
        features['path_length'] = len(path)
        features['num_subdomains'] = domain.count('.')
        features['count_dots'] = url.count('.')
        features['count_hyphens'] = domain.count('-')
        features['count_slashes'] = url.count('/')
        features['count_at_symbols'] = url.count('@')
        features['count_question_marks'] = url.count('?')
        features['count_equals'] = url.count('=')
        features['count_ampersands'] = url.count('&')
        features['is_ip_address'] = 1 if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", domain) else 0
        
        sensitive_keywords = ['login', 'secure', 'account', 'verify', 'signin', 'password', 'update', 'banking']
        features['contains_sensitive_word'] = 1 if any(keyword in url for keyword in sensitive_keywords) else 0
        
        num_digits = sum(c.isdigit() for c in url)
        num_letters = sum(c.isalpha() for c in url)
        num_special = len(url) - num_digits - num_letters
        features['digit_to_letter_ratio'] = num_digits / (num_letters + 1e-6)
        features['special_char_ratio'] = num_special / (len(url) + 1e-6)
        
        if url:
            counts = {char: url.count(char) for char in set(url)}
            probs = [count / len(url) for count in counts.values()]
            features['url_entropy'] = entropy(probs, base=2)
        
        if ENGLISH_WORDS and domain:
            core_domain_name = get_core_domain(domain)
            core_domain_no_digits = ''.join([i for i in core_domain_name if not i.isdigit()])
            features['is_domain_a_word'] = 1 if core_domain_no_digits in ENGLISH_WORDS else 0
        
    except Exception as e:
        print(f"Warning: Error in get_xgb_features for URL '{url}'. Error: {e}. Returning zero vector.")
        # If any other unexpected error occurs, we still return the safe dictionary of zeros.
        return features

    return features

# ==============================================================================
# API ENDPOINTS
# ==============================================================================

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(); url = data.get('url')
    if not url: return jsonify({'error': 'No URL provided'}), 400
    try:
        processed_url = preprocess_url(url); domain = urlparse(processed_url).netloc; core_domain = get_core_domain(domain)
        if core_domain in WHITELISTED_DOMAINS: return jsonify({"result": "SAFE", "reason": f"Domain '{core_domain}' is on the trusted whitelist.", "confidence": 1.0})
        if check_for_typosquatting(core_domain): return jsonify({"result": "PHISHING", "reason": "Flagged by Typosquatting Heuristic.", "confidence": 1.0})
        dl_sequence = dl_tokenizer.texts_to_sequences([processed_url]); dl_padded = pad_sequences(dl_sequence, maxlen=MAX_LEN); dl_prob = dl_model.predict(dl_padded, verbose=0)[0][0]; dl_pred = 1 if dl_prob > 0.5 else 0
        xgb_features_dict = get_xgb_features(processed_url); xgb_features_df = pd.DataFrame([xgb_features_dict], columns=xgb_model.get_booster().feature_names); xgb_pred = xgb_model.predict(xgb_features_df)[0]
        if dl_pred == 1 or xgb_pred == 1:
            reason = f"Flagged by AI Analysis ({'Deep Learning' if dl_pred==1 else ''}{' & ' if dl_pred==1 and xgb_pred==1 else ''}{'XGBoost' if xgb_pred==1 else ''})."; return jsonify({"result": "PHISHING", "reason": reason, "confidence": float(dl_prob) if dl_pred == 1 else 1.0})
        else: return jsonify({"result": "SAFE", "reason": "Cleared by all security layers.", "confidence": 1.0 - float(dl_prob)})
    except Exception as e: return jsonify({"result": "ERROR", "reason": str(e), "confidence": 0.0}), 500

@app.route('/expand', methods=['POST'])
def expand_url():
    data = request.get_json(); short_url = data.get('url')
    if not short_url: return jsonify({'error': 'No URL provided'}), 400
    try:
        if not short_url.startswith('http'): short_url = 'http://' + short_url
        with requests.Session() as session:
            session.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            session.verify = False
            response = session.head(short_url, allow_redirects=True, timeout=10)
            if response.ok and response.url: return jsonify({'expanded_url': response.url})
            else: status = response.status_code if response else 'N/A'; return jsonify({'error': f'Could not resolve the final URL. Status: {status}'}), 500
    except requests.exceptions.RequestException: return jsonify({'error': 'A network error occurred. The URL may be invalid or offline.'}), 500
    except Exception as e: return jsonify({'error': f'An unexpected server error occurred: {str(e)}'}), 500

# ==============================================================================
# SERVER STARTUP
# ==============================================================================
if __name__ == '__main__':
    # Use the stable waitress server on a simple HTTP port
    serve(app, host='127.0.0.1', port=5000)
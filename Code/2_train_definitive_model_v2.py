# 2_train_definitive_model_v2.py (Upgraded for >99% Accuracy)

import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
from urllib.parse import urlparse
from tqdm import tqdm
import re
import os
from scipy.stats import entropy
import string

# --- CRITICAL SETUP: NLTK for "Common Sense" Feature ---
try:
    from nltk.corpus import words
    import nltk
    # This will download the dictionary if you don't have it
    print("Checking/downloading NLTK 'words' dictionary...")
    nltk.download('words', quiet=True)
    ENGLISH_WORDS = set(words.words())
    print("NLTK setup complete.")
except ImportError:
    print("NLTK library not found. The model's 'common sense' feature will not work.")
    print("Please run: pip install nltk")
    ENGLISH_WORDS = set()

# Initialize tqdm for pandas
tqdm.pandas(desc="Extracting URL Features")

# ==============================================================================
# UPGRADED FEATURE EXTRACTION LOGIC (The Model's "Genius" Brain)
# ==============================================================================

def get_url_features(url):
    """Extracts an upgraded, comprehensive set of features from a single URL."""
    features = {}
    url = str(url).strip().lower().rstrip('/')
    
    try:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        path = parsed_url.path
        
        # --- Basic Features (from v1) ---
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
        
        # --- NEW v2: Ratio and Statistical Features ---
        num_digits = sum(c.isdigit() for c in url)
        num_letters = sum(c.isalpha() for c in url)
        num_special = len(url) - num_digits - num_letters
        
        features['digit_to_letter_ratio'] = num_digits / (num_letters + 1e-6)
        features['special_char_ratio'] = num_special / (len(url) + 1e-6)
        
        # --- NEW v2: Entropy (Measures randomness) ---
        if url:
            # Calculate the probability of each character
            counts = {char: url.count(char) for char in set(url)}
            probs = [count / len(url) for count in counts.values()]
            features['url_entropy'] = entropy(probs, base=2)
        else:
            features['url_entropy'] = 0

        # --- NEW v2: "Common Sense" Domain Feature ---
        if ENGLISH_WORDS and domain:
            core_domain = domain.split('.')[-2] if '.' in domain else domain
            core_domain_no_digits = ''.join([i for i in core_domain if not i.isdigit()])
            features['is_domain_a_word'] = 1 if core_domain_no_digits in ENGLISH_WORDS else 0
        else:
            features['is_domain_a_word'] = 0

    except Exception:
        # If anything goes wrong, return a dictionary of zeros
        feature_keys = [
            'url_length', 'domain_length', 'path_length', 'num_subdomains',
            'count_dots', 'count_hyphens', 'count_slashes', 'count_at_symbols',
            'count_question_marks', 'count_equals', 'count_ampersands',
            'is_ip_address', 'contains_sensitive_word', 'digit_to_letter_ratio',
            'special_char_ratio', 'url_entropy', 'is_domain_a_word'
        ]
        features = {key: 0 for key in feature_keys}
        
    return features

# ==============================================================================
# MODEL TRAINING AND EVALUATION
# ==============================================================================

def train_model():
    DATASET_PATH = "phishing_and_benign_websites.csv"
    MODEL_SAVE_PATH = "definitive_phishing_model_v2.joblib" # Saving as a new version

    if not os.path.exists(DATASET_PATH):
        print(f"Error: Golden dataset not found at '{DATASET_PATH}'")
        return

    print("--- Loading Golden Dataset ---")
    df = pd.read_csv(DATASET_PATH)
    df.dropna(inplace=True)

    print("--- Extracting Upgraded Features from URLs ---")
    feature_series = df['url'].progress_apply(get_url_features)
    features_df = pd.DataFrame(feature_series.tolist(), index=df.index)
    
    X = features_df
    y = df['label'].apply(lambda x: 1 if x == 'phishing' else 0)

    print(f"Feature extraction complete. Shape of feature matrix: {X.shape}")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"Data split: {len(X_train)} training samples, {len(X_test)} testing samples.")

    print("\n--- Training the Upgraded XGBoost Model (This may take several minutes) ---")
    # --- NEW v2: Tuned Hyperparameters for higher accuracy ---
    model = xgb.XGBClassifier(
        n_estimators=2000,          # More trees for more learning
        max_depth=8,                # Slightly deeper trees to capture more patterns
        learning_rate=0.01,         # A smaller learning rate for more careful learning
        subsample=0.7,              # Use 70% of data per tree to fight overfitting
        colsample_bytree=0.7,       # Use 70% of features per tree
        objective='binary:logistic',
        use_label_encoder=False,
        eval_metric='logloss',
        random_state=42,
        n_jobs=-1                   # Use all available CPU cores
    )
    
    # Using the simplified, compatible training command
    model.fit(X_train, y_train, verbose=False)
              
    print("--- Model Training Complete ---")

    print("\n--- Evaluating Upgraded Model Performance ---")
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Overall Accuracy: {accuracy:.4f}\n")
    print(classification_report(y_test, y_pred, target_names=['Benign', 'Phishing']))
    
    print(f"\n--- Saving the Upgraded Model to '{MODEL_SAVE_PATH}' ---")
    joblib.dump(model, MODEL_SAVE_PATH)
    print("Model v2 saved successfully. Ready for deployment!")

if __name__ == "__main__":
    train_model()
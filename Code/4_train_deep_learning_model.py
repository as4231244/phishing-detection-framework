# 4_train_deep_learning_model.py

import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

# TensorFlow / Keras for Deep Learning
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Conv1D, GlobalMaxPooling1D, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping

# ==============================================================================
# CONFIGURATION
# ==============================================================================
DATASET_PATH = "phishing_and_benign_websites.csv"
MAX_VOCAB_SIZE = 100    # Total number of unique characters to consider
MAX_LEN = 200           # The fixed length for all URL sequences
EMBEDDING_DIM = 64      # The size of the vector for each character

# ==============================================================================
# DATA PREPARATION FOR DEEP LEARNING
# ==============================================================================
print("--- Loading and Preparing Data for Deep Learning ---")
df = pd.read_csv(DATASET_PATH)
df.dropna(inplace=True)

urls = df['url'].values
y = df['label'].apply(lambda x: 1 if x == 'phishing' else 0).values

# 1. Tokenization: Convert URLs from strings of characters to sequences of integers
# We treat every character as a "word".
tokenizer = Tokenizer(num_words=MAX_VOCAB_SIZE, char_level=True, oov_token="<UNK>")
tokenizer.fit_on_texts(urls)

# Save the tokenizer - this is CRITICAL for making predictions later
joblib.dump(tokenizer, 'dl_tokenizer.joblib')
print("Tokenizer saved to 'dl_tokenizer.joblib'")

sequences = tokenizer.texts_to_sequences(urls)

# 2. Padding: Make all integer sequences the same length
X = pad_sequences(sequences, maxlen=MAX_LEN)

print(f"Data shape: {X.shape}")

# 3. Split the data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"Data split: {len(X_train)} training samples, {len(X_test)} testing samples.")

# ==============================================================================
# BUILDING THE DEEP LEARNING MODEL (CNN)
# ==============================================================================
print("\n--- Building the Deep Learning Model ---")

model = Sequential([
    # 1. Embedding Layer: Turns character integers into dense vectors of a fixed size.
    # It learns a meaningful representation for each character.
    Embedding(input_dim=MAX_VOCAB_SIZE, output_dim=EMBEDDING_DIM, input_length=MAX_LEN),
    
    # 2. Convolutional Layer: Acts as a pattern detector.
    # It slides a "window" across the URL to find suspicious character sequences.
    Conv1D(filters=128, kernel_size=5, activation='relu'),
    
    # 3. Pooling Layer: Takes the most important pattern found by the convolutional layer.
    GlobalMaxPooling1D(),
    
    # 4. Dense (Fully Connected) Layers: The decision-making part of the network.
    Dense(64, activation='relu'),
    
    # 5. Dropout Layer: A regularization technique to prevent overfitting.
    # It randomly "turns off" some neurons during training.
    Dropout(0.5),
    
    # 6. Output Layer: A single neuron with a sigmoid activation to output a
    # probability between 0 (benign) and 1 (phishing).
    Dense(1, activation='sigmoid')
])

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

model.summary()

# ==============================================================================
# TRAINING THE MODEL
# ==============================================================================
print("\n--- Training the Deep Learning Model (This will take some time) ---")

# Early stopping will halt training if the performance on the validation set stops improving.
early_stopping = EarlyStopping(monitor='val_accuracy', patience=3, restore_best_weights=True)

history = model.fit(
    X_train, y_train,
    epochs=10,  # Number of passes through the entire dataset
    batch_size=128, # Number of samples per gradient update
    validation_data=(X_test, y_test),
    callbacks=[early_stopping],
    verbose=1
)

# ==============================================================================
# EVALUATING AND SAVING THE FINAL MODEL
# ==============================================================================
print("\n--- Final Model Performance ---")
# Evaluate the model on the test data
loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f"Final Overall Accuracy: {accuracy:.4f}\n")

# Get detailed classification report
y_pred_prob = model.predict(X_test)
y_pred = (y_pred_prob > 0.5).astype(int)
print(classification_report(y_test, y_pred, target_names=['Benign', 'Phishing']))

MODEL_SAVE_PATH = "definitive_phishing_model_v4_deep_learning.h5"
print(f"\n--- Saving the Deep Learning Model to '{MODEL_SAVE_PATH}' ---")
model.save(MODEL_SAVE_PATH)
print("Deep Learning model v4 saved successfully!")
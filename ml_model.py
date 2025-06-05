import pickle
import re
import os
import numpy as np

model_path = os.path.join(os.path.dirname(__file__), "models", "email_model.pkl")
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model not found at: {model_path}")
model = pickle.load(open(model_path, "rb"))

def extract_features(email):
    generic_prefixes = ['info', 'support', 'contact', 'admin']
    prefix = email.split('@')[0].lower()
    is_generic = int(prefix in generic_prefixes)
    features = [
        int(bool(re.match(r"[a-z]+\.[a-z]+@", email))),
        len(email),
        email.count("."),
        is_generic
    ]
    return np.array(features).reshape(1, -1)

def predict_email_deliverability(email):
    if email == 'N/A' or '@' not in email:
        return 'unknown'
    X = extract_features(email)
    pred = model.predict(X)[0]
    return 'likely_valid' if pred == 1 else 'likely_invalid'

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import numpy as np
import pickle
import os

# Features: [has_dot_format, email_length, dot_count, is_generic_prefix]
X = np.array([
    [1, 20, 2, 0],   # john.doe@example.com → valid
    [0, 18, 1, 1],   # info@example.com → valid
    [0, 25, 1, 1],   # support@company.com → valid
    [0, 10, 0, 1],   # hi@x.com → invalid
    [1, 30, 3, 0],   # emily.smith@domain.com → valid
    [0, 12, 0, 1],   # contact@weird.io → invalid
    [1, 22, 2, 0],   # mike.b@safe.org → valid
    [0, 14, 1, 0]    # a@b.c → invalid
])

y = [1, 1, 1, 0, 1, 0, 1, 0]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
model = LogisticRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print("✅ Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

os.makedirs("models", exist_ok=True)
with open("models/email_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model saved to models/email_model.pkl")

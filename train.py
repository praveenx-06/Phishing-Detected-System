import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from extractor import extract_features

print("⏳ Loading real-world Kaggle dataset...")

# 1. Load the dataset
try:
    df_raw = pd.read_csv("malicious_phish.csv")
except FileNotFoundError:
    print("❌ Error: 'malicious_phish.csv' not found in your directory!")
    print("Please make sure you downloaded it from Kaggle and placed it here.")
    exit()

# 2. Filter for only 'benign' and 'phishing' rows
df_filtered = df_raw[df_raw['type'].isin(['benign', 'phishing'])].copy()

# 3. Map categories to binary numbers: benign -> 0, phishing -> 1
df_filtered['label'] = df_filtered['type'].map({'benign': 0, 'phishing': 1})

# 4. Sample 10,000 rows so it trains fast on your computer
df_sampled = df_filtered.sample(n=10000, random_state=42).reset_index(drop=True)

print(f"⚙️ Extracting structural features from {len(df_sampled)} URLs...")

# 5. Loop through and extract features
processed_data = []
for index, row in df_sampled.iterrows():
    try:
        # Get features from our extractor.py script
        features = extract_features(row['url'])
        features['label'] = row['label']
        processed_data.append(features)
    except Exception as e:
        continue

df_features = pd.DataFrame(processed_data)

# 6. Split data into Features (X) and Target Label (y)
X = df_features.drop(columns=['label'])
y = df_features['label']

# Split into Training (80%) and Testing (20%) sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("🧠 Training the Random Forest Classifier on real-world patterns...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 7. Evaluate performance
y_pred = model.predict(X_test)
print("\n📊 --- MODEL PERFORMANCE METRICS ---")
print(f"Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# 8. Save the newly upgraded model
joblib.dump(model, 'phishing_model.pkl')
print("\n✅ Success! Upgraded 'phishing_model.pkl' saved to your project directory.")
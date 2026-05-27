# 🛡️ Intelligent Phishing URL Detection System

A machine learning-powered cybersecurity solution designed to analyze, detect, and classify malicious phishing URLs. By extracting high-signal structural, lexical, and behavioral features from raw URLs, this system trains a Random Forest Classifier to identify social engineering traps and brand impersonation attempts. The system exposes a dynamic, three-tier risk evaluation dashboard via Streamlit to prevent security blind spots.

---

## 🚀 Key Features

* **Advanced Feature Engineering:** Extracts 12 specific structural parameters from raw URL strings without requiring external network lookups, keeping analysis fast and lightweight.
* **Combosquatting & Brand Protection:** Actively maps variations of highly targeted brands (Google, PayPal, Microsoft, Apple, Amazon, Netflix) to detect spoofed domains.
* **3-Tier Risk Mitigation Matrix:** Replaces simple binary safe/malicious guessing with an enterprise risk filter:
  * 🟢 **Verified Safe:** Highly confident clean domain (>85% safety score).
  * ⚠️ **Suspicious Warning:** Catch-all for ambiguous, low-confidence "gray area" links (<85% safety score).
  * 🚨 **Malicious Threat:** Confirmed phishing indicators identified.
* **Real-Time Telemetry Breakdown:** Displays an expandable JSON interface showing exactly which mathematical vectors triggered the security flags.

---

## 📁 Project Architecture

```text
phishing-detection-system/
│
├── app.py                 # Streamlit UI Dashboard & Threat Analysis Logic
├── train.py               # Machine Learning Model Training & Evaluation Pipeline
├── extractor.py           # Cybersecurity Feature Engineering Matrix
├── .gitignore             # Safety filters protecting repo from dataset/cache bloat
└── README.md              # Comprehensive Project Documentation


⚙️ Core Telemetry Matrix (12 Extracted Features)
The system passes the following mathematical features into the Random Forest model for threat evaluation:

1.url_length: Total length of the URL string (Phishing paths are often abnormally long).

2.dot_count: Number of periods in the hostname (detects excessive subdomains).

3.has_at_symbol: Binary flag checking for @ (used to mask malicious routing).

4.hyphen_count: Number of dashes (frequently used to mimic official brand names).

5.is_ip_address: Identifies if the host skips domain names entirely for raw IP addresses.

6.digit_count: Counts total numbers used to confuse legacy pattern-matching filters.

7.suspicious_word_count: Scans for high-frequency social engineering triggers (login, secure, verify).

8.double_slash_path: Detects intermediate internal path redirections (//).

9.hostname_length: Isolates the explicit length of the web server address.

10.path_length: Isolates the explicit length of the deep link directory path.

11.is_shortened: Flags obfuscation through link shorteners (bit.ly, tinyurl.com).

12.brand_impersonation: Evaluates if a key brand name is present while pointing to an unofficial domain.

🚀 Detailed Installation & Local Usage Guide
Follow these step-by-step instructions to clone, configure, and execute the project locally on a Windows machine.

1. Environment Setup
Open your terminal or Command Prompt inside your project workspace and run:

Bash
# Clone the repository (Replace with your actual GitHub username)
git clone [https://github.com/YOUR_USERNAME/phishing-url-detection-system.git](https://github.com/YOUR_USERNAME/phishing-url-detection-system.git)
cd phishing-url-detection-system

# Create a clean isolated virtual environment
python -m venv venv

# Activate the virtual environment
venv\Scripts\activate
2. Install Project Requirements
Install the required data science and security UI packages directly using pip:

Bash
pip install pandas numpy scikit-learn streamlit joblib
3. Model Training & Synchronization
Before running the web app, you must calibrate the system against your Kaggle dataset. Ensure malicious_phish.csv is placed in the root directory, then run:

Bash
python train.py
4. Deploy the Local Dashboard
Launch the live interactive system inside your web browser:

Bash
streamlit run app.py
📊 Model Performance Evaluation
When running the training pipeline (train.py), the model performance metrics are evaluated using an 80/20 train-test split pattern. The system measures Precision (minimizing false alerts) and Recall (ensuring no threats slip through undetected).
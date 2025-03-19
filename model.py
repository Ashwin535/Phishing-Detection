import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import os
from urllib.parse import urlparse

# Sample function to extract basic URL features
def extract_url_features(url):
    # Extract URL components
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    path = parsed_url.path
    query = parsed_url.query

    # Feature 1: URL length
    url_length = len(url)

    # Feature 2: Number of subdomains (e.g., "mail.google.com" has 2 subdomains)
    num_subdomains = domain.count('.') - 1

    # Feature 3: Presence of '@' in URL (phishing often uses this)
    at_sign = 1 if '@' in url else 0

    # Feature 4: Query length (long queries might indicate phishing)
    query_length = len(query)

    # Combine the features
    features = [url_length, num_subdomains, at_sign, query_length]

    return features

# Sample dataset for training (you can replace with a real phishing dataset)
data = {
    "url": [
        "http://www.google.com",
        "http://www.phishing.com",
        "https://secure.bank.com",
        "http://www.paypal.com",
        "http://malicious-website.xyz",
    ],
    "label": [0, 1, 0, 0, 1]  # 0 = Legitimate, 1 = Phishing
}

# Create DataFrame
df = pd.DataFrame(data)

# Extract features for each URL
X = np.array([extract_url_features(url) for url in df["url"]])
y = df["label"].values

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize a classifier (Random Forest)
model = RandomForestClassifier()

# Train the model
model.fit(X_train, y_train)

# Test the model
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))

# Function to detect phishing URLs
def is_phishing(url):
    features = extract_url_features(url)
    prediction = model.predict([features])
    return "Phishing" if prediction[0] == 1 else "Legitimate"

# Function to block phishing websites by modifying the system's hosts file (Windows version)
def block_phishing_site(url):
    print(f"Blocking phishing website: {url}")
    hosts_file = r"C:\\Windows\\System32\\drivers\\etc\\hosts"  # Windows hosts file location
    try:
        with open(hosts_file, "a") as f:
            f.write(f"\n127.0.0.1 {url}\n")  # Redirect phishing site to local machine (localhost)
        print(f"Successfully blocked {url} by modifying the hosts file.")
    except PermissionError:
        print(f"Permission denied. You might need to run the script as an administrator to modify {hosts_file}.")

# Example of URL detection and blocking
test_url = "http://malicious-website.xyz"
result = is_phishing(test_url)
print(f"The website {test_url} is {result}.")

# Block the phishing site if detected
if result == "Phishing":
    block_phishing_site(test_url)
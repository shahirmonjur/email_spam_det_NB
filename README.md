Project Overview
![image](https://github.com/user-attachments/assets/4acf7516-9517-4231-83f9-0f4a171b4576)


This project implements an intelligent email spam detection system that:

# Classifies emails as spam or ham using a Multinomial Naive Bayes classifier
# Provides real-time classification through Gmail API integration
# Offers a secure web interface with Google OAuth authentication
# Includes both automated inbox scanning and manual email checking capabilities

The system achieved 99% accuracy in testing and cross-validation, demonstrating robust performance in real-world email classification scenarios.
Key Features

🔒 Secure Authentication

1. Google OAuth 2.0 implementation
2. No credential storage required

📧 Real-time Processing

1. Live Gmail inbox scanning
2. Instant classification results
3. Manual email text input option

📊 High Performance

# 99% accuracy in testing
# Comprehensive metrics (Precision, Recall, F1-Score)
# 5-fold cross-validation tested

🖥️ User-Friendly Interface

Clean dashboard displaying classified emails
Responsive web design
Intuitive manual testing interface

Technical Implementation
Machine Learning Pipeline

*Algorithm: Multinomial Naive Bayes

*Feature Extraction: CountVectorizer

*Dataset: 5,572 labeled emails (13% spam)

*Preprocessing: Deduplication, null removal, text vectorization

Web Application Stack

Backend: Flask
Frontend: HTML5, CSS3, JavaScript
Templating: Jinja2
Authentication: Flask-Dance (OAuth 2.0)
API Integration: Gmail API

Core Libraries

- scikit-learn (ML model)
- pandas (data processing)
- joblib (model persistence)
- Google API Client (Gmail integration)

Performance Metrics
Metric	Score
Accuracy	99%
Precision	0.98
Recall	0.99
F1 Score	0.985


# Installation Guide
Prerequisites

Python 3.8+

Google Developer Account (for API credentials)

pip package manager

Setup Instructions

Clone the repository:
bash

    git clone https://github.com/yourusername/email-spam-detection.git
    cd email-spam-detection

Create and activate a virtual environment:
bash

    python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies:
bash

    pip install -r requirements.txt

Set up Google OAuth credentials:

Create a project in Google Cloud Console

Enable Gmail API

Create OAuth 2.0 credentials

Download credentials as client_secret.json in project root


Run the application:
bash

    python app.py

Usage Instructions

Access the web interface at http://localhost:5000
Click "Login with Google" to authenticate
View your classified emails in the dashboard
Use the manual input form to test custom email text
Click "See More" to fetch additional emails

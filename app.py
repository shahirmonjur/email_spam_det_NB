from flask import Flask, render_template, redirect, url_for, session, request, jsonify
from flask_dance.contrib.google import make_google_blueprint, google
import os
import joblib
import json
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from base64 import urlsafe_b64decode

app = Flask(__name__)
app.secret_key = "REPLACE_WITH_YOUR_SECRET_KEY_IN_PRODUCTION"
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False

model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

with open("client_secret.json") as f:
    client_secrets = json.load(f)["web"]
	GOOGLE_CLIENT_ID = "your-google-client-id"
	GOOGLE_CLIENT_SECRET = "your-google-client-secret"


os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

google_bp = make_google_blueprint(
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    redirect_to="dashboard",
    scope=[
        "https://www.googleapis.com/auth/gmail.readonly",
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",  # Fix typo here (.profile)
        "openid"
    ],
    offline=True,  # Add this if you need refresh tokens
    reprompt_consent=True  # Helps if you change scopes
)
app.register_blueprint(google_bp, url_prefix="/login")


def get_gmail_service():
    if not google.authorized:
        return None
    token = google.token
    credentials = Credentials(
        token=token["access_token"],
        refresh_token=token.get("refresh_token"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET
    )
    if credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
    return build("gmail", "v1", credentials=credentials)


def fetch_emails(service, start=0, count=10):
    results = service.users().messages().list(
        userId="me", labelIds=["INBOX"], maxResults=start + count
    ).execute()
    messages = results.get("messages", [])[start:start+count]
    emails = []

    for message in messages:
        msg = service.users().messages().get(userId="me", id=message["id"]).execute()
        subject = ""
        body = ""
        for header in msg["payload"].get("headers", []):
            if header["name"] == "Subject":
                subject = header["value"]
                break
        payload = msg["payload"]
        data = ""
        parts = payload.get("parts", [])
        if not parts and 'body' in payload:
            data = payload["body"].get("data", "")
        else:
            for part in parts:
                if part["mimeType"] == "text/plain":
                    data = part["body"].get("data", "")
                    break
                elif part["mimeType"] == "text/html":
                    data = part["body"].get("data", "")
        if data:
            try:
                body = urlsafe_b64decode(data.encode("UTF-8")).decode("UTF-8", errors="ignore")
            except:
                body = "(Unable to decode)"
        content = subject + " " + body
        label = model.predict(vectorizer.transform([content]))[0]
        emails.append({
            "subject": subject,
            "body": body,
            "label": "SPAM" if label == 1 else "HAM"
        })
    return emails


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    if not resp.ok:
        return "Failed to get user info"
    user_info = resp.json()
    session["user"] = {
        "name": user_info["name"],
        "email": user_info["email"],
        "picture": user_info["picture"]
    }
    service = get_gmail_service()
    emails = fetch_emails(service, start=0, count=10)
    return render_template("dashboard.html", emails=emails, user=session["user"])


@app.route("/load_more", methods=["POST"])
def load_more():
    start = int(request.form.get("start", 0))
    service = get_gmail_service()
    emails = fetch_emails(service, start=start, count=10)
    return jsonify(emails)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allow frontend to connect

# Mock database
users = {
    "123456789012": {"name": "Shristi kumari", "services": {"electricity": "Paid", "water": "Pending", "waste": "Scheduled"}}
}

service_requests = []

translations = {
    "en": {"welcome": "Welcome to SUVIDHA"},
    "hi": {"welcome": "SUVIDHA में आपका स्वागत है"},
    "bn": {"welcome": "SUVIDHA এ আপনাকে স্বাগতম"}
}

@app.route("/")
def home():
    return jsonify({"message": "Welcome to SUVIDHA Civic Service API"})

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    aadhaar = data.get("aadhaar")
    otp = data.get("otp")
    if aadhaar in users and otp == "1234":
        return jsonify({"status": "success", "user": users[aadhaar]})
    return jsonify({"status": "failed", "message": "Invalid Aadhaar or OTP"}), 401

@app.route("/services/<aadhaar>", methods=["GET"])
def get_services(aadhaar):
    if aadhaar in users:
        return jsonify(users[aadhaar]["services"])
    return jsonify({"error": "User not found"}), 404

@app.route("/request", methods=["POST"])
def create_request():
    data = request.json
    aadhaar = data.get("aadhaar")
    department = data.get("department")
    issue = data.get("issue")

    if aadhaar not in users:
        return jsonify({"error": "User not found"}), 404

    request_id = len(service_requests) + 1
    new_request = {
        "id": request_id,
        "aadhaar": aadhaar,
        "department": department,
        "issue": issue,
        "status": "Pending"
    }
    service_requests.append(new_request)
    return jsonify({"message": "Request created", "request": new_request})

@app.route("/all-requests", methods=["GET"])
def get_all_requests():
    return jsonify({
        "total_requests": len(service_requests),
        "all_complaints": service_requests
    })

@app.route("/translate/<lang>", methods=["GET"])
def translate(lang):
    if lang in translations:
        return jsonify(translations[lang])
    return jsonify({"error": "Language not supported"}), 404

if __name__ == '__main__':
    app.run(debug=True)
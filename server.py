from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__)

@app.route("/")
def index():
    return send_from_directory("", "lead_form.html")

@app.route("/submit", methods=["POST"])
def submit():
    try:
        data = request.form.to_dict()

        if not data:
            return jsonify({"success": False, "error": "Нет данных"}), 400

        # IP пользователя
        forwarded = request.headers.get("X-Forwarded-For", "")
        ip = forwarded.split(",")[0] if forwarded else request.remote_addr

        payload = {
            "token": "55604c61-4716-423a-9021-f86815941190",
            "firstname": data.get("firstname", ""),
            "lastname": data.get("lastname", ""),
            "email": data.get("email", ""),
            "phone": data.get("phone", ""),
            "country": data.get("country", "RU"),  # РФ
            "language": "ru",
            "funnel": "p2p_purple",  # можешь назвать как хочешь
            "comment": data.get("comment", "")
        }

        CRM_URL = "https://crm-globalcrypto.com/api/v1/lead"

        response = requests.post(
            CRM_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=20
        )

        return jsonify({
            "success": True,
            "crm_status": response.status_code,
            "crm_response": response.text,
            "sent_payload": payload
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
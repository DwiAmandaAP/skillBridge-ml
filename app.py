import time
import logging
from functools import wraps
from flask import Flask, request, jsonify
from config import Config
from services.matcher import extract_skills_from_text
from services.taxonomy import taxonomy

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
START_TIME = time.time()


def require_service_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        expected = f"Bearer {Config.SERVICE_TOKEN}"

        if not Config.SERVICE_TOKEN or auth_header != expected:
            return jsonify({
                "status": 401,
                "message": "Service token tidak valid",
                "data": None,
            }), 401

        return f(*args, **kwargs)

    return decorated


@app.route("/health", methods=["GET"])
def health():
    uptime = int(time.time() - START_TIME)
    return jsonify({
        "status": 200,
        "message": "Service healthy",
        "data": {"uptime_seconds": uptime},
    }), 200


@app.route("/extract-skills", methods=["POST"])
@require_service_token
def extract_skills():
    payload = request.get_json(silent=True)

    if not payload or "jobs" not in payload:
        return jsonify({
            "status": 422,
            "message": "Payload tidak valid, field 'jobs' wajib ada",
            "data": None,
        }), 422

    jobs = payload["jobs"]
    results = []

    for job in jobs:
        job_posting_id = job.get("job_posting_id")
        text = job.get("text", "")

        # title dipisahkan dari text untuk fallback matching -- karena
        # description sintetis BE biasanya diawali title, kita ambil
        # bagian sebelum tanda titik pertama sebagai perkiraan title.
        title_guess = text.split(".")[0] if text else ""

        matched_skills = extract_skills_from_text(text, title_guess)

        results.append({
            "job_posting_id": job_posting_id,
            "matched_skills": matched_skills,
        })

    return jsonify({
        "status": 200,
        "message": "OK",
        "data": {"results": results},
    }), 200


if __name__ == "__main__":
    # Fetch taxonomy sekali di awal supaya request pertama tidak lambat.
    taxonomy.refresh_if_stale()
    app.run(host="0.0.0.0", port=Config.PORT, debug=True)
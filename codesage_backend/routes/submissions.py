from flask import Blueprint, request, jsonify
from services.judge0_service import run_code

submissions_bp = Blueprint("submissions", __name__)

@submissions_bp.route("/", methods=["POST"])
def submit_code():
    data = request.get_json()
    code = data.get("code", "")
    language = data.get("language", "python")

    if not code:
        return jsonify({"error": "No code provided"}), 400

    # Run code via Judge0
    result = run_code(code, language)
    return jsonify(result)

from flask import Blueprint, request, jsonify
import requests
import random
from database import db_helpers as dbh

problems_bp = Blueprint("problems", __name__)

@problems_bp.route("/", methods=["GET"])
def get_problems():
    """
    Returns 1 random Codeforces problem around the candidate's rating.
    Candidate rating can be passed as a query param: ?rating=1500
    """
    # Get rating from query parameter, default 1500
    try:
        candidate_rating = int(request.args.get("rating", 1500))
    except ValueError:
        candidate_rating = 1500

    # 1️⃣ Check DB first
    problems_in_db = dbh.get_problems_by_rating(candidate_rating - 200, candidate_rating + 200)

    if problems_in_db:
        selected_problem = random.choice(problems_in_db)
    else:
        # 2️⃣ Fetch problems from Codeforces API
        try:
            resp = requests.get("https://codeforces.com/api/problemset.problems")
            resp.raise_for_status()
            all_problems = resp.json()["result"]["problems"]
        except Exception as e:
            return jsonify({"error": "Failed to fetch problems from Codeforces", "details": str(e)}), 500

        # Filter problems with a rating near candidate_rating
        filtered = [p for p in all_problems if p.get("rating") and abs(p["rating"] - candidate_rating) <= 200]

        if not filtered:
            return jsonify({"error": "No problems found near the given rating"}), 404

        selected_problem = random.choice(filtered)

        # 3️⃣ Insert into DB
        dbh.insert_problem(
            contest_id=selected_problem["contestId"],
            problem_index=selected_problem["index"],
            name=selected_problem["name"],
            rating=selected_problem["rating"],
            tags=",".join(selected_problem.get("tags", []))
        )

    # 4️⃣ Return only relevant fields to frontend
    result = {
        "contest_id": selected_problem.get("contestId") or selected_problem.get("contest_id"),
        "problem_index": selected_problem.get("problem_index") or selected_problem.get("index"),
        "name": selected_problem.get("name"),
        "rating": selected_problem.get("rating"),
        "tags": selected_problem.get("tags")
    }

    return jsonify(result)

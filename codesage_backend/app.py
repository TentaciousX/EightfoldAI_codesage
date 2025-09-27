from flask import Flask
from flask_cors import CORS
from database.db import init_db

# Import blueprints
from routes.problems import problems_bp
from routes.submissions import submissions_bp
from routes.llm import llm_bp

def create_app():
    app = Flask(__name__)
    CORS(app)  # allow frontend to access API
    init_db()

    # Register blueprints
    app.register_blueprint(problems_bp, url_prefix="/api/v1/problems")
    app.register_blueprint(submissions_bp, url_prefix="/api/v1/submissions")
    app.register_blueprint(llm_bp, url_prefix="/api/v1/llm")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)

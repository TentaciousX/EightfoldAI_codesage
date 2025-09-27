import requests
import time

# Judge0 endpoint
JUDGE0_URL = "https://ce.judge0.com/submissions/?base64_encoded=false&wait=true"

def run_code(code, language):
    """
    code: string of candidate code
    language: 'python', 'cpp', 'java', etc.
    """
    # Map language to Judge0 language IDs (simplified)
    language_map = {
        "python": 71,  # Python 3
        "cpp": 54,     # C++17
        "java": 62     # Java 17
    }

    payload = {
        "source_code": code,
        "language_id": language_map.get(language.lower(), 71),  # default Python 3
        "stdin": ""
    }

    try:
        response = requests.post(JUDGE0_URL, json=payload)
        if response.status_code == 201 or response.status_code == 200:
            result = response.json()
            return {
                "stdout": result.get("stdout"),
                "stderr": result.get("stderr"),
                "time": result.get("time"),
                "memory": result.get("memory"),
                "status": result.get("status", {}).get("description")
            }
        else:
            return {"error": "Failed to execute code", "details": response.text}
    except Exception as e:
        return {"error": str(e)}

import os
import requests

# API_URL = os.getenv("API_URL", "http://127.0.0.1:5000")
API_URL = os.getenv("API_URL", "http://127.0.0.1:5000")


def get_history():
    try:
        response = requests.get(f"{API_URL}/history", timeout=10)
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []


def upload_file(file, username):
    try:
        files = {
            "file": (file.name, file.getvalue())
        }

        data = {
            "user": username
        }

        response = requests.post(
            f"{API_URL}/upload",
            files=files,
            data=data,
            timeout=30
        )

        if response.status_code == 200:
            return response.json()

        return {"error": "Upload failed"}

    except Exception as e:
        return {"error": str(e)}
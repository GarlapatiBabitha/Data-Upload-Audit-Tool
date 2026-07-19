import requests

BASE_URL = "http://localhost:5000"

def upload_file(file, user):
    files = {"file": file}
    data = {"user": user}
    return requests.post(f"{BASE_URL}/upload", files=files, data=data).json()

def get_history():
    return requests.get(f"{BASE_URL}/history").json()
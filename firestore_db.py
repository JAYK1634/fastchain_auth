import requests
import os

PROJECT_ID = "fastfoodchain-8a5cb" 

def save_user_profile(uid, name, email, id_token):
    url = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents/users/{uid}"  # Fixed
    headers = {"Authorization": f"Bearer {id_token}"}
    data = {
        "fields": {
            "name": {"stringValue": name},
            "email": {"stringValue": email}
        }
    }
    return requests.patch(url, json=data, headers=headers).json()

def get_user_profile(uid, id_token):
    url = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents/users/{uid}"  # Fixed
    headers = {"Authorization": f"Bearer {id_token}"}
    return requests.get(url, headers=headers).json()

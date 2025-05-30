import requests

def save_user_profile(uid, name, email, token, branch, semester):
    url = f"https://firestore.googleapis.com/v1/projects/login3-3d1f0/databases/(default)/documents/students/{uid}"
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "fields": {
            "name": {"stringValue": name},
            "email": {"stringValue": email},
            "branch": {"stringValue": branch},
            "semester": {"stringValue": semester}
        }
    }
    response = requests.patch(url, headers=headers, json=data)
    return response.json()


def get_user_profile(uid, token):
    url = f"https://firestore.googleapis.com/v1/projects/login3-3d1f0/databases/(default)/documents/students/{uid}"
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(url, headers=headers)
    return res.json()

import os
import requests
from dotenv import load_dotenv
load_dotenv()
# API_URL = "https://api2.frontapp.com"
# API_KEY = os.getenv("API_KEY") 
# HEADERS = {
#     "Authorization": f"Bearer {API_KEY}"
# }
OAUTH_URL = "https://api2.frontapp.com/auth/token"
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

def check_api_key():
    url = "https://api2.frontapp.com/me"
    headers = {
        "Authorization": f"Bearer {os.getenv('API_KEY')}"
    }
    response = requests.get(url, headers=headers)

    print("Status code:", response.status_code)
    print("Response:")
    print(response.text)



def get_oauth_token():
    response = requests.post(OAUTH_URL, data={
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    })
    
    if response.status_code == 200:
        token = response.json()['access_token']
        return token
    else:
        print("Error getting token:", response.status_code, response.text)
        return None



def get_all_template_folders():
    url = "https://api2.frontapp.com/message_template_folders"
    headers = {
        "Authorization": f"Bearer {os.getenv('API_KEY')}"
    }
    response = requests.get(url, headers=headers)
    return response.json().get("results", [])

def get_all_templates():
    url = f"{API_URL}/message_templates"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        return []

    return response.json().get("results", [])

def main():
    
    folders=get_all_template_folders()
    templates = get_all_templates()
    print("Folders found:", folders)
    print(f"Found {len(templates)} templates.")
    for t in templates:
        print(f"- [{t['id']}] {t['name']}")
        print(f"  Subject: {t.get('subject', '')}")
        print(f"  Body: {t.get('body', '')[:80]}...")  # Solo primera parte del cuerpo
        print()

def get_teams():
    url = f"{API_URL}/teams"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        print("Error al obtener equipos:", response.status_code, response.text)
        return []
    
def get_templates_by_team(team_id):
    url = f"{API_URL}/teams/{team_id}/message_templates"
    response = requests.get(url, headers=HEADERS)
    return response.json().get("results", [])


def get_folders_by_team(team_id):
    url = f"{API_URL}/teams/{team_id}/message_template_folders"
    response = requests.get(url, headers=HEADERS)
    return response.json().get("results", [])

def mama():
    teams = get_teams()
    print(f"Equipos encontrados: {len(teams)}")
    for team in teams:
        print(f" Equipo: {team['name']} ({team['id']})")

        folders = get_folders_by_team(team["id"])
        print(f"   Carpetas: {len(folders)}")
        for folder in folders:
            print(f"    - {folder['name']} ({folder['id']})")

        templates = get_templates_by_team(team["id"])
        print(f"   Plantillas: {len(templates)}")
        for t in templates:
            print(f"    - {t['name']} | Subject: {t.get('subject', '')}")

def get_me():
    url = f"{API_URL}/me"
    response = requests.get(url, headers=HEADERS)
    print(" endpoint /me: ",response.json())

if __name__ == "__main__":
    # check_api_key()
    # get_me()
    # main()
    print(CLIENT_ID)
    print(CLIENT_SECRET)
    access_token = get_oauth_token()
    if access_token:
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = requests.get("https://api2.frontapp.com/message_templates", headers=headers)
        print(response.status_code)
        print(response.text)
        #mama()

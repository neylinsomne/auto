import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://familify.api.frontapp.com"
STATIC_API_KEY = os.getenv("API_KEY")  

# === Headers ===
def get_headers():
    return {
        "Authorization": STATIC_API_KEY,  
        "Accept": "application/json"
    }

# === API Calls ===
def get_me(headers):
    url = f"{API_URL}/me"
    response = requests.get(url, headers=headers)
    print("\n🧑 Respuesta de /me:")
    print(response.status_code, response.json())


def get_ans(headers):
    url = f"{API_URL}/answers"
    response = requests.get(url, headers=headers)
    print("\n📚 Respuesta de /answers:")
    print(response.status_code, response.json())


def get_all_template_folders(headers):
    url = f"{API_URL}/message_template_folders"
    response = requests.get(url, headers=headers)
    return response.json().get("results", [])


def get_all_templates(headers):
    templates = []
    url = f"{API_URL}/message_templates?limit=100"

    while url:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"❌ Error: {response.status_code} - {response.text}")
            break
        
        data = response.json()
        page_templates = data.get("results", [])
        templates.extend(page_templates)

        # Obtener el siguiente link de paginación
        pagination = data.get("_pagination", {})
        url = pagination.get("next")  # Si es None, termina

    return templates


def get_templates_in_folders(headers):
    print("\n📂 Buscando plantillas dentro de carpetas...")
    folders = get_all_template_folders(headers)
    all_templates = []

    for folder in folders:
        folder_id = folder["id"]
        folder_name = folder.get("name", "Sin nombre")
        print(f"\n- Carpeta: {folder_name} ({folder_id})")

        url = f"{API_URL}/message_template_folders/{folder_id}/message_templates"
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            templates = r.json().get("results", [])
            print(f"  ✉️ Plantillas encontradas: {len(templates)}")
            for t in templates:
                print(f"   - {t['name']} | Subject: {t.get('subject', '')}")
            all_templates.extend(templates)
        else:
            print(f"  ⚠️ Error al obtener templates: {r.status_code} {r.text}")
    return all_templates


def get_teams(headers):
    url = f"{API_URL}/teams"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error al obtener teams: {response.status_code} - {response.text}")
        return []
    return response.json().get("results", [])

def get_team_templates(team_id, headers):
    url = f"{API_URL}/teams/{team_id}/message_templates?limit=100"
    templates = []
    while url:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Error al obtener plantillas del team {team_id}: {response.status_code} - {response.text}")
            break
        data = response.json()
        templates += data.get("results", [])
        url = data.get("_pagination", {}).get("next")
    return templates

def get_all_shared_templates(headers):
    teams = get_teams(headers)
    all_templates = []
    for team in teams:
        print(f"🔍 Revisando plantillas del equipo: {team['name']} ({team['id']})")
        team_templates = get_team_templates(team['id'], headers)
        print(f"  ✉️ Plantillas encontradas: {len(team_templates)}")
        all_templates.extend(team_templates)
    return all_templates





def ver_plantillas_personales(headers):
    print("\n🙋 TEMPLATES PERSONALES:")
    folders = get_all_template_folders(headers)
    templates = get_all_templates(headers)
    print(f"Carpetas personales: {len(folders)}")
    print(f"Plantillas personales: {len(templates)}")
    for t in templates:
        print(f"- {t['name']} (ID: {t['id']})")
        print(f"  Subject: {t.get('subject', '')}")
        print(f"  Body: {t.get('body', '')[:60]}...")
        print()


# === MAIN ===
if __name__ == "__main__":
    headers = get_headers()

    print("\n🔐 Probando autenticación...")
    get_me(headers)


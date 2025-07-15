import os
import requests
from dotenv import load_dotenv
import pandas as pd
from utils.upa import limpiar_html

load_dotenv()
BASE_URL="https://api2.frontapp.com"
API_URL = "https://familify.api.frontapp.com"
STATIC_API_KEY = os.getenv("API_KEY")
TEAM_ID = "tim_4mhec"

def get_headers_place():
    return{
    "Authorization": STATIC_API_KEY,
    "accept": "application/json",
    "content-type": "application/json"
    } 


# url = "https://api2.frontapp.com/tags"

# payload = { "is_visible_in_conversation_lists": False }
# headers = {
#     "accept": "application/json",
#     "content-type": "application/json"
# }

# response = requests.post(url, json=payload, headers=headers)



#ADD TAG:
def add_tag_revisar(id_message):
    url = f"/conversations/{id_message}/tags"
    payload = { "tag_ids": ["Necesita_Revision"] }
    headers = get_headers_place()
    response = requests.post(url, json=payload, headers=headers)
    print(response.text)



def obtener_conversaciones_con_tag_revision(limit=50) -> list:
    """
    Retorna las conversaciones que tienen el tag 'Necesita_Revision'.
    """
    # Asegúrate de que esta sea la ID del tag, no solo el nombre
    tag_id = "Necesita_Revision"  # Cambia por el ID real si es diferente
    url = f"{BASE_URL}/conversations?q=tag:{tag_id}&limit={limit}"
    headers = get_headers_place()
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json().get("_results", [])
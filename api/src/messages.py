
import requests
from sentence_transformers import SentenceTransformer, util
import os
from dotenv import load_dotenv

load_dotenv()
API_URL = "https://api2.frontapp.com"
API_KEY = os.getenv("API_KEY") 
HEADERS = {
    'Authorization': API_KEY,
    'Accept': 'application/json'
}

BASE_URL = 'https://api2.frontapp.com'


# === 1. OBTENER MENSAJES RECIENTES ===
def obtener_mensajes(limit=5):
    url = f'{BASE_URL}/inboxes?limit={limit}'  # Obtiene últimas conversaciones
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    conversaciones = response.json().get('_conversations', [])

    mensajes_json = []
    for conv in conversaciones:
        conv_id = conv['id']

        # Traemos los mensajes de cada conversación
        mensajes_url = f"{BASE_URL}/conversations/{conv_id}/messages"
        mensajes_resp = requests.get(mensajes_url, headers=HEADERS)
        mensajes_resp.raise_for_status()
        mensajes = mensajes_resp.json().get('_results', [])

        for m in mensajes:
            cuerpo = m.get("body", "")
            etiquetas = m.get("metadata", {}).get("tags", [])
            mensajes_json.append({
                "mensaje": cuerpo,
                "etiquetas": etiquetas
            })
    return mensajes_json


if __name__ == "__main__":
    
    resultados = obtener_mensajes()
    for i, r in enumerate(resultados):
        print(f"\n--- Mensaje {i+1} ---")
        print("Texto:", r["mensaje"])
        print("Etiquetas:", r["etiquetas"])

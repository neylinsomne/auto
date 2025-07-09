
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import pandas as pd 
from difflib import SequenceMatcher

load_dotenv()
API_KEY = os.getenv("API_KEY") 
HEADERS = {
    'Authorization': API_KEY,
    'Accept': 'application/json'
}

BASE_URL = 'https://api2.frontapp.com'

def obtener_conversaciones_inbox(limit=10,id="inb_bhllg"):
    url = f'{BASE_URL}/inboxes/{id}/conversations?limit={limit}'
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()

    conversaciones = response.json().get('_results', [])
    conversaciones_completas = []

    for conv in conversaciones:
        conv_id = conv['id']
        subject = conv.get('subject')
        tags = [tag.get('name') for tag in conv.get('tags', [])]
        recipient = conv.get('recipient', {}).get('handle', '')

        # Traemos los mensajes de esta conversación
        mensajes_url = f"{BASE_URL}/conversations/{conv_id}/messages"
        mensajes_resp = requests.get(mensajes_url, headers=HEADERS)
        mensajes_resp.raise_for_status()
        mensajes = mensajes_resp.json().get('_results', [])

        # Guardamos todos los mensajes asociados
        mensajes_lista = []
        for m in mensajes:
            cuerpo = m.get("body", "")
            mensajes_lista.append(cuerpo.strip() or "[Mensaje vacío]")

        # Guardamos toda la conversación como un dict
        conversaciones_completas.append({
            "conversacion_id": conv_id,
            "subject": subject,
            "recipient": recipient,
            "tags_conversacion": tags,
            "mensajes": mensajes_lista,
        })

    return conversaciones_completas


def obtener_mensajes_nuestros(mensajes: list) -> list:
    """
    Retorna los mensajes enviados por nuestro equipo (is_inbound == False).
    """
    return [m for m in mensajes if not m.get("is_inbound")]


def ya_respondimos(mensajes: list) -> bool:
    """
    Retorna True si ya existe al menos una respuesta nuestra (is_inbound == False).
    """
    return any(not m.get("is_inbound") for m in mensajes)


def obtener_ultimo_mensaje_usuario(mensajes: list) -> dict:
    """
    Retorna el último mensaje enviado por el usuario (is_inbound=True).
    Si no hay mensajes entrantes, retorna None.
    """
    mensajes_usuario = [msg for msg in mensajes if msg.get("is_inbound")]
    if not mensajes_usuario:
        return None

    # Ordenar por fecha de creación (más reciente al final)
    mensajes_usuario.sort(key=lambda x: x.get("created_at", 0), reverse=False)
    
    # Retornar el más reciente
    return mensajes_usuario[-1]


def mensaje_similar_a_template(mensaje: str, df_templates: pd.DataFrame, umbral: float = 0.9) -> str | None:
    """
    Compara el mensaje con cada template en el DataFrame.
    Devuelve el template más similar si supera el umbral.
    """
    mensaje = mensaje.strip().lower()
    for template in df_templates["texto"]:
        ratio = SequenceMatcher(None, mensaje, template.lower()).ratio()
        if ratio >= umbral:
            return template
    return None


def obtener_conversaciones(limit=10):
    url = f'{BASE_URL}/conversations?limit={limit}'
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()

    conversaciones = response.json().get('_results', [])
    conversaciones_completas = []

    for conv in conversaciones:
        conv_id = conv['id']
        subject = conv.get('subject')
        tags = [tag.get('name') for tag in conv.get('tags', [])]
        recipient = conv.get('recipient', {}).get('handle', '')

        # Traemos los mensajes de esta conversación
        mensajes_url = f"{BASE_URL}/conversations/{conv_id}/messages"
        mensajes_resp = requests.get(mensajes_url, headers=HEADERS)
        mensajes_resp.raise_for_status()
        mensajes = mensajes_resp.json().get('_results', [])

        # Guardamos todos los mensajes asociados
        mensajes_lista = []
        for m in mensajes:
            cuerpo = m.get("body", "")
            mensajes_lista.append(cuerpo.strip() or "[Mensaje vacío]")

        # Guardamos toda la conversación como un dict
        conversaciones_completas.append({
            "conversacion_id": conv_id,
            "subject": subject,
            "recipient": recipient,
            "tags_conversacion": tags,
            "mensajes": mensajes_lista,
        })

    return conversaciones_completas





# === MOSTRAR RESULTADOS ===
if __name__ == "__main__":
    conversaciones = obtener_conversaciones_inbox()

    for i, conv in enumerate(conversaciones):
        print(f"\n====== Conversación {i+1} ======")
        print("ID:", conv["conversacion_id"])
        print("Subject:", conv.get("subject", "Sin asunto"))
        print("Recipient:", conv.get("recipient", "Desconocido"))
        print("Tags:", ", ".join(conv.get("tags_conversacion", [])) or "Ninguna")

        print("\n--- Mensajes ---")
        for j, mensaje in enumerate(conv["mensajes"]):
            #print(f"Mensaje {j+1}:\n{mensaje}\n")
            texto_limpio = limpiar_html(mensaje)
            print(f"Mensaje {j+1}:\n{texto_limpio}\n")


import requests

import os
from dotenv import load_dotenv
import pandas as pd 
from utils.upa import limpiar_html

load_dotenv()
API_KEY = os.getenv("API_KEY") 
HEADERS = {
    'Authorization': API_KEY,
    'Accept': 'application/json'
}

BASE_URL = 'https://api2.frontapp.com'




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


def construir_df_multiples_conversaciones(limit=100, inbox_id="inb_bhllg")->pd.DataFrame:
    """
    Retorna el último mensaje enviado por el usuario (is_inbound=True).
    Si no hay mensajes entrantes, retorna None.
    """
    url = f'{BASE_URL}/inboxes/{inbox_id}/conversations?limit={limit}'
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()

    conversaciones = response.json().get('_results', [])
    filas = []

    for conv in conversaciones:
        conv_id = conv['id']

        
        mensajes_url = f"{BASE_URL}/conversations/{conv_id}/messages"
        mensajes_resp = requests.get(mensajes_url, headers=HEADERS)
        mensajes_resp.raise_for_status()
        mensajes_data = mensajes_resp.json()

        
        df_conversacion = construir_df_conversacion(mensajes_data)

       
        if not df_conversacion.empty:
            filas.append(df_conversacion)

    # Concatenar todas las filas
    if filas:
        return pd.concat(filas, ignore_index=True)
    else:
        return pd.DataFrame(columns=[
            "id_conversacion", "msg_cliente", "msg_cliente_id", 
            "respondido", "msg_nuestro", "msg_nuestro_id"
        ])

def construir_df_conversaciones_archivadas(limit=50) -> pd.DataFrame:
    """
    Descarga conversaciones archivadas y construye un DataFrame con:
    - msg_cliente
    - msg_nuestro
    - respondido
    """
    url = f"{BASE_URL}/conversations?q=status:archived&limit={limit}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    conversaciones = response.json().get("_results", [])

    filas = []

    for conv in conversaciones:
        conv_id = conv['id']
        mensajes_url = f"{BASE_URL}/conversations/{conv_id}/messages"
        mensajes_resp = requests.get(mensajes_url, headers=HEADERS)
        mensajes_resp.raise_for_status()
        mensajes_data = mensajes_resp.json()

        df_conversacion = construir_df_conversacion(mensajes_data)

        if not df_conversacion.empty:
            filas.append(df_conversacion)

    if filas:
        return pd.concat(filas, ignore_index=True)
    else:
        return pd.DataFrame(columns=[
            "id_conversacion", "msg_cliente", "msg_cliente_id", 
            "respondido", "msg_nuestro", "msg_nuestro_id"
        ])



def construir_df_conversacion(data)->pd.DataFrame:
    mensajes = data["_results"]
    
    if len(mensajes) < 1:
        return pd.DataFrame(columns=[
            "id_conversacion", "msg_cliente", "msg_cliente_id", 
            "respondido", "msg_nuestro", "msg_nuestro_id"
        ])

    def extraer_texto_limpio(msg):
        return msg.get("text") or limpiar_html(msg.get("body", ""))

    # Tomamos el último mensaje recibido (cliente) y penúltimo (nosotros)
    msg_cliente = next((m for m in mensajes if m.get("is_inbound")), None)
    msg_nuestro = next((m for m in mensajes if not m.get("is_inbound")), None)
    
    
    id_conversacion = mensajes[0]["_links"]["related"]["conversation"].split("/")[-1]

    fila = {
        "id_conversacion": id_conversacion,
        "msg_cliente": extraer_texto_limpio(msg_cliente) if msg_cliente else None,
        "msg_cliente_id": msg_cliente["id"] if msg_cliente else None,
        "respondido": msg_nuestro is not None,
        "msg_nuestro": extraer_texto_limpio(msg_nuestro) if msg_nuestro else None,
        "msg_nuestro_id": msg_nuestro["id"] if msg_nuestro else None
    }

    return pd.DataFrame([fila])


#+------------------------------------------- TROUBLESHOOTING------------------------------------------
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

        
        mensajes_url = f"{BASE_URL}/conversations/{conv_id}/messages"
        mensajes_resp = requests.get(mensajes_url, headers=HEADERS)
        mensajes_resp.raise_for_status()
        mensajes = mensajes_resp.json().get('_results', [])

        
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



def main():
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
# === MOSTRAR RESULTADOS ===


if __name__ == "__main__":
    #main()
    df=construir_df_multiples_conversaciones(limit=10)
    print(df.columns)
    print(df.info())
    print(df.head())
    
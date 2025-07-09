import json
from front_connector import FrontConnector
from classifier import clasificar_mensaje
from Automatizacion.api.src.solicitudes import cargar_plantilla
from util import handle_rate_limiting

with open("examples/example_messages.json", "r", encoding="utf-8") as f:
    examples = json.load(f)

with open("inbox_mapping.json", "r", encoding="utf-8") as f:
    inbox_id_mapping = json.load(f)

def get_inbox_id(message):
    handle = message['to'][0] if message['metadata']['is_inbound'] else message['sender']['handle']
    return inbox_id_mapping.get(handle)

def procesar_logica(mensaje):
    cuerpo = mensaje.get("body", "")
    plantilla = clasificar_mensaje(cuerpo)
    if plantilla:
        return cargar_plantilla(plantilla)
    return None

def main():
    for example in examples:
        respuesta = procesar_logica(example)
        if respuesta:
            reply_request = {
                "sender": {
                    "handle": "soporte@tuempresa.com",
                    "name": "Soporte",
                    "role": "user"
                },
                "body": respuesta,
                "body_format": "plain_text",
                "type": "outgoing",
                "metadata": {
                    "is_inbound": False,
                    "created_at": int(__import__('time').time() * 1000)
                },
                "external_id": f"reply-{example['external_id']}"
            }
            inbox_id = get_inbox_id(example)
            response = FrontConnector.import_inbox_message(inbox_id, reply_request)

            while response.status_code == 429:
                print(f"Rate limit for {example['external_id']}")
                handle_rate_limiting(response)
                response = FrontConnector.import_inbox_message(inbox_id, reply_request)

            if response.status_code >= 400:
                print(f"Error HTTP {response.status_code} en {example['external_id']}")
            else:
                print(f"Respuesta enviada a {example['sender']['handle']}")
        else:
            print(f"Sin intención detectada en: {example['external_id']}")

if __name__ == "__main__":
    main()

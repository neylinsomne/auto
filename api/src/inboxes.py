def obtener_inboxes(data_json: dict) -> dict:
    """
    Extrae los inboxes y retorna un diccionario con su nombre como clave y su ID como valor.
    """
    inboxes = {}
    for inbox in data_json.get("_results", []):
        nombre = inbox.get("name", "Sin nombre")
        id_inbox = inbox.get("id", "")
        inboxes[nombre] = id_inbox

    print(inboxes)
    return inboxes


if __name__ == "__main__":
    obtener_inboxes()

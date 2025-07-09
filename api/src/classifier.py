from sentence_transformers import SentenceTransformer, util
#sentence-transformers
from Automatizacion.api.src.conversaciones_messages import obtener_mensajes
intenciones = {
    "reembolso": [
        "quiero un reembolso",
        "cancelar los cargos",
        "quiero que me devuelvan el dinero",
        "quiero que me retornen el crédito",
        "quiero un reembolso",
        "cancelar los cargos",
        "quiero que me devuelvan el dinero",
        "quiero que me retornen el crédito",
        "solicito la devolución de mi dinero",
        "me gustaría un reembolso completo",
        "por favor, cancelen el cobro",
        "quiero que se me acredite el monto pagado",
        "no estoy satisfecho y deseo mi dinero de vuelta",
        "necesito que me hagan una devolución",
        "¿Cómo puedo solicitar mi reembolso?",
        "se me cobró por error, pido un reembolso",
        "no he usado el servicio y quiero mi dinero"

    ],
    "cancelacion_membresia": [
        "quiero cancelar mi membresía",
        "ya no quiero el servicio",
        "dar de baja la suscripción",
        "quiero dar de baja mi suscripción",
        "ya no deseo continuar con la membresía",
        "por favor, cancelen mi cuenta",
        "no quiero renovar mi membresía",
        "cómo puedo terminar mi suscripción?",
        "deseo finalizar mi servicio",
        "por favor, detengan los cobros de la membresía",
        "me gustaría cancelar mi membresía ahora",
        "no estoy interesado en seguir siendo miembro",
        "ya no necesito la membresía, por favor, desactívenla",
        "ya no necesito esta membresia",
        "quiero finalizar esta memebresia",
    ],


    "soporte_tecnico": [
        "no me funciona",
        "tengo un problema",
        "necesito ayuda con la plataforma",
        "tengo un error en la plataforma",
        "la aplicación no me carga",
        "necesito ayuda con un problema técnico",
        "mi cuenta no funciona correctamente",
        "hay un fallo en el sistema",
        "no puedo acceder a las funcionalidades",
        "me aparece un error al intentar X",
        "¿Cómo soluciono este problema?",
        "la página no responde",
        "necesito asistencia técnica con mi suscripción"
    ]
}



modelo = SentenceTransformer('paraphrase-MiniLM-L6-v2')  

intencion_embeddings = {}
for etiqueta, ejemplos in intenciones.items():
    intencion_embeddings[etiqueta] = modelo.encode(ejemplos, convert_to_tensor=True)

def clasificar_mensaje(texto: str) -> dict: # Cambiamos el tipo de retorno a dict
    texto_embedding = modelo.encode(texto, convert_to_tensor=True)

    mejor_intencion = None
    mejor_similitud = -1
    similitudes_por_intencion = {} 
    for etiqueta, embeddings in intencion_embeddings.items():
        #similitud = util.max_cosine_sim(texto_embedding, embeddings).item() # .item() para obtener el valor escalar
        cosine_scores = util.cos_sim(texto_embedding, embeddings)
        similitud = cosine_scores.max().item()
        similitudes_por_intencion[etiqueta] = similitud
        if similitud > mejor_similitud:
            mejor_similitud = similitud
            mejor_intencion = etiqueta

    umbral_conocido = 0.7 # Un umbral más estricto para intenciones conocidas
    umbral_sugerencia = 0.4 # Un umbral para sugerir intenciones cercanas

    if mejor_similitud >= umbral_conocido:
        return {"intencion": mejor_intencion, "confianza": mejor_similitud}
    elif mejor_similitud >= umbral_sugerencia:
        # Ordenar intenciones por similitud descendente para sugerir las más cercanas
        intenciones_sugeridas = sorted(
            [ (sim, intencion) for intencion, sim in similitudes_por_intencion.items() if sim >= umbral_sugerencia and intencion != mejor_intencion],
            reverse=True
        )[:2] # Sugerir las 2 más cercanas
        return {
            "intencion": "intencion_desconocida_sugerencia",
            "mensaje_sugerencia": f"No estoy completamente seguro, pero tu consulta podría estar relacionada con: {', '.join([sug[1] for sug in intenciones_sugeridas])}. ¿Es correcto?",
            "confianza": mejor_similitud # Confianza de la mejor coincidencia
        }
    else:
        return {"intencion": "intencion_desconocida", "confianza": mejor_similitud}
    

def procesar_y_clasificar():
    mensajes = obtener_mensajes(limit=3)  # Puedes cambiar el límite
    resultado = []
    for m in mensajes:
        clasificacion = clasificar_mensaje(m['mensaje'])
        resultado.append({
            "mensaje": m["mensaje"],
            "etiquetas_originales": m["etiquetas"],
            "clasificacion": clasificacion
        })
    return resultado




if __name__=="__main__":
# Ejemplo de uso con la nueva función
  print(clasificar_mensaje("Quiero que me regresen el dinero de mi última compra."))
  print(clasificar_mensaje("Mi aplicación no me deja iniciar sesión."))
  print(clasificar_mensaje("Quiero finalizar mi suscripción mensual."))
  print(clasificar_mensaje("Necesito poder acceder a mi cuenta, caso contrario voy a cancelar mi suscripción y pedir reembolso")) # Ejemplo de mensaje desconocido
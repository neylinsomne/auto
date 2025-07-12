
from difflib import SequenceMatcher
import pandas as pd
from templates import get_all_templates_df
from conversaciones_messages import construir_df_multiples_conversaciones



def mensaje_similar_a_template(mensaje: str, df_templates: pd.DataFrame, umbral: float = 0.9) -> dict | None:
    """
    Compara el mensaje con cada template y devuelve un dict con name, subject y body
    si encuentra una coincidencia que supere el umbral.
    """
    mensaje = mensaje.strip().lower()
    mejor_match = None
    mejor_ratio = 0

    for _, template in df_templates.iterrows():
        ratio = SequenceMatcher(None, mensaje, template["body"].lower()).ratio()
        if ratio > mejor_ratio and ratio >= umbral:
            mejor_ratio = ratio
            mejor_match = {
                "name": template["name"],
                "subject": template["subject"],
                "body": template["body"]
            }

    return mejor_match

    
# para hacer la conexión entre popo y pollo
def add_template(df_mensajes: pd.DataFrame, df_templates: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega al DataFrame de mensajes columnas con el template usado si fue respondido:
    name, subject y body del template.
    """
    nombres, subjects, bodies = [], [], []

    for _, row in df_mensajes.iterrows():
        if row["respondido"] and pd.notnull(row["msg_nuestro"]):
            match = mensaje_similar_a_template(row["msg_nuestro"], df_templates)
            if match:
                nombres.append(match["name"])
                subjects.append(match["subject"])
                bodies.append(match["body"])
            else:
                nombres.append(None)
                subjects.append(None)
                bodies.append(None)
        else:
            nombres.append(None)
            subjects.append(None)
            bodies.append(None)

    df_mensajes = df_mensajes.copy()
    df_mensajes["template_name"] = nombres
    df_mensajes["template_subject"] = subjects
    df_mensajes["template_body"] = bodies

    return df_mensajes




def template_a_clasificacion(df_mensajes: pd.DataFrame, df_templates: pd.DataFrame) -> pd.DataFrame:
    



def main():
    o=1

if __name__ == "__main__":
    df=add_template(construir_df_multiples_conversaciones(limit=10),get_all_templates_df())
    print(df.info)
    print(df.head())
    print(df.columns)
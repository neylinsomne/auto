from utils.upa import detectar_idioma
from tag import add_tag_revisar
from classifier import extraer_subject
from conversaciones_messages import construir_df_multiples_conversaciones

def pipe():
    df=construir_df_multiples_conversaciones()
    df["subject"] = df["msg_cliente"].apply(extraer_subject)
    df["idioma"] = df["msg_cliente"].apply(detectar_idioma)
    df_es = df[df["idioma"] == "es"]
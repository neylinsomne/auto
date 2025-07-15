from bs4 import BeautifulSoup
import os

from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

def limpiar_html(texto_html):
    soup = BeautifulSoup(texto_html, "html.parser")
    texto = soup.get_text(separator="\n").strip()
    return texto.replace("\n", " ")



def detectar_idioma(texto):
    try:
        if texto and isinstance(texto, str):
            return detect(texto)
        else:
            return "desconocido"
    except LangDetectException:
        return "desconocido"

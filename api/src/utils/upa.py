from bs4 import BeautifulSoup

def limpiar_html(texto_html):
    soup = BeautifulSoup(texto_html, "html.parser")
    texto = soup.get_text(separator="\n").strip()
    return texto.replace("\n", " ")
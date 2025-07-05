import webbrowser
import os
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("CLIENT_ID")
redirect_uri = os.getenv("REDIRECT_URI")

auth_url = f"https://app.frontapp.com/oauth/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}"
webbrowser.open(auth_url)
print("🔗 Abriendo navegador para autenticación...")

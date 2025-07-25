from fastapi import FastAPI, Request
from src.utils.token_exchange import exchange_code_for_token
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hola desde Vercel con FastAPI!"}

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

if not ACCESS_TOKEN:
    print("No ACCESS_TOKEN found. Please authenticate manually via /callback.")
else:
    print("ACCESS_TOKEN already set.")

@app.get("/callback")
async def callback(request: Request):
    global ACCESS_TOKEN
    code = request.query_params.get("code")
    if not code:
        return {"error": "No code provided"}

    token_data = exchange_code_for_token(code)
    ACCESS_TOKEN = token_data.get("access_token")

    print("Token recibido:", ACCESS_TOKEN)

    return {"message": "Token received!", "access_token": ACCESS_TOKEN}

@app.get("/get_templates")
def get_templates():
    global ACCESS_TOKEN
    if not ACCESS_TOKEN:
        return {"error": "Access token not available. Please authenticate first."}

    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    url = "https://api2.frontapp.com/message_templates"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.status_code, "details": response.text}

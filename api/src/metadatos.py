#para 

import os
import requests
from dotenv import load_dotenv
import pandas as pd
from utils.upa import limpiar_html

load_dotenv()

API_URL = "https://familify.api.frontapp.com"
STATIC_API_KEY = os.getenv("API_KEY")
TEAM_ID = "tim_4mhec"

def get_headers():
    return {
        "Authorization": STATIC_API_KEY,  
        "Accept": "Content-Type"
    }


def add_mark_review(message:json)->:
    if low_mark<:
        e=connect_base()
        e-add message
    return message


def review_message(message:json)->json:



##LLAMADA DEL ENDPOINT:


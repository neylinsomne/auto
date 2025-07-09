import os
import requests
from dotenv import load_dotenv
load_dotenv()

url = "https://api2.frontapp.com/auth/token"
data = {
    "grant_type": "client_credentials",
    "client_id": os.getenv("CLIENT_ID"),
    "client_secret": os.getenv("CLIENT_SECRET")
}
response = requests.post(url, data=data)

print(response.status_code)
print(response.text)

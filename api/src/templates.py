
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
        "Accept": "application/json"
    }


def get_all_templates(headers):
    url = f"{API_URL}/teams/{TEAM_ID}/message_templates"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        for template in data.get("_results", []):
            print(f"ID: {template['id']}")
            print(f"Nombre: {template['name']}")
            print(f"Asunto: {template['subject']}")
            print(f"Disponible para todos: {template['is_available_for_all_inboxes']}")
            print("-" * 50)
    else:
            print("Error:", response.status_code, response.text)


def get_all_templates_df():
    headers=get_headers()
    url = f"{API_URL}/teams/{TEAM_ID}/message_templates"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        templates = []

        for template in data.get("_results", []):
            x=limpiar_html(template.get("body"))
            templates.append({
                
                "id": template.get("id"),
                "name": template.get("name"),
                "subject": template.get("subject"),
                #"is_available_for_all_inboxes": template.get("is_available_for_all_inboxes"),
                "created_at": template.get("created_at"),
                "updated_at": template.get("updated_at"),
                "body": x
            })
            
        
        df = pd.DataFrame(templates)
        return df
    else:
        print("Error:", response.status_code, response.text)
        return None




def manejo_categoria(df, col):
    print(df[col].unique())
    category_map = {
        'CANCELAR': 'cancel_es',
        'CANCEL': 'cancel_en',
        'Desuscribir': 'cancel_es',
        'UNSUSCRIBE': 'cancel_en',
        'REEMBOLSO ': 'refund_es',
        'Refund': 'refund_en',
        'REFUND': 'refund_en',
        'Reembolso ': 'refund_es',
        'REEMBOLSO REALIZADO ': 'refund_done_es',
        'REEMBOLSO FINALIZADO': 'refund_done_es',
        'Reembolso Storybook': 'refund_es',
        'refund 50%': 'refund_partial_en',
        'PROBLEMA APP': 'app_issue_es',
        'APP PROBLEM': 'app_issue_en',
        'PROBLEMA TARJETA': 'payment_issue_es',
        'CHANGE THE LANGUAGE': 'change_lang_en',
        'Cambiar correo': 'email_change_es',
        'Email': 'email_en',
        'Account': 'account_en',
        'Cuenta': 'account_es',
        'Cambio de dispositivo ': 'device_change_es',
        'CUPÓN': 'coupon_es',
        'ACTIVAR TIEMPO': 'activation_es',
        'PAY PAL': 'paypal',
        'INFORMACIÓN': 'info_es',
        'Información': 'info_es',
        'MAIL': 'email_en',
        'USUARIO PRIVILEGIADO': 'special_user_es',
        'Reseña': 'review_es',
        'Canjear': 'redeem_es',
        '': 'unknown',
        None: 'unknown'
    }
    df['subject_category'] = df['subject'].map(category_map)
    return df

# FUNCION A LLAMAR
def get_templates():
    headers=get_headers()
    df=get_all_templates_df(headers)
    df=manejo_categoria(df,"subject")
    return df


if __name__=="__main__":
    headers=get_headers()
    print("Tomando Templates")
    get_all_templates(headers)
    df=get_all_templates_df(headers)
    print("Los Templates se ven asi:")
    print("-" * 50)
    print( df.head(5))
    print( df.shape[0])
    print("-" * 50)
    print("\n ")
    df=manejo_categoria(df,"subject")
    #dfa=agrupar_categoria(df)
    #print(dfa)
   
    print()
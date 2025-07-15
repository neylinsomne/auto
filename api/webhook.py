import hmac
import hashlib
import base64
import time
from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse
import uvicorn
import os
from src.solicitudes import a

app = FastAPI()

# Tu clave de firma definida en la configuración del webhook
FRONT_SIGNING_KEY = os.getenv("FRONT_SIGNING_KEY", "tu_clave_aqui")

@app.post("/webhook/front")
async def front_webhook(
    request: Request,
    x_front_signature: str = Header(None),
    x_front_request_timestamp: str = Header(None),
    x_front_challenge: str = Header(None)
):
    raw_body = await request.body()

    # Si es un mensaje de validación inicial
    if x_front_challenge:
        return JSONResponse(content={"challenge": x_front_challenge})

    # Verificación de firma
    if not (x_front_signature and x_front_request_timestamp):
        raise HTTPException(status_code=400, detail="Faltan cabeceras de autenticación")

    try:
        # Construye la cadena base como Front indica
        base_string = f"{x_front_request_timestamp}:".encode("utf-8") + raw_body
        digest = hmac.new(FRONT_SIGNING_KEY.encode("utf-8"), base_string, hashlib.sha256).digest()
        computed_signature = base64.b64encode(digest).decode()

        if not hmac.compare_digest(computed_signature, x_front_signature):
            raise HTTPException(status_code=401, detail="Firma no válida")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error verificando firma: {str(e)}")

    # Cuerpo del evento (ya verificado)
    body = await request.json()
    evento = body.get("type")
    payload = body.get("payload", {})
    company_id = body.get("authorization", {}).get("id")

    print(f"\n📨 Nuevo evento de Front: {evento}")
    print(f"🏢 Empresa: {company_id}")
    print(f"🔍 Payload: {payload}\n")

    # Ejemplo: solo manejar mensajes entrantes
    if evento == "inbound_received":
        mensaje_id = payload.get("id")
        cuerpo = payload.get("body")
        print(f"📩 Nuevo mensaje entrante [{mensaje_id}]: {cuerpo}")

    return JSONResponse(content={"status": "ok"})

# Para pruebas locales con `uvicorn`
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

import os
import requests

FRONT_URL = "https://api2.frontapp.com"

class FrontConnector:
    @staticmethod
    def import_inbox_message(inbox_id: str, payload: dict):
        endpoint = f"{FRONT_URL}/inboxes/{inbox_id}/imported_messages"
        return FrontConnector._make_import_api_request(endpoint, payload)

    @staticmethod
    def _make_import_api_request(url: str, payload: dict):
        has_attachments = 'attachments' in payload and len(payload['attachments']) > 0
        headers = FrontConnector._build_headers(has_attachments)

        if has_attachments:
            files = [
                ('attachments', (att['filename'], att['buffer'], att['content_type']))
                for att in payload['attachments']
            ]
            response = requests.post(url, headers=headers, files=files, data={k: v for k, v in payload.items() if k != 'attachments'})
        else:
            response = requests.post(url, headers=headers, json=payload)

        return response

    @staticmethod
    def _build_headers(has_attachments: bool):
        headers = {
            "Authorization": f"Bearer {os.getenv('API_KEY')}"
        }
        if not has_attachments:
            headers["Content-Type"] = "application/json"
        return headers
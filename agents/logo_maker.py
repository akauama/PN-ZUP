# agents/logo_maker.py

import os
import requests
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_KEY = os.getenv("CLIENT_KEY")
REALM = os.getenv("REALM", "stackspot-freemium")
OAUTH_URL = f"https://idm.stackspot.com/{REALM}/oidc/oauth/token"
AGENT_ID = "01K5VTYNFBDQQ0VR9PD29HNYC8"  # Troque pelo ID do seu agente, se necessário
AGENT_URL = f"https://genai-inference-app.stackspot.com/v1/agent/{AGENT_ID}/chat"

def run_logo_maker(input_data):
    prompt = input_data.get("logo_prompt_for_ai", "").strip()
    if not prompt:
        return {
            "original_prompt": "",
            "logo_image_url": "",
            "logo_image_markdown": "",
            "image_meta": {},
            "notes": "Prompt para a logo não fornecido."
        }
    if not CLIENT_ID or not CLIENT_KEY:
        return {
            "original_prompt": prompt,
            "logo_image_url": "",
            "logo_image_markdown": "",
            "image_meta": {},
            "notes": "Client ID ou Client Key não encontrados nas variáveis de ambiente."
        }
    try:
        # 1️⃣ Obter token OAuth
        payload = {
            "grant_type": "client_credentials",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_KEY
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        token_response = requests.post(OAUTH_URL, data=payload, headers=headers, timeout=30)
        token_response.raise_for_status()
        access_token = token_response.json().get("access_token", "")
        if not access_token:
            raise Exception("Não foi possível obter o access token.")

        # 2️⃣ Chamar o agente StackSpot
        agent_headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        agent_payload = {
            "streaming": False,
            "user_prompt": prompt,
            "stackspot_knowledge": False,
            "return_ks_in_response": True
        }
        response = requests.post(AGENT_URL, headers=agent_headers, json=agent_payload, timeout=120)
        response.raise_for_status()
        data = response.json()

        # Tenta extrair a URL da imagem da resposta do agente
        image_url = ""
        # 1. Tenta campos comuns
        for key in ["image_url", "logo_image_url", "url", "message"]:
            if key in data and isinstance(data[key], str) and data[key].startswith("http"):
                image_url = data[key]
                break
        # 2. Tenta buscar por URL em texto (markdown, etc)
        if not image_url and "http" in str(data):
            import re
            urls = re.findall(r'(https?://[^\s)]+)', str(data))
            if urls:
                image_url = urls[0]

        return {
            "original_prompt": prompt,
            "logo_image_url": image_url,
            "logo_image_markdown": f"![logo]({image_url})" if image_url else "",
            "image_meta": {},  # O agente pode retornar mais metadados, adapte se necessário
            "notes": "Resposta do agente StackSpot."
        }
    except Exception as e:
        return {
            "original_prompt": prompt,
            "logo_image_url": "",
            "logo_image_markdown": "",
            "image_meta": {},
            "notes": f"Erro ao gerar imagem: {str(e)}"
        }
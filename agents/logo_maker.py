import os
import requests
import streamlit as st

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Função auxiliar para carregar variáveis
def get_secret(key, default=None):
    if key in st.secrets:  # Streamlit Cloud
        return st.secrets[key]
    return os.getenv(key, default)  # Local .env

# Configurações
CLIENT_ID = get_secret("CLIENT_ID")
CLIENT_KEY = get_secret("CLIENT_KEY")
REALM = get_secret("REALM", "stackspot-freemium")

OAUTH_URL = f"https://idm.stackspot.com/{REALM}/oidc/oauth/token"
AGENT_ID = "01K5VTYNFBDQQ0VR9PD29HNYC8"
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
            "notes": "Client ID ou Client Key não encontrados."
        }

    try:
        # Autenticação
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

        # Chamada ao agente
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

        # Extração da URL da imagem
        image_url = ""
        for key in ["image_url", "logo_image_url", "url", "message"]:
            if key in data and isinstance(data[key], str) and data[key].startswith("http"):
                image_url = data[key]
                break
        if not image_url and "http" in str(data):
            import re
            urls = re.findall(r'(https?://[^\s)]+)', str(data))
            if urls:
                image_url = urls[0]

        return {
            "original_prompt": prompt,
            "logo_image_url": image_url,
            "logo_image_markdown": f"![logo]({image_url})" if image_url else "",
            "image_meta": {},
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


# ----------------------------
# Teste no terminal
# ----------------------------
if __name__ == "__main__":
    print("🔹 Testando logo_maker.py")
    test_input = {"logo_prompt_for_ai": "Logomarca moderna e minimalista para cafeteria"}
    resultado = run_logo_maker(test_input)
    print("Resultado:", resultado)

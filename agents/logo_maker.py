import requests
import re
import streamlit as st

# Carrega credenciais do secrets
CLIENT_ID = st.secrets.get("CLIENT_ID", "")
CLIENT_KEY = st.secrets.get("CLIENT_KEY", "")
REALM = st.secrets.get("REALM", "stackspot-freemium")

AGENT_ID = "01K5VTYNFBDQQ0VR9PD29HNYC8"
OAUTH_URL = f"https://idm.stackspot.com/{REALM}/oidc/oauth/token"
AGENT_URL = f"https://genai-inference-app.stackspot.com/v1/agent/{AGENT_ID}/chat"


def run_logo_maker(input_data):
    prompt = input_data.get("logo_prompt_for_ai", "").strip()
    client_id = input_data.get("client_id", CLIENT_ID)
    client_key = input_data.get("client_key", CLIENT_KEY)
    realm = input_data.get("realm", REALM)

    if not prompt:
        return {
            "original_prompt": "",
            "logo_image_url": "",
            "logo_image_markdown": "",
            "image_meta": {},
            "notes": "Prompt para a logo não fornecido."
        }
    if not all([client_id, client_key, realm]):
        return {
            "original_prompt": prompt,
            "logo_image_url": "",
            "logo_image_markdown": "",
            "image_meta": {},
            "notes": "Credenciais StackSpot ausentes."
        }

    try:
        # 1️⃣ Obter token OAuth
        payload = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_key
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

        # 3️⃣ Extrair URL da imagem
        image_url = ""
        for key in ["image_url", "logo_image_url", "url", "message"]:
            if key in data and isinstance(data[key], str) and data[key].startswith("http"):
                image_url = data[key]
                break

        if not image_url and "http" in str(data):
            urls = re.findall(r'(https?://[^\s)"]+)', str(data))
            if urls:
                image_url = urls[0]

        image_url = image_url.strip().strip('",')

        return {
            "original_prompt": prompt,
            "logo_image_url": image_url,
            "logo_image_markdown": f"![logo]({image_url})" if image_url else "",
            "image_meta": {},
            "notes": "Resposta do agente StackSpot." if image_url else "Não foi possível extrair a URL da imagem."
        }

    except Exception as e:
        return {
            "original_prompt": prompt,
            "logo_image_url": "",
            "logo_image_markdown": "",
            "image_meta": {},
            "notes": f"Erro ao gerar imagem: {str(e)}"
        }


if __name__ == "__main__":
    print("🔹 Testando logo_maker.py")
    test_input = {"logo_prompt_for_ai": "Logomarca moderna e minimalista para cafeteria"}
    resultado = run_logo_maker(test_input)
    print("Resultado:", resultado)

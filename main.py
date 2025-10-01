import json
import os
from dotenv import load_dotenv
print("CWD:", os.getcwd())
print("Existe .env?", os.path.exists(".env"))
from orchestrator import multiagent_flow

import os


# Carrega variáveis do .env (StackSpot credentials)
load_dotenv()

CLIENT_ID= os.getenv("CLIENT_ID")
CLIENT_KEY= os.getenv("CLIENT_KEY")
REALM= os.getenv("STACKSPOT_REALM", "stackspot-freemium")

if __name__ == "__main__":
    # Exemplo de entrada fixa (pode adaptar para entrada dinâmica)
    user_input = {
        "business_idea": "Cafeteria para jovens com cafés especiais e doces artesanais",
        "audience": "Universitários de 18 a 25 anos",
        "context_costs": {
            "cidade": "Salvador",
            "tamanho_ponto_m2": 25
        },
        # Passa as credenciais para o orchestrator, se necessário
        "stackspot_credentials": {
            "client_id": CLIENT_ID,
            "client_key": CLIENT_KEY,
            "realm": REALM
        }
    }

    try:
        # Executa o fluxo multiagente
        final_output = multiagent_flow(user_input)
        # Exibe o JSON final formatado
        print(json.dumps(final_output, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Erro ao executar o fluxo multiagente: {e}")

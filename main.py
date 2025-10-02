import json
import os
from dotenv import load_dotenv
from orchestrator import multiagent_flow

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_KEY = os.getenv("CLIENT_KEY")
REALM = os.getenv("REALM", "stackspot-freemium")

if __name__ == "__main__":
    user_input = {
        "business_idea": "Cafeteria para jovens com cafés especiais e doces artesanais",
        "audience": "Universitários de 18 a 25 anos",
        "context_costs": {
            "cidade": "Salvador",
            "tamanho_ponto_m2": 25
        },
        "stk_client_id": CLIENT_ID,
        "stk_client_key": CLIENT_KEY,
        "stk_realm": REALM
    }

    try:
        final_output = multiagent_flow(user_input)
        print(json.dumps(final_output, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Erro ao executar o fluxo multiagente: {e}")

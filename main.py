import json
from orchestrator import multiagent_flow

if __name__ == "__main__":
    user_input = {
        "business_idea": "Cafeteria para jovens com cafés especiais e doces artesanais",
        "audience": "Universitários de 18 a 25 anos",
        "context_costs": {
            "cidade": "Salvador",
            "tamanho_ponto_m2": 25
        }
    }

    # Executa o fluxo multiagente
    final_output = multiagent_flow(user_input)

    # Exibe o JSON final formatado
    print(json.dumps(final_output, indent=2, ensure_ascii=False))

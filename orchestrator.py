from agents import branding_marketing, costwiz, logo_maker

def multiagent_flow(user_input):
    """
    Orquestra o fluxo multiagente:
    1. Gera branding e marketing.
    2. Calcula custos (CAPEX/OPEX).
    3. Gera logo.
    Retorna um dicionário consolidado para exibição ao usuário.
    """

    # Padroniza campos para os agentes
    # Extrai cidade/tamanho e repassa como location/size
    context_costs = user_input.get("context_costs", {})
    location = context_costs.get("cidade") or user_input.get("cidade", "")
    size = context_costs.get("tamanho_ponto_m2") or user_input.get("tamanho_ponto_m2", "")

    # Monta input padronizado para todos os agentes
    agent_input = {
        "business_idea": user_input.get("business_idea", ""),
        "audience": user_input.get("audience", ""),
        "location": location,
        "size": size,
        # Mantém campos originais para compatibilidade
        **user_input
    }

    # 1️⃣ Branding & Marketing
    try:
        branding_result = branding_marketing.run_branding_marketing(agent_input)
    except Exception as e:
        branding_result = {
            "suggested_names": [],
            "slogan": "",
            "brand_tone": "",
            "notes_for_marketing": f"Erro ao gerar branding: {type(e).__name__}: {str(e)}",
            "logo_prompt_for_ai": ""
        }
        print(f"[ERRO] Branding: {e}")

    # 2️⃣ Custos
    try:
        costs_result = costwiz.run_costwiz(agent_input)
    except Exception as e:
        costs_result = {
            "capex_estimate": {},
            "opex_monthly": {},
            "summary_text": "",
            "one_line_assumptions": f"Erro ao calcular custos: {type(e).__name__}: {str(e)}"
        }
        print(f"[ERRO] CostWiz: {e}")

    # 3️⃣ Logo
    try:
        logo_result = logo_maker.run_logo_maker(branding_result)
    except Exception as e:
        logo_result = {
            "original_prompt": branding_result.get("logo_prompt_for_ai", ""),
            "logo_image_url": "",
            "logo_image_markdown": "",
            "image_meta": {},
            "notes": f"Erro ao gerar logo: {type(e).__name__}: {str(e)}"
        }
        print(f"[ERRO] LogoMaker: {e}")

    # 4️⃣ Montar JSON final
    final_output = {
        "business_idea": agent_input.get("business_idea", ""),
        "audience": agent_input.get("audience", ""),
        "location": agent_input.get("location", ""),
        "size": agent_input.get("size", ""),
        "branding": branding_result,
        "costs": costs_result,
        "logo": logo_result,
        "errors": {
            "branding": branding_result.get("notes_for_marketing", "") if not branding_result.get("suggested_names") else "",
            "costs": costs_result.get("one_line_assumptions", "") if not costs_result.get("capex_estimate") else "",
            "logo": logo_result.get("notes", "") if not logo_result.get("logo_image_url") else ""
        }
    }

    return final_output

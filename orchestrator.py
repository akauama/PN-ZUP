from agents import branding_marketing, costwiz, logo_maker


def multiagent_flow(user_input):
    context_costs = user_input.get("context_costs", {})
    location = context_costs.get("cidade") or user_input.get("cidade", "")
    size = context_costs.get("tamanho_ponto_m2") or user_input.get("tamanho_ponto_m2", "")

    agent_input = {
        "business_idea": user_input.get("business_idea", ""),
        "audience": user_input.get("audience", ""),
        "location": location,
        "size": size,
        **user_input
    }

    # Branding
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

    # Custos
    try:
        costs_result = costwiz.run_costwiz(agent_input)
    except Exception as e:
        costs_result = {
            "capex_estimate": {},
            "opex_monthly": {},
            "summary_text": "",
            "one_line_assumptions": f"Erro ao calcular custos: {type(e).__name__}: {str(e)}"
        }

    # Logo
    try:
        logo_input = {
            "logo_prompt_for_ai": branding_result.get("logo_prompt_for_ai", ""),
            "client_id": user_input.get("stk_client_id"),
            "client_key": user_input.get("stk_client_key"),
            "realm": user_input.get("stk_realm")
        }
        if not all([logo_input["client_id"], logo_input["client_key"], logo_input["realm"]]):
            raise Exception("Credenciais do StackSpot ausentes para geração de logo.")
        logo_result = logo_maker.run_logo_maker(logo_input)
    except Exception as e:
        logo_result = {
            "original_prompt": branding_result.get("logo_prompt_for_ai", ""),
            "logo_image_url": "",
            "logo_image_markdown": "",
            "image_meta": {},
            "notes": f"Erro ao gerar logo: {type(e).__name__}: {str(e)}"
        }

    return {
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

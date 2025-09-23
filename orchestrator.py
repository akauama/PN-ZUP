from agents import branding_marketing, costwiz, logo_maker

def multiagent_flow(user_input):
    # 1️⃣ Branding & Marketing
    try:
        branding_result = branding_marketing.run_branding_marketing(user_input)
    except Exception as e:
        branding_result = {
            "suggested_names": [],
            "slogan": "",
            "brand_tone": "",
            "notes_for_marketing": f"Erro: {str(e)}",
            "logo_prompt_for_ai": ""
        }

    # 2️⃣ Custos
    try:
        costs_result = costwiz.run_costwiz(user_input)
    except Exception as e:
        costs_result = {
            "capex_estimate": {},
            "opex_monthly": {},
            "one_line_assumptions": f"Erro: {str(e)}"
        }

    # 3️⃣ Logo
    try:
        logo_result = logo_maker.run_logo_maker(branding_result)
    except Exception as e:
        logo_result = {
            "original_prompt": branding_result.get("logo_prompt_for_ai", ""),
            "logo_image_url": "",
            "logo_image_markdown": "",
            "image_meta": {},
            "notes": f"Erro ao gerar logo: {str(e)}"
        }

    # 4️⃣ Montar JSON final
    final_output = {
        "business_idea": user_input.get("business_idea", ""),
        "audience": user_input.get("audience", ""),
        "branding": branding_result,
        "costs": costs_result,
        "logo": logo_result
    }

    return final_output

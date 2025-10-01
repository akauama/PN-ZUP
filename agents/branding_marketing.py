#branding_marketing.py
import random

def run_branding_marketing(input_data):
    """
    Gera sugestões de branding e marketing de forma dinâmica, a partir das informações do usuário.
    Ajustes de prompt engineering:
    - Nomes curtos (1-3 palavras)
    - Evita repetir literal da descrição
    - Slogans mais criativos
    """
    business_idea = input_data.get("business_idea", "").strip()
    audience = input_data.get("audience", "").strip()
    
    if not business_idea:
        business_idea = "Negócio"
    if not audience:
        audience = "Público-alvo"

    # Lista de palavras/ideias para criar nomes curtos
    modifiers = ["Pro", "Hub", "Lab", "Co", "360", "Prime", "Point", "Studio"]
    
    # Geração de 3 nomes curtos
    suggested_names = []
    base_words = business_idea.split()
    for i in range(3):
        name = random.choice(base_words[:2])  # pega até 2 palavras do negócio
        modifier = random.choice(modifiers)
        suggested_names.append(f"{name} {modifier}")

    # Slogan criativo
    slogans = [
        f"Transformando {business_idea} em experiências inesquecíveis",
        f"O jeito inovador de {business_idea} para {audience}",
        f"{business_idea} que conecta com {audience}",
        f"Mais do que {business_idea}, uma experiência para {audience}",
        f"Inspirando {audience} com {business_idea}"
    ]
    slogan = random.choice(slogans)

    # Tom de marca
    brand_tone = f"Tom de comunicação alinhado ao público {audience}, moderno, acolhedor e criativo"

    # Descrição da logomarca
    logo_description = (
        f"Logomarca que represente {business_idea} para {audience}, "
        "estilo moderno e minimalista, foco em símbolo representativo, cores harmoniosas"
    )

    # Prompt para o agente de geração de logo
    logo_prompt_for_ai = (
        f"Minimalist vector logo for {business_idea}. "
        f"Focus on a clean, simple symbol that represents {business_idea} for {audience}, "
        "flat design, no text, professional, centered composition, white or transparent background."
    )

    notes_for_marketing = (
        f"Foque em estratégias de marketing voltadas para {audience}, "
        f"destaque diferenciais do {business_idea}, e mantenha identidade visual consistente."
    )

    return {
        "suggested_names": suggested_names,
        "slogan": slogan,
        "brand_tone": brand_tone,
        "logo_description": logo_description,
        "logo_prompt_for_ai": logo_prompt_for_ai,
        "notes_for_marketing": notes_for_marketing
    }

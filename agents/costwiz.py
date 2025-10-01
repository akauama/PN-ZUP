def run_costwiz(input_data):
    """
    Simula estimativas de CAPEX e OPEX de forma genérica e apresenta as métricas em reais
    em um texto interessante, único e coeso para o usuário.
    """
    # Extrai informações do usuário ou define valores padrão genéricos
    business_idea = input_data.get("business_idea", "novo negócio")
    location = input_data.get("location", "sua região")
    size = input_data.get("size", "um espaço compacto")
    capex = input_data.get("capex_estimate", {
        "equipamentos": "R$ 20.000",
        "estrutura": "R$ 10.000",
        "licenças": "R$ 2.000"
    })
    opex = input_data.get("opex_monthly", {
        "aluguel": "R$ 3.000",
        "insumos": "R$ 1.500",
        "salários": "R$ 6.000"
    })

    # Função auxiliar para listar custos de forma genérica
    def format_costs(cost_dict, title):
        lines = [f"{title}:"]
        for key, value in cost_dict.items():
            # Capitaliza a chave e substitui underscores por espaço
            label = key.replace("_", " ").capitalize()
            lines.append(f"- {label}: {value}")
        return "\n".join(lines)

    capex_text = format_costs(capex, "Investimento inicial (CAPEX)")
    opex_text = format_costs(opex, "Custos operacionais mensais (OPEX)")

    resumo = (
        f"Para o seu {business_idea} em {location}, considerando {size}, "
        f"as estimativas iniciais são:\n\n"
        f"{capex_text}\n\n"
        f"{opex_text}\n\n"
        "Esses valores são aproximados e podem variar conforme o porte do negócio, localização e necessidades específicas. "
        "Use-os como referência para o seu planejamento financeiro!"
    )

    return {
        "capex_estimate": capex,
        "opex_monthly": opex,
        "summary_text": resumo,
        "one_line_assumptions": (
            f"Premissas baseadas em {business_idea}, localizado em {location}, porte: {size}."
        )
    }
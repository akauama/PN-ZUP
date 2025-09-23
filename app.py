import streamlit as st
from orchestrator import multiagent_flow

st.title("PN-ZUP Multiagente")

business_idea = st.text_input("Ideia de negócio")
audience = st.text_input("Público-alvo")
cidade = st.text_input("Cidade")
tamanho = st.number_input("Tamanho do ponto (m²)", min_value=5, value=25)

if st.button("Gerar plano"):
    user_input = {
        "business_idea": business_idea,
        "audience": audience,
        "context_costs": {"cidade": cidade, "tamanho_ponto_m2": tamanho}
    }
    final_output = multiagent_flow(user_input)
    st.subheader("JSON Final")
    st.json(final_output)

    logo_url = final_output.get("logo", {}).get("logo_image_url", "")
    if logo_url:
        st.image(logo_url, use_column_width=True)
    else:
        st.warning("Logo não gerada.")

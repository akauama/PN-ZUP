import streamlit as st
from agents.logo_maker import run_logo_maker

st.set_page_config(page_title="Gerador de Logomarcas", layout="centered")

st.title("🎨 Gerador de Logomarcas com StackSpot")

st.markdown("Digite uma descrição para gerar sua logomarca automaticamente.")

# Campo para prompt
prompt = st.text_input("Descrição da logomarca", "Logomarca moderna e minimalista para cafeteria")

if st.button("Gerar Logomarca"):
    with st.spinner("Gerando sua logomarca..."):
        resultado = run_logo_maker({"logo_prompt_for_ai": prompt})

    if resultado["logo_image_url"]:
        st.success("✅ Logomarca gerada com sucesso!")
        st.image(resultado["logo_image_url"], caption=prompt, width=512)
        st.markdown(resultado["logo_image_markdown"])
    else:
        st.error(f"⚠️ Erro: {resultado['notes']}")

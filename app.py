import streamlit as st
import json
import base64
import requests
from io import BytesIO
from PIL import Image
from orchestrator import multiagent_flow

# Credenciais do secrets
CLIENT_ID = st.secrets.get("CLIENT_ID", "")
CLIENT_SECRET = st.secrets.get("CLIENT_KEY", "")
REALM = st.secrets.get("REALM", "stackspot-freemium")

if not all([CLIENT_ID, CLIENT_SECRET, REALM]):
    st.error("⚠️ Credenciais não carregadas. Configure-as no Streamlit Cloud (Secrets).")
    st.stop()

st.set_page_config(page_title="PN-ZUP Multiagente", layout="wide")
st.title("PN-ZUP Multiagente - Teste")

with st.form("user_inputs"):
    business_idea = st.text_input(
        "Ideia de negócio",
        "Cafeteria para jovens com cafés especiais e doces artesanais",
        help="Descreva sua ideia de negócio."
    )
    audience = st.text_input(
        "Público-alvo",
        "Universitários de 18 a 25 anos",
        help="Quem é o público principal?"
    )
    cidade = st.text_input("Cidade", "Salvador")
    tamanho = st.number_input("Tamanho do ponto (m²)", min_value=5, value=25)
    logo_style = st.selectbox(
        "Estilo da logomarca",
        ["Moderno e profissional", "Divertido e colorido", "Minimalista", "Clássico", "Vintage"],
        help="Escolha o estilo visual desejado para a logomarca."
    )
    submitted = st.form_submit_button("Gerar plano")

if submitted:
    if not business_idea or not audience or not cidade:
        st.warning("Por favor, preencha todos os campos obrigatórios.")
        st.stop()

    user_input = {
        "business_idea": business_idea,
        "audience": audience,
        "context_costs": {
            "cidade": cidade,
            "tamanho_ponto_m2": tamanho
        },
        "logo_style": logo_style,
        "stk_client_id": CLIENT_ID,
        "stk_client_key": CLIENT_SECRET,
        "stk_realm": REALM
    }

    with st.spinner("Gerando plano de negócio..."):
        try:
            final_output = multiagent_flow(user_input)
        except Exception as e:
            st.error(f"Erro ao gerar o plano: {e}")
            st.stop()

    # ⚡️ Mantive toda a parte de exibição igual ao seu local
    errors = final_output.get("errors", {})
    for key, msg in errors.items():
        if msg:
            st.warning(f"⚠️ {key.capitalize()}: {msg}")

    branding = final_output.get("branding", {})
    st.header("🎨 Branding & Marketing")

    nomes = branding.get('suggested_names', [])
    st.subheader("Sugestões de nomes")
    if nomes:
        cols = st.columns(len(nomes))
        for i, name in enumerate(nomes):
            if cols[i].button(name, key=f"name_{i}_{name}"):
                st.success(f"Nome '{name}' copiado! (Copie manualmente)")
    else:
        st.info("Nenhum nome sugerido.")

    st.subheader("Slogan")
    st.info(branding.get('slogan', '-'))

    st.subheader("Tom de marca")
    st.write(branding.get('brand_tone', '-'))

    st.subheader("Descrição da logomarca")
    st.write(branding.get('logo_description', '-'))

    st.subheader("Logo gerada")
    logo_dict = final_output.get("logo", {})
    logo_url = logo_dict.get("logo_image_url", "")
    logo_base64 = logo_dict.get("logo_image_base64", "")

    if logo_base64:
        try:
            base64_data = logo_base64.split(",")[1] if "," in logo_base64 else logo_base64
            image_data = base64.b64decode(base64_data)
            image = Image.open(BytesIO(image_data))
            st.image(image, caption="Logo criada para seu negócio", use_column_width=True)
        except Exception as e:
            st.error(f"Erro ao decodificar imagem Base64: {e}")
    elif logo_url:
        try:
            response = requests.get(logo_url)
            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                st.image(image, caption="Logo criada para seu negócio", use_column_width=True)
            else:
                st.error(f"Erro ao baixar imagem: Status {response.status_code}")
        except Exception as e:
            st.error(f"Erro ao exibir imagem da URL: {e}")
    else:
        st.warning("Logo não gerada. Verifique as credenciais e a API.")

    # ⚡️ Custos
    custos = final_output.get("costs", {})
    st.header("💰 Investimento Inicial (CAPEX)")
    capex = custos.get("capex_estimate", {})
    if capex:
        capex_cols = st.columns(len(capex))
        for i, (k, v) in enumerate(capex.items()):
            capex_cols[i].metric(k.capitalize(), v)
    else:
        st.info("Sem dados de CAPEX disponíveis.")

    st.header("📅 Custos Mensais (OPEX)")
    opex = custos.get("opex_monthly", {})
    if opex:
        opex_cols = st.columns(len(opex))
        for i, (k, v) in enumerate(opex.items()):
            opex_cols[i].metric(k.capitalize(), v)
    else:
        st.info("Sem dados de OPEX disponíveis.")

    st.header("Resumo Financeiro")
    st.success(custos.get("summary_text", ""))

    with st.expander("Premissas e Observações"):
        st.write(custos.get("one_line_assumptions", ""))

    st.header("🚀 Próximos Passos")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Validar ideia com clientes"):
            st.info("Converse com potenciais clientes para validar sua proposta!")
    with col2:
        if st.button("Ajustar plano financeiro"):
            st.info("Revise custos e receitas com um contador especializado.")
    with col3:
        if st.button("Ver dicas de marketing"):
            st.info("Foque em diferenciais e comunicação visual consistente.")

    with st.expander("Baixar plano em JSON"):
        st.download_button(
            label="Baixar plano (JSON)",
            data=json.dumps(final_output, ensure_ascii=False, indent=2),
            file_name="plano_negocio.json",
            mime="application/json"
        )

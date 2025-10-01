# PN-ZUP Multiagente
Transforme qualquer ideia de negócio em um plano completo com branding, estimativas financeiras e logomarca gerada via IA.

✨ Funcionalidades

💡 Sugestões de nomes e slogans.

📊 Estimativa de CAPEX e OPEX.

🖌️ Criação de prompts de logomarca e geração de imagens via StackSpot AI.

📑 Consolidação em JSON estruturado.

🌐 Interface amigável com Streamlit.

🎯 Público-Alvo

Empreendedores, estudantes e equipes de planejamento que querem visualizar rapidamente impactos financeiros e de branding de qualquer ideia de negócio.

📂 Estrutura do Projeto
PN-ZUP/
│
├─ app.py                  # Interface Streamlit
├─ main.py                 # Script de teste local
├─ orchestrator.py         # Fluxo multiagente
├─ requirements.txt        # Dependências
├─ .gitignore              # Ignora venv, .env e caches
├─ .env                    # Variáveis de ambiente (não subir)
└─ agents/
    ├─ __init__.py
    ├─ branding_marketing.py
    ├─ costwiz.py
    └─ logo_maker.py

⚙️ Instalação
git clone https://github.com/USERNAME/REPO.git
cd REPO
python -m venv venv
.\venv\Scripts\Activate.ps1   # Windows PowerShell
pip install -r requirements.txt


Crie o arquivo .env com suas credenciais:

CLIENT_ID=seu_client_id
CLIENT_KEY=seu_client_key
REALM=stackspot-freemium


🔒 Não suba o .env para o GitHub.

▶️ Rodando a Aplicação
streamlit run app.py


Preencha os campos de ideia de negócio, público-alvo, cidade e tamanho do ponto.

Clique em Gerar plano para visualizar o JSON completo e a logomarca (quando a API estiver configurada).

📝 Observações

As imagens dependem de credenciais válidas StackSpot AI.

As estimativas financeiras são simuladas, mas podem ser ajustadas.

Projeto estruturado em multiagentes, permitindo expansão para qualquer tipo de negócio.

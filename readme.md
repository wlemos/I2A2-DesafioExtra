IA CSV Multi-Agente — README
Visão Geral
Esse projeto permite que o usuário faça perguntas livres sobre qualquer arquivo CSV e receba respostas analíticas, visualizações interativas (Plotly), e contexto de memória de análises passadas, usando uma arquitetura de agentes CrewAI e interface Streamlit.

Estrutura do Projeto
text
.
├── main.py
├── requirements.uv
├── agents/
│   ├── orchestrator.py
│   ├── dataloader.py
│   ├── analyzer.py
│   ├── visualization.py
│   └── memory.py
├── utils/
│   └── supabase_client.py
├── .env.example
└── README.md
Pré-requisitos
Python >=3.10 e <=3.12

Conta no Supabase (para banco de memória)

Chave de API Gemini Flash 2.5 (Google)

Gerenciador de dependências UV

Navegador moderno (para interface Streamlit)

Instalação
1. Instale o UV (se não tiver)
bash
pip install uv
2. Crie ambiente virtual
No Linux/Mac:

bash
uv venv .venv
.venv\Scripts\activate
3. Instale as dependências
bash
uv pip install -r requirements.uv
4. Crie e configure o arquivo .env
Copie .env.example para .env e edite com suas chaves:

text
GEMINI_API_KEY=sua_chave_gemini
SUPABASE_URL=sua_url_supabase
SUPABASE_KEY=sua_chave_supabase
Execução
bash
streamlit run main.py
Acesse pelo navegador, faça upload de um CSV e digite perguntas.

Arquivos e Funções
main.py: Interface do usuário, conecta e exibe resposta dos agentes.

agents/orchestrator.py: Orquestrador geral, coordena agentes e integra resultados.

agents/dataloader.py: Ingere e valida o CSV, oferece estatísticas básicas.

agents/analyzer.py: Realiza análises estatísticas e interpreta os dados.

agents/visualization.py: Gera os gráficos interativos da análise (Plotly).

agents/memory.py: Recupera e armazena contexto/resultado no Supabase.

utils/supabase_client.py: Faz a conexão com a API Supabase.

requirements.uv: Lista de dependências para o UV instalar.

.env.example: Modelo de variáveis de ambiente.

Dicas
Se houver erro de chave, revise o .env.

Se o CSV for pesado, o processamento pode demorar.

Recomenda-se rodar localmente (localhost) para segurança das chaves.

Referências
CrewAI - Documentação e exemplos

Streamlit - Guia oficial

Gemini API - Quickstart Google

Supabase - Documentação Python

Exemplo de integração CrewAI + Streamlit


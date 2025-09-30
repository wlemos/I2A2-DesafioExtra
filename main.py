import os
import streamlit as st
from agents.orchestrator import OrchestratorAgent

os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]
os.environ["SUPABASE_URL"] = st.secrets["SUPABASE_URL"]
os.environ["SUPABASE_KEY"] = st.secrets["SUPABASE_KEY"]

def precisa_grafico(pergunta: str) -> bool:
    termos_grafico = ['gráfico', 'grafico', 'plot', 'visualização', 'visualizacao', 'mostrar', 'exibir', 'desenhar']
    pergunta_lower = pergunta.lower()
    return any(termo in pergunta_lower for termo in termos_grafico)

st.set_page_config(page_title='IA CSV Multi-Agente 🚀', layout='wide')

st.title('Análise Inteligente de CSV com AI Agentes')

st.markdown("Faça perguntas livres sobre o CSV e veja respostas analíticas e visuais!")

uploaded_file = st.file_uploader('Carregue seu arquivo CSV')

user_input = st.text_input("""Sua pergunta: \n
                           obs: para visualizar gráficoa adionar os termos a seguir na sua pergunta \n
                        ['gráfico', 'grafico', 'plot', 'visualização', 'visualizacao', 'mostrar', 'exibir', 'desenhar']""")

if 'orchestrator' not in st.session_state:
    st.session_state['orchestrator'] = OrchestratorAgent()

if uploaded_file and user_input:
    resposta = st.session_state['orchestrator'].handle_query(user_input, uploaded_file)
    st.subheader('Resposta da IA')
    st.write(resposta['resumo'])  

    if precisa_grafico(user_input):
        st.subheader('Visualizações')
        for fig in resposta['graficos']:
            st.plotly_chart(fig)
        if resposta['contexto_passado']:
            st.subheader('Histórico/Memória')
            st.write(resposta['contexto_passado'])        

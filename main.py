import os
import streamlit as st
from agents.orchestrator import OrchestratorAgent

os.environ["GEMINIAPIKEY"] = os.getenv("GEMINIAPIKEY", "")
os.environ["SUPABASEURL"] = os.getenv("SUPABASEURL", "")
os.environ["SUPABASEKEY"] = os.getenv("SUPABASEKEY", "")

def precisa_grafico(pergunta: str) -> bool:
    termos_grafico = ["grafico", "gráfico", "plot", "visualizacao", "visualização", "mostrar", "exibir", "desenhar"]
    pergunta_lower = pergunta.lower()
    return any(termo in pergunta_lower for termo in termos_grafico)

st.set_page_config(page_title="IA CSV Multi-Agente", layout="wide")

st.title("Análise Inteligente de CSV com AI Agentes")
st.markdown("Faça perguntas livres sobre o CSV e veja respostas analíticas e visuais!")

uploaded_file = st.file_uploader("Carregue seu arquivo CSV")
st.write("Obs: para gráficos, adicione termos como gráfico, visualizar, plot, exibir na sua pergunta.")

user_input = st.text_input("Sua pergunta")

if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = OrchestratorAgent()

if uploaded_file and user_input:
    resposta = st.session_state.orchestrator.handle_query(user_input, uploaded_file)

    if resposta:
        resumo = resposta.get("resumo", "")
        detalhes = resposta.get("detalhes", "")
        graficos = resposta.get("graficos", [])

        st.subheader("Resumo")
        st.write(resumo if resumo else "Nenhum resumo disponível.")

        st.subheader("Detalhes")
        st.write(detalhes if detalhes else "Nenhum detalhe disponível.")

        if graficos:
            st.subheader("Gráficos")
            # Certifique-se que graficos é iterável e não None
            for grafico in graficos:
                st.plotly_chart(grafico)
        else:
            st.write("Nenhum gráfico gerado para essa consulta.")
else:
    if not uploaded_file:
        st.info("Por favor, carregue um arquivo CSV para iniciar.")
    if not user_input:
        st.info("Por favor, digite uma pergunta para começar a análise.")

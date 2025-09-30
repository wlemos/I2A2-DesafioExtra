import streamlit as st
# from google import genai
import google.genai as genai

client = genai.Client()

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)

def chamar_gemini(pergunta: str, resumo_dataset: str) -> str:
    prompt = (
        "Você é um analista de dados exploratórios.\n"
        "Analise cuidadosamente o seguinte resumo do CSV e responda à pergunta do usuário de forma clara, detalhada e didática.\n\n"
        "Instruções:\n"
        "- Forneça interpretações, estatísticas descritivas e análises conforme apropriado.\n"
        "- **Gere sugestões e descrições de gráficos somente se o usuário solicitar visualizações explícitas na pergunta.**\n"
        "- Evite produzir descrições gráficas se não forem pedidas.\n"
        "- Termine com insights ou recomendações práticas baseadas nos dados.\n\n"
        f"Resumo do CSV:\n{resumo_dataset}\n\n"
        f"Pergunta do usuário:\n{pergunta}\n\n"
        "Responda de forma objetiva e sem repetir o resumo."
    )
    chat = client.chats.create(model="gemini-2.5-flash")
    response = chat.send_message(message=prompt)
    return response.text  # Retorna somente o texto gerado pela LLM

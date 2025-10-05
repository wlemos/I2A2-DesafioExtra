from agents.memory import MemoryAgent
from agents.dataloader import DataLoaderAgent
from agents.analyzer import AnalyzerAgent
from agents.visualization import VisualizationAgent
import re

class OrchestratorAgent:
    def __init__(self):
        self.memory = MemoryAgent()
        self.dataloader = DataLoaderAgent()
        self.analyzer = AnalyzerAgent()
        self.visualizer = VisualizationAgent()

    def precisa_grafico(self, pergunta: str) -> bool:
        termos_grafico = ["grafico", "gráfico", "plot", "visualizacao", "visualização", "mostrar", "exibir", "desenhar"]
        pergunta_lower = pergunta.lower()
        return any(termo in pergunta_lower for termo in termos_grafico)

    def extrair_colunas_pergunta(self, pergunta: str, dataset_info) -> list:
        if dataset_info is None:
            return []
        colunas = dataset_info[0].columns.tolist()
        colunas_achadas = []
        pergunta_lower = pergunta.lower()
        for col in colunas:
            col_lower = col.lower()
            pattern = re.compile(r'\b' + re.escape(col_lower) + r'\b')
            if pattern.search(pergunta_lower):
                colunas_achadas.append(col)
        return colunas_achadas

    def handle_query(self, user_input, uploaded_file):
        contexto_historico = self.memory.get_conclusoes()
        if uploaded_file:
            df, stats, dataset_id = self.dataloader.load(uploaded_file)
            dataset_info = (df, stats)
        else:
            dataset_id = None
            dataset_info = None

        analise = self.analyzer.analyze(dataset_info, user_input, contexto=contexto_historico)

        if self.precisa_grafico(user_input):
            colunas_pedidas = self.extrair_colunas_pergunta(user_input, dataset_info)
            graficos = self.visualizer.visualize(analise, dataset_info, colunas_filtradas=colunas_pedidas)
        else:
            graficos = None
            self.memory.save_context(user_input, analise, dataset_info, dataset_id)

        return {
            "resumo": analise.get(["resumo"], ""),
            "detalhes": analise.get("detalhes", {}),
            "graficos": graficos,
            "conclusao": analise.get("conclusao", ""),
            "contexto_passado": contexto_historico,
        }

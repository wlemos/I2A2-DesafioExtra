from agents.memory import MemoryAgent
from agents.dataloader import DataLoaderAgent
from agents.analyzer import AnalyzerAgent
from agents.visualization import VisualizationAgent

class OrchestratorAgent:
    def __init__(self):
        self.memory = MemoryAgent()
        self.dataloader = DataLoaderAgent()
        self.analyzer = AnalyzerAgent()
        self.visualizer = VisualizationAgent()

    def precisa_grafico(self, pergunta: str) -> bool:
        termos_grafico = ['gráfico', 'grafico', 'plot', 'visualização', 'visualizacao', 'mostrar', 'exibir', 'desenhar']
        pergunta_lower = pergunta.lower()
        return any(termo in pergunta_lower for termo in termos_grafico)

    def handle_query(self, user_input, uploaded_file):
        contexto_historico = self.memory.get_conclusoes()
        dataset_info = self.dataloader.load(uploaded_file) if uploaded_file else None
        analise = self.analyzer.analyze(dataset_info, user_input, contexto=contexto_historico)

        if self.precisa_grafico(user_input):
            graficos = self.visualizer.visualize(analise, dataset_info)
        else:
            graficos = []

        self.memory.save_context(user_input, analise, dataset_info=dataset_info)

        return {
            "resumo": analise.get('resumo', ''),
            "detalhes": analise.get('detalhes', ''),
            "graficos": graficos,
            "conclusao": analise.get('conclusao', ''),
            "contexto_passado": contexto_historico
        }

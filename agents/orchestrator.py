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
        contexto = self.memory.get_context(user_input)

        if uploaded_file:
            dataset_info = self.dataloader.load(uploaded_file)
        else:
            dataset_info = contexto.get('dataset_info', None)

        analise = self.analyzer.analyze(dataset_info, user_input)

        # Só gera gráfico se detectar no texto da pergunta
        if self.precisa_grafico(user_input):
            graficos = self.visualizer.visualize(analise, dataset_info)
        else:
            graficos = []

        self.memory.save_context(user_input, analise, graficos, dataset_info)
        return {
            "resumo": analise['resumo'],
            "detalhes": analise['detalhes'],
            "graficos": graficos,
            "contexto_passado": contexto.get('historico', None)
        }

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
        """
        Extrai possíveis nomes de colunas mencionados na pergunta, baseando-se nos nomes das colunas do dataset.
        Retorna lista de colunas filtradas que aparecem na pergunta.
        """
        if dataset_info is None:
            return []
        colunas = dataset_info.df.columns.tolist()
        # Colunas que aparecem na pergunta (case insensitive)
        colunas_achadas = []
        pergunta_lower = pergunta.lower()
        for col in colunas:
            # Verifica se o nome da coluna está explicitamente na pergunta, ignorando case e caracteres especiais básicos
            col_lower = col.lower()
            # Usar regex com \b para pegar somente palavras inteiras (evitar pegar "idade" dentro de "idades")
            pattern = re.compile(r'\b' + re.escape(col_lower) + r'\b')
            if pattern.search(pergunta_lower):
                colunas_achadas.append(col)
        return colunas_achadas

    def handle_query(self, user_input, uploaded_file):
        contexto_historico = self.memory.get_conclusoes()
        dataset_info = self.dataloader.load_uploaded_file(uploaded_file) if uploaded_file else None
        analise = self.analyzer.analyze(dataset_info, user_input, contexto=contexto_historico)

        if self.precisa_grafico(user_input):
            colunas_pedidas = self.extrair_colunas_pergunta(user_input, dataset_info)
            graficos = self.visualizer.visualize(analise, dataset_info, colunas_filtradas=colunas_pedidas)
        else:
            graficos = None
            self.memory.save_context(user_input, analise, dataset_info)

        return {
            "resumo": analise.get_resumo(),
            "detalhes": analise.get_detalhes(),
            "graficos": graficos,
            "conclusao": analise.get_conclusao(),
            "contexto_passado": contexto_historico,
        }

import plotly.express as px

class VisualizationAgent:
    def visualize(self, analise, datasetinfo, colunas_filtradas=None):
        if datasetinfo is None or datasetinfo[0] is None:
            return None
        df = datasetinfo[0]
        numeric_cols = df.select_dtypes(include='number').columns.tolist()
        if not colunas_filtradas:
            colunas_filtradas = numeric_cols
        cols_para_graficos = [col for col in colunas_filtradas if col in numeric_cols]
        if not cols_para_graficos:
            return None
        graficos = []
        for col in cols_para_graficos:
            graficos.append(px.histogram(df, x=col, title=f'Histograma de {col}'))
            graficos.append(px.box(df, y=col, title=f'Boxplot de {col}'))
        return graficos

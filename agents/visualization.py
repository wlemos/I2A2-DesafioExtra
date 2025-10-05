import plotly.express as px

class VisualizationAgent:
    def visualize(self, analise, datasetinfo, colunas_filtradas=None):
        """
        Gera gráficos apenas para as colunas numéricas filtradas.
        Se colunas_filtradas for None ou vazia, não gera gráficos.
        """
        if datasetinfo is None or datasetinfo[0] is None:
            return None

        df = datasetinfo[0]

        if not colunas_filtradas:
            return None

        numeric_cols = df.select_dtypes(include='number').columns.tolist()
        cols_para_graficos = [col for col in colunas_filtradas if col in numeric_cols]

        graficos = []
        for col in cols_para_graficos:
            fig_hist = px.histogram(df, x=col, title=f'Histograma de {col}')
            graficos.append(fig_hist)
            fig_box = px.box(df, y=col, title=f'Boxplot de {col}')
            graficos.append(fig_box)

        return graficos

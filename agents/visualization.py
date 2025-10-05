import plotly.express as px

class VisualizationAgent:
    def visualize(self, analise, dataset_info, colunas_filtradas=None):
        """
        Gera gráficos apenas para as colunas numéricas filtradas.
        Se colunas_filtradas for None ou vazia, não gera gráficos.
        """
        if dataset_info is None or dataset_info.df is None:
            return None

        df = dataset_info.df
        
        # Se colunas_filtradas vazia ou None, não gera gráficos
        if not colunas_filtradas:
            return None

        # Filtrar somente colunas numéricas entre as colunas pedidas
        numeric_cols = df.select_dtypes(include='number').columns.tolist()
        cols_para_graficos = [col for col in colunas_filtradas if col in numeric_cols]

        graficos = []
        for col in cols_para_graficos:
            fig_hist = px.histogram(df, x=col, title=f'Histograma de {col}')
            graficos.append(fig_hist)
            fig_box = px.box(df, y=col, title=f'Boxplot de {col}')
            graficos.append(fig_box)

        return graficos

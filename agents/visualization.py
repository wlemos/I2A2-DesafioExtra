import plotly.express as px

class VisualizationAgent:
    def visualize(self, analise, dataset_info):
        df = dataset_info["df"]
        numeric_cols = df.select_dtypes(include='number').columns.tolist()
        graficos = []

        for col in numeric_cols:
            fig = px.histogram(df, x=col, title=f'Histograma de {col}')
            graficos.append(fig)
            fig2 = px.box(df, y=col, title=f'Boxplot de {col}')
            graficos.append(fig2)
        return graficos

import numpy as np
from agents import gemini_client

class AnalyzerAgent:
    def gerar_resumo_dataset(self, dataset_info, max_cols_show=20, max_rows_example=3):
        df = dataset_info["df"]
        resumo = []

        # Informações gerais
        resumo.append(f"Número de linhas: {df.shape[0]}, Número de colunas: {df.shape[1]}")

        # Nomes das colunas (limite a 20)
        colunas_str = ', '.join(df.columns[:max_cols_show])
        if len(df.columns) > max_cols_show:
            colunas_str += ' ...'
        resumo.append(f"Colunas: {colunas_str}")

        # Tipos de dado
        tipos = df.dtypes.astype(str).to_dict()
        tipos_str = ', '.join([f"{col}: {tipo}" for col, tipo in list(tipos.items())[:max_cols_show]])
        resumo.append(f"Tipos de dados (amostra): {tipos_str}")

        # Nulos por coluna (amostra)
        nulos = df.isnull().sum()
        nulos_info = ', '.join([f"{col}: {nulos[col]}" for col in df.columns[:max_cols_show]])
        resumo.append(f"Nulos por coluna (amostra): {nulos_info}")

        # Estatísticas numéricas principais (limite)
        numericas = df.select_dtypes(include='number').columns[:max_cols_show]
        for col in numericas:
            try:
                stats = df[col].describe()
                resumo.append(
                    f"{col}: min={stats['min']:.2f}, Q1={stats['25%']:.2f}, mediana={stats['50%']:.2f}, "
                    f"Q3={stats['75%']:.2f}, max={stats['max']:.2f}, média={stats['mean']:.2f}, std={stats['std']:.2f}"
                )
            except Exception:
                continue

        # Maiores frequências de variáveis categóricas (se houver)
        categorias = df.select_dtypes(include='object').columns[:5]
        for col in categorias:
            freq = df[col].value_counts().head(3).to_dict()
            resumo.append(f"{col}: valores mais frequentes {freq}")

        # Exemplo de linhas (head)
        exemplos = df.head(max_rows_example).to_dict(orient='records')
        resumo.append(f"Exemplo de linhas: {exemplos}")

        # Limite final do tamanho para evitar prompt gigante
        return "\n".join(resumo[:40])

    def analyze(self, dataset_info, pergunta):
        resumo_dataset = self.gerar_resumo_dataset(dataset_info)
        resposta_ia = gemini_client.chamar_gemini(pergunta, resumo_dataset)
        return {
            "resumo": resposta_ia,       # resposta dinâmica e personalizada
            "detalhes": resposta_ia
        }

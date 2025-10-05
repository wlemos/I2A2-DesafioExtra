import pandas as pd
import hashlib

class DataLoaderAgent:
    def load(self, uploaded_file):
        df = pd.read_csv(uploaded_file)
        stats = {
            "num_linhas": len(df),
            "num_colunas": len(df.columns),
            "tipos_colunas": dict(df.dtypes),
            "nulos_por_coluna": df.isnull().sum().to_dict(),
            "cardinalidade": df.nunique().to_dict(),
            "minimos": df.min(numeric_only=True).to_dict(),
            "maximos": df.max(numeric_only=True).to_dict(),
        }
        dataset_id = self.gerar_dataset_id(df)
        return df, stats, dataset_id

    def gerar_dataset_id(self, df):
        # Gerar hash md5 baseado em hash dos valores do dataframe
        data_bytes = pd.util.hash_pandas_object(df, index=True).values.tobytes()
        return hashlib.md5(data_bytes).hexdigest()

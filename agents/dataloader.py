import hashlib
import pandas as pd

class DataLoaderAgent:
    def gerar_dataset_id(self, df):
        def convert_lists_to_strings(val):
            if isinstance(val, list):
                return str(val)
            return val

        # Aplica a conversão célula a célula para transformar listas em strings
        df_for_hash = df.applymap(convert_lists_to_strings)

        # Gera hash md5 baseado no dataframe modificado
        data_bytes = pd.util.hash_pandas_object(df_for_hash, index=True).values.tobytes()
        return hashlib.md5(data_bytes).hexdigest()

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

import pandas as pd
import io

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
            "maximos": df.max(numeric_only=True).to_dict()
        }
        return {"df": df, "stats": stats}

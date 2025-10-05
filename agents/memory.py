from utils.supabase_client import supabase

class MemoryAgent:
    def __init__(self):
        self.historico = []

    def save_context(self, pergunta, resposta, dataset_info=None, dataset_id=None):
        self.historico.append({
            "pergunta": pergunta,
            "resposta": resposta,
            "resumo": resposta,
            "dataset_id": dataset_id
        })
        supabase.table("memorias").insert({
            "pergunta": pergunta,
            "resposta": resposta,
            "resumo": resposta,
            "dataset_id": dataset_id
        }).execute()

    def get_conclusoes(self, dataset_id=None):
        conclusoes = [item["resposta"] for item in self.historico
                      if dataset_id is None or item["dataset_id"] == dataset_id]
        if conclusoes:
            return "\n".join(conclusoes)
        query = supabase.table("memorias").select("resposta")
        if dataset_id:
            query = query.eq("dataset_id", dataset_id)
        dados = query.execute()
        if dados.data:
            return "\n".join(item["resposta"] for item in dados.data)
        else:
            return "Ainda não há análises anteriores registradas."

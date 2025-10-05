from utils.supabase_client import supabase

class MemoryAgent:
    def __init__(self):
        self.historico = []

    def save_context(self, pergunta, resposta, dataset_info=None):
        dataset_id = dataset_info.get_id() if dataset_info else None
        self.historico.append({
            "pergunta": pergunta,
            "resposta": resposta,
            "resumo": resposta,
            "dataset_id": dataset_id
        })
        # Salva também no Supabase
        supabase.table("memorias").insert({
            "pergunta": pergunta,
            "resposta": resposta,
            "resumo": resposta,
            "dataset_id": dataset_id
        }).execute()

    def get_conclusoes(self, dataset_id=None):
        # Busca localmente
        conclusoes = [item["resposta"] for item in self.historico
                      if dataset_id is None or item["dataset_id"] == dataset_id]
        if conclusoes:
            return "\n".join(conclusoes)
        # Busca no Supabase se não encontrar localmente
        query = supabase.table("memorias").select("resposta")
        if dataset_id:
            query = query.eq("dataset_id", dataset_id)
        dados = query.execute()
        if dados.data:
            return "\n".join(item["resposta"] for item in dados.data)
        else:
            return "Ainda não há análises anteriores registradas."

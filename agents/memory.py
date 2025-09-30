from utils.supabase_client import supabase

class MemoryAgent:
    def get_context(self, pergunta):
        # Recuperação simples das últimas interações relacionadas
        dados = supabase.table('memorias').select('*').order('id', desc=True).limit(10).execute()
        for entry in dados.data:
            if pergunta in entry['pergunta']:
                return entry
        return {}

    def save_context(self, pergunta, analise, graficos, dataset_info):
        supabase.table('memorias').insert({
            'pergunta': pergunta,
            'analise': str(analise),
            'dataset_info': str(dataset_info)
            # 'graficos' pode ser serializado como imagem/HTML, se desejado
        }).execute()

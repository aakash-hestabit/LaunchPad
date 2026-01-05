from sentence_transformers import CrossEncoder

class Reranker:
    def __init__(self, model_name='BAAI/bge-reranker-v2-m3'):
        self.model = CrossEncoder(model_name)

    async def rerank(self, query, candidates):
        if not candidates:
            return []
        
        pairs = [[query, c['text']] for c in candidates]
        scores = self.model.predict(pairs)
        
        for i, candidate in enumerate(candidates):
            candidate['rerank_score'] = float(scores[i])
            
        return sorted(candidates, key=lambda x: x['rerank_score'], reverse=True)
    
import os
import pinecone
from sentence_transformers import SentenceTransformer
from config import Config

PINECONE_API_KEY = Config.PINECONE_API_KEY
PINECONE_ENV = Config.PINECONE_ENV
PINECONE_INDEX = Config.PINECONE_INDEX

EMBED_MODEL = 'all-MiniLM-L6-v2'  # 384 dims

class RetrieverService:
    def __init__(self):
        if not PINECONE_API_KEY:
            raise RuntimeError('PINECONE_API_KEY not set in environment')
        pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)
        if PINECONE_INDEX not in pinecone.list_indexes():
            pinecone.create_index(PINECONE_INDEX, dimension=384, metric='cosine')
        self.index = pinecone.Index(PINECONE_INDEX)
        self.embedder = SentenceTransformer(EMBED_MODEL)

    def add_documents(self, docs: list):
        # docs: [{id:str, text:str}]
        texts = [d['text'] for d in docs]
        ids = [d['id'] for d in docs]
        embeddings = self.embedder.encode(texts, normalize_embeddings=True).tolist()
        to_upsert = list(zip(ids, embeddings, [{'text':t} for t in texts]))
        self.index.upsert(vectors=to_upsert)

    def retrieve(self, query: str, top_k: int = 5):
        embed = self.embedder.encode([query], normalize_embeddings=True).tolist()[0]
        result = self.index.query(queries=[embed], top_k=top_k, include_metadata=True)
        docs = []
        # result format: result['results'][0]['matches'] or for older SDK result['matches']
        # handle both
        matches = result.get('matches') or (result.get('results', [{}])[0].get('matches', []))
        for match in matches:
            docs.append({'id': match['id'], 'text': match['metadata'].get('text','')})
        return docs


import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from .loaders import extract_text_from_pdf, split_into_clauses

class ClauseMatcher:
    def __init__(self, store):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.store = store
        self.index = faiss.IndexFlatL2(384)
        self.clauses, self.embeddings = self.store.load()
        if self.embeddings:
            self.index.add(np.array(self.embeddings))

    def ingest_precedent(self, file):
        text = extract_text_from_pdf(file)
        clauses = split_into_clauses(text)
        embeddings = self.model.encode(clauses, convert_to_tensor=False)
        self.store.add_clauses(clauses, embeddings)
        self.index.add(np.array(embeddings))
        self.clauses.extend(clauses)
        self.embeddings.extend(embeddings)

    def has_precedents(self):
        return len(self.embeddings) > 0

    def find_most_similar(self, clause):
        embedding = self.model.encode([clause], convert_to_tensor=False)
        D, I = self.index.search(np.array(embedding), k=1)
        return self.clauses[I[0][0]], 1 - D[0][0]

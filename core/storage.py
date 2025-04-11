
import os
import json

class PersistentStore:
    def __init__(self, file_path="precedent_data.json"):
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            self.save([], [])

    def load(self):
        with open(self.file_path, "r") as f:
            data = json.load(f)
        return data["clauses"], data["embeddings"]

    def save(self, clauses, embeddings):
        with open(self.file_path, "w") as f:
            json.dump({"clauses": clauses, "embeddings": embeddings}, f)

    def add_clauses(self, new_clauses, new_embeddings):
        clauses, embeddings = self.load()
        clauses.extend(new_clauses)
        embeddings.extend(new_embeddings)
        self.save(clauses, embeddings)

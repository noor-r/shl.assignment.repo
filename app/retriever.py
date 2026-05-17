
import faiss
import numpy as np
import pandas as pd

from sentence_transformers import SentenceTransformer


class SHLRetriever:

    def __init__(
        self,
        catalog_path,
        index_path,
        embeddings_path
    ):

        self.df = pd.read_csv(catalog_path)

        self.index = faiss.read_index(index_path)

        self.embeddings = np.load(
            embeddings_path
        )

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    def search(
        self,
        query,
        top_k=10
    ):

        embedding = self.model.encode(
            [query]
        ).astype("float32")

        distances, indices = self.index.search(
            embedding,
            top_k
        )

        results = []

        for idx in indices[0]:

            row = self.df.iloc[idx]

            results.append({
                "name": row["name"],
                "url": row["url"],
                "test_type": row["test_type"],
                "description": row["description"]
            })

        return results

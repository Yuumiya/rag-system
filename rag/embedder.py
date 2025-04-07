import json
import os

import faiss
import numpy as np
from openai import OpenAI
from tqdm import tqdm


def embed_chunks(chunks_path: str = "../data/chunks.json", index_path: str = "../data/faiss.index") -> None:
    """
    Embeds text chunks from a JSON file using OpenAI's API and saves the resulting embeddings to a FAISS index file.

    :param chunks_path: The path to the JSON file containing the chunks to embed.
    :param index_path: The path where the FAISS index will be saved.
    :return: None
    """
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if openai_api_key is None:
        raise ValueError("API key must be provided as an environment variable.")

    client = OpenAI(api_key=openai_api_key)

    with open(chunks_path, encoding="utf-8") as f:
        chunks = json.load(f)

    chunk_texts = [chunk["content"] for chunk in chunks]
    embeddings = []

    BATCH_SIZE = 100
    for i in tqdm(range(0, len(chunk_texts), BATCH_SIZE), desc="Embedding chunk batches..."):
        batch = chunk_texts[i : i + BATCH_SIZE]
        try:
            response = client.embeddings.create(input=batch, model="text-embedding-ada-002")
            batch_vectors = [e.embedding for e in response.data]
            embeddings.extend(batch_vectors)
        except Exception as e:
            print(f"Error embedding batch {i // BATCH_SIZE}: {e}")
            continue

    embedding_matrix = np.array(embeddings).astype("float32")

    dim = embedding_matrix.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embedding_matrix)

    faiss.write_index(index, index_path)

    print(f"Embedded {len(embeddings)} chunks, saved at {index_path}")

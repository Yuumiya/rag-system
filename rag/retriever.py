import json
import os

import faiss
import numpy as np
from openai import OpenAI


def search_similar(
    query: str,
    index_path: str = "../data/faiss.index",
    chunks_path: str = "../data/chunks.json",
    top_k: int = 10,
    rerank: bool = False,
) -> list[dict]:
    """
    Searches for the most similar chunks to the given query using FAISS and OpenAI's embeddings.

    :param query: The query string to search for in the embedded text.
    :param index_path: The path to the FAISS index file.
    :param chunks_path: The path to the JSON file containing the chunks to compare against.
    :param top_k: The number of top similar chunks to return. Default is 10.
    :param rerank: Whether to rerank the chunks using a language model. Default is False.
    :return: A list of dictionaries representing the top `top_k` most similar chunks.
    """
    openai_api_key = os.getenv("OPENAI_API_KEY")
    with open(chunks_path, encoding="utf-8") as f:
        chunks = json.load(f)

    index = faiss.read_index(index_path)

    client = OpenAI(api_key=openai_api_key)
    response = client.embeddings.create(input=[query], model="text-embedding-ada-002")
    query_embedding = np.array(response.data[0].embedding, dtype=np.float32).reshape(1, -1)

    retrieve_k = top_k * 2 if rerank else top_k
    distances, indices = index.search(query_embedding, retrieve_k)

    top_chunks = [chunks[i] for i in indices[0] if i < len(chunks)]

    if rerank:
        top_chunks = rerank_chunks(top_chunks, query, top_k)

    return top_chunks


def rerank_chunks(chunks: list[dict], query: str, top_k: int = 10) -> list[dict]:
    """
    Reranks the top-k retrieved chunks based on their relevance to the query using a language model.

    :param chunks: List of chunks to rerank.
    :param query: The query string to assess relevance to.
    :param top_k: Number of top chunks to return after reranking.
    :return: A list of chunks ordered by relevance to the query.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    prompt = (
        f"Given the following code snippets and the question: '{query}',\n"
        f"return a list of snippet numbers (like: 3, 1, 2, ...) ranked from most to least relevant.\n"
        f"Only return a comma-separated list of snippet numbers without any explanation.\n"
        f"Return exactly {top_k} numbers, even if some snippets seem less relevant.\n\n"
    )
    for i, chunk in enumerate(chunks):
        prompt += f"Snippet {i + 1}:\n{chunk['content']}\n\n"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that ranks code snippets by relevance."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=100,
        temperature=0,
    )

    ranking_str = response.choices[0].message.content.strip()

    try:
        indices = [int(i.strip()) - 1 for i in ranking_str.split(",")]
        ranked_chunks = [chunks[i] for i in indices if 0 <= i < len(chunks)]
    except Exception as e:
        print("Error parsing ranking:", e)
        ranked_chunks = chunks

    return ranked_chunks[:top_k]

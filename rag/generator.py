import os

from openai import OpenAI

from rag.retriever import search_similar


def generate_answer(
    query: str,
    index_path: str = "../data/faiss.index",
    chunks_path: str = "../data/chunks.json",
    top_k: int = 10,
    rerank: bool = False,
) -> str:
    """
    Generates an answer to a given query based on the top-k most similar code chunks.
    Uses the `search_similar` function to fetch relevant code chunks, then generates an answer
    using OpenAI's models.

    """
    similar_chunks = search_similar(query, index_path, chunks_path, top_k, rerank)
    context = "\n".join([chunk["content"] for chunk in similar_chunks])

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    messages = [
        {
            "role": "system",
            "content": (
                "You are an intelligent assistant that helps answer questions about a codebase. "
                "Given the following code snippets and a question, you should summarize the relevant information "
                "and provide a concise answer based on the provided code. Your answer should include an explanation "
                "of how the code addresses the question, based on the context provided. "
                "You must generate a clear and concise answer, summarizing the relevant code, if necessary."
                "Do not give broad answers, answer on exact questions and include code snippets in your answers."
            ),
        },
        {"role": "user", "content": (f"Context (code snippets):\n{context}\n\nQuestion: {query}\nAnswer:")},
    ]

    completion = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages, max_tokens=200)

    return completion.choices[0].message.content.strip()

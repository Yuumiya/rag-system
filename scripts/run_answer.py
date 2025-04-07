import argparse
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from rag.generator import generate_answer


def run_answer():
    parser = argparse.ArgumentParser(description="Generate an answer for a given query based on relevant code chunks.")
    parser.add_argument("query", help="The query to generate an answer for.")
    parser.add_argument("--top_k", type=int, default=10, help="Number of top retrieved chunks to consider.")
    parser.add_argument("--index_path", default="data/faiss.index", help="Path to the FAISS index.")
    parser.add_argument("--chunks_path", default="data/chunks.json", help="Path to the JSON file with chunk metadata.")
    parser.add_argument("--rerank", action="store_true", help="Whether to rerank the retrieved chunks using LLM.")
    args = parser.parse_args()

    answer = generate_answer(
        query=args.query,
        index_path=os.path.join(os.getcwd(), args.index_path),
        chunks_path=os.path.join(os.getcwd(), args.chunks_path),
        top_k=args.top_k,
        rerank=args.rerank,
    )

    print("\nGenerated Answer:\n" + "=" * 30)
    print(f"{answer}\n")
    print("=" * 30 + "\n")


if __name__ == "__main__":
    run_answer()

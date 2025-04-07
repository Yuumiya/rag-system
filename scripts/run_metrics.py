import argparse
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from rag.metrics import evaluate_retriever
from rag.retriever import search_similar


def retrieve_fn(query, top_k, index_path, chunks_path, rerank=False):
    return search_similar(query=query, index_path=index_path, chunks_path=chunks_path, top_k=top_k, rerank=rerank)


def run_metrics():
    parser = argparse.ArgumentParser(description="Evaluate retrieval metrics.")
    parser.add_argument(
        "--ground_truth_path",
        help="Path to the ground truth JSON file with 'question' and 'files' fields.",
        default="data/test_set_questions.json",
    )
    parser.add_argument("--top_k", type=int, default=10, help="Number of top retrieved chunks to consider.")
    parser.add_argument("--index_path", default="data/faiss.index", help="Path to the FAISS index.")
    parser.add_argument("--chunks_path", default="data/chunks.json", help="Path to the JSON file with chunk metadata.")
    parser.add_argument("--rerank", action="store_true", help="Whether to use LLM-based reranking of results.")

    args = parser.parse_args()

    print(f"Running retrieval evaluation {'with reranking' if args.rerank else 'without reranking'}...")

    evaluate_retriever(
        ground_truth_path=os.path.join(os.getcwd(), args.ground_truth_path),
        retriever=lambda query, top_k: retrieve_fn(
            query=query,
            top_k=top_k,
            index_path=os.path.join(os.getcwd(), args.index_path),
            chunks_path=os.path.join(os.getcwd(), args.chunks_path),
        ),
        top_k=args.top_k,
    )


if __name__ == "__main__":
    run_metrics()

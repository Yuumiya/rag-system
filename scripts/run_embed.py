import argparse
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from rag.embedder import embed_chunks


def run():
    parser = argparse.ArgumentParser(description="Embed chunks into a FAISS index using OpenAI embeddings.")
    parser.add_argument(
        "--chunks_path", type=str, default="data/chunks.json", help="Path to the JSON file with text chunks."
    )
    parser.add_argument("--index_path", type=str, default="data/faiss.index", help="Path to save the FAISS index.")

    args = parser.parse_args()

    chunks_path = os.path.abspath(args.chunks_path)
    index_path = os.path.abspath(args.index_path)

    embed_chunks(chunks_path=chunks_path, index_path=index_path)


if __name__ == "__main__":
    run()

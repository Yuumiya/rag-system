import argparse
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from rag.chunker import make_chunks


def run():
    parser = argparse.ArgumentParser(description="Chunk files from a cloned repository.")
    parser.add_argument("repo_path", help="Path to the local cloned repository.")
    parser.add_argument("--chunk_size", type=int, default=500, help="Number of characters per chunk.")
    parser.add_argument("--overlap", type=int, default=50, help="Number of overlapping characters between chunks.")
    parser.add_argument("--output", help="Output JSON path for chunks.")

    args = parser.parse_args()
    repo_path = os.path.abspath(args.repo_path)
    output_path = (
        os.path.abspath(args.output)
        if args.output
        else os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "data", "chunks.json")
    )

    make_chunks(repo_path=repo_path, chunk_size=args.chunk_size, overlap=args.overlap, output_path=output_path)


if __name__ == "__main__":
    run()

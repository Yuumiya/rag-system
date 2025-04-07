import argparse
import os
import subprocess
import sys
import time


def wait_for_files(repo_path, retries=5, delay=10):
    """Waits for files to load by checking if the repository folder exists and contains files."""
    for _ in range(retries):
        if os.path.exists(repo_path) and len(os.listdir(repo_path)) > 0:
            return True
        time.sleep(delay)
    return False


def run_script(script_name, *args):
    result = subprocess.run([sys.executable, script_name] + list(args), capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error running {script_name}: {result.stderr.decode()}")
    else:
        print(f"Successfully ran {script_name}: {result.stdout.decode()}")


def main():
    parser = argparse.ArgumentParser(description="Run the entire RAG pipeline (load, chunk, embed).")

    parser.add_argument("repo_url", help="URL of the GitHub repository to clone.")
    parser.add_argument("--destination", help="Destination path for cloning the repository.", default="data")
    parser.add_argument("--chunk_size", type=int, default=500, help="Number of characters per chunk.")
    parser.add_argument("--overlap", type=int, default=50, help="Number of overlapping characters between chunks.")
    parser.add_argument("--chunks_output", help="Output path for chunks JSON.", default="data/chunks.json")
    parser.add_argument("--index_path", help="Path to save the FAISS index.", default="data/faiss.index")

    args = parser.parse_args()

    print("Running load step...")
    run_script("scripts/run_load.py", args.repo_url, "--destination", args.destination)

    print("Waiting for the repository to load before chunking...")
    time.sleep(30)

    print("Running chunk step...")
    run_script(
        "scripts/run_chunk.py",
        args.repo_url,
        "--chunk_size",
        str(args.chunk_size),
        "--overlap",
        str(args.overlap),
        "--output",
        args.chunks_output,
    )

    print("Running embed step...")
    run_script("scripts/run_embed.py", "--chunks_path", args.chunks_output, "--index_path", args.index_path)


if __name__ == "__main__":
    main()

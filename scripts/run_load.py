import argparse
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from rag.loader import clone_repo


def load():
    parser = argparse.ArgumentParser(description="Enter a target GitHub repository.")
    parser.add_argument("url", help="URL of the GitHub repository to make index of.")
    parser.add_argument("--destination", help="Destination path for cloning the repository.", default="data")

    args = parser.parse_args()
    clone_repo(args.url, args.destination)


if __name__ == "__main__":
    load()

import json
import os
import uuid


def is_readable(filepath: str, block_size: int = 512) -> bool:
    """
    Checks if the given file is a readable text or rag file. It returns True if the file is a text file
    (including rag files), and False if the file is binary (e.g., images or other non-text files).

    :param filepath: The path to the file to check.
    :param block_size: The number of bytes to read for the check. Default is 512 bytes.
    :return: True if the file is a readable text or rag file, False if it is a binary file.
    """
    try:
        with open(filepath, "rb") as f:
            chunk = f.read(block_size)
            if b"\x00" in chunk:
                return False
            try:
                chunk.decode("utf-8")
                return True
            except UnicodeDecodeError:
                return False
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return False


def chunk_text(text: str, file_path: str, chunk_size: int = 500, overlap: int = 50) -> list[tuple[int, int, str]]:
    """
    Splits a given text into smaller chunks of a specified size with overlap between them.
    Adds the file path to the beginning of each chunk.

    :param text: The text to be split into chunks.
    :param file_path: The path to the file, which will be added to each chunk's content.
    :param chunk_size: The size of each chunk. Default is 500 characters.
    :param overlap: The number of overlapping characters between consecutive chunks. Default is 50.
    :return: A list of tuples, each containing the start index, end index, and the chunk content.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk_content = f"FILENAME: {file_path}\n{text[start:end]}"
        chunks.append((start, end, chunk_content))
        start += chunk_size - overlap
    return chunks


def make_chunks(
    repo_path: str, chunk_size: int = 500, overlap: int = 50, output_path: str = "../data/chunks.json"
) -> None:
    """
    Processes a repository, reading all text files, and splitting them into chunks. The chunks are then saved to a JSON file.

    :param repo_path: The root directory of the repository to process.
    :param chunk_size: The size of each chunk. Default is 500 characters.
    :param overlap: The number of characters that should overlap between consecutive chunks. Default is 50.
    :param output_path: The file path where the chunks will be saved in JSON format. Default is "../data/chunks.json".
    :return: None
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_path = os.path.abspath(repo_path)
    if output_path is None:
        output_path = os.path.abspath(os.path.join(script_dir, "..", "data", "chunks.json"))
    else:
        output_path = os.path.abspath(output_path)

    chunks = []
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if not d.startswith(".")]

        for file in files:
            file_path = os.path.join(root, file)

            if not is_readable(file_path):
                continue

            try:
                with open(file_path, encoding="utf-8") as f:
                    text = f.read()

                rel_path = os.path.relpath(file_path, repo_path).replace("\\", "/")
                file_chunks = chunk_text(text, rel_path, chunk_size, overlap)

                for start, end, content in file_chunks:
                    chunk_id = str(uuid.uuid4())
                    chunks.append({
                        "id": chunk_id,
                        "file_path": rel_path,
                        "start": start,
                        "end": end,
                        "content": content,
                    })

            except Exception as e:
                print(f"Failed to process {file_path}: {e}")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    print(f"Job done: {len(chunks)} chunks are saved to {output_path}")

# RAG-system

## Installation Steps:

## 1. Clone repository

## 2. Create virtual environment:
- Create:
    ```bash
    python -m venv .venv
    ```
- Activate:
    ```bash
    .\.venv\Scripts\activate
    ```
## 3. Install dependencies
- Using `pip`:
  ```bash
    pip install -r requirements.tx
    ```
- Using `uv`:

    ```bash
    uv pip install -r requirements.txt
    ```

This will install the necessary libraries including:
- `ruff==0.11.4`
- `faiss-cpu>=1.7.2`
- `numpy>=1.23.0`
- `openai>=0.27.0`
- `tqdm>=4.62.3`
- `pathlib>=1.0.0`

## Setup
In order to start sending queries make sure to:
- Have an OPENAI_API_KEY as an environmental variable.
- Load the target repository:
  ```bash
  python scripts/run_load.py <repo_url> [--destination <destination_path>]
  ```
  example:
  ```bash
  python scripts/run_load.py https://github.com/viarotel-org/escrcpy
  ```
- Make chunks:
  ```bash
  python scripts/run_chunk.py <repo_path> [--chunk_size <size>] [--overlap <overlap>] [--output <output_path>]
  ```
  example:
  ```bash
  python scripts/run_chunk.py data/escrcpy
  ```
- Embed chunks into an index file
  ```bash
  python scripts/run_embed.py [--chunks_path <chunks_file>] [--index_path <index_file>]
  ```
    example:
  ```bash
  python scripts/run_embed.py
  ```
## How to use
Now you can run your queries in CLI as follows:
  ```bash
  python scripts/run_answer.py <query> [--top_k <k>] [--index_path <index_file>] [--chunk_path <chunk_file>] [--rerank]
  ```
example:
  ```bash
  python scripts/run_answer.py "How does the SelectDisplay component handle the device options when retrieving display IDs?" --rerank
  ```
`--rerank`: Indicates whether to perform reranking on the retrieved chunks after they are fetched. Use --rerank to enable.

## Metrics 
To see the metrics of the retriever you can use script `run_metrics.py`:
  ```bash
  python scripts/run_metrics.py [--ground_truth_path <gt_file>] [--top_k <k>] [--index_path <index_file>] [--chunks_path <json_file>] [--rerank]
  ```
example:
  ```bash
  python scripts/run_metrics.py --rerank
  ```
## Results:
The current pipeline achieved the values of
- `Recall@10: 0.6471`
- `MRR@10: 0.4281`

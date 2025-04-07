import json
from typing import Callable


class RecallMetric:
    def __init__(self):
        self.correct = 0
        self.total = 0
        self.mrr_total = 0.0

    def update(self, relevant_indices: list[int], retrieved_indices: list[int]):
        """
        relevant_indices: list of ground truth indices (can be more than one correct answer)
        retrieved_indices: list of retrieved result indices (in ranked order)
        """
        self.total += 1

        for rank, idx in enumerate(retrieved_indices):
            if idx in relevant_indices:
                self.correct += 1
                self.mrr_total += 1 / (rank + 1)
                break

    @property
    def recall(self) -> float:
        return self.correct / self.total if self.total > 0 else 0.0

    @property
    def mrr(self) -> float:
        return self.mrr_total / self.total if self.total > 0 else 0.0


def evaluate_retriever(ground_truth_path: str, retriever: Callable[[str, int], list], top_k: int = 10) -> None:
    """
    :parame ground_truth_path: path to JSON file with 'question' and 'files' fields.
    :param retriever: function(question: str, top_k: int) -> list of retrieved chunks with 'file_path'
    :param top_k: number of chunks to retrieve per question
    :return None:
    """
    with open(ground_truth_path, encoding="utf-8") as f:
        examples = json.load(f)

    metric = RecallMetric()

    for example in examples:
        question = example["question"]
        relevant_files = set(example["files"])

        retrieved_chunks = retriever(question, top_k)
        retrieved_paths = [chunk["file_path"] for chunk in retrieved_chunks]

        found = False
        for _rank, path in enumerate(retrieved_paths):
            if path in relevant_files:
                metric.update(relevant_indices=[path], retrieved_indices=retrieved_paths)
                found = True
                break

        if not found:
            metric.update(relevant_indices=[], retrieved_indices=retrieved_paths)

    print(f"Recall@{top_k}: {metric.recall:.4f}")
    print(f"MRR@{top_k}: {metric.mrr:.4f}")
    return metric

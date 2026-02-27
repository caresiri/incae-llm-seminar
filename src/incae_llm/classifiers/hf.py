from __future__ import annotations

from typing import Sequence

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer


class HFTextClassifier:
    """Thin wrapper around Hugging Face sequence classification models."""

    def __init__(
        self,
        model_name_or_path: str,
        tokenizer_name_or_path: str | None = None,
        max_length: int = 128,
        device: str | None = None,
    ) -> None:
        self.max_length = max_length
        self.device = torch.device(device or ("cuda" if torch.cuda.is_available() else "cpu"))

        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name_or_path or model_name_or_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name_or_path)
        self.model.to(self.device)
        self.model.eval()

    @torch.inference_mode()
    def predict(self, texts: Sequence[str], batch_size: int = 16) -> tuple[list[int], list[float]]:
        labels: list[int] = []
        scores: list[float] = []

        for start in range(0, len(texts), batch_size):
            batch = list(texts[start : start + batch_size])
            encoded = self.tokenizer(
                batch,
                truncation=True,
                padding=True,
                max_length=self.max_length,
                return_tensors="pt",
            )
            encoded = {k: v.to(self.device) for k, v in encoded.items()}

            outputs = self.model(**encoded)
            probs = torch.softmax(outputs.logits, dim=-1)
            batch_scores, batch_labels = probs.max(dim=-1)

            labels.extend(batch_labels.cpu().tolist())
            scores.extend(batch_scores.cpu().tolist())

        return labels, scores

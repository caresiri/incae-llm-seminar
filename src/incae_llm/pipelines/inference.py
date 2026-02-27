from __future__ import annotations

from pathlib import Path

import pandas as pd

from incae_llm.classifiers.hf import HFTextClassifier
from incae_llm.config import load_session_config


def run_inference(config_file: str | Path) -> Path:
    config = load_session_config(config_file)
    frame = pd.read_csv(config.input_file)

    if config.text_column not in frame.columns:
        raise ValueError(f"Expected column '{config.text_column}' in {config.input_file}")

    classifier = HFTextClassifier(
        model_name_or_path=config.model_name_or_path,
        tokenizer_name_or_path=config.tokenizer_name_or_path,
        max_length=config.max_length,
    )

    labels, scores = classifier.predict(
        frame[config.text_column].astype(str).tolist(),
        batch_size=config.batch_size,
    )

    output = frame.copy()
    output["predicted_labels"] = labels
    output["predicted_scores"] = scores

    if config.label_map:
        output["predicted_label_name"] = [config.label_map.get(int(i), str(i)) for i in labels]

    output_path = Path(config.output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output.to_csv(output_path, index=False)
    return output_path

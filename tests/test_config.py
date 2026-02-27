from pathlib import Path

from incae_llm.config import load_session_config


def test_load_session_config_resolves_paths() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    config = load_session_config(repo_root / "configs" / "session1.yaml")

    assert Path(config.input_file).name == "session1_input.csv"
    assert Path(config.output_file).name == "NewSentence_Classified_DEI.csv"
    assert Path(config.model_name_or_path).name == "model_1"
    assert config.tokenizer_name_or_path == "distilbert-base-uncased"

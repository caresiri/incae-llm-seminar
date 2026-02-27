from pathlib import Path

from incae_llm.pipelines.inference import run_inference


def main() -> None:
    config_file = Path(__file__).resolve().parents[1] / "configs" / "session1.yaml"
    output_path = run_inference(config_file)
    print(f"Session 1 predictions saved to: {output_path}")


if __name__ == "__main__":
    main()


# INCAE LLM Seminar

This repository packages Session 1 and Session 2 instructional materials into a reusable project so anyone can clone, install, and run the classifiers.

## Project Layout

```text
INCAE LLM Seminar/
├─ src/incae_llm/                    # Shared Python package
├─ notebooks/session1/               # Session 1 notebook
├─ notebooks/session2/               # Session 2 notebook
├─ configs/                          # Session configs and data-source manifest
├─ data/
│  ├─ sample/                        # Lightweight demo input/output files
│  └─ raw/                           # Large/private data (gitignored)
├─ artifacts/local_models/           # Local model weights (gitignored)
├─ scripts/                          # Bootstrap + run scripts
├─ tests/                            # Lightweight tests
└─ .github/workflows/                # CI
```

## Quickstart

1. Clone and enter the project.
2. Create environment and install dependencies:

```bash
# Linux/macOS
./scripts/bootstrap.sh
```

```powershell
# Windows PowerShell
./scripts/bootstrap.ps1
```

3. Copy `.env.example` to `.env` and set any secrets (optional for local models).
4. Run one of the session pipelines:

```bash
python scripts/run_session1.py
python scripts/run_session2.py
```

```powershell
py -3 scripts/run_session1.py
py -3 scripts/run_session2.py
```

Outputs are written to `data/sample/` by default.

## Data and Models

- `data/raw/` and `artifacts/local_models/` are intentionally gitignored.
- Use `scripts/fetch_data.py` with `configs/data_sources.yaml` if you host data/model files externally.
- Keep only lightweight examples in `data/sample/`.

## CI

- `ci.yml`: installs package and runs `pytest`.
- `notebook-smoke-test.yml`: validates notebook JSON integrity and required files.

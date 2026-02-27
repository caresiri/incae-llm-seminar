# Getting Started

## 1. Install dependencies

```bash
./scripts/bootstrap.sh
```

or on Windows:

```powershell
./scripts/bootstrap.ps1
```

## 2. Verify setup

```bash
python -m pytest
python scripts/notebook_smoke_test.py
```

## 3. Run each session pipeline

```bash
python scripts/run_session1.py
python scripts/run_session2.py
```

```powershell
py -3 scripts/run_session1.py
py -3 scripts/run_session2.py
```

Outputs land in `data/sample/`.

## 4. Connect GitHub

```bash
git add .
git commit -m "Scaffold INCAE LLM seminar project"
git remote add origin <your-repo-url>
git push -u origin main
```

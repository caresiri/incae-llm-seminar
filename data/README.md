# Data

- `sample/`: lightweight CSV files for quick local runs.
- `raw/`: original training/evaluation assets. This folder is gitignored by default.

If you host datasets externally, add URLs to `configs/data_sources.yaml` and run:

```bash
python scripts/fetch_data.py --manifest configs/data_sources.yaml
```


# Data

This project is designed to be **fully reproducible** while avoiding accidental redistribution of data that may be subject to licensing.

By default, `data/raw/` is **git-ignored**. Your local ZIP includes the raw files so you can run everything immediately,
but they will not be pushed to GitHub unless you intentionally change `.gitignore`.

## Expected raw inputs

Place the following files under:

```
data/raw/
```

- `ipo_data.csv` — IPO metadata (company, PERMNO, IPO date)
- `return.csv` — monthly returns by PERMNO with market return column (`sprtrn`)
- `permnos.txt` — list of PERMNOs used in the analysis (optional helper)

A small, safe subset for quick demos is included under `data/sample/`.

## Using the sample data

To run a lightweight demo (fast, no large files), point `run.py` to sample files:

```bash
python run.py --ipo_csv data/sample/ipo_data_sample.csv --ret_csv data/sample/return_sample.csv
```

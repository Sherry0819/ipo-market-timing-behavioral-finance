# IPO Post‑Issue Returns: Market Timing & Limits to Arbitrage (Event Study)

This repository studies **post‑IPO abnormal return patterns** using a clean event‑time design and a market‑model benchmark.

## Research questions

1. **How dispersed is systematic risk across IPOs?**  
   Estimate each IPO’s market beta using post‑issue months 31–60.

2. **Do IPOs exhibit systematic abnormal returns shortly after issuance?**  
   Compute monthly abnormal returns (AR) and cumulative abnormal returns (CAR) over event months 1–30.

3. **Are return patterns consistent with limits to arbitrage?**  
   Re‑plot CARs for high vs low idiosyncratic volatility IPOs (measured by market‑model MSE in months 31–60).

4. **How sensitive are CARs to beta estimation choices?**  
   Compare the baseline CARs with a simple benchmark that assumes **beta = 1** for all IPOs.

## Method summary

- **Event time:** event month 1 is the first calendar month after the IPO month; then 2, 3, …  
- **Beta estimation window:** months 31–60  
- **Performance window:** months 1–30  
- **Market model:**  
Ri,t​=αi​+βi​Rm,t​+εi,t​

Abnormal return is the residual:  
ARi,t​=Ri,t​−(α^i​+β^​i​Rm,t​)

## Project layout

- `src/` — reusable modules (I/O, estimation, analysis, plots)
- `run.py` — one‑command replication script
- `reports/` — generated tables and figures

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python run.py
```

### Run with sample data (fast demo)

```bash
python run.py --ipo_csv data/sample/ipo_data_sample.csv --ret_csv data/sample/return_sample.csv
```

## Outputs

Running `python run.py` will create:

- `reports/beta_percentiles.csv` — 25/50/75th percentiles of beta
- `reports/avg_ar_car_1_30.csv` — average AR and CAR by event month
- `reports/figures/avg_ar_by_event_month.png`
- `reports/figures/car_1_30.png`
- `reports/figures/car_low_vs_high_ivol.png`
- `reports/figures/car_market_model_vs_beta1.png`

## Notes on data
Raw inputs often come from licensed sources; by default `data/raw/` is **git‑ignored** to avoid accidental redistribution.
See `data/README.md` for details.

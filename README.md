# MLOps Engineering Internship – Technical Assessment

This repository contains a miniature MLOps-style batch pipeline that demonstrates reproducibility, configuration-driven execution, structured logging, machine-readable metrics output, and Dockerized deployment.

The dataset used in this project is **real-world historical cryptocurrency OHLCV data sourced from Binance public data collections**. The raw exchange data was normalized into the required schema (`timestamp, open, high, low, close, volume_btc, volume_usd`) before being used by the pipeline.


##  Project Structure

mlops-task/
├── run.py
├── config.yaml
├── data.csv
├── requirements.txt
├── Dockerfile
├── README.md
├── metrics.json   # example output from a successful local run
├── run.log        # example log file from a successful local run


##  Setup Instructions

Ensure Python 3.x is installed.

pip install -r requirements.txt


##  Local Execution

Run the batch job locally using the required CLI:

python run.py --input data.csv --config config.yaml --output metrics.json --log-file run.log

This will:
- Load configuration from config.yaml  
- Process data.csv (real Binance OHLCV data)  
- Generate metrics.json  
- Write detailed logs to run.log  
- Print final metrics to stdout  


##  Docker Instructions (Mandatory)

### Build the Docker image
docker build -t mlops-task .

### Run the container
docker run --rm mlops-task

The container:
- Executes the batch job on startup  
- Prints final metrics to stdout  
- Exits with code 0 on success (non-zero on failure)  


##  Expected Output (metrics.json structure)

{
  "version": "v1",
  "rows_processed": 44640,
  "metric": "signal_rate",
  "value": 0.5006,
  "latency_ms": 83,
  "seed": 42,
  "status": "success"
}

If an error occurs, the output follows:

{
  "version": "v1",
  "status": "error",
  "error_message": "Description of what went wrong"
}


## 🧾 Logging

Logs are written to run.log and include:
- Job start timestamp  
- Configuration verification (seed, window, version)  
- Data ingestion summary (rows loaded)  
- Processing steps (rolling mean calculation, signal generation)  
- Metrics summary  
- Job completion status and latency  
- Error details (if any)  


## Dependencies

- pandas  
- numpy  
- pyyaml  

(Defined in requirements.txt)

## Reproducibility

- Deterministic execution via seeded randomness (seed in config.yaml)  
- Configuration-driven window size and versioning  
- Identical inputs and configuration produce identical outputs across runs  


## Notes

- The pipeline processes OHLCV data using the close column for all calculations.  
- The dataset is based on **real Binance historical market data** (publicly available) and converted to the required CSV schema for this assessment.  
- The solution was validated both locally and via Docker:
  - docker build -t mlops-task .
  - docker run --rm mlops-task
- This project is implemented as a batch job, not a web service. 


##  Interview-ready Summary

The solution implements a reproducible, Dockerized batch pipeline with structured logging and machine-readable metrics, using real-world Binance OHLCV data, validated both locally and inside the container.
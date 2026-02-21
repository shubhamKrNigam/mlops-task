import argparse
import json
import logging
import os
import sys
import time
import yaml
import numpy as np
import pandas as pd


def setup_logger(log_file):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def load_config(config_path):
    if not os.path.exists(config_path):
        raise FileNotFoundError("Config file not found")

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    required_keys = ["seed", "window", "version"]
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing key in config: {key}")

    return config


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--log-file", required=True)
    args = parser.parse_args()

    start_time = time.time()
    status = "success"

    try:
        setup_logger(args.log_file)
        logging.info("Job started")

        config = load_config(args.config)
        seed = config["seed"]
        window = config["window"]
        version = config["version"]

        np.random.seed(seed)
        logging.info(f"Config loaded: seed={seed}, window={window}, version={version}")

        if not os.path.exists(args.input):
            raise FileNotFoundError("Input CSV file not found")

        df = pd.read_csv(args.input)

        if df.empty:
            raise ValueError("Input CSV file is empty")

        if "close" not in df.columns:
            raise ValueError("Missing required column: close")

        rows_processed = len(df)
        logging.info(f"Data loaded: {rows_processed} rows")

        df["rolling_mean"] = df["close"].rolling(window=window).mean()
        logging.info(f"Rolling mean calculated with window={window}")

        df["signal"] = (df["close"] > df["rolling_mean"]).astype(int)
        logging.info("Signals generated")

        signal_rate = float(df["signal"].mean(skipna=True))

        latency_ms = int((time.time() - start_time) * 1000)

        metrics = {
            "version": version,
            "rows_processed": rows_processed,
            "metric": "signal_rate",
            "value": round(signal_rate, 4),
            "latency_ms": latency_ms,
            "seed": seed,
            "status": "success"
        }

        with open(args.output, "w") as f:
            json.dump(metrics, f, indent=2)

        logging.info(f"Metrics: signal_rate={signal_rate:.4f}, rows_processed={rows_processed}")
        logging.info(f"Job completed successfully in {latency_ms}ms")

        print(json.dumps(metrics, indent=2))

    except Exception as e:
        status = "error"
        error_metrics = {
            "version": "v1",
            "status": "error",
            "error_message": str(e)
        }

        with open(args.output, "w") as f:
            json.dump(error_metrics, f, indent=2)

        logging.error(f"Job failed: {str(e)}")
        print(json.dumps(error_metrics, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
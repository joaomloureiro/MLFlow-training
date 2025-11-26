import argparse
import pandas as pd
import requests
from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(description="Batch inference via MLflow model server")
    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Path to input CSV with feature columns",
    )
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Path to output CSV with predictions",
    )
    parser.add_argument(
        "--url",
        type=str,
        default="http://127.0.0.1:5001/invocations",
        help="MLflow server /invocations URL",
    )
    return parser.parse_args()

def main():
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)

    # Read input data
    df = pd.read_csv(input_path)

    # Optional: ensure column order matches training
    # For California housing:
    expected_cols = [
        "MedInc", "HouseAge", "AveRooms", "AveBedrms",
        "Population", "AveOccup", "Latitude", "Longitude",
    ]
    if set(expected_cols) <= set(df.columns):
        df = df[expected_cols]
    
    # Build payload for MLflow pyfunc server
    payload = {
        "dataframe_split": df.to_dict(orient="split")
    }

    # Send POST request
    resp = requests.post(args.url, json=payload)
    resp.raise_for_status()

    preds = resp.json()
    
    # Handle both possible response formats
    if isinstance(preds, dict) and "predictions" in preds:
        pred_values = preds["predictions"]
    else:
        pred_values = preds

    if len(pred_values) != len(df):
        raise ValueError(
            f"Number of predictions ({len(pred_values)}) "
            f"does not match number of rows ({len(df)})"
        )
    
    # Save predictions alongside original data
    df_out = df.copy()
    df_out["prediction"] = pred_values
    df_out.to_csv(output_path, index=False)

    print(f"Wrote {len(df_out)} predictions to {output_path}")

if __name__ == "__main__":
    main()

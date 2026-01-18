import pandas as pd
import argparse
import os
from datetime import datetime

def process_file(input_path, output_path):
    print(f"Processing {input_path} -> {output_path}")
    df = pd.read_csv(input_path)
    df['processed_at'] = datetime.now()
    df['source_file'] = os.path.basename(input_path)
    df.to_csv(output_path, index=False)
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, help='Input CSV file')
    parser.add_argument('--output', required=True, help='Output CSV file')
    args = parser.parse_args()
    
    process_file(args.input, args.output)

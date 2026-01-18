import pandas as pd
import argparse
import os

def combine_files(input_paths, output_path):
    print(f"Combining {len(input_paths)} files into {output_path}")
    dfs = [pd.read_csv(f) for f in input_paths]
    combined_df = pd.concat(dfs, ignore_index=True)
    combined_df.to_csv(output_path, index=False)
    print("Combined Data:")
    print(combined_df)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--inputs', nargs='+', required=True, help='Input CSV files')
    parser.add_argument('--output', required=True, help='Output CSV file')
    args = parser.parse_args()
    
    combine_files(args.inputs, args.output)

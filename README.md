# ds_flow

A data processing framework example using **Netflix Metaflow**, **Python**, and **Bash**.

This project demonstrates a polyglot pipeline where:
1.  **Orchestration**: Managed by Metaflow.
2.  **Processing**: Performed by Python scripts (Pandas).
3.  **Aggregation**: Performed by Bash scripts.
4.  **Dependency Management**: Handled by `uv`.

## Project Structure

```
ds_flow/
├── flow.py              # Main Metaflow pipeline definition
├── pyproject.toml       # Python dependencies (uv)
├── data/                # Input and Output data
│   ├── student_1.csv    # Test input 1
│   └── student_2.csv    # Test input 2
├── scripts/
│   └── process.py       # Python script for individual file processing
└── bash/
    └── combine.sh       # Bash script for merging CSV files
```

## Prerequisites

-   **Python 3.10+**
-   **uv**: Used for fast python package management.
    ```bash
    pip install uv
    # or
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

## Installation

1.  Navigate to the project directory:
    ```bash
    cd ds_flow
    ```

2.  Sync dependencies:
    ```bash
    uv sync
    ```

## Usage

Run the pipeline using the `uv run` command to ensure dependencies are loaded correctly:

```bash
uv run python flow.py run
```

### What happens?

1.  **Start**: The flow finds all `student_*.csv` files in the `data/` directory.
2.  **Process (`process.py`)**: 
    -   Runs in parallel for each file.
    -   Adds `processed_at` timestamp and `source_file` column.
    -   Saves to `data/processed_<filename>`.
3.  **Combine (`combine.sh`)**:
    -   Takes all processed files.
    -   Concatenates them into a single CSV using Bash.
    -   Preserves the header from the first file.
4.  **End**: success message and location of the final file (`data/final_combined.csv`).

## Output

The final result is saved to `data/final_combined.csv`.

Example content:
```csv
student_name,processed_at,source_file
Alice,2026-01-17 20:30:00.123456,student_1.csv
Bob,2026-01-17 20:30:00.123456,student_1.csv
Charlie,2026-01-17 20:30:00.123456,student_2.csv
David,2026-01-17 20:30:00.123456,student_2.csv
```

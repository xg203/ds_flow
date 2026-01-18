# ds_flow

A data processing framework example using **Netflix Metaflow**, **Python**, and **Bash**.

This project demonstrates a polyglot pipeline where:
1.  **Orchestration**: Managed by Metaflow.
2.  **Processing**: Performed by Python scripts (Pandas).
3.  **Aggregation**: Performed by Bash scripts.
4.  **HPC Integration**: Submits jobs to LSF queues.
5.  **Configuration**: Managed via Environment Variables.

## Project Structure

```
ds_flow/
├── flow.py              # Main Metaflow pipeline definition
├── .env                 # Environment variables config
├── pyproject.toml       # Python dependencies (uv)
├── bsub                 # Mock LSF submission script (for local testing)
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
-   **LSF Cluster** (Optional): If running on HPC, `bsub` should be available in PATH.

## Installation

1.  Navigate to the project directory:
    ```bash
    cd ds_flow
    ```

2.  Sync dependencies:
    ```bash
    uv sync
    ```

## Configuration

Create or edit the `.env` file to set processing parameters:

```bash
PROCESS_TAG=v1-env-tagged
```

This tag will be added as a column to the processed data.

## Usage

Run the pipeline using the `uv run` command:

```bash
uv run python flow.py run
```

### what happens?

1.  **Start**: The flow finds all `student_*.csv` files in the `data/` directory.
2.  **Process (`process.py`)**: 
    -   Runs in parallel for each file.
    -   Reads `PROCESS_TAG` from the environment.
    -   Adds `processed_at`, `source_file`, and `tag` columns.
    -   Saves to `data/processed_<filename>`.
3.  **Combine (`bash/combine.sh`)**:
    -   **LSF Submission**: This step is submitted to the **LSF 'short' queue** using `bsub -q short -K`.
    -   Concatenates processed files into a single CSV.
4.  **End**: Success message and location of `data/final_combined.csv`.

## Local Testing (Mock LSF)

The project includes a mock `bsub` script in the root directory. This allows you to verify the LSF submission logic locally without an actual cluster. Most execution environments will prioritize the local `./bsub` if strictly configured, but usually you might need to ensure it's used if testing locally. The `flow.py` temporarily adds the current directory to `PATH` to ensure this mock is found during local runs.

---
*This project has been assisted by Antigravity version 1.14.2*

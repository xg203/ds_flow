# ds_flow

A data processing framework example using **Netflix Metaflow**, **Python**, and **Bash**.

This project demonstrates a polyglot pipeline where:
1.  **Orchestration**: Managed by Metaflow.
2.  **Processing**: Performed by Python scripts (Pandas).
3.  **Aggregation**: Performed by Bash scripts via LSF.
4.  **Analysis**: Performed by Docker containers.
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
-   **Docker**: Required for the final analysis step.
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

### What happens?

1.  **Start**: The flow finds all `student_*.csv` files in the `data/` directory.
2.  **Process**: 
    -   Runs in parallel for each file.
    -   Adds metadata and environment tags.
    -   Saves to `data/processed_<filename>`.
3.  **Combine**:
    -   **LSF Submission**: Submits the bash script to the **LSF 'short' queue**.
    -   Concatenates processed files into a single CSV.
4.  **Analyze**:
    -   **Docker**: Mounting the `data` directory to an `ubuntu` container.
    -   runs `wc -l` to count the lines in the final file.
5.  **End**: Success message.

## Debugging and Logs

### Viewing Logs
By default, logs are printed to the terminal. To save them to a file:

```bash
uv run python flow.py run > pipeline.log 2>&1
```

To view logs for a specific past run using Metaflow:
```bash
# List recent runs
uv run python flow.py show

# Show logs for a specific run and step
uv run python flow.py logs <RunID>/start
```

### Common Issues
-   **Docker Failed**: If you see "Docker command returned non-zero exit status", ensure Docker is running (`docker info`).
-   **LSF Issues**: If the `join` step hangs, check the `bsub` mock or your cluster queue status.

## Local Testing (Mock LSF)

The project includes a mock `bsub` script in the root directory. This allows you to verify the LSF submission logic locally without an actual cluster.

---
*This project has been assisted by Antigravity version 1.14.2*

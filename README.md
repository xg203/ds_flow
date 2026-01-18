# ds_flow

A production-grade data processing framework using **Netflix Metaflow**, **Python**, and **Bash**.

This project demonstrates a polyglot pipeline engineered for reliability and scale.

## Key Features

1.  **Polyglot Processing**: Seamlessly integrates Python for data science (Pandas) and Bash for high-performance file manipulation.
2.  **Orchestration**: Managed by Metaflow, handling state, retries, and parallelism.
3.  **Production Best Practices**:
    *   **Configuration Management**: Uses `config/settings.yaml` to decouple code from parameters.
    *   **Artifact Versioning**: All output files are tagged with the unique Run ID (e.g., `processed_file_1768...csv`), ensuring complete reproducibility and lineage tracking.
    *   **Structured Logging**: Uses Python's logging module for standardized, timestamped logs. Logs are saved to `log/`.
4.  **HPC & Container Integration**: Supports submitting jobs to LSF queues and running analysis in Docker containers.

## Project Structure

```
ds_flow/
├── flow.py              # Main Metaflow pipeline
├── config/
│   └── settings.yaml    # Centralized configuration
├── .env                 # Secrets/Env variables
├── out/                 # Output artifacts (ignored by git)
├── log/                 # Persistent logs (ignored by git)
├── data/                # Input data
├── scripts/
│   └── process.py       # Python processing script
└── bash/
    └── combine.sh       # Bash merging script
```

## Installation

```bash
cd ds_flow
uv sync
```

## Configuration

Edit `config/settings.yaml` to control pipeline behavior:

```yaml
project_name: ds_flow
paths:
  input_pattern: "data/student_*.csv"
  output_dir: "out"
  log_dir: "log"
compute:
  lsf_queue: "short"
```

## Usage

```bash
uv run python flow.py run
```

### Output Lineage
The pipeline produces versioned artifacts in the `out/` directory:
-   `out/processed_student_1_<RunID>.csv`
-   `out/final_combined_<RunID>.csv`

## Debugging and Logs

### Viewing Logs
Logs are saved to `log/run_<RunID>.log` and printed to the terminal.

To view logs for a specific past run using Metaflow:
```bash
uv run python flow.py logs <RunID>/start
```

---
*This project has been assisted by Antigravity version 1.14.2*

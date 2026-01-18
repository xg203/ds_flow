# ds_flow

A production-grade data processing framework using **Netflix Metaflow**, **Python**, and **Bash**.

This project demonstrates a polyglot pipeline engineered for reliability and scale.

## Key Features

1.  **Polyglot Processing**: Seamlessly integrates Python for data science (Pandas) and Bash for high-performance file manipulation.
2.  **Orchestration**: Managed by Metaflow, handling state, retries, and parallelism.
3.  **Production Best Practices**:
    *   **Configuration Management**: Uses `config/settings.yaml` to decouple code from parameters.
    *   **Artifact Versioning**: All output files are tagged with the unique Run ID (e.g., `processed_file_1768...csv`), ensuring complete reproducibility and lineage tracking.
    *   **Structured Logging**: Uses Python's logging module for standardized, timestamped logs instead of `print` statements.
4.  **HPC & Container Integration**: Supports submitting jobs to LSF queues and running analysis in Docker containers.

## Project Structure

```
ds_flow/
├── flow.py              # Main Metaflow pipeline
├── config/
│   └── settings.yaml    # Centralized configuration
├── .env                 # Secrets/Env variables
├── pyproject.toml       # Python dependencies (uv)
├── bsub                 # Mock LSF script
├── data/                # Data artifacts (Versioned)
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
compute:
  lsf_queue: "short"
```

## Usage

```bash
uv run python flow.py run
```

### Output Lineage
Instead of overwriting files, the pipeline produces versioned artifacts:
-   `data/processed_student_1_<RunID>.csv`
-   `data/final_combined_<RunID>.csv`

This allows you to look back at the exact state of data for any historical run.

## Debugging and Logs

### Viewing Logs
Logs are formatted with timestamps and severity levels:
```
2026-01-17 21:21:00,508 - ds_flow - INFO - Loaded config: {...}
```

To save logs to a file:
```bash
uv run python flow.py run > pipeline.log 2>&1
```

## Local Testing (Mock LSF)
The included `bsub` script allows for local verification of HPC logic.

---
*This project has been assisted by Antigravity version 1.14.2*

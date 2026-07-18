# Data Generator (Phase 1)

This module creates synthetic Netflix-style streaming events and writes them to a parquet file for downstream Bronze ingestion.

## Output

- Format: Parquet (`snappy` compression)
- File: `netflix_streaming_events.parquet`
- Schema source: `data-generator/schemas.py`

## Event Model

Each event contains the following fields:

- `event_id`: deterministic event identifier (`evt_##########`)
- `user_id`: synthetic user key (`user_######`)
- `content_id`: content key from the catalog
- `event_type`: playback/search/system style event type
- `timestamp`: realistic UTC timestamp with deterministic jitter
- `device`: device category (mobile, TV, web, console, etc.)
- `country`: ISO-like country code
- `session_id`: synthetic session key (`session_##########`)

## How Timestamps Work

Timestamps are deterministic so repeated runs are reproducible:

- Events are grouped into sessions (`EVENTS_PER_SESSION`)
- Session start times are spread across days and minute-of-day windows
- Events within each session move forward in time
- A small hash-based jitter avoids identical second-level timestamps

This produces realistic time variation without introducing randomness that breaks reproducibility.

## Run the Generator

From the project root:

```bash
python data-generator/generator.py
```

## Dependencies

Install Python dependencies from the repository root:

```bash
pip install -r requirements.txt
```

Key runtime dependencies for this module:

- `pandas`
- `pyarrow`

## Notes

- Generation uses a full cartesian combination of catalog pools.
- Output is intentionally large and can take significant time/disk.
- Existing parquet output file is replaced at the start of each run.

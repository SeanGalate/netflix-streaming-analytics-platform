from __future__ import annotations

import hashlib
from dataclasses import asdict
from datetime import UTC, datetime, timedelta
from itertools import product
from pathlib import Path

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from content import (
	CONTENT_IDS,
	COUNTRIES,
	DEVICES,
	EVENT_TYPES,
)
from schemas import StreamingEvent

# Generator configuration
NUM_USERS = 10_000
OUTPUT_FILE = Path("netflix_streaming_events.parquet")
SIMULATION_START = datetime(2026, 1, 1, 0, 0, 0, tzinfo=UTC)
EVENTS_PER_SESSION = 24


def generate_user_id(event_index: int) -> str:
	"""Generate a user ID from the event index."""
	user_num = ((event_index - 1) % NUM_USERS) + 1
	return f"user_{user_num:06d}"


def generate_session_id(event_index: int) -> str:
	"""Generate a session ID from the event index."""
	session_num = ((event_index - 1) // EVENTS_PER_SESSION) + 1
	return f"session_{session_num:010d}"


def generate_realistic_timestamp(event_index: int) -> datetime:
	"""Generate deterministic but realistic UTC timestamps for user sessions.

	The timeline advances in sessions and adds small per-event jitter so records
	look natural while remaining reproducible across runs.
	"""
	session_num = ((event_index - 1) // EVENTS_PER_SESSION) + 1

	# Spread sessions over the year with a rotating minute-of-day start.
	day_offset = (session_num - 1) % 365
	minute_of_day = ((session_num - 1) * 17) % (24 * 60)
	session_start = SIMULATION_START + timedelta(days=day_offset, minutes=minute_of_day)

	# Events progress inside a session.
	event_in_session = (event_index - 1) % EVENTS_PER_SESSION
	intra_session_seconds = event_in_session * 45

	# Stable jitter derived from the event index keeps timestamps varied.
	hash_hex = hashlib.sha256(str(event_index).encode("utf-8")).hexdigest()
	jitter_seconds = int(hash_hex[:2], 16) % 25

	return session_start + timedelta(seconds=intra_session_seconds + jitter_seconds)


def generate_all_streaming_events() -> None:
	"""Generate all possible streaming event combinations and write to parquet file.
	
	Generates every combination of content_id, event_type, device, and country.
	This produces 103,455,000+ unique events (550 * 30 * 33 * 190).
	
	Events are batched and written to a single parquet file for efficient storage.
	"""
	events_batch = []
	batch_size = 100_000  # Write in batches for memory efficiency
	total_events = 0
	writer = None

	if OUTPUT_FILE.exists():
		OUTPUT_FILE.unlink()
	
	try:
		for event_index, (content_id, event_type, device, country) in enumerate(
			product(CONTENT_IDS, EVENT_TYPES, DEVICES, COUNTRIES), start=1
		):
			user_id = generate_user_id(event_index)
			session_id = generate_session_id(event_index)
			timestamp = generate_realistic_timestamp(event_index)
			
			event = StreamingEvent(
				event_id=f"evt_{event_index:010d}",
				user_id=user_id,
				content_id=content_id,
				event_type=event_type,
				timestamp=timestamp,
				device=device,
				country=country,
				session_id=session_id,
			)
			
			events_batch.append(asdict(event))
			total_events += 1
			
			if len(events_batch) >= batch_size:
				df = pd.DataFrame(events_batch)
				table = pa.Table.from_pandas(df, preserve_index=False)
				if writer is None:
					writer = pq.ParquetWriter(OUTPUT_FILE, table.schema, compression="snappy")
				writer.write_table(table)
				
				if total_events % 1_000_000 == 0:
					print(f"Generated and wrote {total_events:,} events...")
				
				events_batch = []

		if events_batch:
			df = pd.DataFrame(events_batch)
			table = pa.Table.from_pandas(df, preserve_index=False)
			if writer is None:
				writer = pq.ParquetWriter(OUTPUT_FILE, table.schema, compression="snappy")
			writer.write_table(table)
	finally:
		if writer is not None:
			writer.close()
	
	print(f"\nTotal events generated and written to {OUTPUT_FILE}: {total_events:,}")


def main() -> None:
	"""Generate and write all streaming events to parquet file."""
	print(f"Starting event generation (103,455,000+ events)...")
	generate_all_streaming_events()
	print("Event generation complete!")


if __name__ == "__main__":
	main()

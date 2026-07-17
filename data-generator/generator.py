from __future__ import annotations

import hashlib
from dataclasses import asdict
from datetime import UTC, datetime
from itertools import product
from pathlib import Path

import pandas as pd

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


def generate_user_id(event_index: int) -> str:
	"""Generate a user ID from the event index."""
	user_num = (event_index % NUM_USERS) + 1
	return f"user_{user_num:06d}"


def generate_session_id(event_index: int) -> str:
	"""Generate a session ID from the event index."""
	return f"session_{event_index:010d}"


def generate_all_streaming_events() -> None:
	"""Generate all possible streaming event combinations and write to parquet file.
	
	Generates every combination of content_id, event_type, device, and country.
	This produces 103,455,000+ unique events (550 * 30 * 33 * 190).
	
	Events are batched and written to a parquet file for efficient storage.
	"""
	timestamp = datetime(2026, 7, 13, 20, 30, 0, tzinfo=UTC)
	events_batch = []
	batch_size = 100_000  # Write in batches for memory efficiency
	total_events = 0
	
	for event_index, (content_id, event_type, device, country) in enumerate(
		product(CONTENT_IDS, EVENT_TYPES, DEVICES, COUNTRIES), start=1
	):
		user_id = generate_user_id(event_index)
		session_id = generate_session_id(event_index)
		
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
		
		# Write batch to parquet file
		if len(events_batch) >= batch_size:
			df = pd.DataFrame(events_batch)
			
			# Append mode: use mode='append' if file exists
			if OUTPUT_FILE.exists():
				df.to_parquet(OUTPUT_FILE, engine="pyarrow", compression="snappy", index=False, append=True)
			else:
				df.to_parquet(OUTPUT_FILE, engine="pyarrow", compression="snappy", index=False)
			
			if total_events % 1_000_000 == 0:
				print(f"Generated and wrote {total_events:,} events...")
			
			events_batch = []
	
	# Write remaining events
	if events_batch:
		df = pd.DataFrame(events_batch)
		if OUTPUT_FILE.exists():
			df.to_parquet(OUTPUT_FILE, engine="pyarrow", compression="snappy", index=False, append=True)
		else:
			df.to_parquet(OUTPUT_FILE, engine="pyarrow", compression="snappy", index=False)
	
	print(f"\nTotal events generated and written to {OUTPUT_FILE}: {total_events:,}")


def main() -> None:
	"""Generate and write all streaming events to parquet file."""
	print(f"Starting event generation (103,455,000+ events)...")
	generate_all_streaming_events()
	print("Event generation complete!")


if __name__ == "__main__":
	main()

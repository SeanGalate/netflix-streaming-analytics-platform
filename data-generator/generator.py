from __future__ import annotations

import json
from dataclasses import asdict
from datetime import UTC, datetime

from content import (
	CONTENT_ID,
	COUNTRY,
	DEVICE,
	EVENT_TYPE,
)
from schemas import StreamingEvent


def build_sample_streaming_event() -> StreamingEvent:
	"""Create one fixed streaming event for schema and JSON validation."""

	return StreamingEvent(
		event_id="evt_20260713_0001",
		user_id="user_1024",
		content_id=CONTENT_ID,
		event_type=EVENT_TYPE,
		timestamp=datetime(2026, 7, 13, 20, 30, 0, tzinfo=UTC),
		device=DEVICE,
		country=COUNTRY,
		session_id="sess_8f3c2a91",
	)


def streaming_event_to_json(event: StreamingEvent) -> str:
	"""Serialize a streaming event into formatted JSON."""

	event_payload = asdict(event)
	event_payload["timestamp"] = event.timestamp.isoformat()
	return json.dumps(event_payload, indent=4)


def main() -> None:
	"""Build and print one sample streaming event as formatted JSON."""

	event = build_sample_streaming_event()
	print(streaming_event_to_json(event))


if __name__ == "__main__":
	main()

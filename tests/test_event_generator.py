from __future__ import annotations

import importlib.util
from datetime import UTC, datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
GENERATOR_DIR = PROJECT_ROOT / "data-generator"
GENERATOR_PATH = GENERATOR_DIR / "generator.py"

spec = importlib.util.spec_from_file_location("generator", GENERATOR_PATH)
if spec is None or spec.loader is None:
	raise ImportError(f"Unable to load generator module from {GENERATOR_PATH}")

generator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generator)


def test_generate_user_id_wraps_within_configured_population() -> None:
	first_user = generator.generate_user_id(1)
	wrapped_user = generator.generate_user_id(generator.NUM_USERS + 1)

	assert first_user == "user_000001"
	assert wrapped_user == "user_000001"


def test_generate_session_id_groups_events_per_session() -> None:
	first = generator.generate_session_id(1)
	same_session = generator.generate_session_id(generator.EVENTS_PER_SESSION)
	next_session = generator.generate_session_id(generator.EVENTS_PER_SESSION + 1)

	assert first == "session_0000000001"
	assert same_session == "session_0000000001"
	assert next_session == "session_0000000002"


def test_generate_realistic_timestamp_is_utc_and_deterministic() -> None:
	ts_one = generator.generate_realistic_timestamp(42)
	ts_two = generator.generate_realistic_timestamp(42)

	assert ts_one.tzinfo is UTC
	assert ts_one == ts_two
	assert isinstance(ts_one, datetime)


def test_timestamps_progress_inside_single_session() -> None:
	first_event = generator.generate_realistic_timestamp(1)
	later_event = generator.generate_realistic_timestamp(2)

	assert later_event > first_event

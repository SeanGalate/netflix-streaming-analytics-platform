from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class StreamingEvent:
	"""Canonical schema for a single Netflix streaming event.

	This model defines the minimum event contract that downstream systems can
	rely on before we introduce event generation, validation, or persistence.
	"""

	event_id: str
	user_id: str
	content_id: str
	event_type: str
	timestamp: datetime
	device: str
	country: str
	session_id: str


__all__ = ["StreamingEvent"]

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from j1939.address_claim import J1939AddressClaim


@dataclass(frozen=True)
class AddressClaimEvent:
    """Record an event involving a J1939 address claim."""

    claim: J1939AddressClaim
    event_type: str
    timestamp: datetime
    previous_claim: J1939AddressClaim | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.claim, J1939AddressClaim):
            raise TypeError("claim must be a J1939AddressClaim")

        if not isinstance(self.event_type, str) or not self.event_type.strip():
            raise ValueError("event_type must be a non-empty string")

        if not isinstance(self.timestamp, datetime):
            raise TypeError("timestamp must be a datetime")

        if self.timestamp.tzinfo is None:
            raise ValueError("timestamp must be timezone-aware")

        if self.previous_claim is not None and not isinstance(
            self.previous_claim,
            J1939AddressClaim,
        ):
            raise TypeError(
                "previous_claim must be a J1939AddressClaim or None"
            )

    @classmethod
    def create(
        cls,
        claim: J1939AddressClaim,
        event_type: str,
        previous_claim: J1939AddressClaim | None = None,
    ) -> "AddressClaimEvent":
        """Create an event using the current UTC time."""
        return cls(
            claim=claim,
            event_type=event_type,
            timestamp=datetime.now(timezone.utc),
            previous_claim=previous_claim,
        )

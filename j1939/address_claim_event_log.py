from __future__ import annotations

from dataclasses import dataclass, field

from j1939.address_claim_event import AddressClaimEvent


@dataclass
class AddressClaimEventLog:
    """Store and query J1939 address-claim events."""

    _events: list[AddressClaimEvent] = field(default_factory=list)

    def add(self, event: AddressClaimEvent) -> None:
        """Add an address-claim event to the log."""
        if not isinstance(event, AddressClaimEvent):
            raise TypeError("event must be an AddressClaimEvent")

        self._events.append(event)

    def all_events(self) -> tuple[AddressClaimEvent, ...]:
        """Return all recorded events in insertion order."""
        return tuple(self._events)

    def for_source_address(
        self,
        source_address: int,
    ) -> tuple[AddressClaimEvent, ...]:
        """Return events associated with a source address."""
        if not 0 <= source_address <= 0xFF:
            raise ValueError("source_address must be between 0 and 255")

        return tuple(
            event
            for event in self._events
            if event.claim.source_address == source_address
        )

    def for_event_type(
        self,
        event_type: str,
    ) -> tuple[AddressClaimEvent, ...]:
        """Return events matching an event type."""
        if not isinstance(event_type, str) or not event_type.strip():
            raise ValueError("event_type must be a non-empty string")

        return tuple(
            event
            for event in self._events
            if event.event_type == event_type
        )

    def clear(self) -> None:
        """Remove all recorded events."""
        self._events.clear()

    def __len__(self) -> int:
        """Return the number of recorded events."""
        return len(self._events)

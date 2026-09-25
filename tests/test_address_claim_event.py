from datetime import datetime, timezone

import pytest

from j1939.address_claim import J1939AddressClaim
from j1939.address_claim_event import AddressClaimEvent


def test_create_event_uses_current_utc_time():
    claim = J1939AddressClaim(source_address=0x80, name=0x1000)

    event = AddressClaimEvent.create(
        claim=claim,
        event_type="claim_received",
    )

    assert event.claim == claim
    assert event.event_type == "claim_received"
    assert event.timestamp.tzinfo is not None
    assert event.timestamp.utcoffset() == timezone.utc.utcoffset(
        event.timestamp
    )
    assert event.previous_claim is None


def test_event_can_store_previous_claim():
    claim = J1939AddressClaim(source_address=0x80, name=0x1000)
    previous = J1939AddressClaim(source_address=0x80, name=0x2000)

    event = AddressClaimEvent.create(
        claim=claim,
        event_type="claim_replaced",
        previous_claim=previous,
    )

    assert event.claim == claim
    assert event.previous_claim == previous


def test_event_accepts_timezone_aware_timestamp():
    claim = J1939AddressClaim(source_address=0x80, name=0x1000)
    timestamp = datetime(2026, 1, 1, tzinfo=timezone.utc)

    event = AddressClaimEvent(
        claim=claim,
        event_type="claim_received",
        timestamp=timestamp,
    )

    assert event.timestamp == timestamp


def test_event_rejects_invalid_claim():
    timestamp = datetime.now(timezone.utc)

    with pytest.raises(TypeError, match="J1939AddressClaim"):
        AddressClaimEvent(
            claim=object(),
            event_type="claim_received",
            timestamp=timestamp,
        )


def test_event_rejects_empty_event_type():
    claim = J1939AddressClaim(source_address=0x80, name=0x1000)
    timestamp = datetime.now(timezone.utc)

    with pytest.raises(ValueError, match="non-empty"):
        AddressClaimEvent(
            claim=claim,
            event_type="   ",
            timestamp=timestamp,
        )


def test_event_rejects_invalid_event_type():
    claim = J1939AddressClaim(source_address=0x80, name=0x1000)
    timestamp = datetime.now(timezone.utc)

    with pytest.raises(ValueError, match="non-empty"):
        AddressClaimEvent(
            claim=claim,
            event_type="",
            timestamp=timestamp,
        )


def test_event_rejects_naive_timestamp():
    claim = J1939AddressClaim(source_address=0x80, name=0x1000)
    timestamp = datetime(2026, 1, 1)

    with pytest.raises(ValueError, match="timezone-aware"):
        AddressClaimEvent(
            claim=claim,
            event_type="claim_received",
            timestamp=timestamp,
        )


def test_event_rejects_invalid_timestamp_type():
    claim = J1939AddressClaim(source_address=0x80, name=0x1000)

    with pytest.raises(TypeError, match="datetime"):
        AddressClaimEvent(
            claim=claim,
            event_type="claim_received",
            timestamp="2026-01-01",
        )


def test_event_rejects_invalid_previous_claim():
    claim = J1939AddressClaim(source_address=0x80, name=0x1000)
    timestamp = datetime.now(timezone.utc)

    with pytest.raises(TypeError, match="J1939AddressClaim"):
        AddressClaimEvent(
            claim=claim,
            event_type="claim_received",
            timestamp=timestamp,
            previous_claim=object(),
        )

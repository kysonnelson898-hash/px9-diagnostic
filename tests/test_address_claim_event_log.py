from datetime import datetime, timezone

import pytest

from j1939.address_claim import J1939AddressClaim
from j1939.address_claim_event import AddressClaimEvent
from j1939.address_claim_event_log import AddressClaimEventLog


def make_event(source_address=0x80, name=0x1000, event_type="claim_received"):
    claim = J1939AddressClaim(source_address=source_address, name=name)
    return AddressClaimEvent(
        claim=claim,
        event_type=event_type,
        timestamp=datetime.now(timezone.utc),
    )


def test_add_event():
    log = AddressClaimEventLog()
    event = make_event()
    log.add(event)
    assert log.all_events() == (event,)
    assert len(log) == 1


def test_events_are_returned_in_insertion_order():
    log = AddressClaimEventLog()
    first = make_event(name=0x1000)
    second = make_event(name=0x2000)
    log.add(first)
    log.add(second)
    assert log.all_events() == (first, second)


def test_filter_by_source_address():
    log = AddressClaimEventLog()
    first = make_event(source_address=0x80)
    second = make_event(source_address=0x81)
    third = make_event(source_address=0x80)

    for event in (first, second, third):
        log.add(event)

    assert log.for_source_address(0x80) == (first, third)


def test_filter_by_event_type():
    log = AddressClaimEventLog()
    first = make_event(event_type="claim_received")
    second = make_event(event_type="claim_lost")
    third = make_event(event_type="claim_received")

    for event in (first, second, third):
        log.add(event)

    assert log.for_event_type("claim_received") == (first, third)


def test_clear_removes_events():
    log = AddressClaimEventLog()
    log.add(make_event())
    log.clear()

    assert log.all_events() == ()
    assert len(log) == 0


def test_add_rejects_invalid_event():
    log = AddressClaimEventLog()

    with pytest.raises(TypeError, match="AddressClaimEvent"):
        log.add(object())


def test_source_address_validation():
    log = AddressClaimEventLog()

    with pytest.raises(ValueError, match="between 0 and 255"):
        log.for_source_address(-1)

    with pytest.raises(ValueError, match="between 0 and 255"):
        log.for_source_address(256)


def test_event_type_validation():
    log = AddressClaimEventLog()

    with pytest.raises(ValueError, match="non-empty"):
        log.for_event_type("")

    with pytest.raises(ValueError, match="non-empty"):
        log.for_event_type("   ")

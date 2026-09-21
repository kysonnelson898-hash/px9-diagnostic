import pytest

from can_transport.transport import CanFrame
from j1939.identifier import J1939Identifier
from j1939.request import J1939Request, REQUEST_PGN


def test_j1939_request_round_trip():
    request = J1939Request(
        requested_pgn=0x00F004,
        source_address=0x80,
        destination_address=0x00,
        priority=3,
    )

    frame = request.to_can_frame()
    identifier = J1939Identifier.from_arbitration_id(frame.arbitration_id)

    assert identifier.pgn.value == REQUEST_PGN
    assert identifier.source_address == 0x80
    assert identifier.destination_address == 0x00
    assert identifier.priority == 3
    assert frame.data == bytes.fromhex("04F000")

    decoded = J1939Request.from_can_frame(frame)

    assert decoded.requested_pgn == 0x00F004
    assert decoded.source_address == 0x80
    assert decoded.destination_address == 0x00
    assert decoded.priority == 3


def test_j1939_request_rejects_non_extended_frame():
    frame = CanFrame(
        arbitration_id=0x123,
        data=b"\x04\xF0\x00",
        is_extended_id=False,
    )

    with pytest.raises(ValueError, match="extended"):
        J1939Request.from_can_frame(frame)


def test_j1939_request_rejects_wrong_payload_length():
    frame = CanFrame(
        arbitration_id=0x18EAFF80,
        data=b"\x04\xF0",
        is_extended_id=True,
    )

    with pytest.raises(ValueError, match="exactly 3 bytes"):
        J1939Request.from_can_frame(frame)


def test_j1939_request_rejects_wrong_pgn():
    identifier = J1939Identifier(
        priority=6,
        pgn=0x00EC00,
        source_address=0x80,
        _destination_address=0x00,
    )

    frame = CanFrame(
        arbitration_id=identifier.to_arbitration_id(),
        data=b"\x04\xF0\x00",
        is_extended_id=True,
    )

    with pytest.raises(ValueError, match="not a J1939 Request"):
        J1939Request.from_can_frame(frame)


